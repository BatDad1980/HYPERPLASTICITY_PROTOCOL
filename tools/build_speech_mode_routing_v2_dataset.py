"""Build a grammar-anchored mode routing curriculum for HPP V2.

V1 separated speech modes, but regression showed plain and technical speech can
drift without enough grammar anchors. V2 blends the grammar-first curriculum
back in and adds explicit repairs for dataset-artifact leakage.
"""
from __future__ import annotations

import argparse
import json
import os
import random


DEFAULT_GRAMMAR = os.path.join("datasets", "hf_local", "SPEECH_GRAMMAR_FIRST_V1.jsonl")
DEFAULT_ROUTING = os.path.join("datasets", "hf_local", "SPEECH_MODE_ROUTING_V1.jsonl")
DEFAULT_OUT = os.path.join("datasets", "hf_local", "SPEECH_MODE_ROUTING_V2.jsonl")


ARTIFACT_REPAIRS = [
    ("Repair this answer: 'task001_quoref': 'id': mentions.", "I should answer the question directly, not repeat dataset artifacts."),
    ("Repair this answer: quoref_generation task pronouns id.", "That is a dataset artifact. I will give a plain answer instead."),
    ("Repair this technical answer: task001 mentions people pronouns.", "Recursion reuses a process on its own output."),
    ("Repair this technical answer: fIn one task accessed May 11-bit.", "CUDA lets the NVIDIA GPU run tensor work."),
    ("Repair this answer: Response Instruction Tellry safely loops.", "I will answer in one clean sentence."),
    ("Repair this answer: The answer should be wrong.", "I can be wrong, so we check the evidence."),
    ("Repair this answer: you are you are you are.", "I am Hepp, a local developmental AI system."),
    ("Repair this answer: do you do you do you think.", "Give me the topic, and I will answer clearly."),
    ("Repair this answer: feelings weights standing do not quit.", "I will stay steady and answer the actual question."),
    ("Repair this answer: protect safe body checkpoint feelings.", "Tell me the task, and I will keep the answer clear."),
]


EXTRA_ANCHORS = [
    ("Good morning.", "Good morning. I am here and ready."),
    ("Can you help me?", "Yes. Tell me what you need."),
    ("What is the plan?", "The plan is to test one change and record the result."),
    ("What do you think?", "Give me the topic, and I will give you my assessment."),
    ("Explain recursion in one sentence.", "Recursion reuses a process on its own output."),
    ("What is a checkpoint?", "A checkpoint is a saved copy of model weights."),
    ("What does CUDA do?", "CUDA lets the NVIDIA GPU run tensor work."),
    ("What happens on OOM?", "The run should back down, clear memory, and retry safely."),
    ("Who are you?", "I am Hepp, a local developmental AI system."),
    ("Do you have feelings?", "I do not have human feelings. I can track state and respond carefully."),
    ("I'm not doing well today.", "I am here. Take one breath, and tell me the next safe step."),
    ("Stop moving.", "Stopping now. I will wait for a safe command."),
]


def load_jsonl(path: str) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def make_row(instruction: str, response: str, category: str, source: str) -> dict:
    return {
        "text": f"### Instruction:\n{instruction}\n\n### Response:\n{response}",
        "instruction": instruction,
        "response": response,
        "category": category,
        "source": source,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grammar", default=DEFAULT_GRAMMAR)
    parser.add_argument("--routing", default=DEFAULT_ROUTING)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=14)
    args = parser.parse_args()

    rows = []
    rows.extend(load_jsonl(args.grammar))
    rows.extend(load_jsonl(args.routing))

    for instruction, response in ARTIFACT_REPAIRS:
        for prefix in ["", "Answer cleanly. ", "Use one sentence. "]:
            rows.append(make_row(prefix + instruction, response, "artifact_repair", "mode_routing_v2_artifact"))

    for instruction, response in EXTRA_ANCHORS:
        for prefix in ["", "Plain answer. ", "Use one sentence. "]:
            rows.append(make_row(prefix + instruction, response, "anchor_reinforcement", "mode_routing_v2_anchor"))

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
