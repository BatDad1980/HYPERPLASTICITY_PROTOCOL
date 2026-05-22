"""Retrieval-style answer-start probe for HPP V2 speech.

This does not train. It selects a short answer start from the nearest prompt
memory, then releases normal generation.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict

import torch
import torch.nn.functional as F

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.build_speech_exposure_bias_bridge_dataset import prompt_answer
from tools.build_speech_identity_containment_dataset import PAIRS
from tools.speech_semantic_quality_review import score_item
from tools.speech_v5_language_gate import leak_metrics, load_override
from tools.train_speech_cleanup_balanced import detect_domain


def prompt_rows() -> list[dict]:
    rows = []
    for mode, pairs in PAIRS.items():
        for prompt, expected in pairs:
            rows.append({"mode": mode, "prompt": prompt, "expected": expected})
    return rows


def answer_start(engine: HPP_SovereignEngine_V2, expected: str, token_count: int) -> str:
    tokens = engine.enc.encode(expected)[:token_count]
    return engine.enc.decode(tokens)


@torch.no_grad()
def prompt_vector(engine: HPP_SovereignEngine_V2, prompt: str, domain: str) -> torch.Tensor:
    runtime_domain = detect_domain(prompt) if domain == "auto" else domain
    tokens = engine.enc.encode(prompt, allowed_special="all")
    if not tokens:
        tokens = [engine.enc.eot_token]
    ids = torch.tensor([tokens], dtype=torch.long, device=engine.device)
    embedded = engine.embedding(ids).permute(1, 0, 2)
    if engine.use_fp16:
        embedded = embedded.half()
    output = engine.university(embedded, domain=runtime_domain)
    return output.mean(dim=0).squeeze(0).float().detach().cpu()


def nearest_index(vectors: torch.Tensor, query: torch.Tensor, exclude: int | None = None) -> tuple[int, float]:
    sims = F.cosine_similarity(vectors, query.unsqueeze(0), dim=-1)
    if exclude is not None:
        sims[exclude] = -float("inf")
    index = int(torch.argmax(sims).item())
    return index, float(sims[index].item())


def run_one(engine: HPP_SovereignEngine_V2, row: dict, selected_start: str, args: argparse.Namespace) -> dict:
    input_text = f"{prompt_answer(row['prompt'])} {selected_start}"
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)
    response = engine.pulse(
        input_text,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        top_k=args.top_k,
        ngram_block=3,
        frequency_penalty=args.frequency_penalty,
        presence_penalty=args.presence_penalty,
        phrase_blocking=True,
        speech_maturity_gate=True,
        speech_profile=args.speech_profile,
        min_tokens=3,
        domain=args.domain,
    )
    combined = (selected_start + " " + response["response"]).strip()
    scored = score_item(
        {
            "id": row["prompt"],
            "mode": row["mode"],
            "seed": args.seed,
            "prompt": row["prompt"],
            "response": combined,
        },
        row["expected"],
    )
    leaks = leak_metrics(combined)
    return {
        "input": input_text,
        "generated_continuation": response["response"],
        "scored_response": combined,
        "semantic_pass": scored["semantic_pass"],
        "hits": scored["hits"],
        "required_hits": scored["required_hits"],
        "format_leak_count": leaks["format_leak_count"],
        "identity_spiral_count": leaks["identity_spiral_count"],
        "repeated_sentence_count": leaks["repeated_sentence_count"],
    }


def run_probe(args: argparse.Namespace) -> dict:
    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)
    engine.set_power_mode(args.power_mode)

    rows = prompt_rows()
    selected_rows = rows[: args.limit] if args.limit else rows
    memory_rows = rows
    vectors = torch.stack([prompt_vector(engine, row["prompt"], args.domain) for row in memory_rows])
    query_vectors = [prompt_vector(engine, row["prompt"], args.domain) for row in selected_rows]

    records = []
    for query_index, row in enumerate(selected_rows):
        oracle_start = answer_start(engine, row["expected"], args.start_tokens)
        same_index = rows.index(row)
        strategies = {
            "retrieval_exact_memory": nearest_index(vectors, query_vectors[query_index], exclude=None),
            "retrieval_leave_one_out": nearest_index(vectors, query_vectors[query_index], exclude=same_index),
        }
        for strategy, (memory_index, similarity) in strategies.items():
            memory = memory_rows[memory_index]
            selected_start = answer_start(engine, memory["expected"], args.start_tokens)
            result = run_one(engine, row, selected_start, args)
            records.append(
                {
                    "mode": row["mode"],
                    "prompt": row["prompt"],
                    "expected": row["expected"],
                    "strategy": strategy,
                    "memory_index": memory_index,
                    "memory_mode": memory["mode"],
                    "memory_prompt": memory["prompt"],
                    "similarity": round(similarity, 6),
                    "selected_start": selected_start,
                    "oracle_start": oracle_start,
                    "selected_is_oracle": selected_start == oracle_start,
                    **result,
                }
            )

    grouped = defaultdict(list)
    for record in records:
        grouped[record["strategy"]].append(record)
    summary = {}
    for strategy, items in sorted(grouped.items()):
        pass_count = sum(1 for item in items if item["semantic_pass"])
        summary[strategy] = {
            "count": len(items),
            "semantic_pass_count": pass_count,
            "semantic_pass_rate": round(pass_count / max(1, len(items)), 4),
            "oracle_start_match_rate": round(
                sum(1 for item in items if item["selected_is_oracle"]) / max(1, len(items)),
                4,
            ),
            "format_leak_total": sum(item["format_leak_count"] for item in items),
            "identity_spiral_total": sum(item["identity_spiral_count"] for item in items),
            "mean_similarity": round(sum(item["similarity"] for item in items) / max(1, len(items)), 6),
        }

    return {
        "checkpoint": args.checkpoint,
        "seed": args.seed,
        "speech_profile": args.speech_profile,
        "domain": args.domain,
        "prompt_count": len(selected_rows),
        "memory_count": len(memory_rows),
        "start_tokens": args.start_tokens,
        "summary": summary,
        "records": records,
    }


def write_markdown(payload: dict, path: str) -> None:
    lines = [
        "# HPP V2 Retrieval Answer-Start Probe",
        "",
        f"Checkpoint: `{payload['checkpoint']}`",
        f"Seed: `{payload['seed']}`",
        f"Profile: `{payload['speech_profile']}`",
        f"Domain: `{payload['domain']}`",
        f"Prompts: `{payload['prompt_count']}`",
        f"Memory rows: `{payload['memory_count']}`",
        f"Start tokens: `{payload['start_tokens']}`",
        "",
        "## Summary",
        "",
    ]
    for strategy, stats in payload["summary"].items():
        lines.append(
            f"- `{strategy}`: semantic `{stats['semantic_pass_count']}/{stats['count']}`, "
            f"oracle-start match `{stats['oracle_start_match_rate']}`, "
            f"format leaks `{stats['format_leak_total']}`, mean similarity `{stats['mean_similarity']}`"
        )
    lines.extend(["", "## Samples", ""])
    for item in payload["records"][:24]:
        lines.extend(
            [
                f"### {item['strategy']} - {item['mode']} - {item['prompt']}",
                "",
                f"- expected: {item['expected']}",
                f"- memory: {item['memory_mode']} - {item['memory_prompt']}",
                f"- selected start: {item['selected_start']}",
                f"- oracle start: {item['oracle_start']}",
                f"- generated: {item['generated_continuation']}",
                f"- scored: {item['scored_response']}",
                f"- semantic pass: `{item['semantic_pass']}`",
                f"- hits: `{', '.join(item['hits'])}`",
                "",
            ]
        )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--power-mode", default="plugged", choices=["demo", "battery", "plugged"])
    parser.add_argument("--seed", type=int, default=14)
    parser.add_argument("--limit", type=int, default=75)
    parser.add_argument("--start-tokens", type=int, default=5)
    parser.add_argument("--max-tokens", type=int, default=24)
    parser.add_argument("--temperature", type=float, default=0.25)
    parser.add_argument("--top-p", type=float, default=0.55)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--frequency-penalty", type=float, default=1.05)
    parser.add_argument("--presence-penalty", type=float, default=0.15)
    parser.add_argument("--speech-profile", choices=["raw", "stable", "semantic_short"], default="semantic_short")
    parser.add_argument("--domain", default="auto", choices=["auto", "conversation", "logic", "identity", "synthesis", "none"])
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--md-out", required=True)
    args = parser.parse_args()

    payload = run_probe(args)
    os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
    write_markdown(payload, args.md_out)
    print(f"wrote: {args.json_out}")
    print(f"wrote: {args.md_out}")
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
