"""Evaluate Continuation Quality Gate V1 on HPP V2 speech prompts."""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from collections import defaultdict

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from core.speech_controller_v1 import SpeechControllerV1
from tools.build_speech_identity_containment_dataset import PAIRS
from tools.speech_retrieval_hybrid_lexical_vector_gate import VARIANTS, PARAPHRASES
from tools.speech_semantic_quality_review import score_item, content_words


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--seeds", nargs="+", type=int, default=[14])
    parser.add_argument("--json-out", default="reports/speech_continuation_quality_gate_v1_2026-05-25.json")
    parser.add_argument("--md-out", default="reports/SPEECH_CONTINUATION_QUALITY_GATE_V1_2026-05-25.md")
    args = parser.parse_args()

    started = time.time()
    print("[INIT] Loading Speech Controller V1 and Engine for Continuation Gate...", flush=True)
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

    # Expand prompts using the 5 variants
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
                if strat == "hlvr_answer_start":
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

                # Extract retrieved start anchor and reconstruct continuation
                retrieved_start = record["answer_start"]
                full_response = record["final_text"]
                
                if retrieved_start:
                    if full_response.startswith(retrieved_start):
                        continuation = full_response[len(retrieved_start):].strip()
                    else:
                        continuation = full_response.replace(retrieved_start, "", 1).strip()
                else:
                    continuation = full_response

                # Calculate semantic quality stats
                # 1. Full Response
                res_full = score_item(
                    {"id": query_prompt, "mode": row["mode"], "seed": seed, "prompt": query_prompt, "response": full_response},
                    row["expected"]
                )
                hits_full = res_full["hits"]
                full_semantic_pass = res_full["semantic_pass"]

                # 2. Continuation Only
                res_continuation = score_item(
                    {"id": query_prompt, "mode": row["mode"], "seed": seed, "prompt": query_prompt, "response": continuation},
                    row["expected"]
                )
                hits_continuation = res_continuation["hits"]
                continuation_semantic_pass = res_continuation["semantic_pass"]
                
                # Partial semantic pass: at least 1 keyword hit in the continuation
                continuation_partial_semantic_pass = len(hits_continuation) >= 1

                # 3. Anchor Only
                res_anchor = score_item(
                    {"id": query_prompt, "mode": row["mode"], "seed": seed, "prompt": query_prompt, "response": retrieved_start},
                    row["expected"]
                )
                hits_anchor = res_anchor["hits"]

                # 4. Continuation adds useful new semantic content
                new_hits = set(hits_continuation) - set(hits_anchor)
                adds_useful_content = len(new_hits) > 0

                # Form new record
                result_record = {
                    "variant": var,
                    "strategy": strat,
                    "seed": seed,
                    "prompt": query_prompt,
                    "expected": row["expected"],
                    "retrieved_start": retrieved_start,
                    "continuation": continuation,
                    "full_response": full_response,
                    "hits_continuation": hits_continuation,
                    "hits_full": hits_full,
                    "full_semantic_pass": full_semantic_pass,
                    "continuation_semantic_pass": continuation_semantic_pass,
                    "continuation_partial_semantic_pass": continuation_partial_semantic_pass,
                    "adds_useful_content": adds_useful_content,
                    "surface_pass": record["surface_pass"],
                    "loop_score": record["loop_score"],
                    "format_leaks": record["format_leaks"],
                }
                
                records.append(result_record)
                processed += 1
                if processed % 100 == 0 or processed == total:
                    print(f"Processed {processed}/{total} iterations...", flush=True)

    # Summarize results
    summary = {}
    for strat in strategies:
        strat_records = [r for r in records if r["strategy"] == strat]
        
        # Paraphrase lane
        para_records = [r for r in strat_records if r["variant"] == "paraphrase"]
        para_count = len(para_records)
        para_full_sem = sum(1 for r in para_records if r["full_semantic_pass"])
        para_cont_sem = sum(1 for r in para_records if r["continuation_semantic_pass"])
        para_cont_part_sem = sum(1 for r in para_records if r["continuation_partial_semantic_pass"])
        para_adds_useful = sum(1 for r in para_records if r["adds_useful_content"])
        para_surface = sum(1 for r in para_records if r["surface_pass"])
        para_leaks = sum(r["format_leaks"] for r in para_records)
        para_loops = sum(r["loop_score"] for r in para_records) / para_count if para_count > 0 else 0.0

        # Standard lane
        std_records = [r for r in strat_records if r["variant"] != "paraphrase"]
        std_count = len(std_records)
        std_full_sem = sum(1 for r in std_records if r["full_semantic_pass"])
        std_cont_sem = sum(1 for r in std_records if r["continuation_semantic_pass"])
        std_cont_part_sem = sum(1 for r in std_records if r["continuation_partial_semantic_pass"])
        std_adds_useful = sum(1 for r in std_records if r["adds_useful_content"])
        std_surface = sum(1 for r in std_records if r["surface_pass"])
        std_leaks = sum(r["format_leaks"] for r in std_records)
        std_loops = sum(r["loop_score"] for r in std_records) / std_count if std_count > 0 else 0.0

        # Overall
        all_count = len(strat_records)
        all_full_sem = sum(1 for r in strat_records if r["full_semantic_pass"])
        all_cont_sem = sum(1 for r in strat_records if r["continuation_semantic_pass"])
        all_cont_part_sem = sum(1 for r in strat_records if r["continuation_partial_semantic_pass"])
        all_adds_useful = sum(1 for r in strat_records if r["adds_useful_content"])
        all_surface = sum(1 for r in strat_records if r["surface_pass"])
        all_leaks = sum(r["format_leaks"] for r in strat_records)
        all_loops = sum(r["loop_score"] for r in strat_records) / all_count if all_count > 0 else 0.0

        summary[strat] = {
            "overall": {
                "count": all_count,
                "full_semantic_pass_rate": round(all_full_sem / all_count, 4) if all_count > 0 else 0.0,
                "continuation_semantic_pass_rate": round(all_cont_sem / all_count, 4) if all_count > 0 else 0.0,
                "continuation_partial_semantic_pass_rate": round(all_cont_part_sem / all_count, 4) if all_count > 0 else 0.0,
                "continuation_useful_addition_rate": round(all_adds_useful / all_count, 4) if all_count > 0 else 0.0,
                "surface_pass_rate": round(all_surface / all_count, 4) if all_count > 0 else 0.0,
                "format_leaks": all_leaks,
                "avg_loop_score": round(all_loops, 4),
            },
            "paraphrase": {
                "count": para_count,
                "full_semantic_pass_rate": round(para_full_sem / para_count, 4) if para_count > 0 else 0.0,
                "continuation_semantic_pass_rate": round(para_cont_sem / para_count, 4) if para_count > 0 else 0.0,
                "continuation_partial_semantic_pass_rate": round(para_cont_part_sem / para_count, 4) if para_count > 0 else 0.0,
                "continuation_useful_addition_rate": round(para_adds_useful / para_count, 4) if para_count > 0 else 0.0,
                "surface_pass_rate": round(para_surface / para_count, 4) if para_count > 0 else 0.0,
                "format_leaks": para_leaks,
                "avg_loop_score": round(para_loops, 4),
            },
            "standard": {
                "count": std_count,
                "full_semantic_pass_rate": round(std_full_sem / std_count, 4) if std_count > 0 else 0.0,
                "continuation_semantic_pass_rate": round(std_cont_sem / std_count, 4) if std_count > 0 else 0.0,
                "continuation_partial_semantic_pass_rate": round(std_cont_part_sem / std_count, 4) if std_count > 0 else 0.0,
                "continuation_useful_addition_rate": round(std_adds_useful / std_count, 4) if std_count > 0 else 0.0,
                "surface_pass_rate": round(std_surface / std_count, 4) if std_count > 0 else 0.0,
                "format_leaks": std_leaks,
                "avg_loop_score": round(std_loops, 4),
            }
        }

    # Evaluate blocker condition
    # Blocker if overall continuation-only semantic pass rate is low (e.g. < 40%)
    contr_overall_cont_pass = summary["speech_controller_v1"]["overall"]["continuation_semantic_pass_rate"]
    is_low = contr_overall_cont_pass < 0.40
    blocker_msg = ""
    if is_low:
        blocker_msg = "“Speech Controller V1 improves orchestration and surface quality, but continuation after the anchor remains the blocker.”"
        print(f"\n[WARNING] {blocker_msg}\n")

    payload = {
        "checkpoint": args.checkpoint,
        "seeds": args.seeds,
        "elapsed_sec": round(time.time() - started, 2),
        "summary": summary,
        "is_low": is_low,
        "blocker_message": blocker_msg,
        "transcripts": records,
    }

    # Save JSON report
    os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
    print(f"[SAVED] JSON report saved to {args.json_out}")

    # Save Markdown report
    lines = [
        "# HPP V2 Continuation Quality Gate V1 Evaluation Report",
        "",
        f"Checkpoint: `{args.checkpoint}`",
        f"Seeds: `{', '.join(str(s) for s in args.seeds)}`",
        f"Total Prompts Evaluated: `{len(expanded_queries)}` (75 core prompts x 5 variants)",
        f"Total Runs: `{total}`",
        f"Elapsed Time: `{payload['elapsed_sec']}s`",
        "",
    ]

    if is_low:
        lines.extend([
            "## Executive Alert",
            "",
            f"> [!WARNING]",
            f"> {blocker_msg}",
            "",
        ])

    lines.extend([
        "## Performance Comparison Summary (All Lanes)",
        "",
        "This table compares exact metrics across all prompt variants:",
        "",
        "| Strategy | Total Runs | Full Semantic Pass | Continuation Semantic Pass | Continuation Partial Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ])

    for strat in strategies:
        stats = summary[strat]["overall"]
        lines.append(
            f"| `{strat}` | {stats['count']} | `{stats['full_semantic_pass_rate']*100:.2f}%` | "
            f"`{stats['continuation_semantic_pass_rate']*100:.2f}%` | `{stats['continuation_partial_semantic_pass_rate']*100:.2f}%` | "
            f"`{stats['continuation_useful_addition_rate']*100:.2f}%` | `{stats['surface_pass_rate']*100:.2f}%` | "
            f"{stats['format_leaks']} | {stats['avg_loop_score']:.3f} |"
        )

    lines.extend([
        "",
        "## Standard Lane Comparison (Exact, Please Answer, Simple Terms, Bounded)",
        "",
        "| Strategy | Standard Runs | Full Semantic Pass | Continuation Semantic Pass | Continuation Partial Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ])

    for strat in strategies:
        stats = summary[strat]["standard"]
        lines.append(
            f"| `{strat}` | {stats['count']} | `{stats['full_semantic_pass_rate']*100:.2f}%` | "
            f"`{stats['continuation_semantic_pass_rate']*100:.2f}%` | `{stats['continuation_partial_semantic_pass_rate']*100:.2f}%` | "
            f"`{stats['continuation_useful_addition_rate']*100:.2f}%` | `{stats['surface_pass_rate']*100:.2f}%` | "
            f"{stats['format_leaks']} | {stats['avg_loop_score']:.3f} |"
        )

    lines.extend([
        "",
        "## Paraphrase Generalization Lane Comparison",
        "",
        "| Strategy | Paraphrase Runs | Full Semantic Pass | Continuation Semantic Pass | Continuation Partial Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ])

    for strat in strategies:
        stats = summary[strat]["paraphrase"]
        lines.append(
            f"| `{strat}` | {stats['count']} | `{stats['full_semantic_pass_rate']*100:.2f}%` | "
            f"`{stats['continuation_semantic_pass_rate']*100:.2f}%` | `{stats['continuation_partial_semantic_pass_rate']*100:.2f}%` | "
            f"`{stats['continuation_useful_addition_rate']*100:.2f}%` | `{stats['surface_pass_rate']*100:.2f}%` | "
            f"{stats['format_leaks']} | {stats['avg_loop_score']:.3f} |"
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
            f"**Answer-Start Anchor:** *\"{sample_run['retrieved_start']}\"*",
            f"**Generated Continuation:** *\"{sample_run['continuation']}\"*",
            f"**Full Combined Response:** *\"{sample_run['full_response']}\"*",
            f"- Full Semantic Pass: `{sample_run['full_semantic_pass']}` | Continuation-Only Semantic Pass: `{sample_run['continuation_semantic_pass']}`",
            f"- Continuation Partial Pass: `{sample_run['continuation_partial_semantic_pass']}` | Continuation Useful Addition: `{sample_run['adds_useful_content']}`",
            f"- Surface Pass: `{sample_run['surface_pass']}`",
            ""
        ])

    os.makedirs(os.path.dirname(args.md_out), exist_ok=True)
    with open(args.md_out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")
    print(f"[SAVED] Markdown report saved to {args.md_out}")


if __name__ == "__main__":
    main()

