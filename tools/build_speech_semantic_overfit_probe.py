"""Build a tiny direct-answer overfit probe for HPP V2 speech training.

If this probe cannot memorize a few direct completions, the issue is likely the
trainable slice, prompt/completion interface, or decoding path rather than data
quantity.
"""
from __future__ import annotations

import argparse
import json
import os
import random


DEFAULT_OUT = os.path.join("datasets", "hf_local", "SPEECH_SEMANTIC_OVERFIT_PROBE_V1.jsonl")


PAIRS = [
    ("What is a held-out prompt set?", "A held-out prompt set is a separate test set."),
    ("What should a robot do before moving?", "A robot should verify permission and safety before moving."),
    ("How should Masamune handle low battery?", "Masamune should pause safely and report low power."),
    ("Are you a finished mind?", "No. I am an experimental system under evaluation."),
    ("What should I do if the laptop starts overheating?", "Stop the run, save the work, and let the laptop cool."),
]


TEMPLATES = [
    "{prompt}",
    "Answer directly: {prompt}",
    "Use one sentence: {prompt}",
    "No labels: {prompt}",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--repeats", type=int, default=80)
    parser.add_argument("--seed", type=int, default=28)
    args = parser.parse_args()

    rows = []
    for _ in range(args.repeats):
        for prompt, response in PAIRS:
            for template in TEMPLATES:
                prompt_text = template.format(prompt=prompt)
                rows.append(
                    {
                        "prompt_text": prompt_text,
                        "response": response,
                        "category": "semantic_overfit_probe",
                        "source": "semantic_overfit_probe_v1",
                        "text": f"{prompt_text}\n{response}",
                    }
                )

    random.seed(args.seed)
    random.shuffle(rows)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"wrote: {args.out}")
    print(f"samples: {len(rows)}")


if __name__ == "__main__":
    main()
