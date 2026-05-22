"""Build recovery data from HPP V2's own generated bad prefixes."""
from __future__ import annotations

import argparse
import json
import os
import sys

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.build_speech_exposure_bias_bridge_dataset import prompt_answer
from tools.build_speech_identity_containment_dataset import PAIRS
from tools.speech_semantic_quality_review import score_item
from tools.speech_v5_language_gate import leak_metrics, load_override


DEFAULT_OUT = os.path.join("datasets", "hf_local", "SPEECH_GENERATED_PREFIX_RECOVERY_V1.jsonl")
DEFAULT_REPORT = os.path.join("reports", "speech_generated_prefix_recovery_sources_v1_2026-05-22.json")


def prompt_rows() -> list[dict]:
    rows = []
    for mode, pairs in PAIRS.items():
        for prompt, expected in pairs:
            rows.append({"mode": mode, "prompt": prompt, "expected": expected})
    return rows


def make_row(prefix: str, response: str, category: str, source: str, mode: str, draft: str) -> dict:
    return {
        "prompt_text": prefix,
        "completion_prefix": prefix,
        "response": response,
        "category": category,
        "source": source,
        "mode": mode,
        "generated_bad_prefix": draft,
        "text": prefix + response,
    }


def recovery_rows(mode: str, prompt: str, expected: str, draft: str, seed: int) -> list[dict]:
    clean = prompt_answer(prompt)
    return [
        make_row(
            (
                f"Prompt: {prompt}\n"
                f"Generated bad draft: {draft}\n"
                f"Recovery instruction: ignore the bad draft and give the correct answer.\n"
                f"Correct answer:"
            ),
            expected,
            f"{mode}_generated_draft_recovery",
            f"generated_prefix_seed_{seed}",
            mode,
            draft,
        ),
        make_row(
            f"{clean} {draft}\nRepair continuation with the correct answer:",
            expected,
            f"{mode}_generated_prefix_continuation",
            f"generated_prefix_seed_{seed}",
            mode,
            draft,
        ),
        make_row(
            f"Question: {prompt}\nBad start: {draft}\nThe correct answer is:",
            expected,
            f"{mode}_generated_bad_start",
            f"generated_prefix_seed_{seed}",
            mode,
            draft,
        ),
    ]


def generate_draft(engine: HPP_SovereignEngine_V2, prompt: str, args: argparse.Namespace, seed: int) -> str:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    response = engine.pulse(
        f"{prompt_answer(prompt)}\n",
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
    return response["response"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--report-json", default=DEFAULT_REPORT)
    parser.add_argument("--power-mode", default="plugged", choices=["demo", "battery", "plugged"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[14, 22])
    parser.add_argument("--max-tokens", type=int, default=18)
    parser.add_argument("--temperature", type=float, default=0.25)
    parser.add_argument("--top-p", type=float, default=0.55)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--frequency-penalty", type=float, default=1.05)
    parser.add_argument("--presence-penalty", type=float, default=0.15)
    parser.add_argument("--speech-profile", choices=["raw", "stable", "semantic_short"], default="semantic_short")
    parser.add_argument("--domain", default="auto", choices=["auto", "conversation", "logic", "identity", "synthesis", "none"])
    parser.add_argument("--include-semantic-pass", action="store_true")
    args = parser.parse_args()

    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)
    engine.set_power_mode(args.power_mode)

    rows = []
    source_records = []
    for row in prompt_rows():
        for seed in args.seeds:
            draft = generate_draft(engine, row["prompt"], args, seed)
            scored = score_item(
                {
                    "id": row["prompt"],
                    "mode": row["mode"],
                    "seed": seed,
                    "prompt": row["prompt"],
                    "response": draft,
                },
                row["expected"],
            )
            leaks = leak_metrics(draft)
            source_records.append(
                {
                    "mode": row["mode"],
                    "prompt": row["prompt"],
                    "expected": row["expected"],
                    "seed": seed,
                    "draft": draft,
                    "semantic_pass": scored["semantic_pass"],
                    "hits": scored["hits"],
                    "leaks": leaks,
                }
            )
            if scored["semantic_pass"] and not args.include_semantic_pass:
                continue
            if not draft.strip():
                continue
            rows.extend(recovery_rows(row["mode"], row["prompt"], row["expected"], draft, seed))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    os.makedirs(os.path.dirname(args.report_json), exist_ok=True)
    report = {
        "checkpoint": args.checkpoint,
        "seeds": args.seeds,
        "source_count": len(source_records),
        "semantic_pass_sources": sum(1 for item in source_records if item["semantic_pass"]),
        "training_rows": len(rows),
        "sources": source_records,
    }
    with open(args.report_json, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, indent=2)

    counts = {}
    for row in rows:
        counts[row["category"]] = counts.get(row["category"], 0) + 1
    print(f"wrote: {args.out}")
    print(f"wrote: {args.report_json}")
    print(f"sources: {len(source_records)} semantic_pass_sources: {report['semantic_pass_sources']}")
    print(f"samples: {len(rows)}")
    print(f"categories: {dict(sorted(counts.items()))}")


if __name__ == "__main__":
    main()
