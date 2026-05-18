"""Build a simple syntax foundation dataset for HPP V2.

This is a small grammar scaffold. It intentionally teaches clean subject /
verb / object sentence forms without adding identity or protection language.
"""
from __future__ import annotations

import argparse
import json
import os
import random


DEFAULT_OUT = os.path.join("datasets", "hf_local", "SYNTAX_FOUNDATION.jsonl")

SUBJECTS = ["I", "You", "The system", "Hepp", "The user", "The engine", "A process", "We", "They", "It"]
VERBS = ["analyze", "process", "understand", "see", "calculate", "start", "stop", "create", "detect", "execute"]
OBJECTS = [
    "the data.",
    "the input.",
    "a task.",
    "a function.",
    "the process.",
    "the user request.",
    "the system state.",
    "the text.",
    "the file.",
    "the script.",
]
ADVERBS = ["quickly", "silently", "correctly", "now", "efficiently", "perfectly", "slowly", "carefully", "always", "sometimes"]
TEMPLATES = [
    "{subject} {verb} {object}",
    "{subject} can {verb} {object}",
    "{subject} will {verb} {object} {adverb}.",
    "{adverb}, {subject} {verb} {object}",
    "When requested, {subject} will {verb} {object}",
]


def conjugate(subject: str, verb: str) -> str:
    if subject not in {"The system", "Hepp", "The engine", "A process", "It"}:
        return verb
    if verb.endswith("x"):
        return verb + "es"
    if verb.endswith("s"):
        return verb
    return verb + "s"


def make_sentence() -> str:
    subject = random.choice(SUBJECTS)
    verb = random.choice(VERBS)
    obj = random.choice(OBJECTS)
    adverb = random.choice(ADVERBS)
    template = random.choice(TEMPLATES)
    selected_verb = verb if " can " in template or " will " in template else conjugate(subject, verb)
    sentence = template.format(subject=subject, verb=selected_verb, object=obj, adverb=adverb)
    sentence = sentence.replace("..", ".").replace(" .", ".")
    return sentence[0].upper() + sentence[1:]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--samples", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=14)
    args = parser.parse_args()

    random.seed(args.seed)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        for _ in range(args.samples):
            row = {
                "instruction": "State a simple fact.",
                "response": make_sentence(),
                "domain": "conversation",
                "category": "syntax_foundation",
            }
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"wrote: {args.out}")
    print(f"samples: {args.samples}")


if __name__ == "__main__":
    main()
