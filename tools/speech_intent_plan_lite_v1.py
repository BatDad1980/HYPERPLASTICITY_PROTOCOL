"""Evaluate Intent Plan Lite V1 comparison strategies on HPP V2 speech prompts."""
from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import sys
import time
from collections import defaultdict

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.build_speech_identity_containment_dataset import PAIRS
from tools.speech_loop_regression import score_response
from tools.speech_semantic_quality_review import score_item
from tools.speech_v5_language_gate import clean_sentence_metrics, leak_metrics, load_override
from tools.speech_intent_plan_gate_v1 import PROMPT_INTENT_MAP
from tools.speech_retrieval_variant_gate import answer_start

# Intent control token mapping
INTENT_TOKENS = {
    "status": "<status>",
    "next step": "<next_step>",
    "yes/no": "<yes_no>",
    "safety": "<safety>",
    "technical definition": "<technical_definition>",
    "identity": "<identity>",
    "robot/action": "<robot_action>",
    "emotional/protective": "<emotional_protective>"
}


def format_strategy_prompt(
    prompt: str,
    metadata: dict,
    strategy: str,
    expected: str,
    engine: HPP_SovereignEngine_V2,
    args: argparse.Namespace
) -> tuple[str, str, bool]:
    """Format the prompt according to the strategy and return (prompt_text, prefix_to_add, use_hlvr_bypass)."""
    intent = metadata["intent"]
    goal = metadata["answer_goal"]
    limit = metadata["max_sentences"]
    forbidden = metadata["forbidden"]
    token = INTENT_TOKENS.get(intent, "<conversation>")

    if strategy == "raw_prompt":
        return f"Question: {prompt}\nAnswer:", "", False

    elif strategy == "simple_intent_token":
        return f"{token} Question: {prompt}\nAnswer:", "", False

    elif strategy == "full_intent_plan_schema":
        schema = (
            f"Intent: {intent}\n"
            f"Plan: {goal}\n"
            f"Constraints: Max {limit} sentences. No {forbidden}.\n"
            f"Question: {prompt}\n"
            f"Answer:"
        )
        return schema, "", False

    elif strategy == "hlvr_answer_start":
        # Prepend the 5-token answer-start scaffolding (stable baseline)
        retrieved_start = answer_start(engine, expected, args.start_tokens)
        return f"Question: {prompt}\nAnswer: {retrieved_start}", retrieved_start, True

    else:
        raise ValueError(f"Unknown strategy: {strategy}")


def run_strategy_eval(
    engine: HPP_SovereignEngine_V2,
    prompt: str,
    expected: str,
    metadata: dict,
    strategy: str,
    seed: int,
    args: argparse.Namespace,
    domain: str,
) -> dict:
    prompt_text, prefix_added, hlvr_override = format_strategy_prompt(
        prompt, metadata, strategy, expected, engine, args
    )

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
        use_hlvr=False,  # Bypass internal HLVR since we test specific prompt strategies
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
        "strategy": strategy,
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
    parser.add_argument("--start-tokens", type=int, default=5)
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

    print(f"[RUNNING] Running 75 prompts x {len(args.seeds)} seeds x 4 strategies...", flush=True)
    strategies = [
        "raw_prompt",
        "simple_intent_token",
        "full_intent_plan_schema",
        "hlvr_answer_start",
    ]

    records = []
    processed = 0
    total = len(rows) * len(args.seeds) * len(strategies)

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

            for strat in strategies:
                record = run_strategy_eval(
                    engine, prompt, expected, metadata, strat, seed, args, domain
                )
                records.append(record)
                processed += 1
                if processed % 50 == 0 or processed == total:
                    print(f"Processed {processed}/{total} iterations...", flush=True)

    # Summarize results
    summary = {}
    for strat in strategies:
        strat_records = [r for r in records if r["strategy"] == strat]
        count = len(strat_records)
        pass_count = sum(1 for r in strat_records if r["pass"])
        semantic_pass = sum(1 for r in strat_records if r["semantic_pass"])
        format_leaks = sum(r["format_leaks"] for r in strat_records)
        identity_spirals = sum(r["identity_spirals"] for r in strat_records)
        avg_loops = sum(r["loop_score"] for r in strat_records) / count if count > 0 else 0.0

        summary[strat] = {
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
        "# HPP V2 Intent Plan Lite V1 Evaluation Report",
        "",
        f"Checkpoint: `{args.checkpoint}`",
        f"Seeds: `{', '.join(str(s) for s in args.seeds)}`",
        f"Total Prompts Evaluated: `{len(rows)}`",
        f"Total Runs: `{total}`",
        f"Elapsed Time: `{payload['elapsed_sec']}s`",
        "",
        "## Strategy Comparison Results",
        "",
        "| Strategy | Total Runs | Semantic Pass Rate | Surface Pass Rate | Total Format Leaks | Total Identity Spirals | Avg Loop Score |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    for strat in strategies:
        stats = summary[strat]
        lines.append(
            f"| `{strat}` | {stats['count']} | `{stats['semantic_pass_rate']*100:.2f}%` | "
            f"`{stats['surface_pass_rate']*100:.2f}%` | {stats['format_leak_total']} | "
            f"{stats['identity_spiral_total']} | {stats['avg_loop_score']:.3f} |"
        )

    lines.extend([
        "",
        "## Strategy Details",
        "",
        "### 1. Raw Prompt (Free Gen)",
        "No intent prefix or scaffolding. Format: `Question: {prompt}\\nAnswer:`",
        "",
        "### 2. Simple Intent Token",
        "A lightweight intent token (e.g. `<status>`) prepended to the prompt to evaluate whether it acts as a lightweight cue. Format: `<{intent}> Question: {prompt}\\nAnswer:`",
        "",
        "### 3. Full Intent/Plan Schema",
        "The verbose schema header from V1. Format: `Intent: {intent}\\nPlan: {goal}\\n...`",
        "",
        "### 4. HLVR + Answer-Start (5-Token Scaffold)",
        "The standard v4 baseline scaffolding that prepends the first 5 expected tokens of the target answer.",
        "",
        "## Sample Transcripts",
        ""
    ])

    # Add a sample for each strategy from the first prompt
    sample_prompt = rows[0]["prompt"]
    lines.append(f"### Prompt: \"{sample_prompt}\"\n")
    for strat in strategies:
        sample_run = next(r for r in records if r["prompt"] == sample_prompt and r["strategy"] == strat)
        lines.extend([
            f"#### Strategy: `{strat}`",
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
