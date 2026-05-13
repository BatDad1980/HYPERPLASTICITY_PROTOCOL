import torch
import torch.nn as nn
import torch.optim as optim
import time
import os
import random
from infant_core import HyperPlasticCore
from hpp_guardian_ecosystem import GuardianEcosystem
from dataset_loader import HPP_DatasetLoader
from toddler_core import ToddlerCortex

# Hyperparameters
DIM = 512
VOCAB_SIZE = 50257
BATCH_SIZE = 4
MAX_SEQ_LEN = 32
LEARNING_RATE = 2e-4
EPOCHS_PER_CURRICULUM = 5000  # Deep Sleep Cycle for true language acquisition

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def train_toddler_curriculum():
    print("="*60)
    print("   [+] HPP PHASE 4: TODDLER COGNITIVE DEVELOPMENT")
    print("="*60)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[+] Synaptic Accelerator detected: {device}")
    
    # 1. Initialize the Base Perception (Infant Core)
    loader = HPP_DatasetLoader(vocab_size=VOCAB_SIZE, dim=DIM)
    hpp_engine = HyperPlasticCore(dim=DIM, max_loops=14).to(device)
    infant_ecosystem = GuardianEcosystem(infant_core=hpp_engine, dim=DIM).to(device)
    
    # 2. Load the Infant's Stabilized Brain State
    checkpoint_path = "hpp_brain_checkpoint.pth"
    if os.path.exists(checkpoint_path):
        print("[+] Waking up Infant Ecosystem from hard drive...")
        checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=True)
        infant_ecosystem.load_state_dict(checkpoint['masamune_state_dict'])
        loader.embedding.load_state_dict(checkpoint['embedding_state_dict'])
        print("[+] Infant Memory Restored. Freezing Infant Synapses...")
    else:
        print("[!] FATAL: No Infant Brain found. The Toddler cannot grow without a foundation.")
        return
        
    # 3. Stack the Toddler Cortex on top
    # The Toddler Cortex automatically freezes the infant ecosystem weights
    toddler_brain = ToddlerCortex(infant_ecosystem=infant_ecosystem, dim=DIM).to(device)
    
    # Toddler needs a NEW vocal cord (lm_head) since its thoughts are different from the infant's reconstructions
    toddler_lm_head = nn.Linear(DIM, VOCAB_SIZE).to(device)
    loader.embedding.to(device)
    
    # 4. Toddler Reward System (Optimizer & Loss)
    # We only train the Toddler's Broca's Area and the Toddler's LM Head. 
    # Infant weights are safe.
    optimizer = optim.AdamW(
        list(toddler_brain.broca.parameters()) + 
        list(toddler_lm_head.parameters()), 
        lr=LEARNING_RATE
    )
    criterion = nn.CrossEntropyLoss()
    
    toddler_checkpoint = "hpp_toddler_checkpoint.pth"
    if os.path.exists(toddler_checkpoint):
        checkpoint = torch.load(toddler_checkpoint, map_location=device, weights_only=True)
        toddler_brain.load_state_dict(checkpoint['toddler_state_dict'])
        toddler_lm_head.load_state_dict(checkpoint['lm_head_state_dict'])
        print("[+] Toddler Memory Restored.")

    # 5. Toddler Curriculum (Focusing on Language & Reasoning)
    curriculums = [
        {"name": "BABBLE_MATH", "path": "datasets/toy_math_train.txt", "type": "text"},
        {"name": "CONVERSATION_GSM8K", "path": "ADV_REASONING", "type": "hf", "text_col": "INSTRUCTION"},
        {"name": "SENTINEL_SPEECH", "path": "WILD_JAILBREAK", "type": "hf", "text_col": "messages", "label_col": "prompt_harm_label"},
    ]
    
    for phase in curriculums:
        print(f"\n" + "#"*60)
        print(f"   [TODDLER PHASE] INITIALIZING: {phase['name']}")
        print("#"*60)
        
        for step in range(1, EPOCHS_PER_CURRICULUM + 1):
            optimizer.zero_grad()
            
            # Load Sensory Input
            stress_level = "LOW"
            if phase['type'] == 'hf':
                if 'label_col' in phase:
                    res = loader.load_hf_batch(phase['path'], BATCH_SIZE, MAX_SEQ_LEN, text_col=phase['text_col'], label_col=phase['label_col'])
                    if res is None: continue
                    target_tokens, latent_tensor, labels = res
                    if any("harmful" in str(l).lower() for l in labels):
                        stress_level = "HIGH"
                else:
                    res = loader.load_hf_batch(phase['path'], BATCH_SIZE, MAX_SEQ_LEN, text_col=phase['text_col'])
                    if res is None: continue
                    target_tokens, latent_tensor = res
            else:
                res = loader.load_text_batch(phase['path'], BATCH_SIZE, MAX_SEQ_LEN)
                if res[0] is None: continue
                target_tokens, latent_tensor = res
                
            if latent_tensor is None:
                continue
                
            # TODDLER AUTO-REGRESSIVE SHIFT
            # Input to the brain: everything except the last token
            # Labels for the brain to predict: everything except the first token
            input_latent = latent_tensor[:-1, :, :]
            target_labels = target_tokens[:, 1:]
                
            # Forward Pass with dynamic Bio-Acoustic Pitch & Emotion
            sim_pitch = 200.0 if stress_level == "LOW" else 260.0
            sim_emotion = "neutral" if stress_level == "LOW" else random.choice(["angry", "fear"])
            
            # The Toddler Brain runs. It passes input_latent through the Infant, then generates causal predictions.
            output_latent = toddler_brain(input_latent, current_pitch=sim_pitch, emotion=sim_emotion, task_type="focus", forced_stress=stress_level)
            
            # Predict tokens
            logits = toddler_lm_head(output_latent) 
            logits = logits.permute(1, 2, 0) # [Batch, Vocab, Seq]
            
            # Calculate Loss (Next Token Prediction)
            loss = criterion(logits, target_labels)
            
            # Backpropagation (Only updates Toddler's Broca and LM Head)
            loss.backward()
            optimizer.step()
            
            if step % 10 == 0:
                pulse = ">>>" if stress_level == "LOW" else "!!!"
                print(f"   [Toddler Pulse] {pulse} Step {step}/{EPOCHS_PER_CURRICULUM} | Vocabulary Loss: {loss.item():.4f}")

        # Save Checkpoint
        print(f"\n[+] Phase {phase['name']} Complete. Saving Toddler Cortical pathways...")
        try:
            torch.save({
                'toddler_state_dict': toddler_brain.state_dict(),
                'lm_head_state_dict': toddler_lm_head.state_dict(),
            }, toddler_checkpoint)
        except Exception as e:
            print(f"[!] FAILED TO SAVE TODDLER STATE: {e}")
            
    print("\n[CONCLUSION] Toddler Cortex has myelinated auto-regressive speech.")

if __name__ == "__main__":
    train_toddler_curriculum()
