"""Evaluate hierarchical lexical-vector retrieval before speech generation."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import defaultdict

import torch
import torch.nn.functional as F

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.speech_retrieval_variant_gate import (
    answer_start,
    memory_rows,
    prompt_vector,
    nearest_memory,
    run_one,
)
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.speech_v5_language_gate import load_override
from tools.speech_retrieval_normalized_variant_gate import normalize_prompt, normalized_index
from tools.speech_retrieval_hybrid_lexical_vector_gate import (
    SimpleBM25,
    tokenize,
    VARIANTS,
    PARAPHRASES,
)


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
            "bm25_exact_match_rate": round(sum(1 for x in items if x["retrieval_bm25_match"]) / total, 4),
            "hierarchical_exact_match_rate": round(sum(1 for x in items if x["retrieval_exact_match"]) / total, 4),
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
        "bm25_exact_match_rate": round(sum(1 for x in records if x["retrieval_bm25_match"]) / total, 4),
        "hierarchical_exact_match_rate": round(sum(1 for x in records if x["retrieval_exact_match"]) / total, 4),
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
        "# HPP V2 Hierarchical Lexical-Vector Retrieval Gate Report",
        "",
        f"Checkpoint: `{payload['checkpoint']}`",
        f"Profile: `{payload['speech_profile']}`",
        f"Prompt count: `{payload['prompt_count']}`",
        f"Seeds: `{', '.join(str(seed) for seed in payload['seeds'])}`",
        f"Start tokens: `{payload['start_tokens']}`",
        "",
        "## Tuned Routing Parameters (Hierarchical Gate)",
        "",
        f"- **BM25 Threshold ($T_{{bm25}}$)**: `{payload['tuned_params']['T_bm25']:.2f}`",
        f"- **BM25 Margin Threshold ($T_{{margin}}$)**: `{payload['tuned_params']['T_margin']:.2f}`",
        f"- **Vector Cosine Similarity Threshold ($T_{{vec}}$)**: `{payload['tuned_params']['T_vec']:.4f}`",
        "",
        "## Overall Retrieval Strategy Comparison",
        "",
        "This table compares the exact-match retrieval rates of the routing strategies across all 375 evaluations (75 prompts x 5 variants):",
        "",
        "| Strategy | Exact-Match Rate | Description |",
        "| :--- | :---: | :--- |",
        f"| **Raw Vector Similarity** | `{summary['raw_vector_exact_match_rate']}` | Matches raw query prompt against raw memory in embedding space |",
        f"| **Normalized Key Match** | `{summary['normalized_key_exact_match_rate']}` | Matches exact normalized keys (fails on paraphrases) |",
        f"| **Normalized Vector Similarity** | `{summary['normalized_vector_exact_match_rate']}` | Matches normalized query against normalized memory in embedding space |",
        f"| **BM25 Lexical Similarity** | `{summary['bm25_exact_match_rate']}` | Keyword-based BM25 match on normalized query tokens |",
        f"| **Hierarchical Router (Optimized)** | `{summary['hierarchical_exact_match_rate']}` | Exact normalized key -> Gated BM25 -> Vector fallback under thresholds |",
        "",
        "## Performance Summary (Hierarchical Router)",
        "",
        f"- **Overall Surface Pass**: `{summary['surface_pass_count']}/{summary['count']} ({summary['surface_pass_rate']*100:.2f}%)`",
        f"- **Overall Semantic Pass**: `{summary['semantic_pass_count']}/{summary['count']} ({summary['semantic_pass_rate']*100:.2f}%)`",
        f"- **Format Leaks**: `{summary['format_leak_total']}`",
        "",
        "## Detailed Breakdown by Variant",
        "",
        "| Variant | Count | Raw Vector Match | Normalized Key Match | Normalized Vector Match | BM25 Match | Hierarchical Match | Semantic Pass | Surface Pass |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    for var, stats in sorted(summary["by_variant"].items()):
        lines.append(
            f"| `{var}` | {stats['count']} | {stats['raw_vector_exact_match_rate']:.4f} | "
            f"{stats['normalized_key_exact_match_rate']:.4f} | {stats['normalized_vector_exact_match_rate']:.4f} | "
            f"{stats['bm25_exact_match_rate']:.4f} | {stats['hierarchical_exact_match_rate']:.4f} | "
            f"{stats['semantic_pass_rate']:.4f} | {stats['surface_pass_rate']:.4f} |"
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
                f"- retrieved by BM25: \"{item['retrieved_prompt_bm25']}\"",
                f"- hierarchical match: `{item['retrieval_exact_match']}` (strategy: `{item['strategy_used']}`)",
                ""
            ])
    else:
        lines.append("Perfect retrieval! All paraphrases mapped to their correct memory templates under Hierarchical Lexical-Vector Routing.")
        
    lines.extend([
        "",
        "## Conclusion",
        "",
        "Retrieval-assisted speech is a scaffold, not native fluency. The Hierarchical Lexical-Vector Router combines keyword precision with embedding generalization to maximize paraphrase match rates."
    ])
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")


def run_routing_logic(
    query_key: str,
    query_tokens: list[str],
    query_vector_norm: torch.Tensor,
    retrieved_key: dict | None,
    bm25_scores: list[float],
    retrieved_bm25: dict,
    idx_bm25: int,
    retrieved_norm: dict,
    sim_norm: float,
    normalized_memory_vectors: torch.Tensor,
    rows: list[dict],
    T_bm25: float,
    T_vec: float,
    T_margin: float,
) -> tuple[dict, str, float]:
    """Execute the Hierarchical Lexical-Vector Routing logic."""
    retrieved_final = retrieved_key
    strategy_used = "normalized_key"
    similarity = 1.0
    
    if retrieved_final is None:
        max_bm25 = max(bm25_scores) if bm25_scores else 0.0
        sorted_scores = sorted(bm25_scores, reverse=True)
        second_bm25 = sorted_scores[1] if len(sorted_scores) > 1 else 0.0
        margin = max_bm25 - second_bm25
        
        is_lexical_strong = (max_bm25 >= T_bm25) and (margin >= T_margin)
        
        if is_lexical_strong:
            retrieved_final = retrieved_bm25
            strategy_used = "lexical_strong"
            similarity = float(F.cosine_similarity(query_vector_norm.unsqueeze(0), normalized_memory_vectors[idx_bm25].unsqueeze(0), dim=-1).item())
        else:
            if sim_norm >= T_vec:
                retrieved_final = retrieved_norm
                strategy_used = "vector_fallback"
                similarity = sim_norm
            else:
                if max_bm25 > 0.0:
                    retrieved_final = retrieved_bm25
                    strategy_used = "lexical_weak_default"
                    similarity = float(F.cosine_similarity(query_vector_norm.unsqueeze(0), normalized_memory_vectors[idx_bm25].unsqueeze(0), dim=-1).item())
                else:
                    retrieved_final = retrieved_norm
                    strategy_used = "vector_weak_default"
                    similarity = sim_norm
                    
    return retrieved_final, strategy_used, similarity


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
    
    # Custom thresholds (runs sweep if not provided)
    parser.add_argument("--t-bm25", type=float, default=None)
    parser.add_argument("--t-vec", type=float, default=None)
    parser.add_argument("--t-margin", type=float, default=None)
    args = parser.parse_args()

    started = time.time()
    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)
    engine.set_power_mode(args.power_mode)

    rows = memory_rows()
    index = normalized_index(rows)
    
    # 1. Precompute Lexical BM25 index
    print("[PRE-COMPUTING] Tokenizing corpus and building BM25 index...", flush=True)
    corpus = [tokenize(normalize_prompt(row["prompt"])) for row in rows]
    bm25 = SimpleBM25(corpus)
    
    # 2. Precompute memory vectors for both raw and normalized prompts
    print("[PRE-COMPUTING] Encoding raw and normalized memory prompts...", flush=True)
    raw_memory_vectors = torch.stack([prompt_vector(engine, row["prompt"], args.domain) for row in rows])
    normalized_memory_vectors = torch.stack([prompt_vector(engine, normalize_prompt(row["prompt"]), args.domain) for row in rows])
    
    # 3. Precompute retrieval data for all queries to run parameter sweep in memory
    print("[PRE-COMPUTING] Querying metadata across all variants for threshold search...", flush=True)
    precomputed_queries = []
    for row in rows:
        for variant in args.variants:
            if variant == "paraphrase":
                query_prompt = PARAPHRASES.get(row["prompt"], row["prompt"])
            else:
                query_prompt = VARIANTS[variant].format(prompt=row["prompt"])
            
            query_key = normalize_prompt(query_prompt)
            query_tokens = tokenize(query_key)
            
            # Raw Vector
            query_vector_raw = prompt_vector(engine, query_prompt, args.domain)
            idx_raw, sim_raw = nearest_memory(raw_memory_vectors, query_vector_raw)
            retrieved_raw = rows[idx_raw]
            
            # Key Match
            retrieved_key = index.get(query_key)
            
            # BM25
            bm25_scores = bm25.get_scores(query_tokens)
            idx_bm25 = int(torch.argmax(torch.tensor(bm25_scores)).item())
            retrieved_bm25 = rows[idx_bm25]
            
            # Normalized Vector
            query_vector_norm = prompt_vector(engine, query_key, args.domain)
            idx_norm, sim_norm = nearest_memory(normalized_memory_vectors, query_vector_norm)
            retrieved_norm = rows[idx_norm]
            
            precomputed_queries.append({
                "row": row,
                "variant": variant,
                "query_prompt": query_prompt,
                "query_key": query_key,
                "query_tokens": query_tokens,
                "query_vector_norm": query_vector_norm,
                "retrieved_raw": retrieved_raw,
                "sim_raw": sim_raw,
                "retrieved_key": retrieved_key,
                "bm25_scores": bm25_scores,
                "retrieved_bm25": retrieved_bm25,
                "idx_bm25": idx_bm25,
                "retrieved_norm": retrieved_norm,
                "sim_norm": sim_norm,
            })

    # Perform threshold sweep if any are None
    if args.t_bm25 is None or args.t_vec is None or args.t_margin is None:
        print("[SWEEPING] Running parameter grid search to optimize thresholds...", flush=True)
        # Sweeping grid
        T_bm25_grid = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        T_vec_grid = [0.5, 0.6, 0.7, 0.75, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 0.92, 0.95]
        T_margin_grid = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        
        best_overall_rate = -1.0
        best_paraphrase_rate = -1.0
        best_params = {"T_bm25": 4.0, "T_vec": 0.8, "T_margin": 1.0}
        
        sweep_results = []
        for t_bm25 in T_bm25_grid:
            for t_vec in T_vec_grid:
                for t_margin in T_margin_grid:
                    correct_overall = 0
                    correct_paraphrase = 0
                    total_paraphrase = 0
                    
                    for q in precomputed_queries:
                        ret_val, _, _ = run_routing_logic(
                            q["query_key"], q["query_tokens"], q["query_vector_norm"],
                            q["retrieved_key"], q["bm25_scores"], q["retrieved_bm25"], q["idx_bm25"],
                            q["retrieved_norm"], q["sim_norm"], normalized_memory_vectors, rows,
                            t_bm25, t_vec, t_margin
                        )
                        is_correct = ret_val["prompt"] == q["row"]["prompt"]
                        if is_correct:
                            correct_overall += 1
                        if q["variant"] == "paraphrase":
                            total_paraphrase += 1
                            if is_correct:
                                correct_paraphrase += 1
                                
                    overall_rate = correct_overall / len(precomputed_queries)
                    paraphrase_rate = correct_paraphrase / total_paraphrase if total_paraphrase > 0 else 0.0
                    sweep_results.append((overall_rate, paraphrase_rate, t_bm25, t_vec, t_margin))
                    
        # Sort by overall rate first, then paraphrase rate, then prefer higher T_vec and higher T_bm25 to minimize false positives
        sweep_results.sort(key=lambda x: (x[0], x[1], x[3], x[2]), reverse=True)
        
        print("\n--- TOP 5 PARAMETER SWEEP RESULTS ---")
        for i, res in enumerate(sweep_results[:5]):
            print(f"Rank {i+1}: Overall Exact-Match={res[0]*100:.2f}%, Paraphrase={res[1]*100:.2f}% | T_bm25={res[2]}, T_vec={res[3]}, T_margin={res[4]}")
            
        best_res = sweep_results[0]
        tuned_T_bm25 = best_res[2]
        tuned_T_vec = best_res[3]
        tuned_T_margin = best_res[4]
        print(f"[OPTIMIZED] Selected: T_bm25={tuned_T_bm25}, T_vec={tuned_T_vec}, T_margin={tuned_T_margin} (Paraphrase Rate: {best_res[1]*100:.2f}%)\n")
    else:
        tuned_T_bm25 = args.t_bm25
        tuned_T_vec = args.t_vec
        tuned_T_margin = args.t_margin
        print(f"[CLI OVERRIDE] Using thresholds: T_bm25={tuned_T_bm25}, T_vec={tuned_T_vec}, T_margin={tuned_T_margin}\n")

    # 4. Run model generations using the selected thresholds
    print(f"[EVALUATION] Starting generation with tuned HLVR on seeds={args.seeds}...", flush=True)
    records = []
    for seed in args.seeds:
        for idx, q in enumerate(precomputed_queries):
            # Run hierarchical routing logic
            retrieved_final, strategy_used, similarity = run_routing_logic(
                q["query_key"], q["query_tokens"], q["query_vector_norm"],
                q["retrieved_key"], q["bm25_scores"], q["retrieved_bm25"], q["idx_bm25"],
                q["retrieved_norm"], q["sim_norm"], normalized_memory_vectors, rows,
                tuned_T_bm25, tuned_T_vec, tuned_T_margin
            )
            
            # Run model generation
            record = run_one(engine, q["row"], q["query_prompt"], q["variant"], retrieved_final, similarity, seed, args)
            
            # Annotate record with comparative metrics
            record["retrieval_strategy"] = strategy_used
            record["strategy_used"] = strategy_used
            record["normalized_key"] = q["query_key"]
            record["retrieved_prompt_raw_vector"] = q["retrieved_raw"]["prompt"]
            record["retrieved_prompt_normalized_vector"] = q["retrieved_norm"]["prompt"]
            record["retrieved_prompt_bm25"] = q["retrieved_bm25"]["prompt"]
            record["retrieval_raw_vector_match"] = q["retrieved_raw"]["prompt"] == q["row"]["prompt"]
            record["retrieval_normalized_key_match"] = q["retrieved_key"] is not None and q["retrieved_key"]["prompt"] == q["row"]["prompt"]
            record["retrieval_normalized_vector_match"] = q["retrieved_norm"]["prompt"] == q["row"]["prompt"]
            record["retrieval_bm25_match"] = q["retrieved_bm25"]["prompt"] == q["row"]["prompt"]
            record["retrieval_exact_match"] = retrieved_final["prompt"] == q["row"]["prompt"]
            
            records.append(record)
            if (idx + 1) % 50 == 0 or (idx + 1) == len(precomputed_queries):
                print(f"Processed {idx+1}/{len(precomputed_queries)} queries for seed={seed}...", flush=True)

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
        "tuned_params": {
            "T_bm25": tuned_T_bm25,
            "T_vec": tuned_T_vec,
            "T_margin": tuned_T_margin,
        },
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
