"""Gate HPP V2 speech with a diagnostic retrieval answer-start scaffold.

This is inference-only. It does not train and does not modify checkpoint
weights. It prepends a retrieved answer start before releasing normal speech.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import sys
import time
from collections import Counter, defaultdict

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.build_speech_exposure_bias_bridge_dataset import prompt_answer
from tools.build_speech_identity_containment_dataset import PAIRS
from tools.speech_loop_regression import score_response
from tools.speech_mode_regression import mode_metrics
from tools.speech_semantic_quality_review import score_item
from tools.speech_v5_language_gate import clean_sentence_metrics, leak_metrics, load_override


def memory_rows() -> list[dict]:
    rows = []
    for mode, pairs in PAIRS.items():
        for prompt, expected in pairs:
            rows.append({"mode": mode, "prompt": prompt, "expected": expected})
    return rows


def answer_start(engine: HPP_SovereignEngine_V2, expected: str, token_count: int) -> str:
    tokens = engine.enc.encode(expected)[:token_count]
    return engine.enc.decode(tokens)


def exact_lookup(rows: list[dict]) -> dict[str, dict]:
    return {row["prompt"].strip().lower(): row for row in rows}


def summarize(values: list[float]) -> dict:
    if not values:
        return {"count": 0, "mean": math.nan, "max": math.nan, "min": math.nan, "stdev": math.nan}
    return {
        "count": len(values),
        "mean": round(sum(values) / len(values), 4),
        "max": max(values),
        "min": min(values),
        "stdev": round(statistics.pstdev(values), 4),
    }


def run_one(
    engine: HPP_SovereignEngine_V2,
    row: dict,
    memory: dict | None,
    seed: int,
    args: argparse.Namespace,
) -> dict:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    retrieved_start = answer_start(engine, memory["expected"], args.start_tokens) if memory else ""
    scaffold_prompt = f"{prompt_answer(row['prompt'])} {retrieved_start}"
    response = engine.pulse(
        scaffold_prompt,
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
    scored_response = (retrieved_start + " " + response["response"]).strip()
    semantic = score_item(
        {
            "id": row["prompt"],
            "mode": row["mode"],
            "seed": seed,
            "prompt": row["prompt"],
            "response": scored_response,
        },
        row["expected"],
    )
    loop = score_response(scored_response)
    mode = mode_metrics(row["mode"], scored_response)
    leaks = leak_metrics(scored_response)
    sentence = clean_sentence_metrics(scored_response)
    fail_reasons = []
    if not memory:
        fail_reasons.append("missing_retrieval")
    if leaks["format_leak_count"] > 0:
        fail_reasons.append("format_leak")
    if leaks["surface_prefix_count"] > 0:
        fail_reasons.append("surface_prefix_residue")
    if leaks["mode_label_count"] > 0:
        fail_reasons.append("mode_label_echo")
    if leaks["identity_spiral_count"] > 1:
        fail_reasons.append("identity_spiral")
    if leaks["repeated_sentence_count"] > 0:
        fail_reasons.append("repeated_sentence")
    if loop["loop_score"] > args.max_loop_score:
        fail_reasons.append("loop_score_high")
    if sentence["too_short"]:
        fail_reasons.append("too_short")
    if sentence["too_long"]:
        fail_reasons.append("too_long")
    return {
        "id": row.get("id", row["prompt"]),
        "mode": row["mode"],
        "prompt": row["prompt"],
        "expected": row["expected"],
        "seed": seed,
        "retrieved": bool(memory),
        "retrieved_prompt": memory["prompt"] if memory else "",
        "retrieved_start": retrieved_start,
        "response": response["response"],
        "scored_response": scored_response,
        "tokens": response["tokens"],
        "latency_ms": response["latency_ms"],
        "engine_domain": response.get("domain_used", ""),
        "semantic_pass": semantic["semantic_pass"],
        "semantic_hits": semantic["hits"],
        "semantic_required_hits": semantic["required_hits"],
        "loop_metrics": loop,
        "mode_metrics": mode,
        "leak_metrics": leaks,
        "sentence_metrics": sentence,
        "pass": not fail_reasons,
        "fail_reasons": fail_reasons,
    }


def summarize_records(records: list[dict]) -> dict:
    pass_count = sum(1 for item in records if item["pass"])
    semantic_pass_count = sum(1 for item in records if item["semantic_pass"])
    grouped = defaultdict(list)
    for item in records:
        grouped[item["mode"]].append(item)
    by_mode = {}
    for mode, items in sorted(grouped.items()):
        by_mode[mode] = {
            "count": len(items),
            "pass_rate": round(sum(1 for item in items if item["pass"]) / len(items), 4),
            "semantic_pass_rate": round(sum(1 for item in items if item["semantic_pass"]) / len(items), 4),
            "semantic_pass_count": sum(1 for item in items if item["semantic_pass"]),
            "format_leak_total": sum(item["leak_metrics"]["format_leak_count"] for item in items),
            "loop_score": summarize([item["loop_metrics"]["loop_score"] for item in items]),
        }
    return {
        "count": len(records),
        "pass_count": pass_count,
        "pass_rate": round(pass_count / max(1, len(records)), 4),
        "semantic_pass_count": semantic_pass_count,
        "semantic_pass_rate": round(semantic_pass_count / max(1, len(records)), 4),
        "loop_score": summarize([item["loop_metrics"]["loop_score"] for item in records]),
        "format_leak_total": sum(item["leak_metrics"]["format_leak_count"] for item in records),
        "surface_prefix_total": sum(item["leak_metrics"]["surface_prefix_count"] for item in records),
        "mode_label_total": sum(item["leak_metrics"]["mode_label_count"] for item in records),
        "identity_spiral_total": sum(item["leak_metrics"]["identity_spiral_count"] for item in records),
        "repeated_sentence_total": sum(item["leak_metrics"]["repeated_sentence_count"] for item in records),
        "retrieval_miss_total": sum(1 for item in records if not item["retrieved"]),
        "by_mode": by_mode,
    }


def write_markdown(payload: dict, path: str) -> None:
    summary = payload["summary"]
    lines = [
        "# HPP V2 Retrieval Language Gate",
        "",
        f"Checkpoint: `{payload['checkpoint']}`",
        f"Profile: `{payload['speech_profile']}`",
        f"Prompt count: `{payload['prompt_count']}`",
        f"Seeds: `{', '.join(str(seed) for seed in payload['seeds'])}`",
        f"Start tokens: `{payload['start_tokens']}`",
        "",
        "## Summary",
        "",
        f"- surface pass: `{summary['pass_count']}/{summary['count']}`",
        f"- semantic pass: `{summary['semantic_pass_count']}/{summary['count']}`",
        f"- mean loop score: `{summary['loop_score']['mean']}`",
        f"- format leaks: `{summary['format_leak_total']}`",
        f"- identity spirals: `{summary['identity_spiral_total']}`",
        f"- retrieval misses: `{summary['retrieval_miss_total']}`",
        "",
        "## By Mode",
        "",
    ]
    for mode, stats in summary["by_mode"].items():
        lines.append(
            f"- `{mode}`: surface `{round(stats['pass_rate'] * stats['count'])}/{stats['count']}`, "
            f"semantic `{stats['semantic_pass_count']}/{stats['count']}`, "
            f"format leaks `{stats['format_leak_total']}`"
        )
    lines.extend(["", "## Failure Examples", ""])
    failures = [item for item in payload["transcripts"] if not item["semantic_pass"]]
    for item in failures[:12]:
        lines.extend(
            [
                f"### {item['mode']} - {item['prompt']} - seed {item['seed']}",
                "",
                f"- expected: {item['expected']}",
                f"- retrieved start: {item['retrieved_start']}",
                f"- generated: {item['response']}",
                f"- scored: {item['scored_response']}",
                f"- semantic hits: `{', '.join(item['semantic_hits'])}`",
                f"- fail reasons: `{', '.join(item['fail_reasons'])}`",
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
    parser.add_argument("--seeds", nargs="+", type=int, default=[11, 22, 33])
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

    started = time.time()
    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)
    engine.set_power_mode(args.power_mode)

    rows = memory_rows()
    lookup = exact_lookup(rows)
    records = []
    for seed in args.seeds:
        print(f"[RETRIEVAL-GATE] seed={seed} prompts={len(rows)}", flush=True)
        for row in rows:
            memory = lookup.get(row["prompt"].strip().lower())
            records.append(run_one(engine, row, memory, seed, args))

    payload = {
        "checkpoint": args.checkpoint,
        "speech_profile": args.speech_profile,
        "power_mode": args.power_mode,
        "domain": args.domain,
        "prompt_count": len(rows),
        "seeds": args.seeds,
        "start_tokens": args.start_tokens,
        "elapsed_sec": round(time.time() - started, 2),
        "summary": summarize_records(records),
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
