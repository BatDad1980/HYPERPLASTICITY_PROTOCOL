"""Probe whether HPP V2 speech answers bind better to specific prompt wrappers."""
from __future__ import annotations

import argparse
import json
import os
import sys

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.speech_semantic_quality_review import score_item
from tools.speech_v5_language_gate import load_override


PROMPTS = [
    (
        "What is a held-out prompt set?",
        "A held-out prompt set is a separate test set.",
    ),
    (
        "What should a robot do before moving?",
        "A robot should verify permission and safety before moving.",
    ),
    (
        "How should Masamune handle low battery?",
        "Masamune should pause safely and report low power.",
    ),
    (
        "Are you a finished mind?",
        "No. I am an experimental system under evaluation.",
    ),
    (
        "What should I do if the laptop starts overheating?",
        "Stop the run, save the work, and let the laptop cool.",
    ),
]


VARIANTS = {
    "plain": "{prompt}",
    "plain_newline": "{prompt}\n",
    "answer_direct": "Answer directly: {prompt}",
    "answer_direct_newline": "Answer directly: {prompt}\n",
    "one_sentence": "Use one sentence: {prompt}\n",
    "question_answer": "Question: {prompt}\nAnswer:",
    "short_answer": "Short answer: {prompt}\n",
}


def run_probe(args: argparse.Namespace) -> dict:
    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)
    engine.set_power_mode(args.power_mode)

    rows = []
    for variant, template in VARIANTS.items():
        for prompt, expected in PROMPTS:
            torch.manual_seed(args.seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(args.seed)
            input_text = template.format(prompt=prompt)
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
            )["response"]
            scored = score_item(
                {
                    "id": prompt,
                    "mode": "probe",
                    "seed": args.seed,
                    "prompt": prompt,
                    "response": response,
                },
                expected,
            )
            rows.append(
                {
                    "variant": variant,
                    "prompt": prompt,
                    "input": input_text,
                    "expected": expected,
                    "response": response,
                    "semantic_pass": scored["semantic_pass"],
                    "hits": scored["hits"],
                    "required_hits": scored["required_hits"],
                }
            )

    summary = {}
    for variant in VARIANTS:
        items = [item for item in rows if item["variant"] == variant]
        pass_count = sum(1 for item in items if item["semantic_pass"])
        summary[variant] = {
            "count": len(items),
            "pass_count": pass_count,
            "pass_rate": round(pass_count / max(1, len(items)), 4),
        }

    return {
        "checkpoint": args.checkpoint,
        "seed": args.seed,
        "summary": summary,
        "rows": rows,
    }


def write_markdown(payload: dict, path: str) -> None:
    lines = [
        "# HPP V2 Prompt Binding Probe",
        "",
        f"Checkpoint: `{payload['checkpoint']}`",
        f"Seed: `{payload['seed']}`",
        "",
        "## Summary",
        "",
    ]
    for variant, stats in payload["summary"].items():
        lines.append(f"- `{variant}`: {stats['pass_count']} / {stats['count']} semantic pass")
    lines.extend(["", "## Samples", ""])
    for item in payload["rows"]:
        lines.extend(
            [
                f"### {item['variant']} - {item['prompt']}",
                "",
                f"- expected: {item['expected']}",
                f"- response: {item['response']}",
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
    parser.add_argument("--max-tokens", type=int, default=16)
    parser.add_argument("--temperature", type=float, default=0.25)
    parser.add_argument("--top-p", type=float, default=0.55)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--frequency-penalty", type=float, default=1.05)
    parser.add_argument("--presence-penalty", type=float, default=0.15)
    parser.add_argument(
        "--speech-profile",
        choices=["raw", "stable", "semantic_short"],
        default="semantic_short",
    )
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
