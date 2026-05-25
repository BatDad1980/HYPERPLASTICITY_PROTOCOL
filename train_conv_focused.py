"""
HPP Phase 17d: Clean conversational training with fixed engine.
No Mission Anchor in generation loop. Divisive repetition penalty.
2500 steps, warmup + cosine decay, OOM protection, response-only loss.
"""
import os, sys, json, time, random, gc, math
import torch
import torch.nn as nn
import torch.optim as optim

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2

STEPS = 2500
LR = 1.2e-4
BATCH = 2
SEQ_LEN = 96
WARMUP = 300
SAVE_EVERY = 500
TEST_EVERY = 1250

def save_checkpoint(engine, step):
    ckpt = {
        'masamune_state_dict': engine.university.state_dict(),
        'lm_head_state_dict': engine.lm_head.state_dict(),
        'embedding_state_dict': engine.embedding.state_dict(),
        'phase': 'conversational_v17d_v2'
    }
    torch.save(ckpt, "checkpoints/hpp_linguistic_anchor.pth")
    print(f"  [SAVED] step {step} to checkpoints/hpp_linguistic_anchor.pth", flush=True)


def test_speech(engine):
    # Set to eval mode for inference
    engine.university.eval()
    engine.lm_head.eval()
    engine.embedding.eval()
    print("  --- SPEECH TEST (WITHOUT HLVR TO TEST RAW WEIGHTS) ---", flush=True)
    # Test queries
    for q in ["Who are you?", "Good morning.", "I need help.",
              "Tell me about Masamune.", "I'm not doing well today."]:
        try:
            # We explicitly pass use_hlvr=False to evaluate the raw neural response changes
            r = engine.pulse(q, max_tokens=50, temperature=0.7, top_p=0.9, use_hlvr=False)
            print(f"  Q: {q}", flush=True)
            print(f"  A: {r['response'][:180]}", flush=True)
        except Exception as e:
            print(f"  [ERR] {e}", flush=True)
    print("  --- END TEST ---\n", flush=True)
    
    # Restore train mode
    engine.university.train()
    engine.lm_head.train()
    engine.embedding.train()
    
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def get_lr(step):
    if step < WARMUP:
        return LR * (step / WARMUP)
    progress = (step - WARMUP) / (STEPS - WARMUP)
    return LR * 0.5 * (1.0 + math.cos(math.pi * progress))


def run():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gb = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"[GPU] {gb:.1f} GB total VRAM", flush=True)

    print(f"[TRAIN] Loading engine v2...", flush=True)
    # Load HPP_SovereignEngine_V2 with use_fp16=False for stable gradient updates
    engine = HPP_SovereignEngine_V2(max_context=512, use_fp16=False, init_hlvr=False, checkpoint_path="checkpoints/hpp_linguistic_anchor.pth")

    # Freeze deep brains & non-speech layers
    for m in [engine.hpp_core, engine.guardian, engine.toddler,
              engine.school, engine.adolescent, engine.agency,
              engine.anchor, engine.samurai_body, engine.proprioception]:
        for p in m.parameters():
            p.requires_grad = False

    # Unlock speech + compass + domains
    trainable = []
    for m in [engine.embedding, engine.lm_head,
              engine.university.compass, engine.university.output_norm,
              engine.university.swarm_gate]:
        for p in m.parameters():
            p.requires_grad = True
            trainable.append(p)
    for name, layer in engine.university.domain_expertise.items():
        for p in layer.parameters():
            p.requires_grad = True
            trainable.append(p)

    optimizer = optim.AdamW(trainable, lr=LR, weight_decay=0.01)
    # Use ignore_index=-100 to mask instruction prompt templates
    criterion = nn.CrossEntropyLoss(ignore_index=-100)

    # Load data
    dataset_path = 'datasets/hf_local/CONVERSATIONAL_FLUENCY.jsonl'
    data = [json.loads(l) for l in open(dataset_path, 'r', encoding='utf-8')]
    print(f"[TRAIN] {len(data)} samples | {STEPS} steps | batch {BATCH} | seq {SEQ_LEN}", flush=True)
    print(f"[TRAIN] LR: {LR} | Warmup: {WARMUP} | Device: {device}", flush=True)

    # Put speech components into train mode
    engine.university.train()
    engine.lm_head.train()
    engine.embedding.train()

    t0 = time.time()

    for step in range(1, STEPS + 1):
        # LR schedule
        current_lr = get_lr(step)
        for pg in optimizer.param_groups:
            pg['lr'] = current_lr

        # Sample batch
        batch = random.choices(data, k=BATCH)
        
        token_batch = []
        label_batch = []
        for s in batch:
            instruction = s.get('instruction', '')
            response = s.get('response', '')
            
            # Construct prefix and response tokens separately
            prefix = f"### Instruction:\n{instruction}\n\n### Response:\n"
            prefix_tokens = engine.enc.encode(prefix)
            response_tokens = engine.enc.encode(response) + [engine.enc.eot_token]
            
            # Concatenate inputs and construct labels
            input_tokens = prefix_tokens + response_tokens
            labels = [-100] * len(prefix_tokens) + response_tokens
            
            # Truncate
            if len(input_tokens) > SEQ_LEN:
                input_tokens = input_tokens[:SEQ_LEN]
                labels = labels[:SEQ_LEN]
            # Pad
            else:
                pad_len = SEQ_LEN - len(input_tokens)
                input_tokens = input_tokens + [engine.enc.eot_token] * pad_len
                labels = labels + [-100] * pad_len
                
            token_batch.append(input_tokens)
            label_batch.append(labels)

        ids = torch.tensor(token_batch, dtype=torch.long, device=device)
        targets = torch.tensor(label_batch, dtype=torch.long, device=device)

        # Forward
        optimizer.zero_grad()
        embedded = engine.embedding(ids[:, :-1]).permute(1, 0, 2)
        # Force domain specialization to "conversation"
        output = engine.university(embedded, domain="conversation")
        logits = engine.lm_head(output).permute(1, 2, 0)
        loss = criterion(logits, targets[:, 1:])

        loss_val = loss.item()

        # Backward
        loss.backward()
        torch.nn.utils.clip_grad_norm_(trainable, max_norm=1.0)
        optimizer.step()

        if step % 100 == 0 or step == 1:
            elapsed = time.time() - t0
            print(f"  Step {step:5d}/{STEPS} | Loss: {loss_val:.4f} | LR: {current_lr:.2e} | {elapsed:.0f}s", flush=True)

        if step % SAVE_EVERY == 0:
            save_checkpoint(engine, step)

        if step % TEST_EVERY == 0:
            test_speech(engine)

        # OOM protection - aggressive for 6GB VRAM
        if step % 100 == 0:
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        del loss, logits, output, embedded, ids, targets
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    save_checkpoint(engine, STEPS)
    elapsed = time.time() - t0
    print(f"\n[DONE] {elapsed:.0f}s ({elapsed/60:.1f}m) | Final loss: {loss_val:.4f}", flush=True)
    test_speech(engine)


if __name__ == "__main__":
    run()
