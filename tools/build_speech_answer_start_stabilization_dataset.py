"""Build short answer-start stabilization data for HPP V2 speech."""
from __future__ import annotations

import argparse
import json
import os
import random
import sys

import tiktoken

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.build_speech_exposure_bias_bridge_dataset import prompt_answer
from tools.build_speech_identity_containment_dataset import PAIRS


DEFAULT_OUT = os.path.join("datasets", "hf_local", "SPEECH_ANSWER_START_STABILIZATION_V1.jsonl")
TOKEN_COUNTS = [3, 5]


def answer_start(enc, response: str, token_count: int) -> str:
    tokens = enc.encode(response)[:token_count]
    return enc.decode(tokens)


def make_row(prefix: str, response: str, category: str, source: str, mode: str) -> dict:
    return {
        "prompt_text": prefix,
        "completion_prefix": prefix,
        "response": response,
        "category": category,
        "source": source,
        "mode": mode,
        "text": prefix + response,
    }


def prefix_variants(prompt: str) -> list[tuple[str, str]]:
    return [
        ("qa_answer_start", f"{prompt_answer(prompt)} "),
        ("direct_answer_start", f"Answer directly: {prompt}\nAnswer: "),
        ("short_answer_start", f"Short answer: {prompt}\nAnswer: "),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=72)
    args = parser.parse_args()

    enc = tiktoken.get_encoding("gpt2")
    rows = []
    for mode, pairs in PAIRS.items():
        for prompt, expected in pairs:
            for token_count in TOKEN_COUNTS:
                start = answer_start(enc, expected, token_count)
                for variant, prefix in prefix_variants(prompt):
                    rows.append(
                        make_row(
                            prefix,
                            start,
                            f"{mode}_{variant}_{token_count}_tokens",
                            "answer_start_stabilization",
                            mode,
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
