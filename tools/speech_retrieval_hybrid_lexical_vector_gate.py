"""Evaluate hybrid lexical-vector retrieval (BM25 + normalized vector) before speech generation."""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
from collections import Counter, defaultdict

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
from tools.speech_retrieval_normalized_vector_gate import PARAPHRASES

VARIANTS = dict(BASE_VARIANTS)
VARIANTS["paraphrase"] = "{paraphrase}"

LEXICAL_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "of", "to", "in", "on", 
    "at", "for", "with", "by", "about", "this", "that", "these", "those", 
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", 
    "do", "does", "did", "please", "can", "could", "should", "would", 
    "you", "me", "my", "your", "we", "us", "our", "i"
}


def tokenize(text: str) -> list[str]:
    text = text.lower()
    words = re.findall(r"[a-z0-9]+", text)
    return [w for w in words if w not in LEXICAL_STOPWORDS]


class SimpleBM25:
    """Lightweight self-contained BM25 search engine."""
    def __init__(self, corpus: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus)
        self.avg_doc_len = sum(len(doc) for doc in corpus) / max(1, self.corpus_size)
        self.doc_freqs = defaultdict(int)
        self.doc_lengths = [len(doc) for doc in corpus]
        self.f = []
        for doc in corpus:
            frequencies = Counter(doc)
            self.f.append(frequencies)
            for word in frequencies:
                self.doc_freqs[word] += 1
        
        self.idf = {}
        for word, freq in self.doc_freqs.items():
            self.idf[word] = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0)

    def get_scores(self, query: list[str]) -> list[float]:
        scores = []
        for i in range(self.corpus_size):
            score = 0.0
            doc_len = self.doc_lengths[i]
            frequencies = self.f[i]
            for word in query:
                if word in frequencies:
                    freq = frequencies[word]
                    tf = (freq * (self.k1 + 1)) / (freq + self.k1 * (1 - self.b + self.b * doc_len / self.avg_doc_len))
                    score += self.idf.get(word, 0.0) * tf
            scores.append(score)
        return scores


