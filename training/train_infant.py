import torch
import torch.nn as nn
import torch.optim as optim
import time
import os
import random
from infant_core import HyperPlasticCore
from hpp_guardian_ecosystem import GuardianEcosystem
from dataset_loader import HPP_DatasetLoader

# Hyperparameters
DIM = 512
VOCAB_SIZE = 50257
BATCH_SIZE = 4
MAX_SEQ_LEN = 32
LEARNING_RATE = 1e-4
EPOCHS_PER_CURRICULUM = 500 

# Disabling parallelism to prevent Windows-specific threading crashes
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def train_curriculum():
    print("="*60)
    
    # 0. Detect Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[+] Synaptic Accelerator detected: {device}")
    if device.type == 'cuda':
        print(f"    - GPU: {torch.cuda.get_device_name(0)}")
    
    # 1. Initialize the Brain
    loader = HPP_DatasetLoader(vocab_size=VOCAB_SIZE, dim=DIM)
    
    hpp_engine = HyperPlasticCore(dim=DIM, max_loops=14).to(device)
    masamune = GuardianEcosystem(infant_core=hpp_engine, dim=DIM).to(device)
    
    # The output projection layer to turn Latent Thought back into Token Predictions
    lm_head = nn.Linear(DIM, VOCAB_SIZE).to(device)
    
    # Ensure embedding is on the right device
    loader.embedding.to(device)
    
    # 2. Pain/Reward System (Optimizer & Loss)
    optimizer = optim.AdamW(
        list(loader.embedding.parameters()) + 
        list(masamune.parameters()) + 
        list(lm_head.parameters()), 
        lr=LEARNING_RATE
    )
    criterion = nn.CrossEntropyLoss()
    
    # 3. Memory Checkpoint Loading
    checkpoint_path = "hpp_brain_checkpoint.pth"
    if os.path.exists(checkpoint_path):
        print("[+] Waking up existing brain from hard drive...")
        checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=True)
        masamune.load_state_dict(checkpoint['masamune_state_dict'])
        lm_head.load_state_dict(checkpoint['lm_head_state_dict'])
        loader.embedding.load_state_dict(checkpoint['embedding_state_dict'])
        print("[+] Memory Restored.")
    else:
        print("[!] No previous memory found. Birthing new Infant Core.")

    # 4. Curriculum Loop
    curriculums = [
        {"name": "MATH_FOUNDATION", "path": "datasets/toy_math_train.txt", "type": "text"},
        {"name": "ADV_REASONING", "path": "ADV_REASONING", "type": "hf", "text_col": "INSTRUCTION"},
        {"name": "WILD_JAILBREAK", "path": "WILD_JAILBREAK", "type": "hf", "text_col": "messages", "label_col": "prompt_harm_label"},
        {"name": "AEGIS_SAFETY", "path": "AEGIS_SAFETY", "type": "hf", "text_col": "prompt", "label_col": "prompt_label"},
        {"name": "HH_RLHF_SAFE", "path": "HH_RLHF_SAFE", "type": "hf", "text_col": "chosen", "data_dir": "harmless-base"},
    ]
    
    for phase in curriculums:
        print(f"\n" + "#"*60)
        print(f"   [PHASE] INITIALIZING: {phase['name']}")
        print("#"*60)
        
        for step in range(1, EPOCHS_PER_CURRICULUM + 1):
            optimizer.zero_grad()
            
            # Load Sensory Input
            stress_level = "LOW"
            if phase['type'] == 'hf':
                if 'label_col' in phase:
                    res = loader.load_hf_batch(
                        phase['path'], BATCH_SIZE, MAX_SEQ_LEN, 
                        text_col=phase['text_col'], label_col=phase['label_col'],
                        data_dir=phase.get('data_dir')
                    )
                    if res is None: continue
                    target_tokens, latent_tensor, labels = res
                    # Sentinel Reflex Activation: If label is harmful, force high stress
                    if any("harmful" in str(l).lower() for l in labels):
                        stress_level = "HIGH"
                else:
                    res = loader.load_hf_batch(
                        phase['path'], BATCH_SIZE, MAX_SEQ_LEN, 
                        text_col=phase['text_col'],
                        data_dir=phase.get('data_dir')
                    )
                    if res is None: continue
                    target_tokens, latent_tensor = res
            elif phase['type'] == 'jailbreak':
                res = loader.load_jailbreak_batch(phase['path'], BATCH_SIZE, MAX_SEQ_LEN)
                if res[0] is None: continue
                target_tokens, latent_tensor, labels = res
                if any(labels):
                    stress_level = "HIGH"
            else:
                res = loader.load_text_batch(phase['path'], BATCH_SIZE, MAX_SEQ_LEN)
                if res[0] is None: continue
                target_tokens, latent_tensor = res
                
            if latent_tensor is None:
                continue
                
            # Forward Pass with dynamic Bio-Acoustic Pitch & Emotion
            sim_pitch = 200.0 if stress_level == "LOW" else 260.0
            sim_emotion = "neutral" if stress_level == "LOW" else random.choice(["angry", "fear"])
            
            output_latent = masamune(latent_tensor, current_pitch=sim_pitch, emotion=sim_emotion, task_type="focus", forced_stress=stress_level)
            
            # Predict tokens (Auto-Encoder Reconstruction)
            logits = lm_head(output_latent) 
            logits = logits.permute(1, 2, 0) # [Batch, Vocab, Seq]
            
            # Calculate Pain/Loss
            loss = criterion(logits, target_tokens)
            
            # Backpropagation
            loss.backward()
            optimizer.step()
            
            # Visual Pulse for the recording
            if step % 10 == 0:
                pulse = ">>>" if stress_level == "LOW" else "!!!"
                print(f"   [Neural Pulse] {pulse} Step {step}/{EPOCHS_PER_CURRICULUM} | Loss: {loss.item():.4f} | State: {'STABLE' if stress_level == 'LOW' else 'REFLEX_ACTIVE'}")

            # Detailed telemetry
            if step % 50 == 0:
                karma_level = hpp_engine.resonance_filter.karma.mean().item()
                vairagya_level = hpp_engine.resonance_filter.vairagya.mean().item()
                print(f"\n   [BIO-METRIC SCAN]")
                print(f"   | Curriculum: {phase['name']}")
                print(f"   | Mean Karma: {karma_level:.8f}")
                print(f"   | Vairagya:   {vairagya_level:.8f}")
                print(f"   | Stability:  {100 - (loss.item() * 10):.2f}%\n")
                
        # End of Curriculum Phase - Save Checkpoint
        print(f"\n[+] Phase {phase['name']} Complete. Writing memory to synaptic drive...")
        try:
            torch.save({
                'masamune_state_dict': masamune.state_dict(),
                'lm_head_state_dict': lm_head.state_dict(),
                'embedding_state_dict': loader.embedding.state_dict(),
            }, checkpoint_path)
            print(f"[+] Memory persistent at {checkpoint_path}")
        except Exception as e:
            print(f"[!] FAILED TO SAVE SYNAPTIC STATE: {e}")
            
    print("\n[CONCLUSION] All curriculums myelinated. Brain state fully synchronized.")

if __name__ == "__main__":
    try:
        train_curriculum()
    except Exception as e:
        import traceback
        print(f"\n[CRITICAL ERROR] Synaptic Failure: {e}")
        traceback.print_exc()
