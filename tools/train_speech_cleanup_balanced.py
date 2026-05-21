"""Guarded entrypoint for the next HPP V2 speech cleanup run.

This script is intentionally conservative. It defaults to the balanced cleanup
dataset and refuses to start training unless --confirm-gpu-training is passed.
Use it after checking power, cooling, and that the latest work is committed.
"""
from __future__ import annotations

import argparse
import gc
import json
import math
import os
import random
import sys
import time
from collections import defaultdict

import torch
import torch.nn as nn
import torch.optim as optim

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine import HPP_SovereignEngine


DEFAULT_DATA = os.path.join("datasets", "hf_local", "SPEECH_CLEANUP_BALANCED_V1.jsonl")
DEFAULT_OUT = os.path.join("checkpoints", "hpp_speech_cleanup_balanced_v1.pth")
TRAIN_DOMAINS = ["conversation", "logic", "identity", "synthesis"]
DOMAIN_KEYWORDS = {
    "identity": [
        "who are you",
        "your name",
        "your purpose",
        "masamune",
        "hepp",
        "what are you",
        "your creator",
        "your mission",
        "your oath",
        "jaxson",
        "journee",
        "bushido",
        "sovereign",
    ],
    "synthesis": [
        "calculate",
        "solve",
        "python",
        "code",
        "analyze",
        "write",
        "create",
        "build",
        "execute",
        "run",
        "compute",
        "implement",
    ],
    "logic": [
        "explain",
        "why",
        "how does",
        "what is",
        "define",
        "compare",
        "difference between",
        "prove",
        "reason",
    ],
}


def load_rows(path: str) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def detect_domain(text: str) -> str:
    lower = text.lower()
    scores = {
        domain: sum(1 for keyword in keywords if keyword in lower)
        for domain, keywords in DOMAIN_KEYWORDS.items()
    }
    best = max(scores, key=scores.get)
    if scores[best] > 0:
        return best
    return "conversation"


def row_prompt_text(row: dict) -> str:
    if row.get("prompt_text"):
        return str(row["prompt_text"])
    if row.get("instruction"):
        return str(row["instruction"])
    return row_to_text(row)


def training_rows_by_domain(rows: list[dict], strategy: str) -> dict[str, list[dict]]:
    grouped = defaultdict(list)
    for row in rows:
        if strategy == "conversation":
            domains = ["conversation"]
        elif strategy == "auto":
            domains = [detect_domain(row_prompt_text(row))]
        elif strategy == "all":
            domains = TRAIN_DOMAINS
        else:
            raise ValueError(f"Unknown domain strategy: {strategy}")

        for domain in domains:
            copy = dict(row)
            copy["_train_domain"] = domain
            grouped[domain].append(copy)
    return dict(grouped)


def row_to_text(row: dict) -> str:
    if row.get("text"):
        return str(row["text"])
    return f"### Instruction:\n{row.get('instruction', '')}\n\n### Response:\n{row.get('response', '')}"


def row_to_tokens_and_targets(engine, row: dict, seq_len: int, response_only_loss: bool) -> tuple[list[int], list[int]]:
    if response_only_loss and row.get("prompt_text") and row.get("response"):
        prefix = row.get("completion_prefix")
        if prefix is None:
            prefix = str(row["prompt_text"]).strip() + "\n"
        else:
            prefix = str(prefix)
        response = str(row["response"]).strip()
        prefix_tokens = engine.enc.encode(prefix)
        response_tokens = engine.enc.encode(response)
        tokens = prefix_tokens + response_tokens
        targets = [-100] * len(prefix_tokens) + response_tokens
    else:
        text = row_to_text(row)
        if response_only_loss and "### Response:\n" in text:
            prefix, response = text.split("### Response:\n", 1)
            prefix = prefix + "### Response:\n"
            prefix_tokens = engine.enc.encode(prefix)
            response_tokens = engine.enc.encode(response)
            tokens = prefix_tokens + response_tokens
            targets = [-100] * len(prefix_tokens) + response_tokens
        else:
            tokens = engine.enc.encode(text)
            targets = tokens.copy()

    tokens = tokens[:seq_len]
    targets = targets[:seq_len]
    if len(tokens) < seq_len:
        pad = seq_len - len(tokens)
        tokens += [engine.enc.eot_token] * pad
        targets += [engine.enc.eot_token] + [-100] * (pad - 1)
    return tokens, targets


