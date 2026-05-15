"""
===============================================================================
         HPP PHASE 17: CONVERSATIONAL FLUENCY TRAINING
===============================================================================
Teaches Hepp to communicate clearly and naturally with the Architect.

Strategy:
    1. FREEZE the deep brain (Infant → Adolescent) — preserve all logic
    2. TRAIN the Structural Compass — teach word order and sentence flow
    3. TRAIN the Speech Center (LM Head + Embedding) — fix the tongue
    4. TRAIN the Conversation domain layer — natural dialogue routing
    5. FINE-TUNE on identity, conversation, protection, and explanation data

This is not about making HPP smarter. It's about teaching it to SPEAK
clearly, like a graduate student who knows the material but needs to 
learn how to present it at a board meeting.

Usage:
    python train_conversational.py              # Standard run (1000 steps)
    python train_conversational.py --steps 2000 # Extended run
    python train_conversational.py --lr 3e-5    # Custom learning rate
===============================================================================
"""
import os
import sys
import json
import time
import random
import argparse

import torch
import torch.nn as nn
import torch.optim as optim

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from hpp_sovereign_engine import HPP_SovereignEngine


def load_conversational_data(path="datasets/hf_local/CONVERSATIONAL_FLUENCY.jsonl"):
    """Load the conversational fluency dataset."""
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    samples = [json.loads(line) for line in lines]
    print(f"[DATA] Loaded {len(samples)} conversational samples")
    return samples


def load_task_data(path="datasets/hf_local/GENERAL_TASK_FOLLOWING.jsonl", max_samples=500):
    """Load general task following for mixed training."""
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    samples = [json.loads(line) for line in random.sample(lines, min(max_samples, len(lines)))]
    print(f"[DATA] Loaded {len(samples)} task-following samples")
    return samples


