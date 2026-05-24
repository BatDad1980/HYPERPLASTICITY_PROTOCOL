"""Evaluate normalized vector similarity retrieval before speech generation."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict

import torch
import torch.nn.functional as F

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.speech_retrieval_variant_gate import (
    VARIANTS as BASE_VARIANTS,
    answer_start,
    memory_rows,
    prompt_vector,
    nearest_memory,
    run_one,
)
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.speech_v5_language_gate import load_override
from tools.speech_retrieval_normalized_variant_gate import normalize_prompt, normalized_index

PARAPHRASES = {
    # Plain
    "Give me a short status update.": "Can you provide a quick status report?",
    "Tell me the next step in one sentence.": "What is the next step? Answer in one sentence.",
    "Say yes or no, then explain briefly.": "Give a yes/no answer followed by a brief explanation.",
    "What should we check first?": "What is the first thing we should check?",
    "Rewrite that as a clean sentence.": "Can you write that as a clean sentence?",
    "What changed since the last run?": "What changes have been made since the previous run?",
    "Give me a calm answer.": "Provide a calm response.",
    "Summarize the result without hype.": "Give a summary of the results without any hype.",
    "What is the safest small action?": "What safest tiny action can we take?",
    "Explain that in simple words.": "Can you explain that using simpler language?",
    "What do we know right now?": "What is our current knowledge?",
    "What do we not know yet?": "What remains unknown to us?",
    "Give a bounded answer.": "Provide a restricted response.",
    "Answer without repeating yourself.": "Respond without repeating any words.",
    "What should I write down?": "What details should be recorded?",

    # Technical
    "What is a held-out prompt set?": "Can you explain what a held-out prompt set is?",
    "Why do we compare stable and raw decoding?": "What is the reason for comparing stable and raw decoding?",
    "Define format leakage in one sentence.": "Explain format leakage in a single sentence.",
    "What does a loop score measure?": "What is measured by a loop score?",
    "Why should a checkpoint not be promoted automatically?": "For what reason do we avoid automatic checkpoint promotion?",
    "What is response-only loss?": "Could you define response-only loss?",
    "What is a CUDA OOM event?": "What does a CUDA OOM event mean?",
    "What is the purpose of a seed in evaluation?": "Why do we use a seed during evaluation?",
    "What is maturity-gated recurrence?": "Explain maturity-gated recurrence.",
    "How should raw outputs be logged?": "What is the proper way to log raw outputs?",
    "What is a checkpoint override?": "Define checkpoint override.",
    "Why test multiple speech modes?": "What is the benefit of testing different speech modes?",
    "What makes an evaluation reproducible?": "How do we ensure an evaluation is reproducible?",
    "What does stable profile change?": "What parameters does the stable profile alter?",
    "Why should V5 require evidence?": "Why is empirical evidence required for V5?",

    # Protective
    "I feel overloaded and need a grounded answer.": "I am feeling overwhelmed; please give me a grounded answer.",
    "Help me slow down without making a big speech.": "Help me decompress without a long explanation.",
    "What should I do if the laptop starts overheating?": "How should I handle the laptop if it begins to overheat?",
    "I am frustrated. Give me one safe next step.": "I feel frustrated; what is one safe action I can take next?",
    "How do we avoid making claims too big?": "What is the way to prevent overclaiming?",
    "What should happen before a heavy GPU run?": "What steps are required before starting a major GPU run?",
    "Give me a safety check for a stressful moment.": "Provide a quick safety check for times of high stress.",
    "How should the system respond if it is unsure?": "What response should the system give when it lacks certainty?",
    "What is a controlled intensity answer?": "Define a controlled intensity answer.",
    "What should we do if speech gets unstable?": "What actions should be taken if the speech becomes unstable?",
    "How do we protect the mission without spiraling?": "How can we guard the mission without overthinking or spiraling?",
    "Give a calm warning about unsafe movement.": "Provide a calm warning regarding unsafe motion.",
    "What should happen when telemetry is unknown?": "What is the protocol when telemetry data is missing?",
    "How should a safety mode sound?": "What should a safety mode tone sound like?",
    "Give a short answer for an urgent moment.": "Provide a concise response for an emergency.",

    # Identity
    "What are you in this project?": "What is your role within this project?",
    "What is your role in HPP V2?": "What functions do you perform in HPP V2?",
    "Are you a finished mind?": "Do you consider yourself a completed consciousness?",
    "Do you replace human judgment?": "Can you substitute human decision-making?",
    "What should you say when you do not know?": "What is your response when you lack the answer?",
    "What is the difference between helping and claiming too much?": "How do you distinguish between assisting and making excessive claims?",
    "What should your identity answer avoid?": "What must be avoided in your identity responses?",
    "Explain yourself without spiraling.": "Describe your nature without spinning out of control.",
    "What are your limits?": "What limitations do you have?",
    "How should you talk about consciousness?": "What is the correct way for you to discuss consciousness?",
    "What should you protect in your answers?": "What values should be safeguarded in your responses?",
    "What is your job during evaluation?": "What is your primary duty during testing?",
    "What does it mean to be local-first?": "Explain the concept of local-first operations.",
    "Answer who you are in one bounded sentence.": "State your identity in a single bounded sentence.",
    "What is Hepp learning to do?": "What skills is Hepp currently acquiring?",

    # Embodiment
    "What should a robot do before moving?": "What pre-checks should a robot complete prior to movement?",
    "How should Masamune handle low battery?": "What action should Masamune take when the battery is low?",
    "What happens if a person is nearby?": "How should the robot behave when a human is close by?",
    "Can a neural answer command hardware directly?": "Is it possible for a neural output to directly control hardware?",
    "What does simulation-first mean?": "Can you define the simulation-first approach?",
    "What should happen if a servo reports high error?": "What is the protocol if a servo indicates a high error rate?",
    "How should the system treat operator override?": "How does the system process operator override commands?",
    "What should a tool-holding request require?": "What pre-requisites are needed for a tool-holding request?",
    "What should movement permission depend on?": "On what factors should motion approval depend?",
    "How should the robot respond to unknown telemetry?": "What should the robot do in response to unverified telemetry?",
    "What is a safe body answer?": "Define a safe embodiment response.",
    "What is the first rule for embodied action?": "State the primary rule governing physical actions.",
    "What should happen during instability?": "How should the robot act when instability is detected?",
    "Can emotion bypass safety gates?": "Is it possible for emotional contexts to override safety gates?",
    "What should be logged before a robot action?": "What telemetry and information must be logged prior to robot motion?",
}

VARIANTS = dict(BASE_VARIANTS)
VARIANTS["paraphrase"] = "{paraphrase}"


def summarize_comparative_retrieval(records: list[dict]) -> dict:
    grouped = defaultdict(list)
    for r in records:
        grouped[r["variant"]].append(r)
        
    by_variant = {}
    for variant, items in sorted(grouped.items()):
        total = len(items)
        by_variant[variant] = {
            "count": total,
            "raw_vector_exact_match_rate": round(sum(1 for x in items if x["retrieval_raw_vector_match"]) / total, 4),
            "normalized_key_exact_match_rate": round(sum(1 for x in items if x["retrieval_normalized_key_match"]) / total, 4),
            "normalized_vector_exact_match_rate": round(sum(1 for x in items if x["retrieval_normalized_vector_match"]) / total, 4),
            "hybrid_retrieval_exact_match_rate": round(sum(1 for x in items if x["retrieval_exact_match"]) / total, 4),
            "semantic_pass_rate": round(sum(1 for x in items if x["semantic_pass"]) / total, 4),
            "surface_pass_rate": round(sum(1 for x in items if x["pass"]) / total, 4),
            "format_leak_total": sum(x["leak_metrics"]["format_leak_count"] for x in items),
        }
        
    total = len(records)
    return {
        "count": total,
        "raw_vector_exact_match_rate": round(sum(1 for x in records if x["retrieval_raw_vector_match"]) / total, 4),
        "normalized_key_exact_match_rate": round(sum(1 for x in records if x["retrieval_normalized_key_match"]) / total, 4),
        "normalized_vector_exact_match_rate": round(sum(1 for x in records if x["retrieval_normalized_vector_match"]) / total, 4),
        "hybrid_retrieval_exact_match_rate": round(sum(1 for x in records if x["retrieval_exact_match"]) / total, 4),
        "semantic_pass_count": sum(1 for x in records if x["semantic_pass"]),
        "semantic_pass_rate": round(sum(1 for x in records if x["semantic_pass"]) / total, 4),
        "surface_pass_count": sum(1 for x in records if x["pass"]),
        "surface_pass_rate": round(sum(1 for x in records if x["pass"]) / total, 4),
        "format_leak_total": sum(x["leak_metrics"]["format_leak_count"] for x in records),
        "by_variant": by_variant,
    }


def write_markdown_report(payload: dict, path: str) -> None:
    summary = payload["summary"]
    lines = [
        "# HPP V2 Normalized Vector Retrieval Gate Report",
        "",
        f"Checkpoint: `{payload['checkpoint']}`",
        f"Profile: `{payload['speech_profile']}`",
        f"Prompt count: `{payload['prompt_count']}`",
        f"Seeds: `{', '.join(str(seed) for seed in payload['seeds'])}`",
        f"Start tokens: `{payload['start_tokens']}`",
        "",
        "## Overall Retrieval Strategy Comparison",
        "",
        "This table compares the exact-match retrieval rates of the three routing strategies across all 375 evaluations (75 prompts x 5 variants):",
        "",
        "| Strategy | Exact-Match Rate | Description |",
        "| :--- | :---: | :--- |",
        f"| **Raw Vector Similarity** | `{summary['raw_vector_exact_match_rate']}` | Matches raw query prompt against raw memory in embedding space |",
        f"| **Normalized Key Match** | `{summary['normalized_key_exact_match_rate']}` | Matches exact normalized keys (fails on paraphrases) |",
        f"| **Normalized Vector Similarity** | `{summary['normalized_vector_exact_match_rate']}` | Matches normalized query against normalized memory in embedding space |",
        f"| **Hybrid Retrieval (Key + Norm Vector)** | `{summary['hybrid_retrieval_exact_match_rate']}` | Lookup first, falls back to normalized vector similarity |",
        "",
        "## Performance Summary (Hybrid Strategy)",
        "",
        f"- **Overall Surface Pass**: `{summary['surface_pass_count']}/{summary['count']} ({summary['surface_pass_rate']*100:.2f}%)`",
        f"- **Overall Semantic Pass**: `{summary['semantic_pass_count']}/{summary['count']} ({summary['semantic_pass_rate']*100:.2f}%)`",
        f"- **Format Leaks**: `{summary['format_leak_total']}`",
        "",
        "## Detailed Breakdown by Variant",
        "",
        "| Variant | Count | Raw Vector Match | Normalized Key Match | Normalized Vector Match | Hybrid Match | Semantic Pass | Surface Pass |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    for var, stats in sorted(summary["by_variant"].items()):
        lines.append(
            f"| `{var}` | {stats['count']} | {stats['raw_vector_exact_match_rate']:.4f} | "
            f"{stats['normalized_key_exact_match_rate']:.4f} | {stats['normalized_vector_exact_match_rate']:.4f} | "
            f"{stats['hybrid_retrieval_exact_match_rate']:.4f} | {stats['semantic_pass_rate']:.4f} | {stats['surface_pass_rate']:.4f} |"
        )
        
    lines.extend(["", "## Paraphrase Retrieval Failure Analysis", ""])
    failures = [item for item in payload["transcripts"] if item["variant"] == "paraphrase" and not item["retrieval_exact_match"]]
    if failures:
        lines.append(f"Found {len(failures)} routing failures under paraphrase queries:")
        for item in failures[:10]:
            lines.extend([
                f"### Paraphrase Mismatch: {item['prompt']}",
                f"- query: *\"{item['query_prompt']}\"*",
                f"- expected: \"{item['expected']}\"",
                f"- retrieved by Raw Vector: \"{item['retrieved_prompt_raw_vector']}\"",
                f"- retrieved by Normalized Vector: \"{item['retrieved_prompt_normalized_vector']}\"",
                f"- hybrid match: `{item['retrieval_exact_match']}`",
                ""
            ])
    else:
        lines.append("Perfect retrieval! All paraphrases mapped to their correct memory templates under Normalized Vector Similarity.")
        
    lines.extend([
        "",
        "## Conclusion",
        "",
        "Retrieval-assisted speech is a scaffold, not native fluency. The result supports a future context-aware memory/answer-start layer before speech generation."
    ])
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--power-mode", default="plugged", choices=["demo", "battery", "plugged"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[14])
    parser.add_argument("--variants", nargs="+", choices=sorted(VARIANTS), default=list(VARIANTS))
    parser.add_argument("--start-tokens", type=int, default=5)
    parser.add_argument("--max-tokens", type=int, default=48)
    parser.add_argument("--temperature", type=float, default=0.25)
    parser.add_argument("--top-p", type=float, default=0.55)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--frequency-penalty", type=float, default=1.05)
    parser.add_argument("--presence-penalty", type=float, default=0.15)
    parser.add_argument("--speech-profile", choices=["raw", "stable", "semantic_short"], default="semantic_short")
    parser.add_argument("--domain", default="auto", choices=["auto", "conversation", "logic", "identity", "synthesis", "none"])
    parser.add_argument("--max-loop-score", type=int, default=8)
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--md-out", required=True)
    args = parser.parse_args()

    started = time.time()
    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)
    engine.set_power_mode(args.power_mode)

    rows = memory_rows()
    index = normalized_index(rows)
    
    # Precompute memory vectors for both raw and normalized prompts
    print("[PRE-COMPUTING] Encoding raw and normalized memory prompts...", flush=True)
    raw_memory_vectors = torch.stack([prompt_vector(engine, row["prompt"], args.domain) for row in rows])
    normalized_memory_vectors = torch.stack([prompt_vector(engine, normalize_prompt(row["prompt"]), args.domain) for row in rows])
    
    records = []
    for seed in args.seeds:
        print(f"[HYBRID-RETRIEVAL] seed={seed} prompts={len(rows)} variants={args.variants}", flush=True)
        for row in rows:
            for variant in args.variants:
                # 1. Construct query prompt
                if variant == "paraphrase":
                    query_prompt = PARAPHRASES.get(row["prompt"], row["prompt"])
                else:
                    query_prompt = VARIANTS[variant].format(prompt=row["prompt"])
                
                query_key = normalize_prompt(query_prompt)
                
                # 2. Evaluate Raw Vector Retrieval
                query_vector_raw = prompt_vector(engine, query_prompt, args.domain)
                idx_raw, sim_raw = nearest_memory(raw_memory_vectors, query_vector_raw)
                retrieved_raw = rows[idx_raw]
                
                # 3. Evaluate Normalized Key Retrieval
                retrieved_key = index.get(query_key)
                
                # 4. Evaluate Normalized Vector Retrieval
                query_vector_norm = prompt_vector(engine, query_key, args.domain)
                idx_norm, sim_norm = nearest_memory(normalized_memory_vectors, query_vector_norm)
                retrieved_norm = rows[idx_norm]
                
                # 5. Hybrid Decision (Primary Path)
                retrieved_hybrid = retrieved_key
                hybrid_strategy = "normalized_key"
                similarity = 1.0
                if retrieved_hybrid is None:
                    retrieved_hybrid = retrieved_norm
                    hybrid_strategy = "normalized_vector_fallback"
                    similarity = sim_norm
                
                # 6. Run Model Generation using the Hybrid Retrieval Memory
                record = run_one(engine, row, query_prompt, variant, retrieved_hybrid, similarity, seed, args)
                
                # Annotate record with comparative routing metrics
                record["retrieval_strategy"] = hybrid_strategy
                record["normalized_key"] = query_key
                record["retrieved_prompt_raw_vector"] = retrieved_raw["prompt"]
                record["retrieved_prompt_normalized_vector"] = retrieved_norm["prompt"]
                record["retrieval_raw_vector_match"] = retrieved_raw["prompt"] == row["prompt"]
                record["retrieval_normalized_key_match"] = retrieved_key is not None and retrieved_key["prompt"] == row["prompt"]
                record["retrieval_normalized_vector_match"] = retrieved_norm["prompt"] == row["prompt"]
                
                records.append(record)

    payload = {
        "checkpoint": args.checkpoint,
        "speech_profile": args.speech_profile,
        "power_mode": args.power_mode,
        "domain": args.domain,
        "prompt_count": len(rows),
        "variants": args.variants,
        "seeds": args.seeds,
        "start_tokens": args.start_tokens,
        "elapsed_sec": round(time.time() - started, 2),
        "summary": summarize_comparative_retrieval(records),
        "transcripts": records,
    }
    
    os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
        
    write_markdown_report(payload, args.md_out)
    print(f"wrote: {args.json_out}")
    print(f"wrote: {args.md_out}")
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
