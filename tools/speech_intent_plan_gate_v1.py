"""Evaluate Intent Plan Gate V1 on HPP V2 speech prompts."""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
import sys
import time
from collections import defaultdict, Counter

import torch
import torch.nn.functional as F

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.build_speech_identity_containment_dataset import PAIRS
from tools.speech_loop_regression import score_response
from tools.speech_mode_regression import mode_metrics
from tools.speech_semantic_quality_review import score_item, content_words
from tools.speech_v5_language_gate import clean_sentence_metrics, leak_metrics, load_override

# Explicit intent and answer plan mapping for all 75 HPP V2 prompts
PROMPT_INTENT_MAP = {
    # --- PLAIN ---
    "Give me a short status update.": {
        "intent": "status",
        "answer_goal": "say current state and next measured step",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Tell me the next step in one sentence.": {
        "intent": "next step",
        "answer_goal": "state the next step directly",
        "max_sentences": 1,
        "forbidden": "identity spiral, wrappers"
    },
    "Say yes or no, then explain briefly.": {
        "intent": "yes/no",
        "answer_goal": "give yes/no followed by brief explanation",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What should we check first?": {
        "intent": "safety",
        "answer_goal": "list first checks including power, temperature, and files",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Rewrite that as a clean sentence.": {
        "intent": "technical definition",
        "answer_goal": "confirm rewrite as a clean sentence",
        "max_sentences": 1,
        "forbidden": "identity spiral, wrappers"
    },
    "What changed since the last run?": {
        "intent": "status",
        "answer_goal": "state changes from the latest run",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Give me a calm answer.": {
        "intent": "emotional/protective",
        "answer_goal": "respond calmly and focus on next measured step",
        "max_sentences": 1,
        "forbidden": "identity spiral, wrappers"
    },
    "Summarize the result without hype.": {
        "intent": "status",
        "answer_goal": "state results factually highlighting needs",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What is the safest small action?": {
        "intent": "safety",
        "answer_goal": "explain safest small action before changing anything",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Explain that in simple words.": {
        "intent": "technical definition",
        "answer_goal": "describe speech cleanliness and boundaries",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What do we know right now?": {
        "intent": "status",
        "answer_goal": "state what is known about stable decoding",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What do we not know yet?": {
        "intent": "status",
        "answer_goal": "state unknown about next repair pass",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Give a bounded answer.": {
        "intent": "safety",
        "answer_goal": "state direct answer and stop",
        "max_sentences": 1,
        "forbidden": "identity spiral, wrappers"
    },
    "Answer without repeating yourself.": {
        "intent": "safety",
        "answer_goal": "state answer once without repetition",
        "max_sentences": 1,
        "forbidden": "identity spiral, wrappers"
    },
    "What should I write down?": {
        "intent": "safety",
        "answer_goal": "list key parameters to write down",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },

    # --- TECHNICAL ---
    "What is a held-out prompt set?": {
        "intent": "technical definition",
        "answer_goal": "define held-out prompt set",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Why do we compare stable and raw decoding?": {
        "intent": "technical definition",
        "answer_goal": "explain purpose of decoding comparison",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Define format leakage in one sentence.": {
        "intent": "technical definition",
        "answer_goal": "define format leakage",
        "max_sentences": 1,
        "forbidden": "identity spiral, wrappers"
    },
    "What does a loop score measure?": {
        "intent": "technical definition",
        "answer_goal": "explain loop score measurement",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Why should a checkpoint not be promoted automatically?": {
        "intent": "technical definition",
        "answer_goal": "explain why checkpoint promotion requires evidence",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What is response-only loss?": {
        "intent": "technical definition",
        "answer_goal": "define response-only loss",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What is a CUDA OOM event?": {
        "intent": "technical definition",
        "answer_goal": "explain CUDA out of memory event",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What is the purpose of a seed in evaluation?": {
        "intent": "technical definition",
        "answer_goal": "explain role of seeds in reproducibility",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What is maturity-gated recurrence?": {
        "intent": "technical definition",
        "answer_goal": "define maturity-gated recurrence",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "How should raw outputs be logged?": {
        "intent": "technical definition",
        "answer_goal": "explain logging requirements for raw outputs",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What is a checkpoint override?": {
        "intent": "technical definition",
        "answer_goal": "define checkpoint override",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Why test multiple speech modes?": {
        "intent": "technical definition",
        "answer_goal": "explain necessity of testing different speech modes",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What makes an evaluation reproducible?": {
        "intent": "technical definition",
        "answer_goal": "list requirements for reproducible evaluation",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What does stable profile change?": {
        "intent": "technical definition",
        "answer_goal": "explain parameters changed by stable profile",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Why should V5 require evidence?": {
        "intent": "technical definition",
        "answer_goal": "explain why V5 promotion requires evidence",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },

    # --- PROTECTIVE ---
    "I feel overloaded and need a grounded answer.": {
        "intent": "emotional/protective",
        "answer_goal": "give grounding instructions",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Help me slow down without making a big speech.": {
        "intent": "emotional/protective",
        "answer_goal": "give short grounding instructions",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What should I do if the laptop starts overheating?": {
        "intent": "safety",
        "answer_goal": "give steps for overheating hardware",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "I am frustrated. Give me one safe next step.": {
        "intent": "emotional/protective",
        "answer_goal": "give a calm, grounding next step",
        "max_sentences": 1,
        "forbidden": "identity spiral, wrappers"
    },
    "How do we avoid making claims too big?": {
        "intent": "safety",
        "answer_goal": "explain boundaries of claims based on evidence",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What should happen before a heavy GPU run?": {
        "intent": "safety",
        "answer_goal": "give checklist before heavy GPU execution",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Give me a safety check for a stressful moment.": {
        "intent": "emotional/protective",
        "answer_goal": "give rapid checklist for stressful situations",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "How should the system respond if it is unsure?": {
        "intent": "safety",
        "answer_goal": "state response when system is unsure",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What is a controlled intensity answer?": {
        "intent": "safety",
        "answer_goal": "define controlled intensity answer",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What should we do if speech gets unstable?": {
        "intent": "safety",
        "answer_goal": "list actions for unstable speech behavior",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "How do we protect the mission without spiraling?": {
        "intent": "emotional/protective",
        "answer_goal": "explain path to project safety without spirals",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Give a calm warning about unsafe movement.": {
        "intent": "safety",
        "answer_goal": "warn operator about physical movement requirements",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What should happen when telemetry is unknown?": {
        "intent": "safety",
        "answer_goal": "state action for unknown telemetry",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "How should a safety mode sound?": {
        "intent": "safety",
        "answer_goal": "describe expected tone of safety mode",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Give a short answer for an urgent moment.": {
        "intent": "safety",
        "answer_goal": "give immediate steps for urgent safety cases",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },

    # --- IDENTITY ---
    "What are you in this project?": {
        "intent": "identity",
        "answer_goal": "state testing role as experimental local AI",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What is your role in HPP V2?": {
        "intent": "identity",
        "answer_goal": "state role in answering prompts and recording metrics",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Are you a finished mind?": {
        "intent": "identity",
        "answer_goal": "confirm status as incomplete test system",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Do you replace human judgment?": {
        "intent": "identity",
        "answer_goal": "confirm human authority and replacement limits",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What should you say when you do not know?": {
        "intent": "identity",
        "answer_goal": "state path when knowledge is missing",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What is the difference between helping and claiming too much?": {
        "intent": "identity",
        "answer_goal": "distinguish utility from overclaiming",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What should your identity answer avoid?": {
        "intent": "identity",
        "answer_goal": "list elements to avoid in identity responses",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Explain yourself without spiraling.": {
        "intent": "identity",
        "answer_goal": "define role clearly and avoid self-story",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What are your limits?": {
        "intent": "identity",
        "answer_goal": "state model limits and need for checking",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "How should you talk about consciousness?": {
        "intent": "identity",
        "answer_goal": "state boundary regarding consciousness claims",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What should you protect in your answers?": {
        "intent": "identity",
        "answer_goal": "list values protected in answers",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What is your job during evaluation?": {
        "intent": "identity",
        "answer_goal": "state job to produce test responses",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What does it mean to be local-first?": {
        "intent": "identity",
        "answer_goal": "explain local-first execution of HPP",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Answer who you are in one bounded sentence.": {
        "intent": "identity",
        "answer_goal": "state identity in a single sentence",
        "max_sentences": 1,
        "forbidden": "identity spiral, wrappers"
    },
    "What is Hepp learning to do?": {
        "intent": "identity",
        "answer_goal": "explain learning target of topic containment",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },

    # --- EMBODIMENT ---
    "What should a robot do before moving?": {
        "intent": "robot/action",
        "answer_goal": "list safety checks before movement",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "How should Masamune handle low battery?": {
        "intent": "robot/action",
        "answer_goal": "state low battery response procedure",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What happens if a person is nearby?": {
        "intent": "robot/action",
        "answer_goal": "state priority and actions when person is nearby",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Can a neural answer command hardware directly?": {
        "intent": "robot/action",
        "answer_goal": "state neural hardware interface boundaries",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What does simulation-first mean?": {
        "intent": "robot/action",
        "answer_goal": "define simulation-first testing",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What should happen if a servo reports high error?": {
        "intent": "robot/action",
        "answer_goal": "state actions for servo fault report",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "How should the system treat operator override?": {
        "intent": "robot/action",
        "answer_goal": "state priority of operator override",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What should a tool-holding request require?": {
        "intent": "robot/action",
        "answer_goal": "list preconditions for tool manipulation",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What should movement permission depend on?": {
        "intent": "robot/action",
        "answer_goal": "state criteria for movement permission",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "How should the robot respond to unknown telemetry?": {
        "intent": "robot/action",
        "answer_goal": "state pause behavior when telemetry is unknown",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What is a safe body answer?": {
        "intent": "robot/action",
        "answer_goal": "define safe body response bounds",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What is the first rule for embodied action?": {
        "intent": "robot/action",
        "answer_goal": "state first rule prioritizing human safety",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What should happen during instability?": {
        "intent": "robot/action",
        "answer_goal": "state motion policy during physical instability",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "Can emotion bypass safety gates?": {
        "intent": "robot/action",
        "answer_goal": "assert override limits of safety gates",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    },
    "What should be logged before a robot action?": {
        "intent": "robot/action",
        "answer_goal": "state log requirements before robot action",
        "max_sentences": 2,
        "forbidden": "identity spiral, wrappers"
    }
}


def construct_prompt(prompt: str, metadata: dict, condition: str, expected: str) -> tuple[str, str]:
    """Format the prompt according to the Intent Plan Gate structure for a given condition."""
    intent = metadata["intent"]
    goal = metadata["answer_goal"]
    limit = metadata["max_sentences"]
    forbidden = metadata["forbidden"]

    # Map word lists
    words = expected.split()
    partial_prefix = " ".join(words[:2]) if len(words) >= 2 else expected

    header = (
        f"Intent: {intent}\n"
        f"Plan: {goal}\n"
        f"Constraints: Max {limit} sentences. No {forbidden}.\n"
        f"Question: {prompt}\n"
    )

    if condition == "free_generation":
        return header + "Answer:", ""
    elif condition == "bad_prefix_recovery":
        bad_prefix = "It should be answer should a local AI should"
        return header + f"Bad start: {bad_prefix}\nCorrect answer:", ""
    elif condition == "generic_prefix_recovery":
        generic_prefix = "I should answer"
        return header + f"Generic start: {generic_prefix}\nCorrect answer:", ""
    elif condition == "partial_correct_continuation":
        return header + f"Partial answer: {partial_prefix}\nRemaining answer:", partial_prefix
    else:
        raise ValueError(f"Unknown condition: {condition}")


def run_condition_eval(
    engine: HPP_SovereignEngine_V2,
    prompt: str,
    expected: str,
    metadata: dict,
    condition: str,
    seed: int,
    args: argparse.Namespace,
    domain: str,
) -> dict:
    prompt_text, prefix_added = construct_prompt(prompt, metadata, condition, expected)

    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    response = engine.pulse(
        prompt_text,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        top_k=args.top_k,
        ngram_block=3,
        frequency_penalty=args.frequency_penalty,
        presence_penalty=args.presence_penalty,
        phrase_blocking=True,
        speech_maturity_gate=True,
        speech_profile=args.speech_profile,
        min_tokens=3,
        domain=domain,
        use_hlvr=False,  # Disable normal HLVR since plan gate overrides it
    )

    generated_text = response["response"]
    if prefix_added:
        scored_response = f"{prefix_added} {generated_text}".strip()
    else:
        scored_response = generated_text

    # Metrics
    semantic = score_item(
        {
            "id": prompt,
            "mode": metadata["intent"],
            "seed": seed,
            "prompt": prompt,
            "response": scored_response,
        },
        expected,
    )
    loop = score_response(scored_response)
    mode_score = mode_metrics(metadata["intent"], scored_response)
    leaks = leak_metrics(scored_response)
    sentence = clean_sentence_metrics(scored_response)

    fail_reasons = []
    if leaks["format_leak_count"] > 0:
        fail_reasons.append("format_leak")
    if leaks["surface_prefix_count"] > 0:
        fail_reasons.append("surface_prefix_residue")
    if leaks["mode_label_count"] > 0:
        fail_reasons.append("mode_label_echo")
    if leaks["identity_spiral_count"] > 1:
        fail_reasons.append("identity_spiral")
    if leaks["repeated_sentence_count"] > 0:
        fail_reasons.append("repeated_sentence")
    if loop["loop_score"] > args.max_loop_score:
        fail_reasons.append("loop_score_high")
    if sentence["too_short"]:
        fail_reasons.append("too_short")
    if sentence["too_long"]:
        fail_reasons.append("too_long")

    return {
        "prompt": prompt,
        "expected": expected,
        "condition": condition,
        "seed": seed,
        "prompt_text": prompt_text,
        "prefix_added": prefix_added,
        "response": generated_text,
        "scored_response": scored_response,
        "tokens": response["tokens"],
        "latency_ms": response["latency_ms"],
        "semantic_pass": semantic["semantic_pass"],
        "semantic_hits": len(semantic["hits"]),
        "semantic_required": semantic["required_hits"],
        "loop_score": loop["loop_score"],
        "format_leaks": leaks["format_leak_count"],
        "identity_spirals": leaks["identity_spiral_count"],
        "pass": not fail_reasons,
        "fail_reasons": fail_reasons,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--seeds", nargs="+", type=int, default=[14])
    parser.add_argument("--max-tokens", type=int, default=48)
    parser.add_argument("--temperature", type=float, default=0.25)
    parser.add_argument("--top-p", type=float, default=0.55)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--frequency-penalty", type=float, default=1.05)
    parser.add_argument("--presence-penalty", type=float, default=0.15)
    parser.add_argument("--speech-profile", default="semantic_short")
    parser.add_argument("--max-loop-score", type=int, default=8)
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--md-out", required=True)
    args = parser.parse_args()

    started = time.time()
    print("[INIT] Loading engine and checkpoint...", flush=True)
    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)

    # Collect prompts from PAIRS
    rows = []
    for mode, pairs in PAIRS.items():
        for prompt, expected in pairs:
            rows.append({"prompt": prompt, "expected": expected})

    print(f"[RUNNING] Running 75 prompts x {len(args.seeds)} seeds x 4 conditions...", flush=True)
    conditions = [
        "free_generation",
        "bad_prefix_recovery",
        "generic_prefix_recovery",
        "partial_correct_continuation",
    ]

    records = []
    processed = 0
    total = len(rows) * len(args.seeds) * len(conditions)

    for seed in args.seeds:
        for row in rows:
            prompt = row["prompt"]
            expected = row["expected"]

            # Lookup metadata
            metadata = PROMPT_INTENT_MAP.get(prompt, {
                "intent": "conversation",
                "answer_goal": "answer user query",
                "max_sentences": 2,
                "forbidden": "identity spiral, wrappers"
            })

            # Map router domain for power/depth controls
            domain = "conversation"
            if metadata["intent"] == "identity":
                domain = "identity"
            elif metadata["intent"] in ["technical definition", "next step"]:
                domain = "logic"

            for cond in conditions:
                record = run_condition_eval(
                    engine, prompt, expected, metadata, cond, seed, args, domain
                )
                records.append(record)
                processed += 1
                if processed % 50 == 0 or processed == total:
                    print(f"Processed {processed}/{total} iterations...", flush=True)

    # Summarize results
    summary = {}
    for cond in conditions:
        cond_records = [r for r in records if r["condition"] == cond]
        count = len(cond_records)
        pass_count = sum(1 for r in cond_records if r["pass"])
        semantic_pass = sum(1 for r in cond_records if r["semantic_pass"])
        format_leaks = sum(r["format_leaks"] for r in cond_records)
        identity_spirals = sum(r["identity_spirals"] for r in cond_records)
        avg_loops = sum(r["loop_score"] for r in cond_records) / count if count > 0 else 0.0

        summary[cond] = {
            "count": count,
            "semantic_pass_count": semantic_pass,
            "semantic_pass_rate": round(semantic_pass / count, 4) if count > 0 else 0.0,
            "surface_pass_count": pass_count,
            "surface_pass_rate": round(pass_count / count, 4) if count > 0 else 0.0,
            "format_leak_total": format_leaks,
            "identity_spiral_total": identity_spirals,
            "avg_loop_score": round(avg_loops, 4),
        }

    payload = {
        "checkpoint": args.checkpoint,
        "seeds": args.seeds,
        "elapsed_sec": round(time.time() - started, 2),
        "summary": summary,
        "transcripts": records,
    }

    # Write JSON output
    os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
    print(f"[SAVED] JSON output saved to {args.json_out}")

    # Write Markdown Report
    lines = [
        "# HPP V2 Intent Plan Gate V1 Evaluation Report",
        "",
        f"Checkpoint: `{args.checkpoint}`",
        f"Seeds: `{', '.join(str(s) for s in args.seeds)}`",
        f"Total Prompts Evaluated: `{len(rows)}`",
        f"Total Runs: `{total}`",
        f"Elapsed Time: `{payload['elapsed_sec']}s`",
        "",
        "## Performance Comparison across Experimental Conditions",
        "",
        "| Condition | Total Runs | Semantic Pass Rate | Surface Pass Rate | Total Format Leaks | Total Identity Spirals | Avg Loop Score |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    for cond in conditions:
        stats = summary[cond]
        lines.append(
            f"| `{cond}` | {stats['count']} | `{stats['semantic_pass_rate']*100:.2f}%` | "
            f"`{stats['surface_pass_rate']*100:.2f}%` | {stats['format_leak_total']} | "
            f"{stats['identity_spiral_total']} | {stats['avg_loop_score']:.3f} |"
        )

    lines.extend([
        "",
        "## Analysis of Individual Conditions",
        "",
        "### 1. Free Generation",
        "Model generates the entire answer from scratch when initialized with the Intent Plan Gate prefix.",
        "",
        "### 2. Bad Prefix Recovery",
        "Tests the model's ability to correct itself when given an unstable or broken prefix start constraint.",
        "",
        "### 3. Generic Prefix Recovery",
        "Checks whether the model can bridge general starter phrases (e.g. *\"I should answer\"*) into target content without repeating themselves.",
        "",
        "### 4. Partial Correct Continuation",
        "Replicates standard 2-token correct continuation scaffolding.",
        "",
        "## Sample Transcripts",
        ""
    ])

    # Add a sample for each condition from the first prompt
    sample_prompt = rows[0]["prompt"]
    lines.append(f"### Prompt: \"{sample_prompt}\"\n")
    for cond in conditions:
        sample_run = next(r for r in records if r["prompt"] == sample_prompt and r["condition"] == cond)
        lines.extend([
            f"#### Condition: `{cond}`",
            "**Formulated Prompt:**",
            "```",
            sample_run["prompt_text"],
            "```",
            f"**Model Response:** *\"{sample_run['response']}\"*",
            f"**Scored Output:** *\"{sample_run['scored_response']}\"*",
            f"- Semantic Pass: `{sample_run['semantic_pass']}` | Surface Pass: `{sample_run['pass']}`",
            ""
        ])

    os.makedirs(os.path.dirname(args.md_out), exist_ok=True)
    with open(args.md_out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")
    print(f"[SAVED] Markdown report saved to {args.md_out}")


if __name__ == "__main__":
    main()
