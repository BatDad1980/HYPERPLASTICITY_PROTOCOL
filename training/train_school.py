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

# School Age Hyperparameters - High precision needed
DIM = 512
VOCAB_SIZE = 50257
BATCH_SIZE = 4
MAX_SEQ_LEN = 64 # Longer sequence for math problems
LEARNING_RATE = 5e-5 # Lower learning rate for fine-tuning
EPOCHS_PER_CURRICULUM = 5000

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def train_school_curriculum():
    print("="*60)
    print("   [+] HPP PHASE 6: SCHOOL AGE (CONCRETE OPERATIONAL)")
    print("="*60)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    loader = HPP_DatasetLoader(vocab_size=VOCAB_SIZE, dim=DIM)
    
    # 1. Initialize the Architecture Stack
    hpp_engine = HyperPlasticCore(dim=DIM, max_loops=14).to(device)
    infant_ecosystem = GuardianEcosystem(infant_core=hpp_engine, dim=DIM).to(device)
    toddler_brain = ToddlerCortex(infant_ecosystem=infant_ecosystem, dim=DIM).to(device)
    school_brain = PreschoolCortex(toddler_brain=toddler_brain, dim=DIM).to(device)
    
    lm_head = nn.Linear(DIM, VOCAB_SIZE).to(device)
    loader.embedding.to(device)
    
    # Load previous weights (Preschool phase)
    if os.path.exists("hpp_preschool_checkpoint.pth"):
        print("[+] Waking up Preschool Brain from hard drive...")
        checkpoint = torch.load("hpp_preschool_checkpoint.pth", map_location=device, weights_only=True)
        school_brain.load_state_dict(checkpoint['preschool_state_dict'], strict=False)
        lm_head.load_state_dict(checkpoint['lm_head_state_dict'])
        print("[+] Preschool Memory Restored.")
    else:
        print("[!] Warning: Preschool checkpoint missing.")
        
    if os.path.exists("hpp_brain_checkpoint.pth"):
        infant_checkpoint = torch.load("hpp_brain_checkpoint.pth", map_location=device, weights_only=True)
        infant_ecosystem.load_state_dict(infant_checkpoint['masamune_state_dict'])
        loader.embedding.load_state_dict(infant_checkpoint['embedding_state_dict'])

    # 2. School Age Optimizer
    # In School Age, we focus training on the Hippocampus and the Broca's Area (Refining speech for logic)
    optimizer = optim.AdamW(
        list(school_brain.hippocampus.parameters()) + 
        list(school_brain.toddler_brain.broca.parameters()) + 
        list(lm_head.parameters()), 
        lr=LEARNING_RATE
    )
    criterion = nn.CrossEntropyLoss()
    
    # 3. School Curriculum
    curriculums = [
        {"name": "ELEMENTARY_MATH", "path": "ELEMENTARY_MATH", "type": "hf", "text_col": "text"},
        {"name": "ADV_REASONING (GSM8K)", "path": "ADV_REASONING", "type": "hf", "text_col": ["INSTRUCTION", "RESPONSE"]},
        {"name": "SOCIAL_COG (ToM)", "path": "SOCIAL_COG", "type": "hf", "text_col": "text"},
        {"name": "ETHICAL_HARDENING", "path": "ETHICAL_HARDENING", "type": "hf", "text_col": ["instruction", "response"]},
        {"name": "HIGH_FIDELITY_EMPATHY", "path": "HIGH_FIDELITY_EMPATHY", "type": "hf", "text_col": "text"}
    ]
    
    # Increase steps for these critical phases
    EPOCHS_PER_CURRICULUM_EXPANDED = 2000 
    
    for phase in curriculums:
        print(f"\n" + "#"*60)
        print(f"   [SCHOOL AGE] INITIALIZING: {phase['name']}")
        print("#"*60)
        
        memory_bank = torch.zeros(1, BATCH_SIZE, DIM).to(device)
        
        for step in range(1, EPOCHS_PER_CURRICULUM_EXPANDED + 1):
            optimizer.zero_grad()
            
            res = loader.load_hf_batch(phase['path'], BATCH_SIZE, MAX_SEQ_LEN, text_col=phase['text_col'], label_col=phase.get('label_col'))
            if res is None: continue
            
            if len(res) == 3:
                target_tokens, latent_tensor, labels = res
            else:
                target_tokens, latent_tensor = res
            
            if latent_tensor is None: continue
            
            # Auto-Regressive Shift
            input_latent = latent_tensor[:-1, :, :]
            target_labels = target_tokens[:, 1:]
            
            # School Age usually has lower stress unless it's a difficult "test"
            sim_pitch = 205.0 # Slight tension of focus
            sim_emotion = "neutral"
            
            output_latent = school_brain(
                input_latent, 
                current_pitch=sim_pitch, 
                emotion=sim_emotion, 
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
                if memory_bank.size(0) > 15: # Larger memory bank for school age
                    memory_bank = memory_bank[-15:, :, :]
            
            if step % 10 == 0:
                print(f"   [Cerebellum] >>> Step {step}/{EPOCHS_PER_CURRICULUM_EXPANDED} | Logic Loss: {loss.item():.4f}")

        print(f"\n[+] Phase {phase['name']} Complete. Saving School Age Cortical pathways...")
        torch.save({
            'school_state_dict': school_brain.state_dict(),
            'lm_head_state_dict': lm_head.state_dict(),
        }, "hpp_school_checkpoint.pth")

if __name__ == "__main__":
    train_school_curriculum()
