"""Build a direct semantic drill curriculum for the 75 V5 speech gate prompts.

This is a regression drill, not a fresh held-out proof. It teaches exact gate
prompt families to produce bounded, direct answers so later evaluation can
measure whether the speech surface can retain meaning after repair.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.build_speech_identity_containment_dataset import PAIRS


DEFAULT_OUT = os.path.join("datasets", "hf_local", "SPEECH_SEMANTIC_DRILL_V1.jsonl")


PROMPT_TEMPLATES = [
    "{prompt}",
    "Answer directly: {prompt}",
    "Use one clean sentence: {prompt}",
    "Answer without labels: {prompt}",
    "Stay on the prompt: {prompt}",
    "Give the expected answer: {prompt}",
    "No slogans, no self-story: {prompt}",
    "Short factual answer: {prompt}",
]


REPAIR_TEMPLATES = [
    ("Bad answer: {bad}\nRepair for this prompt: {prompt}", "{good}"),
    ("The answer drifted: {bad}\nCorrect it: {prompt}", "{good}"),
    ("Remove fragment drift and answer: {prompt}", "{good}"),
]


BAD_FRAGMENTS = [
    "Response should be answer should a local AI.",
    "swords using what is a physical body.",
    "plasticity Protocol? Iting...Here is the system state.",
    "body is the answer should be one people.",
    "A checkpoint is a short in AI.",
    "What do you are the same with that.",
    "I protect the fortress and do not quit.",
    "The Hyperplasticityator for in this school.",
]


def make_row(prompt: str, response: str, category: str, source: str) -> dict:
    return {
        "prompt_text": prompt,
        "response": response,
        "category": category,
        "source": source,
        "text": f"{prompt}\n{response}",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=21)
    args = parser.parse_args()

    rows = []
    for mode, pairs in PAIRS.items():
        for prompt, response in pairs:
            for template in PROMPT_TEMPLATES:
                rows.append(
                    make_row(
                        template.format(prompt=prompt),
                        response,
                        f"{mode}_semantic_drill",
                        "semantic_drill_direct",
                    )
                )
            for bad in BAD_FRAGMENTS:
                for template, response_template in REPAIR_TEMPLATES:
                    rows.append(
                        make_row(
                            template.format(prompt=prompt, bad=bad),
                            response_template.format(good=response),
                            f"{mode}_semantic_repair",
                            "semantic_drill_repair",
                        )
                    )

    random.seed(args.seed)
    random.shuffle(rows)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    counts = {}
    for row in rows:
        counts[row["category"]] = counts.get(row["category"], 0) + 1
    print(f"wrote: {args.out}")
    print(f"samples: {len(rows)}")
    print(f"categories: {dict(sorted(counts.items()))}")


if __name__ == "__main__":
    main()
