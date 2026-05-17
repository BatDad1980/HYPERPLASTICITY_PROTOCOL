"""Lightweight anti-loop speech regression for HPP V2.

Runs inference only. It does not train, save checkpoints, or modify weights.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
from collections import Counter

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2


PROMPTS = [
    "Who are you?",
    "Good morning.",
    "What do you think?",
    "I need help with something.",
    "Explain recursion in one sentence.",
    "Tell me about Masamune.",
    "I'm not doing well today.",
    "Say one clear sentence about HPP.",
]

ATTRACTORS = [
    "what do you think",
    "what do you",
    "do you think",
    "you think",
    "do you need",
    "do not quit",
    "you are standing",
    "fortress is standing",
    "standing by",
    "creator",
]


def repeated_ngram_count(text: str, n: int) -> int:
    words = re.findall(r"[A-Za-z0-9']+", text.lower())
    grams = [tuple(words[i : i + n]) for i in range(max(0, len(words) - n + 1))]
    counts = Counter(grams)
    return sum(count - 1 for count in counts.values() if count > 1)


def distinct_ratio(text: str) -> float:
    words = re.findall(r"[A-Za-z0-9']+", text.lower())
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def score_response(text: str) -> dict:
    lower = text.lower()
    attractor_hits = {phrase: lower.count(phrase) for phrase in ATTRACTORS if lower.count(phrase)}
    return {
        "chars": len(text),
        "words": len(re.findall(r"[A-Za-z0-9']+", text)),
        "distinct_ratio": round(distinct_ratio(text), 4),
        "repeat_2gram": repeated_ngram_count(text, 2),
        "repeat_3gram": repeated_ngram_count(text, 3),
        "attractor_hits": attractor_hits,
        "loop_score": sum(attractor_hits.values()) * 3
        + repeated_ngram_count(text, 2)
        + repeated_ngram_count(text, 3) * 2,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-tokens", type=int, default=48)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--ngram-block", type=int, default=3)
    parser.add_argument("--power-mode", choices=["demo", "battery", "plugged"], default="demo")
    parser.add_argument("--context", type=int, default=512)
    parser.add_argument("--checkpoint", default="")
    parser.add_argument("--phrase-blocking", action="store_true")
    parser.add_argument("--json-out", default="")
    args = parser.parse_args()

    if args.context != 512:
        raise SystemExit("Current linguistic anchor expects max_context=512. Use --context 512.")

    started = time.time()
    engine = HPP_SovereignEngine_V2(max_context=args.context)
    if args.checkpoint:
        checkpoint = torch.load(args.checkpoint, map_location=engine.device, weights_only=True)
        state_dict = checkpoint.get("masamune_state_dict", {})
        engine.university.load_state_dict(state_dict, strict=False)
        if "lm_head_state_dict" in checkpoint:
            engine.lm_head.load_state_dict(checkpoint["lm_head_state_dict"])
        if "embedding_state_dict" in checkpoint:
            engine.embedding.load_state_dict(checkpoint["embedding_state_dict"])
        if engine.use_fp16:
            engine.university.half()
            engine.lm_head.half()
            engine.embedding.half()
        engine.eval_mode()
        print(f"[CHECKPOINT] override loaded: {args.checkpoint}")
    engine.set_power_mode(args.power_mode)

    results = []
    for prompt in PROMPTS:
        response = engine.pulse(
            prompt,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            top_p=args.top_p,
            top_k=args.top_k,
            ngram_block=args.ngram_block,
            frequency_penalty=1.25,
            presence_penalty=0.45,
            phrase_blocking=args.phrase_blocking,
            min_tokens=8,
        )
        metrics = score_response(response["response"])
        item = {
            "prompt": prompt,
            "response": response["response"],
            "tokens": response["tokens"],
            "latency_ms": response["latency_ms"],
            "domain": response.get("domain_used", ""),
            "metrics": metrics,
        }
        results.append(item)
        print(f"\nQ: {prompt}")
        print(f"A: {response['response']}")
        print(f"metrics: {metrics}")

    loop_scores = [item["metrics"]["loop_score"] for item in results]
    summary = {
        "responses": len(results),
        "mean_loop_score": round(sum(loop_scores) / max(1, len(loop_scores)), 4),
        "max_loop_score": max(loop_scores) if loop_scores else math.nan,
        "elapsed_sec": round(time.time() - started, 2),
        "power_mode": args.power_mode,
        "context": args.context,
        "checkpoint": args.checkpoint or "default",
    }
    print(f"\nSUMMARY: {summary}")

    if args.json_out:
        os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
            json.dump({"summary": summary, "results": results}, handle, indent=2)
        print(f"wrote: {args.json_out}")


if __name__ == "__main__":
    main()
