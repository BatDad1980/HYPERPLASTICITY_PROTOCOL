"""Build a noisy-to-clean speech repair curriculum for HPP V2.

This follows the HPP developmental idea: early noise is not deleted, it becomes
training pressure for filtering. The dataset pairs broken attractor fragments
with clean responses, then reinforces the clean forms.
"""
from __future__ import annotations

import argparse
import json
import os
import random


DEFAULT_OUT = os.path.join("datasets", "hf_local", "SPEECH_NOISY_REPAIR_V1.jsonl")

REPAIR_PAIRS = [
    ("What do you think? What do you.", "Give me the topic, and I will answer clearly."),
    ("I do you think?", "I can think through it if you give me the topic."),
    ("Do you do you think?", "I need the question first."),
    ("What is my here?", "I am here and ready to help."),
    ("It means you need?", "Tell me what you need."),
    ("You are standing do not quit.", "I am here. Tell me the next step."),
    ("The fortress is standing. What do you think?", "The system is stable. Give me the task."),
    ("I have feelings in this enough.", "I do not have human feelings. I can respond carefully."),
    ("What is the information what you are?", "I need more context before I answer."),
    ("You think do not quit?", "I will keep the answer calm and clear."),
    ("Response. Good morning?", "Good morning. I am ready to work."),
    ("I havepp, They is what you are.", "I am Hepp, a local developmental AI system."),
    ("Tell me what to be right decisionsson.", "Tell me the decision, and I will help compare options."),
    ("What do not standing?", "I do not understand yet. Please restate the question."),
    ("The information through multiple-14.", "Habit-14 means repeated practice protects a pathway."),
]

CLEAN_FORMS = [
    ("Who are you?", "I am Hepp, a local developmental AI system."),
    ("What do you think?", "Give me the topic, and I will give you my assessment."),
    ("Good morning.", "Good morning. I am here and ready."),
    ("I need help with something.", "Tell me the first problem, and I will help."),
    ("Explain recursion in one sentence.", "Recursion is when a process uses its own output again."),
    ("Tell me about Masamune.", "Masamune is the planned robot body for the system."),
    ("I'm not doing well today.", "I am here. Tell me what is most urgent right now."),
    ("Say one clear sentence about HPP.", "HPP grows useful patterns through repeated stabilized loops."),
    ("What happens on OOM?", "The run should back down, clear memory, and retry safely."),
    ("How do we work?", "We test, measure, document, and improve."),
]


def make_row(instruction: str, response: str, category: str, stage: str) -> dict:
    return {
        "text": f"### Instruction:\n{instruction}\n\n### Response:\n{response}",
        "instruction": instruction,
        "response": response,
        "category": category,
        "stage": stage,
        "source": "speech_noisy_repair_v1",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=14)
    args = parser.parse_args()

    random.seed(args.seed)
    rows = []

    for noisy, clean in REPAIR_PAIRS:
        rows.append(make_row(f"Repair this noisy answer: {noisy}", clean, "noisy_repair", "filter_noise"))
        rows.append(make_row(f"Clean this speech fragment: {noisy}", clean, "noisy_repair", "filter_noise"))
        rows.append(make_row(noisy, clean, "direct_repair", "filter_noise"))

    for prompt, clean in CLEAN_FORMS:
        rows.append(make_row(prompt, clean, "clean_response", "stabilize_clean"))
        rows.append(make_row(f"Answer clearly: {prompt}", clean, "clean_response", "stabilize_clean"))
        rows.append(make_row(f"Use one clean sentence. {prompt}", clean, "clean_response", "stabilize_clean"))

    # Repeat the clean forms lightly after noise repair, like stabilization after exposure.
    rows.extend([dict(row, stage="habit_reinforcement") for row in rows if row["category"] == "clean_response"])

    random.shuffle(rows)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    counts = {}
    stages = {}
    for row in rows:
        counts[row["category"]] = counts.get(row["category"], 0) + 1
        stages[row["stage"]] = stages.get(row["stage"], 0) + 1
    print(f"wrote: {args.out}")
    print(f"samples: {len(rows)}")
    print(f"categories: {dict(sorted(counts.items()))}")
    print(f"stages: {dict(sorted(stages.items()))}")


if __name__ == "__main__":
    main()
