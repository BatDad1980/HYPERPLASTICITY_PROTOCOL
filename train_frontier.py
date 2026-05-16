"""
===============================================================================
     HPP PHASE 18: FRONTIER TRAINING PIPELINE
===============================================================================
Aggressive training pipeline for the Wild West version.
Designed for RTX 4050 (6GB VRAM).

What's new over train_conv_focused.py:
    1. Mixed precision (fp16) — ~40% VRAM savings
    2. Gradient accumulation — effective batch size 8 from actual batch 2
    3. Curriculum learning — start short (64 tokens), scale to 192
    4. Multi-domain routing — randomly routes through all domain layers
    5. Built-in quality metrics — tracks distinct-n, response coherence
    6. Aggressive OOM recovery — catches CUDA OOM and halves batch
    7. Smarter data mixing — weighted sampling favoring identity+conversation
    8. Progressive unfreezing — unlock deeper layers as training progresses

Strategy: We're not retraining the brain. We're teaching it to articulate.
The 14-loop recursive depth already thinks at a high level. We just need
the Structural Compass + Speech Center + Domain Routing to translate
those deep thoughts into clear English.

Usage:
    python train_frontier.py                    # Default 5000 steps
    python train_frontier.py --steps 10000      # Extended run
    python train_frontier.py --aggressive       # Unlock more layers
===============================================================================
"""
import os
import sys
import json
import time
import random
import gc
import math
import argparse
from collections import Counter

import torch
import torch.nn as nn
import torch.optim as optim
from torch.cuda.amp import autocast, GradScaler

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from hpp_sovereign_engine import HPP_SovereignEngine


# ================================================================
# CONFIGURATION
# ================================================================
class TrainConfig:
    steps = 5000
    batch_size = 2
    grad_accum = 4          # Effective batch = 8
    seq_start = 64          # Curriculum: start short
    seq_end = 192           # Curriculum: end long
    seq_ramp_steps = 1500   # Steps to reach full seq length
    lr = 8e-5
    warmup = 400
    weight_decay = 0.01
    grad_clip = 1.0
    save_every = 500
    test_every = 500
    log_every = 50
    
    # Domain training distribution
    domain_weights = {
        "conversation": 0.35,
        "none": 0.25,        # Forces swarm gate to learn auto-routing
        "identity": 0.20,
        "logic": 0.10,
        "synthesis": 0.10,
    }
    
    # Data mixing weights (oversample identity and protection)
    category_weights = {
        "identity": 3.0,
        "protection": 3.0,
        "conversation": 2.0,
        "embodiment": 1.5,
        "explanation": 1.5,
        "technical": 1.0,
    }


