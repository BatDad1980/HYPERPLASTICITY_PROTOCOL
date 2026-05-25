"""Evaluate Speech Controller V1 comparison strategies on HPP V2 prompts."""
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
from core.speech_controller_v1 import SpeechControllerV1
from tools.build_speech_identity_containment_dataset import PAIRS
from tools.speech_retrieval_hybrid_lexical_vector_gate import VARIANTS, PARAPHRASES
from tools.speech_intent_plan_gate_v1 import PROMPT_INTENT_MAP


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--seeds", nargs="+", type=int, default=[14])
    parser.add_argument("--json-out", default="reports/speech_controller_v1_gate_2026-05-25.json")
    parser.add_argument("--md-out", default="reports/SPEECH_CONTROLLER_V1_GATE_2026-05-25.md")
    args = parser.parse_args()

    started = time.time()
    print("[INIT] Loading Speech Controller V1 and Engine...", flush=True)
    engine = HPP_SovereignEngine_V2(max_context=512)
    # Load checkpoint override safely
    checkpoint = torch.load(args.checkpoint, map_location=engine.device, weights_only=True)
    engine.university.load_state_dict(checkpoint.get("masamune_state_dict", {}), strict=False)
    if "lm_head_state_dict" in checkpoint:
        engine.lm_head.load_state_dict(checkpoint["lm_head_state_dict"])
    if "embedding_state_dict" in checkpoint:
        engine.embedding.load_state_dict(checkpoint["embedding_state_dict"])
    if engine.use_fp16:
        engine.university.half()
        engine.lm_head.half()
        engine.embedding.half()
    engine.eval_mode()

    controller = SpeechControllerV1(engine=engine)

    # Collect prompts from PAIRS
    rows = []
    for mode, pairs in PAIRS.items():
        for prompt, expected in pairs:
            rows.append({"mode": mode, "prompt": prompt, "expected": expected})

    # Expand prompts using the 5 variants (exact, please_answer, simple_terms, bounded, paraphrase)
    variants = ["exact", "please_answer", "simple_terms", "bounded", "paraphrase"]
    expanded_queries = []
    for row in rows:
        for var in variants:
            if var == "paraphrase":
                query_prompt = PARAPHRASES.get(row["prompt"], row["prompt"])
            else:
                query_prompt = VARIANTS[var].format(prompt=row["prompt"])
            expanded_queries.append({
                "row": row,
                "variant": var,
                "query_prompt": query_prompt,
            })

    strategies = [
        "raw_prompt",
        "intent_token_only",
        "hlvr_answer_start",
        "speech_controller_v1",
    ]

    print(f"[RUNNING] Evaluating {len(expanded_queries)} query variants x {len(args.seeds)} seeds x {len(strategies)} strategies...", flush=True)
    records = []
    processed = 0
    total = len(expanded_queries) * len(args.seeds) * len(strategies)

    for seed in args.seeds:
        for q in expanded_queries:
            row = q["row"]
            query_prompt = q["query_prompt"]
            var = q["variant"]

            for strat in strategies:
                if strat == "raw_prompt":
                    record = controller.process(
                        query_prompt,
                        expected_target=row["expected"],
                        seed=seed,
                        prepend_intent_token=False,
                        use_retrieval=False,
                    )
                elif strat == "intent_token_only":
                    record = controller.process(
                        query_prompt,
                        expected_target=row["expected"],
                        seed=seed,
                        prepend_intent_token=True,
                        use_retrieval=False,
                    )
                elif strat == "hlvr_answer_start":
                    record = controller.process(
                        query_prompt,
                        expected_target=row["expected"],
                        seed=seed,
                        prepend_intent_token=False,
                        use_retrieval=True,
                    )
                elif strat == "speech_controller_v1":
                    record = controller.process(
                        query_prompt,
                        expected_target=row["expected"],
                        seed=seed,
                        prepend_intent_token=True,
                        use_retrieval=True,
                    )

                # Add variant metadata
                record["variant"] = var
                record["strategy"] = strat
                record["seed"] = seed
                records.append(record)

                processed += 1
                if processed % 100 == 0 or processed == total:
                    print(f"Processed {processed}/{total} iterations...", flush=True)

    # Summarize results separately for paraphrase vs other lanes
    summary = {}
    for strat in strategies:
        strat_records = [r for r in records if r["strategy"] == strat]
        
        # Paraphrase lane
        para_records = [r for r in strat_records if r["variant"] == "paraphrase"]
        para_count = len(para_records)
        para_semantic = sum(1 for r in para_records if r["semantic_pass"])
        para_surface = sum(1 for r in para_records if r["surface_pass"])
        para_leaks = sum(r["format_leaks"] for r in para_records)
        para_loops = sum(r["loop_score"] for r in para_records) / para_count if para_count > 0 else 0.0

        # Standard lane (non-paraphrase)
        std_records = [r for r in strat_records if r["variant"] != "paraphrase"]
        std_count = len(std_records)
        std_semantic = sum(1 for r in std_records if r["semantic_pass"])
        std_surface = sum(1 for r in std_records if r["surface_pass"])
        std_leaks = sum(r["format_leaks"] for r in std_records)
        std_loops = sum(r["loop_score"] for r in std_records) / std_count if std_count > 0 else 0.0

        # Overall
        all_count = len(strat_records)
        all_semantic = sum(1 for r in strat_records if r["semantic_pass"])
        all_surface = sum(1 for r in strat_records if r["surface_pass"])
        all_leaks = sum(r["format_leaks"] for r in strat_records)
        all_loops = sum(r["loop_score"] for r in strat_records) / all_count if all_count > 0 else 0.0

        summary[strat] = {
            "overall": {
                "count": all_count,
                "semantic_pass_rate": round(all_semantic / all_count, 4) if all_count > 0 else 0.0,
                "surface_pass_rate": round(all_surface / all_count, 4) if all_count > 0 else 0.0,
                "format_leaks": all_leaks,
                "avg_loop_score": round(all_loops, 4),
            },
            "paraphrase": {
                "count": para_count,
                "semantic_pass_rate": round(para_semantic / para_count, 4) if para_count > 0 else 0.0,
                "surface_pass_rate": round(para_surface / para_count, 4) if para_count > 0 else 0.0,
                "format_leaks": para_leaks,
                "avg_loop_score": round(para_loops, 4),
            },
            "standard": {
                "count": std_count,
                "semantic_pass_rate": round(std_semantic / std_count, 4) if std_count > 0 else 0.0,
                "surface_pass_rate": round(std_surface / std_count, 4) if std_count > 0 else 0.0,
                "format_leaks": std_leaks,
                "avg_loop_score": round(std_loops, 4),
            }
        }

    payload = {
        "checkpoint": args.checkpoint,
        "seeds": args.seeds,
        "elapsed_sec": round(time.time() - started, 2),
        "summary": summary,
        "transcripts": records,
    }

    # Save JSON report
    os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
    print(f"[SAVED] JSON report saved to {args.json_out}")

    # Save Markdown report
    lines = [
        "# HPP V2 Speech Controller V1 Validation Gate Report",
        "",
        f"Checkpoint: `{args.checkpoint}`",
        f"Seeds: `{', '.join(str(s) for s in args.seeds)}`",
        f"Total Prompts Evaluated: `{len(expanded_queries)}` (75 core prompts x 5 variants)",
        f"Total Runs: `{total}`",
        f"Elapsed Time: `{payload['elapsed_sec']}s`",
        "",
        "## Performance Comparison Summary (All Lanes)",
        "",
        "This table compares exact metrics across all prompt variants:",
        "",
        "| Strategy | Total Runs | Semantic Pass Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |",
    ]

    for strat in strategies:
        stats = summary[strat]["overall"]
        lines.append(
            f"| `{strat}` | {stats['count']} | `{stats['semantic_pass_rate']*100:.2f}%` | "
            f"`{stats['surface_pass_rate']*100:.2f}%` | {stats['format_leaks']} | {stats['avg_loop_score']:.3f} |"
        )

    lines.extend([
        "",
        "## Standard Lane Comparison (Exact, Please Answer, Simple Terms, Bounded)",
        "",
        "| Strategy | Standard Runs | Semantic Pass Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |",
    ])

    for strat in strategies:
        stats = summary[strat]["standard"]
        lines.append(
            f"| `{strat}` | {stats['count']} | `{stats['semantic_pass_rate']*100:.2f}%` | "
            f"`{stats['surface_pass_rate']*100:.2f}%` | {stats['format_leaks']} | {stats['avg_loop_score']:.3f} |"
        )

    lines.extend([
        "",
        "## Paraphrase Generalization Lane Comparison",
        "",
        "| Strategy | Paraphrase Runs | Semantic Pass Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |",
    ])

    for strat in strategies:
        stats = summary[strat]["paraphrase"]
        lines.append(
            f"| `{strat}` | {stats['count']} | `{stats['semantic_pass_rate']*100:.2f}%` | "
            f"`{stats['surface_pass_rate']*100:.2f}%` | {stats['format_leaks']} | {stats['avg_loop_score']:.3f} |"
        )

    lines.extend([
        "",
        "## Sample Transcripts (First Prompt)",
        ""
    ])

    sample_prompt = expanded_queries[0]["query_prompt"]
    lines.append(f"### Prompt: \"{sample_prompt}\"\n")
    for strat in strategies:
        sample_run = next(r for r in records if r["prompt"] == sample_prompt and r["strategy"] == strat)
        lines.extend([
            f"#### Strategy: `{strat}`",
            f"**Generated Text:** *\"{sample_run['generated_text']}\"*",
            f"**Final Response:** *\"{sample_run['final_text']}\"*",
            f"- Semantic Pass: `{sample_run['semantic_pass']}` | Surface Pass: `{sample_run['surface_pass']}` | Boundary: `{sample_run['boundary']}`",
            ""
        ])

    os.makedirs(os.path.dirname(args.md_out), exist_ok=True)
    with open(args.md_out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")
    print(f"[SAVED] Markdown report saved to {args.md_out}")


if __name__ == "__main__":
    main()
