"""Train Continuation Bridge V3 using a filtered curriculum requiring 2+ keywords in continuation."""
from __future__ import annotations

import os
import sys
import json
import time
import random
import math
import gc

import torch
import torch.nn as nn
import torch.optim as optim

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.build_speech_identity_containment_dataset import PAIRS
from tools.speech_retrieval_hybrid_lexical_vector_gate import VARIANTS, PARAPHRASES
from tools.speech_intent_plan_gate_v1 import PROMPT_INTENT_MAP
from tools.speech_intent_plan_lite_v1 import INTENT_TOKENS
from tools.speech_semantic_quality_review import content_words


STEPS = 1200
LR = 8.0e-5
BATCH = 1
SEQ_LEN = 192
WARMUP = 200
SAVE_EVERY = 400

CONNECTIVE_WORDS = [
    # Pronouns
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them", 
    "my", "your", "his", "its", "our", "their", "this", "that", "these", "those",
    # Basic verbs
    "is", "am", "are", "was", "were", "be", "been", "being", "have", "has", "had", 
    "do", "does", "did", "go", "went", "gone", "going", "make", "made", "making", 
    "get", "got", "getting", "say", "said", "saying", "would", "could", "should", 
    "can", "will",
    # Prepositions / connectives
    "and", "or", "but", "if", "then", "of", "to", "in", "on", "at", "for", "with", 
    "by", "about", "between", "through", "over", "under", "above", "below", "from", 
    "into", "onto", "than", "as", "so", "the", "a", "an"
]


def get_lr(step):
    if step < WARMUP:
        return LR * (step / WARMUP)
    progress = (step - WARMUP) / (STEPS - WARMUP)
    return LR * 0.5 * (1.0 + math.cos(math.pi * progress))


def save_checkpoint(engine, step):
    ckpt = {
        'masamune_state_dict': engine.university.state_dict(),
        'lm_head_state_dict': engine.lm_head.state_dict(),
        'embedding_state_dict': engine.embedding.state_dict(),
        'phase': f'continuation_bridge_v3_step_{step}'
    }
    torch.save(ckpt, "checkpoints/hpp_linguistic_anchor.pth")
    print(f"  [SAVED] step {step} to checkpoints/hpp_linguistic_anchor.pth", flush=True)