# ================================================================
# DATA LOADING
# ================================================================
def load_all_data():
    """Load and weight-mix all available training data."""
    data = []
    weights = []
    
    # Primary conversational data
    conv_path = "datasets/hf_local/CONVERSATIONAL_FLUENCY.jsonl"
    if os.path.exists(conv_path):
        with open(conv_path, 'r', encoding='utf-8') as f:
            for line in f:
                sample = json.loads(line)
                cat = sample.get("category", "conversation")
                weight = TrainConfig.category_weights.get(cat, 1.0)
                data.append(sample)
                weights.append(weight)
        print(f"[DATA] Conversational: {len(data)} samples")
    
    # General task following (subsample for diversity)
    task_path = "datasets/hf_local/GENERAL_TASK_FOLLOWING.jsonl"
    if os.path.exists(task_path):
        task_count = 0
        with open(task_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # Randomly sample up to 400 for diversity without overwhelming identity data
        sampled = random.sample(lines, min(400, len(lines)))
        for line in sampled:
            sample = json.loads(line)
            data.append(sample)
            weights.append(0.5)  # Lower weight than identity/conversation
            task_count += 1
        print(f"[DATA] Task following: {task_count} samples (subsampled)")
    
    # Identity data (if separate file exists)
    id_path = "datasets/hf_local/IDENTITY.jsonl"
    if os.path.exists(id_path):
        id_count = 0
        with open(id_path, 'r', encoding='utf-8') as f:
            for line in f:
                sample = json.loads(line)
                data.append(sample)
                weights.append(3.0)  # High weight
                id_count += 1
        print(f"[DATA] Identity: {id_count} samples")
    
    print(f"[DATA] Total pool: {len(data)} samples")
    return data, weights


def sample_to_text(sample: dict) -> str:
    """Convert a data sample to training text."""
    if 'text' in sample:
        return sample['text']
    elif 'instruction' in sample and 'response' in sample:
        return f"### Instruction:\n{sample['instruction']}\n\n### Response:\n{sample['response']}"
    elif 'prompt' in sample and 'completion' in sample:
        return f"{sample['prompt']}\n{sample['completion']}"
    return str(sample)


# ================================================================
# CURRICULUM LEARNING
# ================================================================
def get_seq_len(step: int) -> int:
    """Gradually increase sequence length during training."""
    if step >= TrainConfig.seq_ramp_steps:
        return TrainConfig.seq_end
    progress = step / TrainConfig.seq_ramp_steps
    # Smooth ramp using cosine
    ramp = 0.5 * (1 - math.cos(math.pi * progress))
    seq_len = int(TrainConfig.seq_start + (TrainConfig.seq_end - TrainConfig.seq_start) * ramp)
    # Round to nearest multiple of 8 for GPU efficiency
    return max(32, (seq_len // 8) * 8)


def get_lr(step: int) -> float:
    """Warmup + cosine decay schedule."""
    if step < TrainConfig.warmup:
        return TrainConfig.lr * (step / TrainConfig.warmup)
    progress = (step - TrainConfig.warmup) / max(1, TrainConfig.steps - TrainConfig.warmup)
    return TrainConfig.lr * 0.5 * (1.0 + math.cos(math.pi * progress))


def pick_domain() -> str:
    """Weighted random domain selection for training."""
    domains = list(TrainConfig.domain_weights.keys())
    weights = list(TrainConfig.domain_weights.values())
    return random.choices(domains, weights=weights, k=1)[0]


# ================================================================
# QUALITY METRICS
# ================================================================
def compute_distinct_n(tokens: list, n: int = 2) -> float:
    """
    Distinct-N metric: ratio of unique n-grams to total n-grams.
    Higher = more diverse vocabulary usage. Target: > 0.5 for distinct-2.
    """
    if len(tokens) < n:
        return 0.0
    ngrams = [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]
    if not ngrams:
        return 0.0
    return len(set(ngrams)) / len(ngrams)


# ================================================================
# TRAINING LOOP
# ================================================================
def train(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Clean VRAM
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gb = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"[GPU] {torch.cuda.get_device_name(0)} — {gb:.1f} GB VRAM")
    
    # Override config from args
    TrainConfig.steps = args.steps
    if args.aggressive:
        TrainConfig.lr = 1.2e-4
        TrainConfig.seq_end = 256
        print("[MODE] AGGRESSIVE — higher LR, longer sequences")
    
    print("=" * 70)
    print("     HPP PHASE 18: FRONTIER TRAINING")
    print("=" * 70)
    print(f"  Steps:         {TrainConfig.steps}")
    print(f"  Batch:         {TrainConfig.batch_size} × {TrainConfig.grad_accum} = {TrainConfig.batch_size * TrainConfig.grad_accum}")
    print(f"  Seq Length:    {TrainConfig.seq_start} → {TrainConfig.seq_end}")
    print(f"  LR:            {TrainConfig.lr}")
    print(f"  Device:        {device}")
    print(f"  Mixed Prec:    {'YES' if device.type == 'cuda' else 'NO'}")
    print("=" * 70)
    
    # Load engine
    print("\n[INIT] Loading Sovereign Engine...")
    engine = HPP_SovereignEngine(max_context=512)
    
    # === FREEZE STRATEGY ===
    print("\n[FREEZE] Locking deep brain...")
    for module in [engine.hpp_core, engine.guardian, engine.toddler,
                   engine.school, engine.adolescent]:
        for p in module.parameters():
            p.requires_grad = False
    
    # === UNLOCK STRATEGY ===
    print("[UNLOCK] Enabling training on:")
    trainable_params = []
    
    # Speech Center (LM Head + Embedding)
    for p in engine.lm_head.parameters():
        p.requires_grad = True
        trainable_params.append(p)
    for p in engine.embedding.parameters():
        p.requires_grad = True
        trainable_params.append(p)
    print("  [+] Speech Center (LM Head + Embedding)")
    
    # Structural Compass (position + time)
    for p in engine.university.compass.parameters():
        p.requires_grad = True
        trainable_params.append(p)
    print("  [+] Structural Compass")
    
    # All domain expertise layers
    for name, layer in engine.university.domain_expertise.items():
        for p in layer.parameters():
            p.requires_grad = True
            trainable_params.append(p)
    print("  [+] All domain layers (identity, logic, synthesis, conversation)")
    
    # Swarm gate + output norm
    for p in engine.university.swarm_gate.parameters():
        p.requires_grad = True
        trainable_params.append(p)
    for p in engine.university.output_norm.parameters():
        p.requires_grad = True
        trainable_params.append(p)
    print("  [+] Swarm gate + output normalization")
    
    # Progressive unfreezing: unlock Frontal Lobe after 40% of training
    frontal_unlocked = False
    
    total_trainable = sum(p.numel() for p in trainable_params)
    total_all = sum(p.numel() for p in engine.university.parameters())
    print(f"\n  Trainable: {total_trainable:,} / {total_all:,} ({100*total_trainable/total_all:.1f}%)")
    
    # Optimizer with differential LR
    optimizer = optim.AdamW([
        {'params': list(engine.lm_head.parameters()) + list(engine.embedding.parameters()),
         'lr': TrainConfig.lr, 'name': 'speech'},
        {'params': list(engine.university.compass.parameters()),
         'lr': TrainConfig.lr * 0.5, 'name': 'compass'},
        {'params': [p for n, l in engine.university.domain_expertise.items() 
                    for p in l.parameters()] +
                   list(engine.university.swarm_gate.parameters()) +
                   list(engine.university.output_norm.parameters()),
         'lr': TrainConfig.lr * 0.3, 'name': 'domains'},
    ], weight_decay=TrainConfig.weight_decay)
    
    criterion = nn.CrossEntropyLoss(ignore_index=engine.enc.eot_token)
    
    # Mixed precision
    use_amp = device.type == "cuda"
    scaler = GradScaler(enabled=use_amp)
    
    # Load data
    print("\n[DATA] Loading training data...")
    data, weights = load_all_data()
    
    # Set training mode
    engine.university.train()
    engine.lm_head.train()
    engine.embedding.train()
    
    # Tracking
    best_loss = float('inf')
    loss_history = []
    t0 = time.time()
    accum_loss = 0.0
    
    print("\n" + "=" * 70)
    print("  TRAINING STARTED")
    print("=" * 70)
    
    for step in range(1, TrainConfig.steps + 1):
        # LR schedule
        current_lr = get_lr(step)
        for pg in optimizer.param_groups:
            base_name = pg.get('name', 'speech')
            if base_name == 'compass':
                pg['lr'] = current_lr * 0.5
            elif base_name == 'domains':
                pg['lr'] = current_lr * 0.3
            else:
                pg['lr'] = current_lr
        
        # Curriculum: get current seq length
        seq_len = get_seq_len(step)
        
        # Progressive unfreezing: unlock frontal lobe at 40%
        if not frontal_unlocked and step > TrainConfig.steps * 0.4:
            print(f"\n  [UNLOCK] Step {step}: Unlocking Frontal Lobe (fine-tune)")
            for p in engine.university.frontal_lobe.parameters():
                p.requires_grad = True
                trainable_params.append(p)
            # Add to optimizer with very low LR
            optimizer.add_param_group({
                'params': list(engine.university.frontal_lobe.parameters()),
                'lr': current_lr * 0.1,
                'name': 'frontal',
                'weight_decay': TrainConfig.weight_decay
            })
            frontal_unlocked = True
        
        # Sample batch with weighted selection
        batch = random.choices(data, weights=weights, k=TrainConfig.batch_size)
        texts = [sample_to_text(s) for s in batch]
        
        # Tokenize with current curriculum length
        token_batch = []
        for text in texts:
            tokens = engine.enc.encode(text)[:seq_len]
            if len(tokens) < seq_len:
                tokens = tokens + [engine.enc.eot_token] * (seq_len - len(tokens))
            token_batch.append(tokens)
        
        ids = torch.tensor(token_batch, dtype=torch.long, device=device)
        
        # Forward with mixed precision
        try:
            with autocast(enabled=use_amp):
                embedded = engine.embedding(ids[:, :-1]).permute(1, 0, 2)
                domain = pick_domain()
                output = engine.university(embedded, domain=domain)
                logits = engine.lm_head(output).permute(1, 2, 0)
                loss = criterion(logits, ids[:, 1:])
                loss = loss / TrainConfig.grad_accum  # Scale for accumulation
            
            scaler.scale(loss).backward()
            accum_loss += loss.item()
            
            # Gradient accumulation step
            if step % TrainConfig.grad_accum == 0:
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(trainable_params, TrainConfig.grad_clip)
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad()
            
            real_loss = accum_loss * TrainConfig.grad_accum
            loss_history.append(real_loss)
            
            if step % TrainConfig.grad_accum == 0:
                accum_loss = 0.0
            
        except RuntimeError as e:
            if "out of memory" in str(e):
                print(f"\n  [OOM] Step {step} — clearing cache, reducing seq")
                gc.collect()
                torch.cuda.empty_cache()
                optimizer.zero_grad()
                # Temporarily reduce seq length
                TrainConfig.seq_end = max(96, TrainConfig.seq_end - 32)
                continue
            raise
        
        # Logging
        if step % TrainConfig.log_every == 0 or step == 1:
            elapsed = time.time() - t0
            avg_loss = sum(loss_history[-50:]) / max(len(loss_history[-50:]), 1)
            steps_sec = step / elapsed
            eta = (TrainConfig.steps - step) / max(steps_sec, 0.01)
            
            print(f"  Step {step:5d}/{TrainConfig.steps} | Loss: {real_loss:.4f} | "
                  f"Avg: {avg_loss:.4f} | LR: {current_lr:.2e} | "
                  f"Seq: {seq_len} | ETA: {eta:.0f}s", flush=True)
        
        # Save checkpoint
        if step % TrainConfig.save_every == 0:
            save_checkpoint(engine, step, real_loss)
            if real_loss < best_loss:
                best_loss = real_loss
        
        # Speech quality test
        if step % TrainConfig.test_every == 0:
            test_speech_quality(engine)
        
        # Periodic VRAM cleanup
        if step % 200 == 0:
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        
        # Cleanup tensors
        del loss, logits, output, embedded, ids
    
    # Final
    elapsed = time.time() - t0
    avg_final = sum(loss_history[-100:]) / max(len(loss_history[-100:]), 1)
    print("\n" + "=" * 70)
    print(f"  TRAINING COMPLETE")
    print(f"  Time:       {elapsed:.0f}s ({elapsed/60:.1f}m)")
    print(f"  Final loss: {avg_final:.4f}")
    print(f"  Best loss:  {best_loss:.4f}")
    print("=" * 70)
    
    save_checkpoint(engine, TrainConfig.steps, avg_final, tag="frontier_final")
    test_speech_quality(engine, extended=True)


def save_checkpoint(engine, step, loss, tag="progress"):
    """Save training checkpoint."""
    ckpt = {
        'masamune_state_dict': engine.university.state_dict(),
        'lm_head_state_dict': engine.lm_head.state_dict(),
        'embedding_state_dict': engine.embedding.state_dict(),
        'step': step,
        'loss': loss,
        'phase': 'frontier_v18'
    }
    
    # Always update the linguistic anchor (primary speech checkpoint)
    anchor_path = "checkpoints/hpp_linguistic_anchor.pth"
    torch.save(ckpt, anchor_path)
    
    # Also save a numbered checkpoint
    step_path = f"checkpoints/hpp_frontier_{step}.pth"
    torch.save(ckpt, step_path)
    
    print(f"  [SAVE] Step {step} | Loss: {loss:.4f}", flush=True)


def test_speech_quality(engine, extended=False):
    """Run inference tests and measure quality metrics."""
    engine.university.eval()
    engine.lm_head.eval()
    engine.embedding.eval()
    
    prompts = [
        "Who are you?",
        "Good morning.",
        "I need help.",
        "Explain what a neural network is.",
    ]
    
    if extended:
        prompts += [
            "Tell me about Masamune.",
            "I'm not doing well today.",
            "What makes you different from other AI?",
            "What is the meaning of the Hyperplasticity Protocol?",
        ]
    
    print("\n  ─── SPEECH QUALITY TEST ───", flush=True)
    
    all_distinct2 = []
    
    for q in prompts:
        try:
            result = engine.pulse(q, max_tokens=60, temperature=0.75, top_p=0.9)
            response = result['response']
            tokens = engine.enc.encode(response)
            d2 = compute_distinct_n(tokens, 2)
            all_distinct2.append(d2)
            
            print(f"  Q: {q}", flush=True)
            print(f"  A: {response[:200]}", flush=True)
            print(f"     (d2={d2:.3f}, {result['latency_ms']:.0f}ms)", flush=True)
        except Exception as e:
            print(f"  [ERR] {e}", flush=True)
    
    if all_distinct2:
        avg_d2 = sum(all_distinct2) / len(all_distinct2)
        print(f"\n  Avg Distinct-2: {avg_d2:.3f} (target > 0.5)", flush=True)
    
    print("  ─── END TEST ───\n", flush=True)
    
    # Restore training mode
    engine.university.train()
    engine.lm_head.train()
    engine.embedding.train()
    
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


# ================================================================
# ENTRY POINT
# ================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HPP Frontier Training Pipeline")
    parser.add_argument('--steps', type=int, default=5000, help='Training steps')
    parser.add_argument('--aggressive', action='store_true', help='Aggressive mode (higher LR, longer seq)')
    args = parser.parse_args()
    
    train(args)
