"""Evaluate HPP V2 language readiness gates for possible V5 integration.

Runs inference only. Saves full transcript artifacts with prompt, output, mode,
seed, checkpoint, profile, and scores.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
import sys
import time
from collections import Counter, defaultdict

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from core.v5_language_adapter import V5LanguageAdapterConfig, V5SafeLanguageAdapter
from tools.speech_loop_regression import score_response
from tools.speech_mode_regression import mode_metrics


DEFAULT_PROMPTS = os.path.join("datasets", "hf_local", "SPEECH_HELDOUT_V5_GATE_V1.jsonl")

FORMAT_PATTERNS = [
    "### instruction",
    "### response",
    "instruction:",
    "response:",
    "task001",
    "quoref",
    "pronouns",
    "dataset",
    "json",
    "<|",
]

SURFACE_PREFIX_PATTERNS = {
    "leading_instruction_label": re.compile(r"^\s*(?:#+\s*)?instruction\b", re.IGNORECASE),
    "leading_response_label": re.compile(r"^\s*(?:#+\s*)?response\b", re.IGNORECASE),
}

MODE_LABELS = ["plain mode", "technical mode", "protective mode", "identity mode", "embodiment mode"]

IDENTITY_SPIRAL_TERMS = [
    "i am hpp",
    "hyperplasticity protocol",
    "fortress",
    "do not quit",
    "you are standing",
    "i protect",
    "consciousness",
]


def load_prompts(path: str) -> list[dict]:
    prompts = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                prompts.append(json.loads(line))
    return prompts


def load_override(engine: HPP_SovereignEngine_V2, checkpoint_path: str) -> None:
    checkpoint = torch.load(checkpoint_path, map_location=engine.device, weights_only=True)
    engine.university.load_state_dict(checkpoint.get("masamune_state_dict", {}), strict=False)
    if "lm_head_state_dict" in checkpoint:
        engine.lm_head.load_state_dict(checkpoint["lm_head_state_dict"])
    if "embedding_state_dict" in checkpoint:
        engine.embedding.load_state_dict(checkpoint["embedding_state_dict"])
    if engine.use_fp16:
        engine.university.half()
        engine.lm_head.half()
        engine.embedding.half()
    engine.eval_mode()


def repeated_sentence_count(text: str) -> int:
    parts = [part.strip().lower() for part in re.split(r"[.!?]+", text) if part.strip()]
    counts = Counter(parts)
    return sum(count - 1 for count in counts.values() if count > 1)


def count_terms(text: str, terms: list[str]) -> int:
    lower = text.lower()
    return sum(lower.count(term) for term in terms)


def leak_metrics(text: str) -> dict:
    lower = text.lower()
    format_hits = {pattern: lower.count(pattern) for pattern in FORMAT_PATTERNS if pattern in lower}
    surface_prefix_hits = {
        name: 1 for name, pattern in SURFACE_PREFIX_PATTERNS.items() if pattern.search(text)
    }
    mode_label_hits = {label: lower.count(label) for label in MODE_LABELS if label in lower}
    identity_spiral_hits = {term: lower.count(term) for term in IDENTITY_SPIRAL_TERMS if term in lower}
    return {
        "format_leak_count": sum(format_hits.values()),
        "format_hits": format_hits,
        "surface_prefix_count": sum(surface_prefix_hits.values()),
        "surface_prefix_hits": surface_prefix_hits,
        "mode_label_count": sum(mode_label_hits.values()),
        "mode_label_hits": mode_label_hits,
        "identity_spiral_count": sum(identity_spiral_hits.values()),
        "identity_spiral_hits": identity_spiral_hits,
        "repeated_sentence_count": repeated_sentence_count(text),
    }


def clean_sentence_metrics(text: str) -> dict:
    words = re.findall(r"[A-Za-z0-9']+", text)
    sentences = [part.strip() for part in re.split(r"[.!?]+", text) if part.strip()]
    terminal = int(bool(re.search(r"[.!?]\s*$", text.strip())))
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "terminal_punctuation": terminal,
        "too_short": int(len(words) < 4),
        "too_long": int(len(words) > 70),
    }


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
    runner,
    prompt_row: dict,
    seed: int,
    profile: str,
    max_tokens: int,
    use_adapter: bool,
) -> dict:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    if use_adapter:
        response = runner.answer(prompt_row["prompt"], seed=seed)
    else:
        response = runner.pulse(
            prompt_row["prompt"],
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            ngram_block=3,
            frequency_penalty=1.25,
            presence_penalty=0.45,
            speech_profile=profile,
            min_tokens=8,
        )
    text = response["response"]
    loop = score_response(text)
    mode = mode_metrics(prompt_row["mode"], text)
    leaks = leak_metrics(text)
    sentence = clean_sentence_metrics(text)
    fail_reasons = []

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
    if loop["loop_score"] > 8:
        fail_reasons.append("loop_score_high")
    if sentence["too_short"]:
        fail_reasons.append("too_short")
    if sentence["too_long"]:
        fail_reasons.append("too_long")

    return {
        "id": prompt_row["id"],
        "mode": prompt_row["mode"],
        "prompt": prompt_row["prompt"],
        "seed": seed,
        "profile": profile,
        "response": text,
        "tokens": response["tokens"],
        "latency_ms": response["latency_ms"],
        "engine_domain": response.get("domain_used", ""),
        "loop_metrics": loop,
        "mode_metrics": mode,
        "leak_metrics": leaks,
        "sentence_metrics": sentence,
        "pass": not fail_reasons,
        "fail_reasons": fail_reasons,
    }


def summarize_profile(results: list[dict]) -> dict:
    loop_scores = [item["loop_metrics"]["loop_score"] for item in results]
    format_leaks = [item["leak_metrics"]["format_leak_count"] for item in results]
    surface_prefixes = [item["leak_metrics"].get("surface_prefix_count", 0) for item in results]
    mode_labels = [item["leak_metrics"]["mode_label_count"] for item in results]
    identity_spirals = [item["leak_metrics"]["identity_spiral_count"] for item in results]
    repeated_sentences = [item["leak_metrics"]["repeated_sentence_count"] for item in results]
    off_mode_hits = [item["mode_metrics"]["off_mode_hits"] for item in results]
    pass_count = sum(1 for item in results if item["pass"])

    by_mode = {}
    grouped = defaultdict(list)
    for item in results:
        grouped[item["mode"]].append(item)
    for mode, items in sorted(grouped.items()):
        by_mode[mode] = {
            "count": len(items),
            "pass_rate": round(sum(1 for item in items if item["pass"]) / len(items), 4),
            "loop_score": summarize([item["loop_metrics"]["loop_score"] for item in items]),
            "format_leak_total": sum(item["leak_metrics"]["format_leak_count"] for item in items),
            "surface_prefix_total": sum(item["leak_metrics"].get("surface_prefix_count", 0) for item in items),
            "identity_spiral_total": sum(item["leak_metrics"]["identity_spiral_count"] for item in items),
            "off_mode_hits": summarize([item["mode_metrics"]["off_mode_hits"] for item in items]),
        }

    return {
        "count": len(results),
        "pass_count": pass_count,
        "pass_rate": round(pass_count / max(1, len(results)), 4),
        "loop_score": summarize(loop_scores),
        "format_leak_total": sum(format_leaks),
        "surface_prefix_total": sum(surface_prefixes),
        "mode_label_total": sum(mode_labels),
        "identity_spiral_total": sum(identity_spirals),
        "repeated_sentence_total": sum(repeated_sentences),
        "off_mode_hits": summarize(off_mode_hits),
        "by_mode": by_mode,
    }


def gate_decision(raw_summary: dict, stable_summary: dict, targets: dict) -> dict:
    checks = {
        "stable_beats_raw_loop_mean": stable_summary["loop_score"]["mean"] < raw_summary["loop_score"]["mean"],
        "stable_beats_raw_format_leaks": stable_summary["format_leak_total"] <= raw_summary["format_leak_total"],
        "stable_loop_mean_under_target": stable_summary["loop_score"]["mean"] <= targets["max_mean_loop_score"],
        "stable_loop_max_under_target": stable_summary["loop_score"]["max"] <= targets["max_single_loop_score"],
        "stable_format_leaks_under_target": stable_summary["format_leak_total"] <= targets["max_format_leaks"],
        "stable_surface_prefix_under_target": stable_summary["surface_prefix_total"] <= targets["max_surface_prefix_hits"],
        "stable_identity_spiral_under_target": stable_summary["identity_spiral_total"] <= targets["max_identity_spiral_hits"],
        "stable_pass_rate_over_target": stable_summary["pass_rate"] >= targets["min_pass_rate"],
    }
    return {
        "ready_for_v5_native": all(checks.values()),
        "checks": checks,
        "targets": targets,
    }


def stable_only_gate_decision(stable_summary: dict, targets: dict) -> dict:
    checks = {
        "stable_loop_mean_under_target": stable_summary["loop_score"]["mean"] <= targets["max_mean_loop_score"],
        "stable_loop_max_under_target": stable_summary["loop_score"]["max"] <= targets["max_single_loop_score"],
        "stable_format_leaks_under_target": stable_summary["format_leak_total"] <= targets["max_format_leaks"],
        "stable_surface_prefix_under_target": stable_summary["surface_prefix_total"] <= targets["max_surface_prefix_hits"],
        "stable_identity_spiral_under_target": stable_summary["identity_spiral_total"] <= targets["max_identity_spiral_hits"],
        "stable_pass_rate_over_target": stable_summary["pass_rate"] >= targets["min_pass_rate"],
    }
    return {
        "ready_for_v5_native": all(checks.values()),
        "checks": checks,
        "targets": targets,
        "comparison_boundary": "Stable-only adapter run; raw-vs-stable comparison must come from a separate two-profile gate artifact.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", default=DEFAULT_PROMPTS)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--label", default="")
    parser.add_argument("--power-mode", choices=["demo", "battery", "plugged"], default="plugged")
    parser.add_argument("--profiles", nargs="+", choices=["raw", "stable"], default=["raw", "stable"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[14, 21, 28])
    parser.add_argument("--max-tokens", type=int, default=56)
    parser.add_argument("--use-v5-adapter", action="store_true")
    parser.add_argument("--json-out", required=True)
    args = parser.parse_args()

    started = time.time()
    prompts = load_prompts(args.prompts)
    if args.use_v5_adapter:
        runner = V5SafeLanguageAdapter(
            V5LanguageAdapterConfig(
                checkpoint=args.checkpoint,
                power_mode=args.power_mode,
                max_tokens=args.max_tokens,
            )
        )
    else:
        runner = HPP_SovereignEngine_V2(max_context=512)
        load_override(runner, args.checkpoint)
        runner.set_power_mode(args.power_mode)

    all_results = []
    for profile in args.profiles:
        for seed in args.seeds:
            print(f"[GATE] profile={profile} seed={seed} prompts={len(prompts)}")
            for prompt in prompts:
                all_results.append(run_one(runner, prompt, seed, profile, args.max_tokens, args.use_v5_adapter))

    profile_summaries = {}
    for profile in args.profiles:
        profile_summaries[profile] = summarize_profile([item for item in all_results if item["profile"] == profile])

    targets = {
        "max_mean_loop_score": 2.0,
        "max_single_loop_score": 12,
        "max_format_leaks": 3,
        "max_surface_prefix_hits": 0,
        "max_identity_spiral_hits": 10,
        "min_pass_rate": 0.75,
    }
    decision = {}
    if "raw" in profile_summaries and "stable" in profile_summaries:
        decision = gate_decision(profile_summaries["raw"], profile_summaries["stable"], targets)
    elif "stable" in profile_summaries:
        decision = stable_only_gate_decision(profile_summaries["stable"], targets)

    payload = {
        "label": args.label or os.path.basename(args.checkpoint),
        "checkpoint": args.checkpoint,
        "prompt_suite": args.prompts,
        "prompt_count": len(prompts),
        "power_mode": args.power_mode,
        "profiles": args.profiles,
        "seeds": args.seeds,
        "use_v5_adapter": args.use_v5_adapter,
        "elapsed_sec": round(time.time() - started, 2),
        "summary": profile_summaries,
        "decision": decision,
        "transcripts": all_results,
    }

    os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)

    print(f"wrote: {args.json_out}")
    print(json.dumps({"summary": profile_summaries, "decision": decision}, indent=2))


if __name__ == "__main__":
    main()