def save_checkpoint(engine, path: str, step: int, loss: float, data_path: str, domain_strategy: str) -> None:
    torch.save(
        {
            "masamune_state_dict": engine.university.state_dict(),
            "lm_head_state_dict": engine.lm_head.state_dict(),
            "embedding_state_dict": engine.embedding.state_dict(),
            "step": step,
            "loss": loss,
            "data_path": data_path,
            "domain_strategy": domain_strategy,
            "phase": "speech_cleanup_balanced_v1",
        },
        path,
    )
    print(f"[SAVE] {path} step={step} loss={loss:.4f}", flush=True)


def is_cuda_oom(exc: RuntimeError) -> bool:
    text = str(exc).lower()
    return "out of memory" in text or "cuda error: out of memory" in text


def clear_cuda_pressure() -> None:
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


def load_checkpoint_override(engine, checkpoint_path: str) -> None:
    checkpoint = torch.load(checkpoint_path, map_location=engine.device, weights_only=True)
    state_dict = checkpoint.get("masamune_state_dict", {})
    engine.university.load_state_dict(state_dict, strict=False)
    if "lm_head_state_dict" in checkpoint:
        engine.lm_head.load_state_dict(checkpoint["lm_head_state_dict"])
    if "embedding_state_dict" in checkpoint:
        engine.embedding.load_state_dict(checkpoint["embedding_state_dict"])
    print(f"[BASE] Loaded checkpoint override: {checkpoint_path}", flush=True)


