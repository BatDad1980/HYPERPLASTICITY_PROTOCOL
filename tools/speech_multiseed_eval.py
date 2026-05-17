"""Multi-seed speech stability evaluation for HPP V2.

Runs inference only. This compares raw plugged speech against the stable speech
profile across fixed seeds, then writes a compact JSON report.
"""
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

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.speech_loop_regression import PROMPTS as LOOP_PROMPTS
from tools.speech_loop_regression import score_response
from tools.speech_mode_regression import PROMPTS_BY_MODE, mode_metrics


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


def run_profile(
    engine: HPP_SovereignEngine_V2,
    seed: int,
    power_mode: str,
    profile: str,
    max_tokens: int,
) -> dict:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    engine.set_power_mode(power_mode)

    loop_results = []
    for prompt in LOOP_PROMPTS:
        response = engine.pulse(
            prompt,
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
        loop_results.append(
            {
                "prompt": prompt,
                "response": response["response"],
                "metrics": score_response(response["response"]),
                "latency_ms": response["latency_ms"],
            }
        )

    mode_results = []
    for mode, prompts in PROMPTS_BY_MODE.items():
        for prompt in prompts:
            response = engine.pulse(
                prompt,
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
            mode_results.append(
                {
                    "mode": mode,
                    "prompt": prompt,
                    "response": text,
                    "loop_metrics": score_response(text),
                    "mode_metrics": mode_metrics(mode, text),
                    "latency_ms": response["latency_ms"],
                }
            )

    loop_scores = [item["metrics"]["loop_score"] for item in loop_results]
    mode_loop_scores = [item["loop_metrics"]["loop_score"] for item in mode_results]
    off_mode_hits = [item["mode_metrics"]["off_mode_hits"] for item in mode_results]
    format_leaks = sum(item["mode_metrics"]["format_leak"] for item in mode_results)

    mode_summary = {}
    by_mode = defaultdict(list)
    for item in mode_results:
        by_mode[item["mode"]].append(item)
    for mode, items in sorted(by_mode.items()):
        mode_summary[mode] = {
            "loop_score": summarize([i["loop_metrics"]["loop_score"] for i in items]),
            "off_mode_hits": summarize([i["mode_metrics"]["off_mode_hits"] for i in items]),
            "format_leak_count": sum(i["mode_metrics"]["format_leak"] for i in items),
        }

    return {
        "seed": seed,
        "profile": profile,
        "power_mode": power_mode,
        "loop_regression": {
            "mean_loop_score": round(sum(loop_scores) / len(loop_scores), 4),
            "max_loop_score": max(loop_scores),
            "results": loop_results,
        },
        "mode_regression": {
            "mean_loop_score": round(sum(mode_loop_scores) / len(mode_loop_scores), 4),
            "max_loop_score": max(mode_loop_scores),
            "mean_off_mode_hits": round(sum(off_mode_hits) / len(off_mode_hits), 4),
            "format_leak_count": format_leaks,
            "mode_summary": mode_summary,
            "results": mode_results,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--label", default="")
    parser.add_argument("--power-mode", choices=["demo", "battery", "plugged"], default="plugged")
    parser.add_argument("--profiles", nargs="+", choices=["raw", "stable"], default=["raw", "stable"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[14, 21, 28])
    parser.add_argument("--max-tokens", type=int, default=48)
    parser.add_argument("--json-out", required=True)
    args = parser.parse_args()

    started = time.time()
    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)

    runs = []
    for profile in args.profiles:
        for seed in args.seeds:
            print(f"[EVAL] profile={profile} seed={seed}")
            runs.append(run_profile(engine, seed, args.power_mode, profile, args.max_tokens))

    summary = {}
    for profile in args.profiles:
        profile_runs = [run for run in runs if run["profile"] == profile]
        summary[profile] = {
            "loop_regression_mean": summarize([run["loop_regression"]["mean_loop_score"] for run in profile_runs]),
            "loop_regression_max": summarize([run["loop_regression"]["max_loop_score"] for run in profile_runs]),
            "mode_regression_mean": summarize([run["mode_regression"]["mean_loop_score"] for run in profile_runs]),
            "mode_regression_max": summarize([run["mode_regression"]["max_loop_score"] for run in profile_runs]),
            "mode_off_mode_mean": summarize([run["mode_regression"]["mean_off_mode_hits"] for run in profile_runs]),
            "format_leak_total": sum(run["mode_regression"]["format_leak_count"] for run in profile_runs),
        }

    payload = {
        "checkpoint": args.checkpoint,
        "label": args.label or os.path.basename(args.checkpoint),
        "power_mode": args.power_mode,
        "profiles": args.profiles,
        "seeds": args.seeds,
        "elapsed_sec": round(time.time() - started, 2),
        "summary": summary,
        "runs": runs,
    }

    os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
    print(f"wrote: {args.json_out}")
    print(json.dumps({"summary": summary}, indent=2))


if __name__ == "__main__":
    main()
