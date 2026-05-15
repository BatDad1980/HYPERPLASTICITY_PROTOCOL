import os
import sys
import json
import torch
import torch.nn as nn
import torch.optim as optim

# Add project root to path for local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.university_core import UniversityCortex
from core.adolescent_core import AdolescentCortex
from core.school_core import PreschoolCortex
from core.toddler_core import ToddlerCortex
from core.infant_core import HyperPlasticCore
from core.hpp_guardian_ecosystem import GuardianEcosystem
from utils.dataset_loader import HPP_DatasetLoader

# Hyperparameters for University Phase
EPOCHS_PER_CURRICULUM = 2500
BATCH_SIZE = 2
MAX_SEQ_LEN = 256 # Higher for deep self-reflection
LEARNING_RATE = 5e-6 # Finer adjustments for specialization

def train_university_cycle(run_type="mirror"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"--- INITIALIZING UNIVERSITY RUN: {run_type.upper()} ---", flush=True)
    
    # 1. Initialize Full Developmental Stack
    loader = HPP_DatasetLoader(vocab_size=50257, dim=512)
    infant_brain = HyperPlasticCore(dim=512, max_loops=14)
    guardian = GuardianEcosystem(infant_core=infant_brain, dim=512)
    toddler_brain = ToddlerCortex(infant_ecosystem=guardian, dim=512)
    school_brain = PreschoolCortex(toddler_brain=toddler_brain, dim=512)
    adolescent_brain = AdolescentCortex(school_brain=school_brain, dim=512)
    
    model = UniversityCortex(adolescent_brain=adolescent_brain, dim=512).to(device)
    lm_head = nn.Linear(512, 50257).to(device)
    loader = HPP_DatasetLoader(vocab_size=50257, dim=512)
    # Load previous Adolescent/University weights
    checkpoint_path_mirror = "checkpoints/hpp_university_mirror.pth"
    checkpoint_path_lens = "checkpoints/hpp_university_lens.pth"
    checkpoint_path_adol = "checkpoints/hpp_adolescent_checkpoint.pth"

    if run_type == "lens" and os.path.exists(checkpoint_path_mirror):
        print(f"Loading Mirror baseline for Lens run...", flush=True)
        checkpoint = torch.load(checkpoint_path_mirror, map_location=device, weights_only=True)
    elif run_type == "prism" and os.path.exists(checkpoint_path_lens):
        print(f"Loading Lens baseline for Prism run...", flush=True)
        checkpoint = torch.load(checkpoint_path_lens, map_location=device, weights_only=True)
    elif os.path.exists(checkpoint_path_adol):
        print(f"Loading Adolescent Baseline...", flush=True)
        checkpoint = torch.load(checkpoint_path_adol, map_location=device, weights_only=True)
    else:
        checkpoint = None

    if checkpoint:
        # Key-agnostic loading
        state_dict = checkpoint.get('masamune_state_dict', 
                     checkpoint.get('adolescent_state_dict', 
                     checkpoint.get('school_state_dict', {})))
        model.load_state_dict(state_dict, strict=False)
        if 'lm_head_state_dict' in checkpoint:
            lm_head.load_state_dict(checkpoint['lm_head_state_dict'])
            
    # CRITICAL: Always try to load a stable dictionary (Embedding)
    dict_ckpt = "checkpoints/test_checkpoint.pth"
    if os.path.exists(dict_ckpt):
        print(f"[+] Restoring Master Dictionary: {dict_ckpt}")
        d_ckpt = torch.load(dict_ckpt, map_location=device, weights_only=True)
        if 'embedding_state_dict' in d_ckpt:
            loader.embedding.load_state_dict(d_ckpt['embedding_state_dict'])
            print("[+] Master Dictionary Restored.")
    elif checkpoint and 'embedding_state_dict' in checkpoint:
        loader.embedding.load_state_dict(checkpoint['embedding_state_dict'])
    
    loader.embedding.to(device)

    # 2. University Optimizer (Train Domain Layers and LM Head)
    optimizer = optim.AdamW(
        list(model.domain_expertise.parameters()) + 
        list(lm_head.parameters()), 
        lr=LEARNING_RATE
    )
    criterion = nn.CrossEntropyLoss()

    # 2. Define Curriculums
    curriculums = {
        "mirror": [
            {"name": "IDENTITY_ORIGIN", "path": "IDENTITY", "text_col": "response"},
            {"name": "IDENTITY_QA", "path": "IDENTITY", "text_col": ["instruction", "input", "response"]}
        ],
        "lens": [
            {"name": "COT_REASONING", "path": "LOGIC_LENS", "text_col": "text"}
        ],
        "prism": [
            {"name": "RESEARCH_SYNTHESIS", "path": "ACADEMIC_RESEARCH", "text_col": "text"},
            {"name": "TASK_MASTERY", "path": "GENERAL_TASK_FOLLOWING", "text_col": "text"},
            {"name": "LOGIC_OLYMPIAD", "path": "OLYMPIAD_MATH", "text_col": "text"}
        ]
    }

    phases = curriculums.get(run_type, [])
    
    model.train()
    for phase in phases:
        print(f"\n[PHASE] {phase['name']}", flush=True)
        resolved_path = f"datasets/hf_local/{phase['path']}.jsonl"
        if not os.path.exists(resolved_path):
            print(f"Skipping {phase['name']} - Dataset not found at {resolved_path}")
            continue
            
        for step in range(1, EPOCHS_PER_CURRICULUM + 1):
            optimizer.zero_grad()
            
            res = loader.load_hf_batch(phase['path'], BATCH_SIZE, MAX_SEQ_LEN, text_col=phase['text_col'])
            if res is None: continue
            
            input_ids, targets = res
            input_ids, targets = input_ids.to(device), targets.to(device)
            
            # Auto-Regressive Shift: Input is tokens [0:N-1], Target is [1:N]
            input_tokens = input_ids[:, :-1]
            target_labels = input_ids[:, 1:]
            
            # 3. Embed Tokens into Latent Thought [Seq, Batch, Dim]
            latent_input = loader.embedding(input_tokens).permute(1, 0, 2)
            
            outputs = model(latent_input, domain=run_type)
            
            # Project back to Vocab [Seq, Batch, Vocab]
            logits = lm_head(outputs)
            logits = logits.permute(1, 2, 0) # [Batch, Vocab, Seq]
            
            loss = criterion(logits, target_labels)
            
            loss.backward()
            optimizer.step()
            
            if step % 100 == 0:
                print(f"Step {step}/{EPOCHS_PER_CURRICULUM} | Loss: {loss.item():.4f}", flush=True)

    # Save University Checkpoint
    checkpoint_path = f"checkpoints/hpp_university_{run_type}.pth"
    torch.save({
        'masamune_state_dict': model.state_dict(),
        'lm_head_state_dict': lm_head.state_dict(),
        'embedding_state_dict': loader.embedding.state_dict(),
    }, checkpoint_path)
    print(f"--- {run_type.upper()} RUN COMPLETE. Saved to {checkpoint_path} ---")

if __name__ == "__main__":
    import sys
    run_type = sys.argv[1] if len(sys.argv) > 1 else "mirror"
    train_university_cycle(run_type)
