"""Probe whether forcing the first answer tokens keeps HPP V2 speech on path."""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.build_speech_exposure_bias_bridge_dataset import prompt_answer
from tools.build_speech_identity_containment_dataset import PAIRS
from tools.speech_semantic_quality_review import score_item
from tools.speech_v5_language_gate import leak_metrics, load_override


def prompt_rows() -> list[dict]:
    rows = []
    for mode, pairs in PAIRS.items():
        for prompt, expected in pairs:
            rows.append({"mode": mode, "prompt": prompt, "expected": expected})
    return rows


def forced_prefix(engine: HPP_SovereignEngine_V2, expected: str, token_count: int) -> str:
    if token_count <= 0:
        return ""
    tokens = engine.enc.encode(expected)[:token_count]
    return engine.enc.decode(tokens)


def run_probe(args: argparse.Namespace) -> dict:
    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)
    engine.set_power_mode(args.power_mode)

    records = []
    rows = prompt_rows()
    selected = rows[: args.limit] if args.limit else rows
    for row in selected:
        for count in args.force_counts:
            prefix = forced_prefix(engine, row["expected"], count)
            input_text = f"{prompt_answer(row['prompt'])} {prefix}"
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
            combined = (prefix + " " + response["response"]).strip()
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
            records.append(
                {
                    "mode": row["mode"],
                    "prompt": row["prompt"],
                    "expected": row["expected"],
                    "forced_token_count": count,
                    "forced_prefix": prefix,
                    "generated_continuation": response["response"],
                    "scored_response": combined,
                    "semantic_pass": scored["semantic_pass"],
                    "hits": scored["hits"],
                    "required_hits": scored["required_hits"],
                    "format_leak_count": leaks["format_leak_count"],
                    "identity_spiral_count": leaks["identity_spiral_count"],
                    "repeated_sentence_count": leaks["repeated_sentence_count"],
                }
            )

    grouped = defaultdict(list)
    for record in records:
        grouped[record["forced_token_count"]].append(record)
    summary = {}
    for count, items in sorted(grouped.items()):
        pass_count = sum(1 for item in items if item["semantic_pass"])
        summary[str(count)] = {
            "count": len(items),
            "semantic_pass_count": pass_count,
            "semantic_pass_rate": round(pass_count / max(1, len(items)), 4),
            "format_leak_total": sum(item["format_leak_count"] for item in items),
            "identity_spiral_total": sum(item["identity_spiral_count"] for item in items),
            "repeated_sentence_total": sum(item["repeated_sentence_count"] for item in items),
        }

    return {
        "checkpoint": args.checkpoint,
        "seed": args.seed,
        "speech_profile": args.speech_profile,
        "domain": args.domain,
        "prompt_count": len(selected),
        "force_counts": args.force_counts,
        "summary": summary,
        "records": records,
    }


def write_markdown(payload: dict, path: str) -> None:
    lines = [
        "# HPP V2 Answer-Start Release Probe",
        "",
        f"Checkpoint: `{payload['checkpoint']}`",
        f"Seed: `{payload['seed']}`",
        f"Profile: `{payload['speech_profile']}`",
        f"Domain: `{payload['domain']}`",
        f"Prompts: `{payload['prompt_count']}`",
        "",
        "## Summary",
        "",
    ]
    for count, stats in payload["summary"].items():
        lines.append(
            f"- force `{count}` token(s): semantic `{stats['semantic_pass_count']}/{stats['count']}`, "
            f"format leaks `{stats['format_leak_total']}`, identity spirals `{stats['identity_spiral_total']}`"
        )
    lines.extend(["", "## Samples", ""])
    for item in payload["records"][:20]:
        lines.extend(
            [
                f"### force {item['forced_token_count']} - {item['mode']} - {item['prompt']}",
                "",
                f"- expected: {item['expected']}",
                f"- forced prefix: {item['forced_prefix']}",
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
    parser.add_argument("--force-counts", nargs="+", type=int, default=[0, 1, 2, 3, 5])
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
