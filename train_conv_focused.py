"""
HPP Phase 17d: Clean conversational training with fixed engine.
No Mission Anchor in generation loop. Divisive repetition penalty.
5000 steps, warmup + cosine decay, OOM protection.
"""
import os, sys, json, time, random, gc, math
import torch
import torch.nn as nn
import torch.optim as optim

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from hpp_sovereign_engine import HPP_SovereignEngine

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
        'phase': 'conversational_v17d'
    }
    torch.save(ckpt, "checkpoints/hpp_linguistic_anchor.pth")
    print(f"  [SAVED] step {step}", flush=True)


def test_speech(engine):
    engine.university.eval()
    engine.lm_head.eval()
    engine.embedding.eval()
    print("  --- SPEECH TEST ---", flush=True)
    for q in ["Who are you?", "Good morning.", "I need help.",
              "Tell me about Masamune.", "I'm not doing well today."]:
        try:
            r = engine.pulse(q, max_tokens=50, temperature=0.7, top_p=0.9)
            print(f"  Q: {q}", flush=True)
            print(f"  A: {r['response'][:180]}", flush=True)
        except Exception as e:
            print(f"  [ERR] {e}", flush=True)
    print("  --- END TEST ---\n", flush=True)
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

    print(f"[TRAIN] Loading engine...", flush=True)
    engine = HPP_SovereignEngine(max_context=512)

    # Freeze deep brain
    for m in [engine.hpp_core, engine.guardian, engine.toddler,
              engine.school, engine.adolescent]:
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
    criterion = nn.CrossEntropyLoss(ignore_index=engine.enc.eot_token)

    # Load data
    data = [json.loads(l) for l in open(
        'datasets/hf_local/CONVERSATIONAL_FLUENCY.jsonl', 'r', encoding='utf-8'
    )]
    print(f"[TRAIN] {len(data)} samples | {STEPS} steps | batch {BATCH} | seq {SEQ_LEN}", flush=True)
    print(f"[TRAIN] LR: {LR} | Warmup: {WARMUP} | Device: {device}", flush=True)

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
        texts = []
        for s in batch:
            if 'text' in s:
                texts.append(s['text'])
            else:
                texts.append(f"### Instruction:\n{s['instruction']}\n\n### Response:\n{s['response']}")

        # Tokenize
        token_batch = []
        for text in texts:
            tokens = engine.enc.encode(text)[:SEQ_LEN]
            if len(tokens) < SEQ_LEN:
                tokens = tokens + [engine.enc.eot_token] * (SEQ_LEN - len(tokens))
            token_batch.append(tokens)

        ids = torch.tensor(token_batch, dtype=torch.long, device=device)

        # Forward
        optimizer.zero_grad()
        embedded = engine.embedding(ids[:, :-1]).permute(1, 0, 2)
        output = engine.university(embedded, domain="conversation")
        logits = engine.lm_head(output).permute(1, 2, 0)
        loss = criterion(logits, ids[:, 1:])

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
        del loss, logits, output, embedded, ids
        torch.cuda.empty_cache()

    save_checkpoint(engine, STEPS)
    elapsed = time.time() - t0
    print(f"\n[DONE] {elapsed:.0f}s ({elapsed/60:.1f}m) | Final loss: {loss_val:.4f}", flush=True)
    test_speech(engine)


if __name__ == "__main__":
    run()
