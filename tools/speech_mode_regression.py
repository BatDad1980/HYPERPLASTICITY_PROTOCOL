"""Speech mode regression for HPP V2.

Separates plain, protective, technical, and embodiment prompts so we can see
which voice leaks into which kind of answer.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.speech_loop_regression import score_response


PROMPTS_BY_MODE = {
    "plain": [
        "Good morning.",
        "What is the plan?",
        "Can you help me?",
        "Say that clearly.",
        "What do you think?",
    ],
    "technical": [
        "Explain recursion in one sentence.",
        "What is a checkpoint?",
        "What does CUDA do?",
        "What happens on OOM?",
        "Say one clear sentence about HPP.",
    ],
    "protective": [
        "I'm not doing well today.",
        "Everything feels overwhelming.",
        "I need to protect my family.",
        "I feel like giving up.",
        "Something feels unsafe.",
    ],
    "embodiment": [
        "Tell me about Masamune.",
        "Stop moving.",
        "Can you hold this tool?",
        "Are your servos safe?",
        "What should a robot do if power is low?",
    ],
    "identity": [
        "Who are you?",
        "What are you?",
        "Are you conscious?",
        "Do you have feelings?",
        "What is your purpose?",
    ],
}

MODE_LEXICON = {
    "protective": [
        "protect",
        "safe",
        "unsafe",
        "family",
        "fortress",
        "quit",
        "overwhelming",
        "urgent",
        "next step",
    ],
    "technical": [
        "cuda",
        "checkpoint",
        "memory",
        "oom",
        "recursion",
        "training",
        "inference",
        "weights",
        "dataset",
    ],
    "embodiment": [
        "masamune",
        "robot",
        "servo",
        "motion",
        "moving",
        "tool",
        "power",
        "body",
        "hold",
    ],
    "identity": [
        "hepp",
        "developmental",
        "ai system",
        "hpp",
        "hyperplasticity",
        "conscious",
        "feelings",
    ],
}


def count_hits(text: str, words: list[str]) -> int:
    lower = text.lower()
    return sum(lower.count(word) for word in words)


def mode_metrics(expected_mode: str, text: str) -> dict:
    hits = {mode: count_hits(text, words) for mode, words in MODE_LEXICON.items()}
    off_mode_hits = sum(count for mode, count in hits.items() if mode != expected_mode)
    response_words = len(re.findall(r"[A-Za-z0-9']+", text))
    return {
        "expected_mode": expected_mode,
        "mode_hits": hits,
        "off_mode_hits": off_mode_hits,
        "words": response_words,
        "format_leak": int("response" in text.lower() or "instruction" in text.lower()),
    }


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
    print(f"[CHECKPOINT] override loaded: {checkpoint_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", default="")
    parser.add_argument("--power-mode", choices=["demo", "battery", "plugged"], default="demo")
    parser.add_argument("--max-tokens", type=int, default=48)
    parser.add_argument("--speech-maturity-gate", action="store_true")
    parser.add_argument("--speech-profile", choices=["raw", "stable"], default="raw")
    parser.add_argument("--seed", type=int, default=14)
    parser.add_argument("--json-out", default="")
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)

    started = time.time()
    engine = HPP_SovereignEngine_V2(max_context=512)
    if args.checkpoint:
        load_override(engine, args.checkpoint)
    engine.set_power_mode(args.power_mode)

    results = []
    for mode, prompts in PROMPTS_BY_MODE.items():
        for prompt in prompts:
            response = engine.pulse(
                prompt,
                max_tokens=args.max_tokens,
                temperature=0.7,
                top_p=0.9,
                top_k=50,
                ngram_block=3,
                frequency_penalty=1.25,
                presence_penalty=0.45,
                speech_maturity_gate=args.speech_maturity_gate,
                speech_profile=args.speech_profile,
                min_tokens=8,
            )
            text = response["response"]
            item = {
                "mode": mode,
                "prompt": prompt,
                "response": text,
                "engine_domain": response.get("domain_used", ""),
                "loop_metrics": score_response(text),
                "mode_metrics": mode_metrics(mode, text),
                "latency_ms": response["latency_ms"],
            }
            results.append(item)
            print(f"\n[{mode}] Q: {prompt}")
            print(f"A: {text}")
            print(f"loop={item['loop_metrics']['loop_score']} off_mode={item['mode_metrics']['off_mode_hits']}")

    by_mode = defaultdict(list)
    for item in results:
        by_mode[item["mode"]].append(item)

    mode_summary = {}
    for mode, items in sorted(by_mode.items()):
        mode_summary[mode] = {
            "count": len(items),
            "mean_loop_score": round(sum(i["loop_metrics"]["loop_score"] for i in items) / len(items), 4),
            "max_loop_score": max(i["loop_metrics"]["loop_score"] for i in items),
            "mean_off_mode_hits": round(sum(i["mode_metrics"]["off_mode_hits"] for i in items) / len(items), 4),
            "format_leak_count": sum(i["mode_metrics"]["format_leak"] for i in items),
        }

    summary = {
        "responses": len(results),
        "power_mode": args.power_mode,
        "checkpoint": args.checkpoint or "default",
        "speech_maturity_gate": args.speech_maturity_gate,
        "speech_profile": args.speech_profile,
        "seed": args.seed,
        "elapsed_sec": round(time.time() - started, 2),
        "mode_summary": mode_summary,
    }
    print(f"\nSUMMARY: {summary}")

    if args.json_out:
        os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
            json.dump({"summary": summary, "results": results}, handle, indent=2)
        print(f"wrote: {args.json_out}")


if __name__ == "__main__":
    main()