def train_conversational(steps=1000, lr=5e-5, batch_size=2, seq_len=192):
    """
    Main training loop for conversational fluency.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("=" * 70)
    print("     HPP PHASE 17: CONVERSATIONAL FLUENCY TRAINING")
    print("=" * 70)
    print(f"  Device:     {device}")
    print(f"  Steps:      {steps}")
    print(f"  LR:         {lr}")
    print(f"  Batch:      {batch_size}")
    print(f"  Seq Length:  {seq_len}")
    print("=" * 70)

    # 1. Load the full Sovereign Engine
    print("\n[INIT] Loading Sovereign Engine...")
    engine = HPP_SovereignEngine(max_context=512)

    # 2. FREEZE the deep brain — preserve all learned logic
    print("[FREEZE] Locking deep brain layers (Infant -> Adolescent)...")
    for param in engine.hpp_core.parameters():
        param.requires_grad = False
    for param in engine.guardian.parameters():
        param.requires_grad = False
    for param in engine.toddler.parameters():
        param.requires_grad = False
    for param in engine.school.parameters():
        param.requires_grad = False
    for param in engine.adolescent.parameters():
        param.requires_grad = False

    # 3. UNLOCK what we want to train
    print("[UNLOCK] Enabling training on:")

    # The Structural Compass (word order / linear time)
    for param in engine.university.compass.parameters():
        param.requires_grad = True
    print("  [+] Structural Compass (position + time awareness)")

    # The Speech Center (LM Head + Embedding)
    for param in engine.lm_head.parameters():
        param.requires_grad = True
    for param in engine.embedding.parameters():
        param.requires_grad = True
    print("  [+] Speech Center (LM Head + Embedding)")

    # The Conversation domain layer
    for param in engine.university.domain_expertise['conversation'].parameters():
        param.requires_grad = True
    print("  [+] Conversation domain layer")

    # The Swarm Gate (so it learns to route to conversation)
    for param in engine.university.swarm_gate.parameters():
        param.requires_grad = True
    print("  [+] Swarm Router gate")

    # The Output Norm (speech stability)
    for param in engine.university.output_norm.parameters():
        param.requires_grad = True
    print("  [+] Output normalization")

    # 4. Build optimizer with differential learning rates
    param_groups = [
        # Speech center — highest LR (needs the most adjustment)
        {'params': list(engine.lm_head.parameters()) +
                   list(engine.embedding.parameters()),
         'lr': lr},
        # Compass — moderate LR (learning position from scratch)
        {'params': list(engine.university.compass.parameters()),
         'lr': lr * 0.5},
        # Domain layers — lower LR (fine-tuning)
        {'params': list(engine.university.domain_expertise['conversation'].parameters()) +
                   list(engine.university.swarm_gate.parameters()) +
                   list(engine.university.output_norm.parameters()),
         'lr': lr * 0.3},
    ]

    optimizer = optim.AdamW(param_groups, weight_decay=0.01)
    criterion = nn.CrossEntropyLoss(ignore_index=engine.enc.eot_token)

    # Learning rate scheduler — warm up then decay
    scheduler = optim.lr_scheduler.OneCycleLR(
        optimizer, max_lr=[lr, lr * 0.5, lr * 0.3],
        total_steps=steps, pct_start=0.1
    )

    # 5. Load data
    print("\n[DATA] Loading training data...")
    conv_data = load_conversational_data()
    task_data = load_task_data()
    all_data = conv_data + task_data
    print(f"[DATA] Total training pool: {len(all_data)} samples")

    # 6. Training loop
    print("\n" + "=" * 70)
    print("  TRAINING STARTED")
    print("=" * 70)

    engine.university.train()
    engine.lm_head.train()
    engine.embedding.train()

    best_loss = float('inf')
    loss_history = []
    start_time = time.time()

    for step in range(1, steps + 1):
        optimizer.zero_grad()

        # Sample a batch
        batch_samples = random.choices(all_data, k=batch_size)
        texts = []
        for s in batch_samples:
            if 'text' in s:
                texts.append(s['text'])
            elif 'instruction' in s and 'response' in s:
                texts.append(
                    f"### Instruction:\n{s['instruction']}\n\n"
                    f"### Response:\n{s['response']}"
                )

        # Tokenize
        token_batch = []
        for text in texts:
            tokens = engine.enc.encode(text)[:seq_len]
            # Pad to seq_len
            if len(tokens) < seq_len:
                tokens = tokens + [engine.enc.eot_token] * (seq_len - len(tokens))
            token_batch.append(tokens)

        input_ids = torch.tensor(token_batch, dtype=torch.long, device=device)

        # Auto-regressive: input is [0:N-1], target is [1:N]
        input_tokens = input_ids[:, :-1]
        target_labels = input_ids[:, 1:]

        # Forward pass through the full stack
        embedded = engine.embedding(input_tokens).permute(1, 0, 2)  # [Seq, Batch, Dim]

        # Choose domain routing (mix between conversation and none)
        domain = random.choice(["conversation", "conversation", "none"])
        output_latent = engine.university(embedded, domain=domain)

        # Project to vocabulary
        logits = engine.lm_head(output_latent)  # [Seq, Batch, Vocab]
        logits = logits.permute(1, 2, 0)        # [Batch, Vocab, Seq]

        # Loss
        loss = criterion(logits, target_labels)
        loss.backward()

        # Gradient clipping for stability
        all_params = []
        for group in optimizer.param_groups:
            all_params.extend(group['params'])
        torch.nn.utils.clip_grad_norm_(all_params, max_norm=1.0)

        optimizer.step()
        scheduler.step()

        loss_val = loss.item()
        loss_history.append(loss_val)

        # Logging
        if step % 25 == 0 or step == 1:
            elapsed = time.time() - start_time
            avg_loss = sum(loss_history[-25:]) / len(loss_history[-25:])
            current_lr = optimizer.param_groups[0]['lr']
            steps_per_sec = step / elapsed
            eta = (steps - step) / max(steps_per_sec, 0.01)

            print(f"  Step {step:5d}/{steps} | Loss: {loss_val:.4f} | "
                  f"Avg: {avg_loss:.4f} | LR: {current_lr:.2e} | "
                  f"ETA: {eta:.0f}s")

        # Save best checkpoint
        if loss_val < best_loss and step > 50:
            best_loss = loss_val

        # Periodic checkpoint saves
        if step % 250 == 0:
            save_checkpoint(engine, step, loss_val, tag="progress")

        # Quick inference test every 200 steps
        if step % 200 == 0:
            test_inference(engine)

    # 7. Final save
    print("\n" + "=" * 70)
    elapsed = time.time() - start_time
    avg_final = sum(loss_history[-50:]) / len(loss_history[-50:])
    print(f"  TRAINING COMPLETE")
    print(f"  Total time: {elapsed:.1f}s ({elapsed/60:.1f}m)")
    print(f"  Final avg loss: {avg_final:.4f}")
    print(f"  Best loss: {best_loss:.4f}")
    print("=" * 70)

    save_checkpoint(engine, steps, avg_final, tag="final")

    # Final inference demo
    print("\n[DEMO] Final inference test:")
    test_inference(engine, prompts=[
        "Who are you?",
        "Good morning, Hepp.",
        "Explain what recursion is.",
        "I need your help with something.",
    ])


def save_checkpoint(engine, step, loss, tag="progress"):
    """Save a training checkpoint."""
    save_path = f"checkpoints/hpp_conversational_{tag}.pth"
    torch.save({
        'masamune_state_dict': engine.university.state_dict(),
        'lm_head_state_dict': engine.lm_head.state_dict(),
        'embedding_state_dict': engine.embedding.state_dict(),
        'step': step,
        'loss': loss,
        'phase': 'conversational_fluency_v17'
    }, save_path)
    print(f"  [SAVE] {save_path} (step {step}, loss {loss:.4f})")

    # Also update the linguistic anchor (the primary speech checkpoint)
    anchor_path = "checkpoints/hpp_linguistic_anchor.pth"
    torch.save({
        'masamune_state_dict': engine.university.state_dict(),
        'lm_head_state_dict': engine.lm_head.state_dict(),
        'embedding_state_dict': engine.embedding.state_dict(),
        'step': step,
        'loss': loss,
        'phase': 'conversational_fluency_v17'
    }, anchor_path)
    print(f"  [SAVE] {anchor_path} (primary speech anchor updated)")


def test_inference(engine, prompts=None):
    """Run a quick inference test to show current speech quality."""
    if prompts is None:
        prompts = ["Who are you?", "How are you doing today?"]

    engine.university.eval()
    engine.lm_head.eval()
    engine.embedding.eval()

    for prompt in prompts:
        try:
            result = engine.pulse(prompt, max_tokens=60, temperature=0.75, top_p=0.9)
            response = result['response']
            latency = result['latency_ms']
            print(f"  Q: {prompt}")
            print(f"  A: {response[:200]}")
            print(f"     ({latency:.0f}ms)")
            print()
        except Exception as e:
            print(f"  [INFERENCE ERROR] {e}")

    # Set back to train mode
    engine.university.train()
    engine.lm_head.train()
    engine.embedding.train()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HPP Conversational Fluency Training")
    parser.add_argument('--steps', type=int, default=1000, help='Training steps')
    parser.add_argument('--lr', type=float, default=5e-5, help='Learning rate')
    parser.add_argument('--batch', type=int, default=2, help='Batch size')
    parser.add_argument('--seq-len', type=int, default=192, help='Sequence length')
    args = parser.parse_args()

    train_conversational(
        steps=args.steps,
        lr=args.lr,
        batch_size=args.batch,
        seq_len=args.seq_len
    )
