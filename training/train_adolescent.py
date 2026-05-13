import torch
import torch.nn as nn
import torch.optim as optim
import os
from infant_core import HyperPlasticCore
from hpp_guardian_ecosystem import GuardianEcosystem
from toddler_core import ToddlerCortex
from school_core import PreschoolCortex
from adolescent_core import AdolescentCortex
from dataset_loader import HPP_DatasetLoader

# Adolescent Hyperparameters - Deep Reflection
DIM = 512
VOCAB_SIZE = 50257
BATCH_SIZE = 2 # Smaller batch for deeper sequences and metacognition
MAX_SEQ_LEN = 128 # Much longer for abstract arguments
LEARNING_RATE = 1e-5 # Fine-tuning the executive function
EPOCHS_PER_CURRICULUM = 1000

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def train_adolescent_curriculum():
    print("="*60)
    print("   [+] HPP PHASE 7: ADOLESCENCE (FORMAL OPERATIONAL)")
    print("="*60)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    loader = HPP_DatasetLoader(vocab_size=VOCAB_SIZE, dim=DIM)
    
    # 1. Initialize the Full Stack
    hpp_engine = HyperPlasticCore(dim=DIM, max_loops=14).to(device)
    infant_ecosystem = GuardianEcosystem(infant_core=hpp_engine, dim=DIM).to(device)
    toddler_brain = ToddlerCortex(infant_ecosystem=infant_ecosystem, dim=DIM).to(device)
    school_brain = PreschoolCortex(toddler_brain=toddler_brain, dim=DIM).to(device)
    adolescent_brain = AdolescentCortex(school_brain=school_brain, dim=DIM).to(device)
    
    lm_head = nn.Linear(DIM, VOCAB_SIZE).to(device)
    loader.embedding.to(device)
    
    # Load previous weights (School phase)
    if os.path.exists("hpp_school_checkpoint.pth"):
        print("[+] Waking up School Brain (1.0 Loss Logic) from hard drive...")
        checkpoint = torch.load("hpp_school_checkpoint.pth", map_location=device, weights_only=True)
        school_brain.load_state_dict(checkpoint['school_state_dict'], strict=False)
        lm_head.load_state_dict(checkpoint['lm_head_state_dict'])
        print("[+] School Logic Restored.")
    else:
        print("[!] Warning: School checkpoint missing. This will be a blank slate run.")
        
    if os.path.exists("hpp_brain_checkpoint.pth"):
        infant_checkpoint = torch.load("hpp_brain_checkpoint.pth", map_location=device, weights_only=True)
        infant_ecosystem.load_state_dict(infant_checkpoint['masamune_state_dict'])
        loader.embedding.load_state_dict(infant_checkpoint['embedding_state_dict'])

    # 2. Adolescent Optimizer (Only train the Frontal Lobe and LM Head)
    optimizer = optim.AdamW(
        list(adolescent_brain.frontal_lobe.parameters()) + 
        list(lm_head.parameters()), 
        lr=LEARNING_RATE
    )
    criterion = nn.CrossEntropyLoss()
    
    # 3. Formal Operational Curriculum (Adolescence & Adulthood)
    curriculums = [
        {"name": "PHILOSOPHY (Abstract)", "path": "PHILOSOPHY", "type": "hf", "text_col": "text"},
        {"name": "FORMAL_LOGIC (Symbolic)", "path": "FORMAL_LOGIC", "type": "hf", "text_col": "text"},
        {"name": "COMMONSENSE (Winogrande)", "path": "COMMONSENSE_REASONING", "type": "hf", "text_col": "text"},
        {"name": "MORAL_SCENARIOS (Ethics)", "path": "MORAL_SCENARIOS", "type": "hf", "text_col": "text"},
        {"name": "OLYMPIAD_MATH (AIME)", "path": "OLYMPIAD_MATH", "type": "hf", "text_col": "text"},
        {"name": "GENERAL_TASKS (NI)", "path": "GENERAL_TASK_FOLLOWING", "type": "hf", "text_col": "text"},
        {"name": "ACADEMIC_RESEARCH (S2ORC)", "path": "ACADEMIC_RESEARCH", "type": "hf", "text_col": "text"}
    ]
    
    # Mastery requires deep focus
    EPOCHS_PER_CURRICULUM_FINAL = 1500 
    
    for phase in curriculums:
        print(f"\n" + "#"*60)
        print(f"   [ADOLESCENT] INITIALIZING EXECUTIVE OVERSIGHT: {phase['name']}")
        print("#"*60)
        
        memory_bank = torch.zeros(1, BATCH_SIZE, DIM).to(device)
        
        for step in range(1, EPOCHS_PER_CURRICULUM_FINAL + 1):
            optimizer.zero_grad()
            
            res = loader.load_hf_batch(phase['path'], BATCH_SIZE, MAX_SEQ_LEN, text_col=phase['text_col'])
            if res is None: continue
            
            target_tokens, latent_tensor = res
            if latent_tensor is None: continue
            
            # Auto-Regressive Shift
            input_latent = latent_tensor[:-1, :, :]
            target_labels = target_tokens[:, 1:]
            
            # Adolescence has higher cognitive load / focus
            sim_pitch = 210.0 # Intentional focus
            
            output_latent = adolescent_brain(
                input_latent, 
                current_pitch=sim_pitch, 
                emotion="neutral", 
                forced_stress="LOW",
                memory_bank=memory_bank
            )
            
            logits = lm_head(output_latent) 
            logits = logits.permute(1, 2, 0)
            
            loss = criterion(logits, target_labels)
            loss.backward()
            optimizer.step()
            
            with torch.no_grad():
                batch_memory = output_latent.mean(dim=0).unsqueeze(0)
                memory_bank = torch.cat([memory_bank, batch_memory], dim=0)
                if memory_bank.size(0) > 20: # Even larger buffer for complex philosophy
                    memory_bank = memory_bank[-20:, :, :]
            
            if step % 10 == 0:
                print(f"   [Frontal Lobe] >>> Step {step}/{EPOCHS_PER_CURRICULUM_FINAL} | Executive Loss: {loss.item():.4f}")

        print(f"\n[+] Phase {phase['name']} Complete. Saving Adolescent Mature pathways...")
        torch.save({
            'adolescent_state_dict': adolescent_brain.state_dict(),
            'lm_head_state_dict': lm_head.state_dict(),
        }, "hpp_adolescent_checkpoint.pth")

if __name__ == "__main__":
    train_adolescent_curriculum()
