import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import random
from hpp_sovereign_engine import HPP_SovereignEngine
from utils.dataset_loader import HPP_DatasetLoader

def train_linguistic_sync():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"--- INITIALIZING LINGUISTIC SYNC (PHASE 8.5) ---")
    
    # 1. Load the existing Sovereign Engine
    engine = HPP_SovereignEngine()
    loader = HPP_DatasetLoader(vocab_size=50257, dim=512)
    
    # 2. FREEZE the Brain Layers
    # We don't want his technical knowledge to change, just his speech center
    for param in engine.university.parameters():
        param.requires_grad = False
    for param in engine.adolescent.parameters():
        param.requires_grad = False
    for param in engine.school.parameters():
        param.requires_grad = False
    for param in engine.toddler.parameters():
        param.requires_grad = False
    for param in engine.hpp_core.parameters():
        param.requires_grad = False
        
    # 3. UNLOCK the Speech Center (Tongue)
    for param in engine.lm_head.parameters():
        param.requires_grad = True
    for param in engine.embedding.parameters():
        param.requires_grad = True
        
    optimizer = optim.AdamW(
        list(engine.lm_head.parameters()) + list(engine.embedding.parameters()), 
        lr=5e-5
    )
    criterion = nn.CrossEntropyLoss()
    
    # 4. Helper for JSONL loading
    import json
    def get_jsonl_batch(file_path, batch_size, seq_len):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        samples = random.sample(lines, batch_size)
        texts = [json.loads(s)['text'] for s in samples]
        tokens = [engine.enc.encode(t)[:seq_len] for t in texts]
        # Pad or truncate
        tokens = [t + [engine.enc.eot_token]*(seq_len-len(t)) for t in tokens]
        return torch.tensor(tokens, device=device)

    print("[+] Syncing Speech Center with University Logic...")
    data_path = "datasets/hf_local/GENERAL_TASK_FOLLOWING.jsonl"
    for step in range(500):
        # Sample training data
        batch = get_jsonl_batch(data_path, batch_size=2, seq_len=128)
        
        # Forward pass through the whole stack
        output_latent = engine.university(engine.embedding(batch), domain="none")
        logits = engine.lm_head(output_latent.permute(1, 0, 2))
        
        # Loss calculation
        loss = criterion(logits.view(-1, 50257), batch.view(-1))
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if step % 50 == 0:
            print(f"Step {step}/500 | Loss: {loss.item():.4f}")

    # 5. Save the 'Linguistic Anchor'
    save_path = "checkpoints/hpp_linguistic_anchor.pth"
    torch.save({
        'embedding_state_dict': engine.embedding.state_dict(),
        'lm_head_state_dict': engine.lm_head.state_dict(),
        'university_state_dict': engine.university.state_dict()
    }, save_path)
    print(f"[+] Linguistic Anchor Saved: {save_path}")

if __name__ == "__main__":
    train_linguistic_sync()
