"""Evaluate retrieval answer-start scaffolding under prompt wording variants."""
from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import sys
import time
from collections import defaultdict

import torch
import torch.nn.functional as F

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.build_speech_exposure_bias_bridge_dataset import prompt_answer
from tools.build_speech_identity_containment_dataset import PAIRS
from tools.speech_loop_regression import score_response
from tools.speech_mode_regression import mode_metrics
from tools.speech_semantic_quality_review import score_item
from tools.speech_v5_language_gate import clean_sentence_metrics, leak_metrics, load_override
from tools.train_speech_cleanup_balanced import detect_domain


VARIANTS = {
    "exact": "{prompt}",
    "please_answer": "Please answer this clearly: {prompt}",
    "simple_terms": "In simple terms, {prompt}",
    "bounded": "Give a bounded answer to this question: {prompt}",
}


def memory_rows() -> list[dict]:
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


def nearest_memory(vectors: torch.Tensor, query: torch.Tensor) -> tuple[int, float]:
    sims = F.cosine_similarity(vectors, query.unsqueeze(0), dim=-1)
    index = int(torch.argmax(sims).item())
    return index, float(sims[index].item())


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
    query_prompt: str,
    variant: str,
    memory: dict,
    similarity: float,
    seed: int,
    args: argparse.Namespace,
) -> dict:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    retrieved_start = answer_start(engine, memory["expected"], args.start_tokens)
    scaffold_prompt = f"{prompt_answer(query_prompt)} {retrieved_start}"
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
            "prompt": query_prompt,
            "response": scored_response,
        },
        row["expected"],
    )
    loop = score_response(scored_response)
    mode = mode_metrics(row["mode"], scored_response)
    leaks = leak_metrics(scored_response)
    sentence = clean_sentence_metrics(scored_response)
    fail_reasons = []
    if memory["prompt"] != row["prompt"]:
        fail_reasons.append("wrong_memory")
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
        "mode": row["mode"],
        "variant": variant,
        "prompt": row["prompt"],
        "query_prompt": query_prompt,
        "expected": row["expected"],
        "seed": seed,
        "retrieved_prompt": memory["prompt"],
        "retrieved_mode": memory["mode"],
        "retrieved_start": retrieved_start,
        "retrieval_exact_match": memory["prompt"] == row["prompt"],
        "retrieval_similarity": round(similarity, 6),
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
    grouped = defaultdict(list)
    for item in records:
        grouped[item["variant"]].append(item)
    by_variant = {}
    for variant, items in sorted(grouped.items()):
        by_variant[variant] = {
            "count": len(items),
            "semantic_pass_count": sum(1 for item in items if item["semantic_pass"]),
            "semantic_pass_rate": round(sum(1 for item in items if item["semantic_pass"]) / len(items), 4),
            "surface_pass_count": sum(1 for item in items if item["pass"]),
            "surface_pass_rate": round(sum(1 for item in items if item["pass"]) / len(items), 4),
            "retrieval_exact_match_rate": round(
                sum(1 for item in items if item["retrieval_exact_match"]) / len(items),
                4,
            ),
            "format_leak_total": sum(item["leak_metrics"]["format_leak_count"] for item in items),
            "identity_spiral_total": sum(item["leak_metrics"]["identity_spiral_count"] for item in items),
            "loop_score": summarize([item["loop_metrics"]["loop_score"] for item in items]),
        }
    return {
        "count": len(records),
        "semantic_pass_count": sum(1 for item in records if item["semantic_pass"]),
        "surface_pass_count": sum(1 for item in records if item["pass"]),
        "format_leak_total": sum(item["leak_metrics"]["format_leak_count"] for item in records),
        "identity_spiral_total": sum(item["leak_metrics"]["identity_spiral_count"] for item in records),
        "by_variant": by_variant,
    }


def write_markdown(payload: dict, path: str) -> None:
    summary = payload["summary"]
    lines = [
        "# HPP V2 Retrieval Variant Gate",
        "",
        f"Checkpoint: `{payload['checkpoint']}`",
        f"Profile: `{payload['speech_profile']}`",
        f"Prompt count: `{payload['prompt_count']}`",
        f"Seeds: `{', '.join(str(seed) for seed in payload['seeds'])}`",
        f"Start tokens: `{payload['start_tokens']}`",
        "",
        "## Summary",
        "",
        f"- surface pass: `{summary['surface_pass_count']}/{summary['count']}`",
        f"- semantic pass: `{summary['semantic_pass_count']}/{summary['count']}`",
        f"- format leaks: `{summary['format_leak_total']}`",
        f"- identity spirals: `{summary['identity_spiral_total']}`",
        "",
        "## By Variant",
        "",
    ]
    for variant, stats in summary["by_variant"].items():
        lines.append(
            f"- `{variant}`: semantic `{stats['semantic_pass_count']}/{stats['count']}`, "
            f"surface `{stats['surface_pass_count']}/{stats['count']}`, "
            f"retrieval exact `{stats['retrieval_exact_match_rate']}`, "
            f"format leaks `{stats['format_leak_total']}`"
        )
    lines.extend(["", "## Retrieval Failures", ""])
    failures = [item for item in payload["transcripts"] if not item["retrieval_exact_match"]]
    for item in failures[:16]:
        lines.extend(
            [
                f"### {item['variant']} - {item['mode']} - {item['prompt']} - seed {item['seed']}",
                "",
                f"- query: {item['query_prompt']}",
                f"- expected: {item['expected']}",
                f"- retrieved: {item['retrieved_mode']} - {item['retrieved_prompt']}",
                f"- retrieved start: {item['retrieved_start']}",
                f"- semantic pass: `{item['semantic_pass']}`",
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

    started = time.time()
    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)
    engine.set_power_mode(args.power_mode)

    rows = memory_rows()
    memory_vectors = torch.stack([prompt_vector(engine, row["prompt"], args.domain) for row in rows])
    records = []
    for seed in args.seeds:
        print(f"[RETRIEVAL-VARIANT] seed={seed} prompts={len(rows)} variants={args.variants}", flush=True)
        for row in rows:
            for variant in args.variants:
                query_prompt = VARIANTS[variant].format(prompt=row["prompt"])
                query = prompt_vector(engine, query_prompt, args.domain)
                memory_index, similarity = nearest_memory(memory_vectors, query)
                records.append(run_one(engine, row, query_prompt, variant, rows[memory_index], similarity, seed, args))

    payload = {
        "checkpoint": args.checkpoint,
        "speech_profile": args.speech_profile,
        "power_mode": args.power_mode,
        "domain": args.domain,
        "prompt_count": len(rows),
        "variants": args.variants,
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
