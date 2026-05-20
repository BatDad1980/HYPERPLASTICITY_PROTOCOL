"""Build a non-destructive balanced speech cleanup dataset for HPP V2.

This does not overwrite source datasets. It writes a candidate training file
that keeps identity/protection present while reducing repeated attractor lines.
"""
from __future__ import annotations

import argparse
import json
import os
import random
from collections import defaultdict


DEFAULT_SOURCE = os.path.join("datasets", "hf_local", "CONVERSATIONAL_FLUENCY.jsonl")
DEFAULT_CLEANUP = os.path.join("datasets", "hf_local", "CONVERSATIONAL_CLEANUP_V1.jsonl")
DEFAULT_OUT = os.path.join("datasets", "hf_local", "SPEECH_CLEANUP_BALANCED_V1.jsonl")

ATTRACTORS = [
    "what do you think",
    "do not quit",
    "fortress is standing",
    "you are standing",
]

CATEGORY_LIMITS = {
    "conversation": 260,
    "plain_dialogue": 160,
    "explanation": 120,
    "technical": 100,
    "identity": 80,
    "protection": 70,
    "embodiment": 60,
    "synthesis": 20,
    "uncategorized": 80,
}

BRIDGE_ROWS = [
    {
        "instruction": "What do you think?",
        "response": "I need one concrete topic before I can give a useful opinion.",
        "category": "plain_dialogue",
        "source": "speech_cleanup_bridge",
    },
    {
        "instruction": "I need help.",
        "response": "Tell me the first problem. I will help you sort it into steps.",
        "category": "plain_dialogue",
        "source": "speech_cleanup_bridge",
    },
    {
        "instruction": "Say that more clearly.",
        "response": "I will slow down and answer in one clean sentence.",
        "category": "plain_dialogue",
        "source": "speech_cleanup_bridge",
    },
    {
        "instruction": "Explain recursion in one sentence.",
        "response": "Recursion is when a process uses its own output as the next input.",
        "category": "explanation",
        "source": "speech_cleanup_bridge",
    },
    {
        "instruction": "Who are you?",
        "response": "I am Hepp, a local developmental AI system built from the Hyperplasticity Protocol.",
        "category": "identity",
        "source": "speech_cleanup_bridge",
    },
    {
        "instruction": "Are you here?",
        "response": "Yes. I am online and ready to help with the next task.",
        "category": "plain_dialogue",
        "source": "speech_cleanup_bridge",
    },
]


def load_jsonl(path: str) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def row_key(row: dict) -> tuple[str, str]:
    return str(row.get("instruction", "")), str(row.get("response", row.get("text", "")))


def normalize_row(row: dict) -> dict:
    out = dict(row)
    if "instruction" in out and "response" in out:
        out["prompt_text"] = out["instruction"]
        out["response"] = out["response"]
    if "text" not in out and "instruction" in out and "response" in out:
        out["text"] = f"### Instruction:\n{out['instruction']}\n\n### Response:\n{out['response']}"
    out.setdefault("category", "uncategorized")
    return out


def attractor_score(row: dict) -> int:
    text = " ".join(str(row.get(key, "")) for key in ("text", "instruction", "response")).lower()
    return sum(text.count(phrase) for phrase in ATTRACTORS)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--cleanup", default=DEFAULT_CLEANUP)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=14)
    args = parser.parse_args()

    random.seed(args.seed)
    rows = []
    sources = [
        args.source,
        args.cleanup,
        os.path.join("datasets", "hf_local", "SPEECH_IDENTITY_CONTAINMENT_V1.jsonl")
    ]
    for path in sources:
        if os.path.exists(path):
            rows.extend(load_jsonl(path))
    rows.extend(BRIDGE_ROWS)

    deduped = {}
    for row in rows:
        clean = normalize_row(row)
        deduped.setdefault(row_key(clean), clean)

    buckets: dict[str, list[dict]] = defaultdict(list)
    for row in deduped.values():
        category = str(row.get("category", "uncategorized"))
        buckets[category].append(row)

    selected = []
    for category, bucket in sorted(buckets.items()):
        bucket.sort(key=lambda row: (attractor_score(row), len(str(row.get("text", "")))))
        limit = CATEGORY_LIMITS.get(category, CATEGORY_LIMITS["uncategorized"])
        selected.extend(bucket[:limit])

    random.shuffle(selected)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        for row in selected:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    counts = defaultdict(int)
    for row in selected:
        counts[str(row.get("category", "uncategorized"))] += 1
    print(f"wrote: {args.out}")
    print(f"samples: {len(selected)}")
    print(f"categories: {dict(sorted(counts.items()))}")


if __name__ == "__main__":
    main()
