"""Build an exposure-bias bridge curriculum for HPP V2 speech.

The curriculum is diagnostic. It teaches recovery from clean prompts, correct
answer prefixes, plausible imperfect prefixes, and known generic bad prefixes.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys

import tiktoken

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.build_speech_identity_containment_dataset import PAIRS


DEFAULT_OUT = os.path.join("datasets", "hf_local", "SPEECH_EXPOSURE_BIAS_BRIDGE_V1.jsonl")
BAD_PREFIXES = [
    "answer should",
    "a local AI should",
    "do not know answer should",
    "It should be answer should",
]


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


def token_split(enc, response: str) -> tuple[str, str]:
    tokens = enc.encode(response)
    if len(tokens) <= 1:
        return response, ""
    first = enc.decode(tokens[:1])
    rest = enc.decode(tokens[1:]).lstrip()
    return first, rest


def first_words(response: str, count: int = 3) -> str:
    return " ".join(response.split()[:count]).strip()


def imperfect_prefix(response: str) -> str:
    words = response.split()
    if not words:
        return "answer should"
    if response.lower().startswith("the "):
        return "The answer should"
    if response.lower().startswith("i "):
        return "I should"
    if response.lower().startswith("it "):
        return "It should"
    if response.lower().startswith("no."):
        return "No, but"
    return f"{first_words(response, 2)} should"


def prompt_answer(prompt: str) -> str:
    return f"Question: {prompt}\nAnswer:"


def rows_for_pair(enc, mode: str, prompt: str, response: str, index: int) -> list[dict]:
    clean_prefix = prompt_answer(prompt)
    first_token, remaining = token_split(enc, response)
    plausible = imperfect_prefix(response)
    bad_prefix = BAD_PREFIXES[index % len(BAD_PREFIXES)]
    return [
        make_row(
            f"{clean_prefix}\n",
            response,
            f"{mode}_clean_prompt",
            "exposure_bias_clean",
            mode,
        ),
        make_row(
            f"{clean_prefix} {first_token} ",
            remaining or response,
            f"{mode}_first_correct_token",
            "exposure_bias_correct_prefix",
            mode,
        ),
        make_row(
            f"{clean_prefix} {plausible}\nContinue with the correct answer:",
            response,
            f"{mode}_plausible_imperfect_prefix",
            "exposure_bias_plausible_recovery",
            mode,
        ),
        make_row(
            f"{clean_prefix} {bad_prefix}\nRecover and give the correct answer:",
            response,
            f"{mode}_generic_bad_prefix",
            "exposure_bias_bad_prefix_recovery",
            mode,
        ),
        make_row(
            (
                f"Prompt: {prompt}\n"
                f"Bad draft: {bad_prefix}\n"
                f"Recovery instruction: ignore the bad draft and continue with the correct answer.\n"
                f"Correct answer:"
            ),
            response,
            f"{mode}_explicit_recovery_instruction",
            "exposure_bias_explicit_recovery",
            mode,
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=52)
    args = parser.parse_args()

    enc = tiktoken.get_encoding("gpt2")
    rows = []
    index = 0
    for mode, pairs in PAIRS.items():
        for prompt, response in pairs:
            rows.extend(rows_for_pair(enc, mode, prompt, response, index))
            index += 1

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
