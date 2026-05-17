"""Audit HPP conversational data for category balance and loop attractors."""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter


DEFAULT_FILES = [
    "CONVERSATIONAL_FLUENCY.jsonl",
    "CONVERSATIONAL_FLUENCY_V2.jsonl",
    "CONVERSATIONAL_CLEANUP_V1.jsonl",
    "IDENTITY.jsonl",
    "SYNTAX_FOUNDATION.jsonl",
]

ATTRACTORS = [
    "what do you think",
    "do not quit",
    "you are standing",
    "fortress is standing",
    "standing",
    "creator",
    "protect",
    "mission",
    "oath",
    "masamune",
]


def iter_rows(path: str):
    with open(path, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield line_number, json.loads(line)
            except json.JSONDecodeError as exc:
                yield line_number, {"_error": str(exc), "_raw": line[:200]}


def row_text(row: dict) -> str:
    parts = [
        str(row.get("text", "")),
        str(row.get("instruction", "")),
        str(row.get("input", "")),
        str(row.get("response", "")),
    ]
    return "\n".join(part for part in parts if part)


def repeated_ngram_count(text: str, n: int) -> int:
    words = re.findall(r"[A-Za-z0-9']+", text.lower())
    grams = [tuple(words[i : i + n]) for i in range(max(0, len(words) - n + 1))]
    counts = Counter(grams)
    return sum(count - 1 for count in counts.values() if count > 1)


def audit_file(path: str, top: int) -> None:
    rows = list(iter_rows(path))
    categories = Counter(str(row.get("category", "uncategorized")) for _, row in rows)
    errors = [(line, row) for line, row in rows if "_error" in row]
    blob = "\n".join(row_text(row).lower() for _, row in rows)

    print(f"\n== {path} ==")
    print(f"samples: {len(rows)}")
    if errors:
        print(f"json_errors: {len(errors)}")
    print(f"categories: {dict(categories.most_common())}")

    hits = {phrase: blob.count(phrase) for phrase in ATTRACTORS if blob.count(phrase)}
    print(f"attractor_hits: {hits}")

    scored = []
    for line_number, row in rows:
        text = row_text(row)
        lower = text.lower()
        phrase_hits = sum(lower.count(phrase) for phrase in ATTRACTORS)
        repeat_hits = repeated_ngram_count(text, 3)
        score = phrase_hits * 3 + repeat_hits
        if score:
            scored.append((score, line_number, row.get("category", "uncategorized"), text[:220].replace("\n", " ")))

    for score, line_number, category, preview in sorted(scored, reverse=True)[:top]:
        print(f"hotspot score={score} line={line_number} category={category}: {preview}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", default=os.path.join("datasets", "hf_local"))
    parser.add_argument("--top", type=int, default=8)
    parser.add_argument("files", nargs="*", default=DEFAULT_FILES)
    args = parser.parse_args()

    for name in args.files:
        path = name if os.path.isabs(name) else os.path.join(args.dir, name)
        if os.path.exists(path):
            audit_file(path, args.top)
        else:
            print(f"\n== {path} ==\nmissing")


if __name__ == "__main__":
    main()
