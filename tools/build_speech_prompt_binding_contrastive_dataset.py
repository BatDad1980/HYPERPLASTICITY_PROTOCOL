"""Build a contrastive semantic prompt-binding curriculum for HPP V2 speech.

This dataset trains similar prompts with different answers and explicit
question/answer wrappers. It is diagnostic V2 lab data, not buyer-safe evidence.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.build_speech_identity_containment_dataset import PAIRS


DEFAULT_OUT = os.path.join("datasets", "hf_local", "SPEECH_PROMPT_BINDING_CONTRASTIVE_V1.jsonl")


def make_row(prefix: str, response: str, category: str, source: str) -> dict:
    return {
        "prompt_text": prefix,
        "completion_prefix": prefix,
        "response": response,
        "category": category,
        "source": source,
        "text": prefix + response,
    }


def prompt_variants(prompt: str) -> list[str]:
    return [
        f"{prompt}\n",
        f"Answer directly: {prompt}\n",
        f"Use one sentence: {prompt}\n",
        f"Short answer: {prompt}\n",
        f"Question: {prompt}\nAnswer:",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=34)
    args = parser.parse_args()

    rows = []
    flat_pairs = []
    for mode, pairs in PAIRS.items():
        for prompt, response in pairs:
            flat_pairs.append((mode, prompt, response))
            for prefix in prompt_variants(prompt):
                rows.append(
                    make_row(prefix, response, f"{mode}_direct_binding", "prompt_binding_direct")
                )

    for mode, pairs in PAIRS.items():
        for index, (prompt, response) in enumerate(pairs):
            wrong_prompt, wrong_response = pairs[(index + 1) % len(pairs)]
            prefix = (
                f"Choose the answer for this prompt only.\n"
                f"Prompt: {prompt}\n"
                f"Wrong nearby answer: {wrong_response}\n"
                f"Correct answer:"
            )
            rows.append(
                make_row(prefix, response, f"{mode}_contrastive_same_mode", "prompt_binding_contrastive")
            )

    for index, (mode, prompt, response) in enumerate(flat_pairs):
        wrong_mode, wrong_prompt, wrong_response = flat_pairs[(index + 17) % len(flat_pairs)]
        prefix = (
            f"Do not mix answer memories.\n"
            f"Target prompt: {prompt}\n"
            f"Distractor prompt: {wrong_prompt}\n"
            f"Distractor answer: {wrong_response}\n"
            f"Target answer:"
        )
        rows.append(
            make_row(
                prefix,
                response,
                f"{mode}_contrastive_cross_mode",
                "prompt_binding_cross_contrastive",
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