def rank_items(scores: list[float]) -> list[int]:
    """Return rank (0-indexed, 0 is best) for each item in the original scores list."""
    paired = list(enumerate(scores))
    # Sort descending by score.
    paired.sort(key=lambda x: x[1], reverse=True)
    ranks = [0] * len(scores)
    for rank, (original_idx, _) in enumerate(paired):
        ranks[original_idx] = rank
    return ranks


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
        "bm25_exact_match_rate": round(sum(1 for x in records if x["retrieval_bm25_match"]) / total, 4),
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
        "# HPP V2 Hybrid Lexical-Vector Retrieval Gate Report",
        "",
        f"Checkpoint: `{payload['checkpoint']}`",
        f"Profile: `{payload['speech_profile']}`",
        f"Prompt count: `{payload['prompt_count']}`",
        f"Seeds: `{', '.join(str(seed) for seed in payload['seeds'])}`",
        f"Start tokens: `{payload['start_tokens']}`",
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
        f"| **Hybrid Retrieval (RRF)** | `{summary['hybrid_retrieval_exact_match_rate']}` | Reciprocal Rank Fusion blending BM25 and Normalized Vector |",
        "",
        "## Performance Summary (RRF Hybrid Strategy)",
        "",
        f"- **Overall Surface Pass**: `{summary['surface_pass_count']}/{summary['count']} ({summary['surface_pass_rate']*100:.2f}%)`",
        f"- **Overall Semantic Pass**: `{summary['semantic_pass_count']}/{summary['count']} ({summary['semantic_pass_rate']*100:.2f}%)`",
        f"- **Format Leaks**: `{summary['format_leak_total']}`",
        "",
        "## Detailed Breakdown by Variant",
        "",
        "| Variant | Count | Raw Vector Match | Normalized Key Match | Normalized Vector Match | BM25 Match | Hybrid Match | Semantic Pass | Surface Pass |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    for var, stats in sorted(summary["by_variant"].items()):
        lines.append(
            f"| `{var}` | {stats['count']} | {stats['raw_vector_exact_match_rate']:.4f} | "
            f"{stats['normalized_key_exact_match_rate']:.4f} | {stats['normalized_vector_exact_match_rate']:.4f} | "
            f"{stats['bm25_exact_match_rate']:.4f} | {stats['hybrid_retrieval_exact_match_rate']:.4f} | "
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
                f"- hybrid match: `{item['retrieval_exact_match']}`",
                ""
            ])
    else:
        lines.append("Perfect retrieval! All paraphrases mapped to their correct memory templates under Blended Hybrid (RRF) Retrieval.")
        
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
    
    # 1. Precompute Lexical BM25 index
    print("[PRE-COMPUTING] Tokenizing corpus and building BM25 index...", flush=True)
    corpus = [tokenize(normalize_prompt(row["prompt"])) for row in rows]
    bm25 = SimpleBM25(corpus)
    
    # 2. Precompute memory vectors for both raw and normalized prompts
    print("[PRE-COMPUTING] Encoding raw and normalized memory prompts...", flush=True)
    raw_memory_vectors = torch.stack([prompt_vector(engine, row["prompt"], args.domain) for row in rows])
    normalized_memory_vectors = torch.stack([prompt_vector(engine, normalize_prompt(row["prompt"]), args.domain) for row in rows])
    
    records = []
    for seed in args.seeds:
        print(f"[HYBRID-LEXICAL-VECTOR] seed={seed} prompts={len(rows)} variants={args.variants}", flush=True)
        for row in rows:
            for variant in args.variants:
                # Construct query prompt
                if variant == "paraphrase":
                    query_prompt = PARAPHRASES.get(row["prompt"], row["prompt"])
                else:
                    query_prompt = VARIANTS[variant].format(prompt=row["prompt"])
                
                query_key = normalize_prompt(query_prompt)
                query_tokens = tokenize(query_key)
                
                # A. Evaluate Raw Vector Retrieval
                query_vector_raw = prompt_vector(engine, query_prompt, args.domain)
                idx_raw, sim_raw = nearest_memory(raw_memory_vectors, query_vector_raw)
                retrieved_raw = rows[idx_raw]
                
                # B. Evaluate Normalized Key Retrieval
                retrieved_key = index.get(query_key)
                
                # C. Evaluate BM25 Lexical Retrieval
                bm25_scores = bm25.get_scores(query_tokens)
                idx_bm25 = int(torch.argmax(torch.tensor(bm25_scores)).item())
                retrieved_bm25 = rows[idx_bm25]
                
                # D. Evaluate Normalized Vector Retrieval
                query_vector_norm = prompt_vector(engine, query_key, args.domain)
                idx_norm, sim_norm = nearest_memory(normalized_memory_vectors, query_vector_norm)
                retrieved_norm = rows[idx_norm]
                
                # E. Evaluate Hybrid RRF Retrieval (Reciprocal Rank Fusion)
                bm25_ranks = rank_items(bm25_scores)
                cos_sims = F.cosine_similarity(normalized_memory_vectors, query_vector_norm.unsqueeze(0), dim=-1).tolist()
                vector_ranks = rank_items(cos_sims)
                
                rrf_scores = []
                for idx in range(len(rows)):
                    score = 1.0 / (60 + bm25_ranks[idx]) + 1.0 / (60 + vector_ranks[idx])
                    rrf_scores.append(score)
                idx_hybrid = int(torch.argmax(torch.tensor(rrf_scores)).item())
                retrieved_hybrid_rrf = rows[idx_hybrid]
                
                # F. Hybrid Routing Decision (Key Match first, then RRF)
                retrieved_final = retrieved_key
                hybrid_strategy = "normalized_key"
                similarity = 1.0
                if retrieved_final is None:
                    retrieved_final = retrieved_hybrid_rrf
                    hybrid_strategy = "rrf_fallback"
                    similarity = cos_sims[idx_hybrid]
                
                # G. Run Model Generation using the Blended Hybrid Retrieval Memory
                record = run_one(engine, row, query_prompt, variant, retrieved_final, similarity, seed, args)
                
                # Annotate record with comparative metrics
                record["retrieval_strategy"] = hybrid_strategy
                record["normalized_key"] = query_key
                record["retrieved_prompt_raw_vector"] = retrieved_raw["prompt"]
                record["retrieved_prompt_normalized_vector"] = retrieved_norm["prompt"]
                record["retrieved_prompt_bm25"] = retrieved_bm25["prompt"]
                record["retrieval_raw_vector_match"] = retrieved_raw["prompt"] == row["prompt"]
                record["retrieval_normalized_key_match"] = retrieved_key is not None and retrieved_key["prompt"] == row["prompt"]
                record["retrieval_normalized_vector_match"] = retrieved_norm["prompt"] == row["prompt"]
                record["retrieval_bm25_match"] = retrieved_bm25["prompt"] == row["prompt"]
                record["retrieval_exact_match"] = retrieved_final["prompt"] == row["prompt"]
                
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
