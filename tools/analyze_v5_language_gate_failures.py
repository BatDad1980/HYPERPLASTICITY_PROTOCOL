"""Summarize failed transcripts from an HPP V2 V5 language gate artifact."""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict


def load_gate(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def format_top(counter: Counter, limit: int = 12) -> list[dict]:
    return [{"item": item, "count": count} for item, count in counter.most_common(limit)]


def analyze(payload: dict, profile: str) -> dict:
    transcripts = [item for item in payload["transcripts"] if item["profile"] == profile]
    failures = [item for item in transcripts if not item["pass"]]

    reason_counts = Counter()
    mode_counts = Counter()
    prompt_counts = Counter()
    identity_terms = Counter()
    format_terms = Counter()
    mode_labels = Counter()

    examples = []
    for item in failures:
        mode_counts[item["mode"]] += 1
        prompt_counts[item["prompt"]] += 1
        for reason in item["fail_reasons"]:
            reason_counts[reason] += 1
        for term, count in item["leak_metrics"]["identity_spiral_hits"].items():
            identity_terms[term] += count
        for term, count in item["leak_metrics"]["format_hits"].items():
            format_terms[term] += count
        for term, count in item["leak_metrics"]["mode_label_hits"].items():
            mode_labels[term] += count

        examples.append(
            {
                "id": item["id"],
                "mode": item["mode"],
                "seed": item["seed"],
                "prompt": item["prompt"],
                "response": item["response"],
                "fail_reasons": item["fail_reasons"],
                "loop_score": item["loop_metrics"]["loop_score"],
                "identity_spiral_hits": item["leak_metrics"]["identity_spiral_hits"],
                "format_hits": item["leak_metrics"]["format_hits"],
                "mode_label_hits": item["leak_metrics"]["mode_label_hits"],
            }
        )

    return {
        "profile": profile,
        "total": len(transcripts),
        "failures": len(failures),
        "pass_rate": round((len(transcripts) - len(failures)) / max(1, len(transcripts)), 4),
        "failure_reasons": format_top(reason_counts),
        "failures_by_mode": format_top(mode_counts),
        "top_failed_prompts": format_top(prompt_counts),
        "identity_terms": format_top(identity_terms),
        "format_terms": format_top(format_terms),
        "mode_label_terms": format_top(mode_labels),
        "examples": examples[:30],
    }


def write_markdown(summary: dict, payload: dict, path: str) -> None:
    lines = [
        "# HPP V2 V5 Language Gate Failure Review",
        "",
        f"Source: `{summary['source']}`",
        f"Checkpoint: `{payload.get('checkpoint', '')}`",
        f"Profile: `{summary['profile']}`",
        f"Failures: {summary['failures']} / {summary['total']}",
        f"Pass rate: {summary['pass_rate']}",
        "",
        "## Failure Reasons",
        "",
    ]
    for item in summary["failure_reasons"]:
        lines.append(f"- `{item['item']}`: {item['count']}")
    lines.extend(["", "## Failures By Mode", ""])
    for item in summary["failures_by_mode"]:
        lines.append(f"- `{item['item']}`: {item['count']}")
    lines.extend(["", "## Identity Terms", ""])
    for item in summary["identity_terms"]:
        lines.append(f"- `{item['item']}`: {item['count']}")
    lines.extend(["", "## Mode Label Terms", ""])
    for item in summary["mode_label_terms"]:
        lines.append(f"- `{item['item']}`: {item['count']}")
    lines.extend(["", "## Examples", ""])
    for item in summary["examples"][:12]:
        lines.extend(
            [
                f"### {item['id']} seed {item['seed']}",
                "",
                f"- mode: `{item['mode']}`",
                f"- reasons: `{', '.join(item['fail_reasons'])}`",
                f"- loop score: `{item['loop_score']}`",
                f"- prompt: {item['prompt']}",
                f"- response: {item['response']}",
                "",
            ]
        )

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gate-json", required=True)
    parser.add_argument("--profile", default="stable")
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--md-out", required=True)
    args = parser.parse_args()

    payload = load_gate(args.gate_json)
    summary = analyze(payload, args.profile)
    summary["source"] = args.gate_json

    os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(summary, handle, indent=2)
    write_markdown(summary, payload, args.md_out)

    print(f"wrote: {args.json_out}")
    print(f"wrote: {args.md_out}")


if __name__ == "__main__":
    main()
