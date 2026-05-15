"""
HPP Phase 17 v3: Clean focused conversational training.
Memory-safe, frequent saves, simple and reliable.
"""
import os, sys, json, time, random, gc
import torch
import torch.nn as nn
import torch.optim as optim

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from hpp_sovereign_engine import HPP_SovereignEngine

STEPS = 3000
LR = 8e-5
BATCH = 2
SEQ_LEN = 96

def save_checkpoint(engine, step):
    ckpt = {
        'masamune_state_dict': engine.university.state_dict(),
        'lm_head_state_dict': engine.lm_head.state_dict(),
        'embedding_state_dict': engine.embedding.state_dict(),
        'phase': 'conversational_v17_v3'
    }
    torch.save(ckpt, "checkpoints/hpp_linguistic_anchor.pth")
    torch.save(ckpt, "checkpoints/hpp_conversational_final.pth")
    print(f"  [SAVED] step {step}", flush=True)


def test_speech(engine):
    engine.university.eval()
    engine.lm_head.eval()
    engine.embedding.eval()
    for q in ["Who are you?", "Good morning.", "I need help."]:
        try:
            r = engine.pulse(q, max_tokens=40, temperature=0.7, top_p=0.9)
            print(f"  Q: {q}", flush=True)
            print(f"  A: {r['response'][:150]}", flush=True)
        except Exception as e:
            print(f"  [ERR] {e}", flush=True)
    print(flush=True)
    engine.university.train()
    engine.lm_head.train()
    engine.embedding.train()
    gc.collect()
    torch.cuda.empty_cache()


def run():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Clear GPU
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

    # Unlock speech layers
    trainable = []
    for m in [engine.lm_head, engine.embedding, engine.university.compass,
              engine.university.domain_expertise['conversation'],
              engine.university.swarm_gate, engine.university.output_norm]:
        for p in m.parameters():
            p.requires_grad = True
            trainable.append(p)

    optimizer = optim.AdamW(trainable, lr=LR, weight_decay=0.01)
    criterion = nn.CrossEntropyLoss(ignore_index=engine.enc.eot_token)

    # Load data
    data = [json.loads(l) for l in open(
        'datasets/hf_local/CONVERSATIONAL_FLUENCY.jsonl', 'r', encoding='utf-8'
    )]
    print(f"[TRAIN] {len(data)} samples | {STEPS} steps | batch {BATCH} | seq {SEQ_LEN}", flush=True)

    engine.university.train()
    engine.lm_head.train()
    engine.embedding.train()

    t0 = time.time()
    last_loss = 0.0

    for step in range(1, STEPS + 1):
        # Sample batch
        batch = random.choices(data, k=BATCH)
        texts = []
        for s in batch:
            if 'text' in s:
                texts.append(s['text'])
            else:
                texts.append(
                    f"### Instruction:\n{s['instruction']}\n\n"
                    f"### Response:\n{s['response']}"
                )

        # Tokenize
        token_batch = []
        for text in texts:
            tokens = engine.enc.encode(text)[:SEQ_LEN]
            pad_len = SEQ_LEN - len(tokens)
            if pad_len > 0:
                tokens = tokens + [engine.enc.eot_token] * pad_len
            token_batch.append(tokens)

        ids = torch.tensor(token_batch, dtype=torch.long, device=device)

        # Forward
        optimizer.zero_grad()
        embedded = engine.embedding(ids[:, :-1]).permute(1, 0, 2)
        output = engine.university(embedded, domain="conversation")
        logits = engine.lm_head(output).permute(1, 2, 0)
        loss = criterion(logits, ids[:, 1:])

        last_loss = loss.item()

        # Backward
        loss.backward()
        torch.nn.utils.clip_grad_norm_(trainable, max_norm=1.0)
        optimizer.step()

        # Log
        if step % 100 == 0 or step == 1:
            elapsed = time.time() - t0
            print(f"  Step {step:5d}/{STEPS} | Loss: {last_loss:.4f} | {elapsed:.0f}s", flush=True)

        # Save
        if step % 500 == 0:
            save_checkpoint(engine, step)

        # Test
        if step % 1000 == 0:
            test_speech(engine)

        # Memory cleanup
        if step % 200 == 0:
            gc.collect()
            torch.cuda.empty_cache()

    # Final
    save_checkpoint(engine, STEPS)
    elapsed = time.time() - t0
    print(f"\n[DONE] {elapsed:.0f}s ({elapsed/60:.1f}m) | Final loss: {last_loss:.4f}", flush=True)
    test_speech(engine)


if __name__ == "__main__":
    run()