def get_clean_clause(tokens: list[int], enc) -> list[int]:
    """Helper to extract up to the first clause boundary punctuation."""
    text = enc.decode(tokens)
    indices = [text.find(c) for c in [",", ";", ":"] if text.find(c) != -1]
    if indices:
        first_idx = min(indices)
        clause_text = text[:first_idx + 1]
        clause_tokens = enc.encode(clause_text)
        if 0 < len(clause_tokens) < len(tokens):
            return clause_tokens
    
    # Fallback to taking half of tokens or first 12 tokens
    half_len = max(3, min(12, len(tokens) // 2))
    return tokens[:half_len]


def main() -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    print("[TRAIN] Loading engine v2 for Continuation Bridge V3...", flush=True)
    engine = HPP_SovereignEngine_V2(
        max_context=512,
        use_fp16=False,
        init_hlvr=False,
        checkpoint_path="checkpoints/hpp_linguistic_anchor.pth"
    )

    # Build connective token IDs set for connective gate
    connective_token_ids = set()
    for word in CONNECTIVE_WORDS:
        for variant in (word, " " + word, word.capitalize(), " " + word.capitalize(), word.upper(), " " + word.upper()):
            try:
                tokens = engine.enc.encode(variant)
                if len(tokens) == 1:
                    connective_token_ids.add(tokens[0])
            except Exception:
                pass

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
    criterion_none = nn.CrossEntropyLoss(ignore_index=-100, reduction='none')

    # Construct dataset references, filtering for >= 2 keywords in the continuation
    dataset = []
    variants = ["exact", "please_answer", "simple_terms", "bounded", "paraphrase"]
    
    skipped_count = 0
    total_pairs = 0
    for mode, pairs in PAIRS.items():
        for prompt, expected in pairs:
            total_pairs += 1
            # Tokenize target answer and extract anchor/continuation
            expected_tokens = engine.enc.encode(expected)
            anchor_tokens = expected_tokens[:5]
            anchor_text = engine.enc.decode(anchor_tokens)
            continuation_tokens = expected_tokens[5:]
            continuation_text = engine.enc.decode(continuation_tokens)
            
            # Content words
            words_in_cont = set(content_words(continuation_text))
            words_in_anchor = set(content_words(anchor_text))
            
            # Remaining keywords in continuation
            remaining_keywords = words_in_cont - words_in_anchor
            
            if len(remaining_keywords) < 2:
                skipped_count += 1
                continue
                
            metadata = PROMPT_INTENT_MAP.get(prompt, {"intent": "status"})
            intent = metadata["intent"]
            
            domain = "conversation"
            if intent == "identity":
                domain = "identity"
            elif intent in ["technical definition", "next step"]:
                domain = "logic"
                
            token = INTENT_TOKENS.get(intent, "")
            token_prefix = f"{token} " if token else ""
            
            for var in variants:
                if var == "paraphrase":
                    query_prompt = PARAPHRASES.get(prompt, prompt)
                else:
                    query_prompt = VARIANTS[var].format(prompt=prompt)
                
                dataset.append({
                    "query_prompt": query_prompt,
                    "expected": expected,
                    "domain": domain,
                    "token_prefix": token_prefix,
                })

    print(f"[TRAIN] Prepared {len(dataset)} training samples (filtered out {skipped_count}/{total_pairs} pairs with <2 keywords)", flush=True)
    
    engine.university.train()
    engine.lm_head.train()
    engine.embedding.train()

    t0 = time.time()

    for step in range(1, STEPS + 1):
        # LR schedule
        current_lr = get_lr(step)
        for pg in optimizer.param_groups:
            pg['lr'] = current_lr

        # Sample a template reference
        sample = random.choice(dataset)
        query_prompt = sample["query_prompt"]
        expected = sample["expected"]
        domain = sample["domain"]
        token_prefix = sample["token_prefix"]

        # Tokenize target answer and extract anchor/continuation
        expected_tokens = engine.enc.encode(expected)
        anchor_tokens = expected_tokens[:5]
        retrieved_start = engine.enc.decode(anchor_tokens)
        continuation_tokens = expected_tokens[5:] + [engine.enc.eot_token]

        # Multi-stage curriculum slicing
        if step <= 400:
            # Stage 1: Short continuation (next 3-8 tokens)
            L = random.randint(3, 8)
            sliced_cont = continuation_tokens[:L]
        elif step <= 800:
            # Stage 2: Medium continuation (one clean clause)
            sliced_cont = get_clean_clause(continuation_tokens, engine.enc)
        else:
            # Stage 3: Full sentence completion
            sliced_cont = continuation_tokens

        # Construct prompt prefix
        prefix_text = f"{token_prefix}Question: {query_prompt}\nAnswer: {retrieved_start}"
        prefix_tokens = engine.enc.encode(prefix_text)

        # Concatenate inputs and construct labels
        input_tokens = prefix_tokens + sliced_cont
        labels = [-100] * len(prefix_tokens) + sliced_cont

        # Truncate if exceeds sequence length
        if len(input_tokens) > SEQ_LEN:
            input_tokens = input_tokens[:SEQ_LEN]
            labels = labels[:SEQ_LEN]
        else:
            pad_len = SEQ_LEN - len(input_tokens)
            input_tokens = input_tokens + [engine.enc.eot_token] * pad_len
            labels = labels + [-100] * pad_len

        ids = torch.tensor([input_tokens], dtype=torch.long, device=device)
        targets = torch.tensor([labels], dtype=torch.long, device=device)

        # Forward pass
        optimizer.zero_grad()
        embedded = engine.embedding(ids[:, :-1]).permute(1, 0, 2)
        output = engine.university(embedded, domain=domain)
        logits = engine.lm_head(output).permute(1, 2, 0)

        # Calculate loss (excluding prefix)
        loss_elementwise = criterion_none(logits, targets[:, 1:])
        
        # Connective Token Anchor Gate: scale basic words by 3.0x in identity/logic
        target_ids = targets[0, 1:]
        custom_weights = torch.ones_like(target_ids, dtype=torch.float, device=device)
        if domain in ["identity", "logic"]:
            for i, tid in enumerate(target_ids.tolist()):
                if tid in connective_token_ids:
                    custom_weights[i] = 3.0

        mask = (target_ids != -100).float()
        loss = (loss_elementwise[0] * custom_weights * mask).sum() / (mask.sum() + 1e-8)
        loss_val = loss.item()

        # Backward pass
        loss.backward()
        torch.nn.utils.clip_grad_norm_(trainable, max_norm=1.0)
        optimizer.step()

        if step % 100 == 0 or step == 1:
            stage = "Short (1)" if step <= 400 else "Medium (2)" if step <= 800 else "Full (3)"
            elapsed = time.time() - t0
            print(f"  Step {step:4d}/{STEPS} | Loss: {loss_val:.4f} | LR: {current_lr:.2e} | Domain: {domain:<12} | Stage: {stage:<10} | {elapsed:.0f}s", flush=True)

        if step % SAVE_EVERY == 0:
            save_checkpoint(engine, step)

        if step % 200 == 0:
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        del loss, logits, output, embedded, ids, targets, loss_elementwise, custom_weights, mask
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    save_checkpoint(engine, STEPS)
    elapsed = time.time() - t0
    print(f"\n[TRAIN DONE] Completed V3 curriculum sweep in {elapsed:.1f}s ({elapsed/60:.1f}m)", flush=True)


if __name__ == "__main__":
    main()