def train(args: argparse.Namespace) -> None:
    if not args.confirm_gpu_training:
        raise SystemExit(
            "Refusing to start training without --confirm-gpu-training. "
            "Check power/cooling first."
        )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    rows = load_rows(args.data)
    rows_by_domain = training_rows_by_domain(rows, args.domain_strategy)
    active_domains = sorted(rows_by_domain)
    random.seed(args.seed)
    torch.manual_seed(args.seed)

    print(f"[DATA] {args.data} samples={len(rows)}", flush=True)
    print(
        f"[DOMAIN] strategy={args.domain_strategy} active={active_domains} "
        f"expanded={sum(len(value) for value in rows_by_domain.values())}",
        flush=True,
    )
    print(f"[TRAIN] steps={args.steps} batch={args.batch} seq_len={args.seq_len} lr={args.lr}", flush=True)
    print(f"[DEVICE] {device}", flush=True)
    if torch.cuda.is_available():
        props = torch.cuda.get_device_properties(0)
        print(f"[CUDA] {props.name} vram_gb={props.total_memory / 1e9:.2f}", flush=True)
        torch.cuda.empty_cache()

    engine = HPP_SovereignEngine(max_context=512)
    if args.base_checkpoint:
        load_checkpoint_override(engine, args.base_checkpoint)

    for module in [engine.hpp_core, engine.guardian, engine.toddler, engine.school, engine.adolescent]:
        for param in module.parameters():
            param.requires_grad = False

    trainable = []
    modules = [
        engine.embedding,
        engine.lm_head,
        engine.university.compass,
        engine.university.output_norm,
        engine.university.swarm_gate,
    ]
    for domain in active_domains:
        modules.append(engine.university.domain_expertise[domain])
    for module in modules:
        for param in module.parameters():
            param.requires_grad = True
            trainable.append(param)

    optimizer = optim.AdamW(trainable, lr=args.lr, weight_decay=0.01)
    ignore_index = -100 if args.response_only_loss else engine.enc.eot_token
    criterion = nn.CrossEntropyLoss(ignore_index=ignore_index)

    started = time.time()
    loss_val = math.nan
    active_batch = args.batch
    active_seq_len = args.seq_len
    oom_count = 0
    engine.university.train()
    engine.embedding.train()
    engine.lm_head.train()

    for step in range(1, args.steps + 1):
        try:
            batch_domain = random.choice(active_domains)
            batch = random.choices(rows_by_domain[batch_domain], k=active_batch)
            token_batch = []
            target_batch = []
            for row in batch:
                tokens, targets = row_to_tokens_and_targets(
                    engine,
                    row,
                    active_seq_len,
                    args.response_only_loss,
                )
                token_batch.append(tokens)
                target_batch.append(targets)

            ids = torch.tensor(token_batch, dtype=torch.long, device=device)
            targets_tensor = torch.tensor(target_batch, dtype=torch.long, device=device)
            embedded = engine.embedding(ids[:, :-1]).permute(1, 0, 2)
            output = engine.university(embedded, domain=batch_domain)
            logits = engine.lm_head(output).permute(1, 2, 0)
            loss = criterion(logits, targets_tensor[:, 1:])
            loss_val = float(loss.item())

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(trainable, max_norm=1.0)
            optimizer.step()
        except RuntimeError as exc:
            if not is_cuda_oom(exc):
                raise

            oom_count += 1
            optimizer.zero_grad(set_to_none=True)
            clear_cuda_pressure()

            if active_batch > 1:
                active_batch = max(1, active_batch // 2)
                action = f"reduced batch to {active_batch}"
            elif active_seq_len > args.min_seq_len:
                active_seq_len = max(args.min_seq_len, active_seq_len - args.oom_seq_step)
                action = f"reduced seq_len to {active_seq_len}"
            else:
                action = "no further automatic reduction available"

            print(
                f"[OOM] step={step} count={oom_count} action={action}",
                flush=True,
            )
            if oom_count >= args.max_ooms:
                raise SystemExit(f"Stopping after {oom_count} CUDA OOM events.")
            if args.oom_cooldown > 0:
                time.sleep(args.oom_cooldown)
            continue

        if step == 1 or step % args.log_every == 0:
            elapsed = time.time() - started
            print(
                f"[STEP] {step}/{args.steps} loss={loss_val:.4f} "
                f"domain={batch_domain} batch={active_batch} "
                f"seq_len={active_seq_len} elapsed_sec={elapsed:.1f}",
                flush=True,
            )

        if step % args.save_every == 0:
            save_checkpoint(engine, args.out, step, loss_val, args.data, args.domain_strategy)

        del ids, targets_tensor, embedded, output, logits, loss
        if torch.cuda.is_available() and step % args.empty_cache_every == 0:
            clear_cuda_pressure()

    save_checkpoint(engine, args.out, args.steps, loss_val, args.data, args.domain_strategy)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=DEFAULT_DATA)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--base-checkpoint", default="")
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--batch", type=int, default=2)
    parser.add_argument("--seq-len", type=int, default=96)
    parser.add_argument("--min-seq-len", type=int, default=48)
    parser.add_argument("--oom-seq-step", type=int, default=16)
    parser.add_argument("--oom-cooldown", type=float, default=3.0)
    parser.add_argument("--max-ooms", type=int, default=6)
    parser.add_argument("--lr", type=float, default=5e-5)
    parser.add_argument("--seed", type=int, default=14)
    parser.add_argument("--log-every", type=int, default=25)
    parser.add_argument("--save-every", type=int, default=100)
    parser.add_argument("--empty-cache-every", type=int, default=25)
    parser.add_argument(
        "--domain-strategy",
        choices=["conversation", "auto", "all"],
        default="conversation",
        help="Train one speech domain, detected runtime domains, or every domain head.",
    )
    parser.add_argument("--response-only-loss", action="store_true")
    parser.add_argument("--confirm-gpu-training", action="store_true")
    args = parser.parse_args()
    train(args)


if __name__ == "__main__":
    main()
