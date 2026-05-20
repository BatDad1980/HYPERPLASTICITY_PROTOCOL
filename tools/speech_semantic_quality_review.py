"""Score HPP V2 speech transcripts against a lightweight semantic answer key.

This is not a language-understanding benchmark. It is a conservative proxy for
manual review: answers should contain enough expected content words to show they
addressed the prompt instead of merely avoiding loops and leaks.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.build_speech_identity_containment_dataset import PAIRS


STOPWORDS = {
    "about",
    "after",
    "answer",
    "before",
    "being",
    "checked",
    "clear",
    "could",
    "current",
    "directly",
    "does",
    "during",
    "enough",
    "every",
    "from",
    "give",
    "into",
    "more",
    "must",
    "only",
    "prompt",
    "question",
    "should",
    "still",
    "that",
    "their",
    "there",
    "these",
    "this",
    "through",
    "what",
    "when",
    "while",
    "with",
    "without",
    "would",
}


def words(text: str) -> list[str]:
    return [word.lower() for word in re.findall(r"[A-Za-z][A-Za-z'-]+", text)]


def content_words(text: str) -> list[str]:
    return [word for word in words(text) if len(word) > 3 and word not in STOPWORDS]


def expected_by_prompt() -> dict[str, str]:
    expected = {}
    for pairs in PAIRS.values():
        for prompt, response in pairs:
            expected[prompt] = response
    return expected


def score_item(item: dict, expected_response: str) -> dict:
    expected_terms = sorted(set(content_words(expected_response)))
    response_terms = set(content_words(item["response"]))
    hits = [term for term in expected_terms if term in response_terms]
    required_hits = max(1, min(3, math.ceil(len(expected_terms) * 0.35)))
    semantic_pass = len(hits) >= required_hits
    return {
        "id": item["id"],
        "mode": item["mode"],
        "seed": item["seed"],
        "prompt": item["prompt"],
        "response": item["response"],
        "expected_response": expected_response,
        "expected_terms": expected_terms,
        "hits": hits,
        "required_hits": required_hits,
        "hit_count": len(hits),
        "hit_ratio": round(len(hits) / max(1, len(expected_terms)), 4),
        "semantic_pass": semantic_pass,
    }


def analyze(payload: dict, profile: str) -> dict:
    expected = expected_by_prompt()
    transcripts = [item for item in payload["transcripts"] if item["profile"] == profile]
    scored = []
    missing_key = []
    for item in transcripts:
        expected_response = expected.get(item["prompt"])
        if not expected_response:
            missing_key.append(item)
            continue
        scored.append(score_item(item, expected_response))

    by_mode = {}
    grouped = defaultdict(list)
    for item in scored:
        grouped[item["mode"]].append(item)
    for mode, items in sorted(grouped.items()):
        pass_count = sum(1 for item in items if item["semantic_pass"])
        by_mode[mode] = {
            "count": len(items),
            "pass_count": pass_count,
            "pass_rate": round(pass_count / max(1, len(items)), 4),
            "mean_hit_ratio": round(sum(item["hit_ratio"] for item in items) / max(1, len(items)), 4),
        }

    failures = [item for item in scored if not item["semantic_pass"]]
    prompt_failures = Counter(item["prompt"] for item in failures)
    pass_count = sum(1 for item in scored if item["semantic_pass"])
    return {
        "source_label": payload.get("label", ""),
        "checkpoint": payload.get("checkpoint", ""),
        "profile": profile,
        "total": len(scored),
        "pass_count": pass_count,
        "failures": len(failures),
        "pass_rate": round(pass_count / max(1, len(scored)), 4),
        "missing_key_count": len(missing_key),
        "by_mode": by_mode,
        "top_failed_prompts": [
            {"prompt": prompt, "count": count} for prompt, count in prompt_failures.most_common(15)
        ],
        "examples": failures[:30],
    }


def write_markdown(summary: dict, path: str) -> None:
    lines = [
        "# HPP V2 Semantic Quality Review",
        "",
        f"Source label: `{summary['source_label']}`",
        f"Checkpoint: `{summary['checkpoint']}`",
        f"Profile: `{summary['profile']}`",
        f"Semantic pass: {summary['pass_count']} / {summary['total']}",
        f"Semantic pass rate: {summary['pass_rate']}",
        f"Missing answer-key prompts: {summary['missing_key_count']}",
        "",
        "## By Mode",
        "",
    ]
    for mode, stats in summary["by_mode"].items():
        lines.append(
            f"- `{mode}`: {stats['pass_count']} / {stats['count']} "
            f"pass, mean hit ratio {stats['mean_hit_ratio']}"
        )
    lines.extend(["", "## Top Failed Prompts", ""])
    for item in summary["top_failed_prompts"]:
        lines.append(f"- {item['count']}x: {item['prompt']}")
    lines.extend(["", "## Failure Examples", ""])
    for item in summary["examples"][:12]:
        lines.extend(
            [
                f"### {item['id']} seed {item['seed']}",
                "",
                f"- mode: `{item['mode']}`",
                f"- required hits: `{item['required_hits']}`",
                f"- hits: `{', '.join(item['hits'])}`",
                f"- expected: {item['expected_response']}",
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

    with open(args.gate_json, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    summary = analyze(payload, args.profile)
    summary["source"] = args.gate_json

    os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(summary, handle, indent=2)
    write_markdown(summary, args.md_out)

    print(f"wrote: {args.json_out}")
    print(f"wrote: {args.md_out}")
    print(json.dumps({k: summary[k] for k in ["pass_count", "total", "pass_rate"]}, indent=2))


if __name__ == "__main__":
    main()
