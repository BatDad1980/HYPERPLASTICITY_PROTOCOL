"""Probe prompt-conditioned signal flow inside HPP V2 speech checkpoints.

This does not generate speech. It measures whether different prompts remain
distinguishable through the embedding, University stack, and LM head.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import Counter, defaultdict

import torch
import torch.nn.functional as F

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.build_speech_identity_containment_dataset import PAIRS
from tools.speech_v5_language_gate import load_override


DOMAINS = ["conversation", "logic", "identity", "none"]


def prompt_rows() -> list[dict]:
    rows = []
    for mode, pairs in PAIRS.items():
        for prompt, expected in pairs:
            rows.append({"mode": mode, "prompt": prompt, "expected": expected})
    return rows


def pool_hidden(hidden: torch.Tensor) -> torch.Tensor:
    # hidden is [Seq, Batch, Dim]
    return hidden.mean(dim=0).squeeze(0).float().detach().cpu()


def rank_token(logits: torch.Tensor, token_id: int) -> int:
    row = logits.float().detach().cpu()
    target = row[token_id].item()
    return int((row > target).sum().item() + 1)


def token_text(engine: HPP_SovereignEngine_V2, token_id: int) -> str:
    try:
        return engine.enc.decode([int(token_id)])
    except Exception:
        return f"<{token_id}>"


@torch.no_grad()
def encode_prompt(engine: HPP_SovereignEngine_V2, prompt: str, domain: str) -> dict:
    tokens = engine.enc.encode(prompt, allowed_special="all")
    if not tokens:
        tokens = [engine.enc.eot_token]
    ids = torch.tensor([tokens], dtype=torch.long, device=engine.device)
    embedded = engine.embedding(ids).permute(1, 0, 2)
    if engine.use_fp16:
        embedded = embedded.half()

    output = engine.university(embedded, domain=domain)
    logits = engine.lm_head(output[-1, 0]).float()
    top = torch.topk(logits, k=8)
    return {
        "embedding": pool_hidden(embedded),
        "university": pool_hidden(output),
        "next_logits": logits.detach().cpu(),
        "top_tokens": [
            {"token_id": int(idx), "text": token_text(engine, int(idx)), "logit": round(float(val), 4)}
            for val, idx in zip(top.values.detach().cpu(), top.indices.detach().cpu())
        ],
    }


def cosine_summary(vectors: list[torch.Tensor], modes: list[str]) -> dict:
    if len(vectors) < 2:
        return {}
    matrix = F.cosine_similarity(
        torch.stack(vectors).unsqueeze(1),
        torch.stack(vectors).unsqueeze(0),
        dim=-1,
    )
    same = []
    different = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            value = float(matrix[i, j].item())
            if modes[i] == modes[j]:
                same.append(value)
            else:
                different.append(value)

    def stats(values: list[float]) -> dict:
        if not values:
            return {"count": 0, "mean": math.nan, "min": math.nan, "max": math.nan}
        return {
            "count": len(values),
            "mean": round(sum(values) / len(values), 6),
            "min": round(min(values), 6),
            "max": round(max(values), 6),
        }

    return {"same_mode": stats(same), "different_mode": stats(different)}


def expected_token_ranks(engine: HPP_SovereignEngine_V2, logits: torch.Tensor, expected: str) -> dict:
    tokens = engine.enc.encode(expected)
    tokens = tokens[:8]
    ranks = []
    for token in tokens:
        ranks.append({"token_id": int(token), "text": token_text(engine, token), "rank": rank_token(logits, token)})
    return {
        "expected_prefix": expected,
        "checked_tokens": ranks,
        "best_rank": min((item["rank"] for item in ranks), default=None),
        "first_rank": ranks[0]["rank"] if ranks else None,
    }


def run(args: argparse.Namespace) -> dict:
    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)
    engine.set_power_mode(args.power_mode)

    rows = prompt_rows()
    selected = rows[: args.limit] if args.limit else rows
    records = []
    embedding_vectors = []
    modes = []
    university_vectors_by_domain = defaultdict(list)
    top_token_counter = Counter()

    for row in selected:
        modes.append(row["mode"])
        base = encode_prompt(engine, row["prompt"], "conversation")
        embedding_vectors.append(base["embedding"])
        top_token_counter.update(item["text"] for item in base["top_tokens"][:3])
        domain_records = {}
        for domain in DOMAINS:
            encoded = base if domain == "conversation" else encode_prompt(engine, row["prompt"], domain)
            university_vectors_by_domain[domain].append(encoded["university"])
            domain_records[domain] = {
                "top_tokens": encoded["top_tokens"],
                "expected_ranks": expected_token_ranks(engine, encoded["next_logits"], row["expected"]),
            }
        records.append(
            {
                "mode": row["mode"],
                "prompt": row["prompt"],
                "expected": row["expected"],
                "domains": domain_records,
            }
        )

    summaries = {
        "embedding_cosine": cosine_summary(embedding_vectors, modes),
        "university_cosine": {
            domain: cosine_summary(vectors, modes)
            for domain, vectors in sorted(university_vectors_by_domain.items())
        },
        "top_conversation_next_tokens": [
            {"text": text, "count": count} for text, count in top_token_counter.most_common(20)
        ],
    }
    for domain in DOMAINS:
        first_ranks = [
            item["domains"][domain]["expected_ranks"]["first_rank"]
            for item in records
            if item["domains"][domain]["expected_ranks"]["first_rank"] is not None
        ]
        best_ranks = [
            item["domains"][domain]["expected_ranks"]["best_rank"]
            for item in records
            if item["domains"][domain]["expected_ranks"]["best_rank"] is not None
        ]
        summaries[f"{domain}_expected_rank"] = {
            "count": len(first_ranks),
            "mean_first_rank": round(sum(first_ranks) / max(1, len(first_ranks)), 2),
            "median_first_rank": sorted(first_ranks)[len(first_ranks) // 2] if first_ranks else None,
            "mean_best_rank": round(sum(best_ranks) / max(1, len(best_ranks)), 2),
            "median_best_rank": sorted(best_ranks)[len(best_ranks) // 2] if best_ranks else None,
            "top100_first_rate": round(sum(1 for rank in first_ranks if rank <= 100) / max(1, len(first_ranks)), 4),
            "top1000_first_rate": round(sum(1 for rank in first_ranks if rank <= 1000) / max(1, len(first_ranks)), 4),
        }

    return {
        "checkpoint": args.checkpoint,
        "power_mode": args.power_mode,
        "prompt_count": len(selected),
        "domains": DOMAINS,
        "summary": summaries,
        "records": records,
    }


def write_markdown(payload: dict, path: str) -> None:
    lines = [
        "# HPP V2 Speech Prompt Signal Probe",
        "",
        f"Checkpoint: `{payload['checkpoint']}`",
        f"Prompts: `{payload['prompt_count']}`",
        "",
        "## Representation Similarity",
        "",
        f"- embedding same-mode cosine mean: `{payload['summary']['embedding_cosine']['same_mode']['mean']}`",
        f"- embedding different-mode cosine mean: `{payload['summary']['embedding_cosine']['different_mode']['mean']}`",
        "",
    ]
    for domain, summary in payload["summary"]["university_cosine"].items():
        lines.append(
            f"- `{domain}` university same/different cosine mean: "
            f"`{summary['same_mode']['mean']}` / `{summary['different_mode']['mean']}`"
        )
    lines.extend(["", "## Expected Token Ranks", ""])
    for domain in payload["domains"]:
        stats = payload["summary"][f"{domain}_expected_rank"]
        lines.append(
            f"- `{domain}` first-rank mean `{stats['mean_first_rank']}`, "
            f"best-rank mean `{stats['mean_best_rank']}`, "
            f"top100 first rate `{stats['top100_first_rate']}`"
        )
    lines.extend(["", "## Common Conversation Top Tokens", ""])
    for item in payload["summary"]["top_conversation_next_tokens"][:12]:
        safe = item["text"].replace("\n", "\\n")
        lines.append(f"- `{safe}`: {item['count']}")
    lines.extend(["", "## Sample Records", ""])
    for item in payload["records"][:8]:
        conv = item["domains"]["conversation"]
        top = ", ".join(token["text"].replace("\n", "\\n") for token in conv["top_tokens"][:5])
        lines.extend(
            [
                f"### {item['mode']} - {item['prompt']}",
                "",
                f"- expected: {item['expected']}",
                f"- conversation top tokens: `{top}`",
                f"- expected first token rank: `{conv['expected_ranks']['first_rank']}`",
                f"- expected best prefix rank: `{conv['expected_ranks']['best_rank']}`",
                "",
            ]
        )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--power-mode", default="plugged", choices=["demo", "battery", "plugged"])
    parser.add_argument("--limit", type=int, default=75)
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--md-out", required=True)
    args = parser.parse_args()

    payload = run(args)
    os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
    write_markdown(payload, args.md_out)
    print(f"wrote: {args.json_out}")
    print(f"wrote: {args.md_out}")
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
