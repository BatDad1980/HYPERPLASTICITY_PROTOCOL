"""Evaluate normalized prompt-key retrieval before speech generation."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.speech_retrieval_variant_gate import (
    VARIANTS,
    answer_start,
    memory_rows,
    prompt_vector,
    nearest_memory,
    run_one,
    summarize_records,
    write_markdown,
)
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.speech_v5_language_gate import load_override


def normalize_prompt(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"^(please\s+answer\s+this\s+clearly\s*:\s*)", "", text)
    text = re.sub(r"^(in\s+simple\s+terms\s*,\s*)", "", text)
    text = re.sub(r"^(give\s+a\s+bounded\s+answer\s+to\s+this\s+question\s*:\s*)", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    text = re.sub(r"[?.!]+$", "", text)
    return text


def normalized_index(rows: list[dict]) -> dict[str, dict]:
    return {normalize_prompt(row["prompt"]): row for row in rows}


def summarize_with_strategy(records: list[dict]) -> dict:
    summary = summarize_records(records)
    grouped = defaultdict(list)
    for item in records:
        grouped[item["retrieval_strategy"]].append(item)
    summary["by_retrieval_strategy"] = {}
    for strategy, items in sorted(grouped.items()):
        summary["by_retrieval_strategy"][strategy] = {
            "count": len(items),
            "semantic_pass_count": sum(1 for item in items if item["semantic_pass"]),
            "semantic_pass_rate": round(sum(1 for item in items if item["semantic_pass"]) / len(items), 4),
            "retrieval_exact_match_rate": round(sum(1 for item in items if item["retrieval_exact_match"]) / len(items), 4),
            "format_leak_total": sum(item["leak_metrics"]["format_leak_count"] for item in items),
        }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--power-mode", default="plugged", choices=["demo", "battery", "plugged"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[14])
    parser.add_argument("--variants", nargs="+", choices=sorted(VARIANTS), default=list(VARIANTS))
    parser.add_argument("--start-tokens", type=int, default=5)
    parser.add_argument("--max-tokens", type=int, default=48)
    parser.add_argument("--temperature", type=float, default=0.25)
    parser.add_argument("--top-p", type=float, default=0.55)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--frequency-penalty", type=float, default=1.05)
    parser.add_argument("--presence-penalty", type=float, default=0.15)
    parser.add_argument("--speech-profile", choices=["raw", "stable", "semantic_short"], default="semantic_short")
    parser.add_argument("--domain", default="auto", choices=["auto", "conversation", "logic", "identity", "synthesis", "none"])
    parser.add_argument("--max-loop-score", type=int, default=8)
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--md-out", required=True)
    args = parser.parse_args()

    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)
    engine.set_power_mode(args.power_mode)

    rows = memory_rows()
    index = normalized_index(rows)
    memory_vectors = torch.stack([prompt_vector(engine, row["prompt"], args.domain) for row in rows])
    records = []
    for seed in args.seeds:
        print(f"[NORMALIZED-RETRIEVAL] seed={seed} prompts={len(rows)} variants={args.variants}", flush=True)
        for row in rows:
            for variant in args.variants:
                query_prompt = VARIANTS[variant].format(prompt=row["prompt"])
                key = normalize_prompt(query_prompt)
                memory = index.get(key)
                retrieval_strategy = "normalized_key"
                similarity = 1.0
                if memory is None:
                    query = prompt_vector(engine, query_prompt, args.domain)
                    memory_index, similarity = nearest_memory(memory_vectors, query)
                    memory = rows[memory_index]
                    retrieval_strategy = "vector_fallback"
                record = run_one(engine, row, query_prompt, variant, memory, similarity, seed, args)
                record["retrieval_strategy"] = retrieval_strategy
                record["normalized_key"] = key
                records.append(record)

    payload = {
        "checkpoint": args.checkpoint,
        "speech_profile": args.speech_profile,
        "power_mode": args.power_mode,
        "domain": args.domain,
        "prompt_count": len(rows),
        "variants": args.variants,
        "seeds": args.seeds,
        "start_tokens": args.start_tokens,
        "summary": summarize_with_strategy(records),
        "transcripts": records,
    }
    os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
    write_markdown(payload, args.md_out)
    print(f"wrote: {args.json_out}")
    print(f"wrote: {args.md_out}")
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
