import torch
import torch.nn as nn
import torch.optim as optim
import os
import random
from infant_core import HyperPlasticCore
from hpp_guardian_ecosystem import GuardianEcosystem
from toddler_core import ToddlerCortex
from school_core import PreschoolCortex
from dataset_loader import HPP_DatasetLoader

DIM = 512
VOCAB_SIZE = 50257
BATCH_SIZE = 4
MAX_SEQ_LEN = 32
LEARNING_RATE = 1e-4
EPOCHS_PER_CURRICULUM = 5000

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def train_preschool_curriculum():
    print("="*60)
    print("   [+] HPP PHASE 5: PRESCHOOL (HIPPOCAMPUS MYELINATION)")
    print("="*60)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    loader = HPP_DatasetLoader(vocab_size=VOCAB_SIZE, dim=DIM)
    
    # 1. Load the frozen Core
    hpp_engine = HyperPlasticCore(dim=DIM, max_loops=14).to(device)
    infant_ecosystem = GuardianEcosystem(infant_core=hpp_engine, dim=DIM).to(device)
    toddler_brain = ToddlerCortex(infant_ecosystem=infant_ecosystem, dim=DIM).to(device)
    preschool_brain = PreschoolCortex(toddler_brain=toddler_brain, dim=DIM).to(device)
    
    lm_head = nn.Linear(DIM, VOCAB_SIZE).to(device)
    loader.embedding.to(device)
    
    # Load previous weights
    if os.path.exists("hpp_toddler_checkpoint.pth"):
        print("[+] Waking up Toddler Cortex from hard drive...")
        checkpoint = torch.load("hpp_toddler_checkpoint.pth", map_location=device, weights_only=True)
        toddler_brain.load_state_dict(checkpoint['toddler_state_dict'], strict=False)
        lm_head.load_state_dict(checkpoint['lm_head_state_dict'])
        print("[+] Toddler Memory Restored.")
    else:
        print("[!] Warning: Toddler checkpoint missing. Starting from scratch.")
        
    if os.path.exists("hpp_brain_checkpoint.pth"):
        infant_checkpoint = torch.load("hpp_brain_checkpoint.pth", map_location=device, weights_only=True)
        infant_ecosystem.load_state_dict(infant_checkpoint['masamune_state_dict'])
        loader.embedding.load_state_dict(infant_checkpoint['embedding_state_dict'])

    # 2. Preschool Reward System
    optimizer = optim.AdamW(
        list(preschool_brain.hippocampus.parameters()) + 
        list(preschool_brain.toddler_brain.broca.parameters()) + 
        list(lm_head.parameters()), 
        lr=LEARNING_RATE
    )
    criterion = nn.CrossEntropyLoss()
    
    # 3. Sesame Street Curriculum
    curriculums = [
        {"name": "STORY_TIME (Grammar)", "path": "TINY_STORIES", "type": "hf", "text_col": "text"},
        {"name": "SHARING_CIRCLE (Empathy)", "path": "EMPATHY_CIRCLE", "type": "hf", "text_col": "situation", "label_col": "emotion"},
    ]
    
    for phase in curriculums:
        print(f"\n" + "#"*60)
        print(f"   [PRESCHOOL] INITIALIZING: {phase['name']}")
        print("#"*60)
        
        # Simulated short-term memory bank (starts empty) [Seq, Batch, Dim]
        memory_bank = torch.zeros(1, BATCH_SIZE, DIM).to(device)
        
        for step in range(1, EPOCHS_PER_CURRICULUM + 1):
            optimizer.zero_grad()
            
            stress_level = "LOW"
            if phase['type'] == 'hf':
                res = loader.load_hf_batch(phase['path'], BATCH_SIZE, MAX_SEQ_LEN, text_col=phase['text_col'], label_col=phase.get('label_col'))
                if res is None: continue
                if len(res) == 3:
                    target_tokens, latent_tensor, labels = res
                    # If the context involves negative emotions, increase stress
                    negative_markers = ["angry", "sad", "afraid", "terrified", "disgusted", "lonely", "ashamed", "devastated", "guilty", "jealous"]
                    if any(l and str(l).lower() in negative_markers for l in labels):
                        stress_level = "HIGH"
                else:
                    target_tokens, latent_tensor = res
            
            if latent_tensor is None: continue
            
            # Auto-Regressive Shift
            input_latent = latent_tensor[:-1, :, :]  # [Seq-1, Batch, Dim]
            target_labels = target_tokens[:, 1:]
            
            sim_pitch = 200.0 if stress_level == "LOW" else 260.0
            sim_emotion = "neutral" if stress_level == "LOW" else random.choice(["angry", "fear"])
            
            output_latent = preschool_brain(
                input_latent, 
                current_pitch=sim_pitch, 
                emotion=sim_emotion, 
                forced_stress=stress_level,
                memory_bank=memory_bank
            )
            
            logits = lm_head(output_latent) 
            logits = logits.permute(1, 2, 0)
            
            loss = criterion(logits, target_labels)
            loss.backward()
            optimizer.step()
            
            # Update memory bank with the latest thoughts (rolling buffer)
            with torch.no_grad():
                # Take the mean of the sequence to represent the "memory" of this batch
                batch_memory = output_latent.mean(dim=0).unsqueeze(0) # [1, Batch, Dim]
                memory_bank = torch.cat([memory_bank, batch_memory], dim=0)
                # Keep only the last 10 memories
                if memory_bank.size(0) > 10:
                    memory_bank = memory_bank[-10:, :, :]
            
            if step % 10 == 0:
                pulse = ">>>" if stress_level == "LOW" else "!!!"
                print(f"   [Hippocampus] {pulse} Step {step}/{EPOCHS_PER_CURRICULUM} | Memory Coherence Loss: {loss.item():.4f}")

        print(f"\n[+] Phase {phase['name']} Complete. Saving Preschool Cortical pathways...")
        torch.save({
            'preschool_state_dict': preschool_brain.state_dict(),
            'lm_head_state_dict': lm_head.state_dict(),
        }, "hpp_preschool_checkpoint.pth")

if __name__ == "__main__":
    train_preschool_curriculum()
