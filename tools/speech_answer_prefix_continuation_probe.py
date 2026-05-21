"""Teacher-forced answer-prefix probe for HPP V2 speech checkpoints.

This does not train and does not free-generate. It measures whether expected
answer tokens rank well when the prompt and earlier expected answer tokens are
already present in context.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import defaultdict

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.build_speech_identity_containment_dataset import PAIRS
from tools.speech_v5_language_gate import load_override
from tools.train_speech_cleanup_balanced import detect_domain


DOMAINS = ["auto", "conversation", "logic", "identity", "synthesis", "none"]


def prompt_rows() -> list[dict]:
    rows = []
    for mode, pairs in PAIRS.items():
        for prompt, expected in pairs:
            rows.append({"mode": mode, "prompt": prompt, "expected": expected})
    return rows


def rank_token(logits: torch.Tensor, token_id: int) -> int:
    row = logits.float().detach().cpu()
    target = row[token_id].item()
    return int((row > target).sum().item() + 1)


def summarize(values: list[float]) -> dict:
    if not values:
        return {"count": 0, "mean": math.nan, "median": math.nan, "top100_rate": math.nan}
    ordered = sorted(values)
    return {
        "count": len(values),
        "mean": round(sum(values) / len(values), 2),
        "median": ordered[len(ordered) // 2],
        "top100_rate": round(sum(1 for value in values if value <= 100) / len(values), 4),
        "top1000_rate": round(sum(1 for value in values if value <= 1000) / len(values), 4),
    }


@torch.no_grad()
def score_row(engine: HPP_SovereignEngine_V2, row: dict, domain: str, max_answer_tokens: int) -> dict:
    runtime_domain = detect_domain(row["prompt"]) if domain == "auto" else domain
    prefix = row["prompt"].strip() + "\n"
    prefix_tokens = engine.enc.encode(prefix)
    answer_tokens = engine.enc.encode(row["expected"])[:max_answer_tokens]
    tokens = prefix_tokens + answer_tokens
    ids = torch.tensor([tokens[:-1]], dtype=torch.long, device=engine.device)
    embedded = engine.embedding(ids).permute(1, 0, 2)
    if engine.use_fp16:
        embedded = embedded.half()
    output = engine.university(embedded, domain=runtime_domain)
    logits = engine.lm_head(output).float()

    ranks = []
    for offset, token_id in enumerate(answer_tokens):
        logit_index = len(prefix_tokens) + offset - 1
        if logit_index < 0 or logit_index >= logits.shape[0]:
            continue
        ranks.append(
            {
                "answer_position": offset + 1,
                "token_id": int(token_id),
                "text": engine.enc.decode([int(token_id)]),
                "rank": rank_token(logits[logit_index, 0], token_id),
            }
        )
    return {
        "mode": row["mode"],
        "prompt": row["prompt"],
        "expected": row["expected"],
        "domain": runtime_domain,
        "ranks": ranks,
    }


def run(args: argparse.Namespace) -> dict:
    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)
    engine.set_power_mode(args.power_mode)

    rows = prompt_rows()
    selected = rows[: args.limit] if args.limit else rows
    records = []
    for domain in args.domains:
        for row in selected:
            records.append(score_row(engine, row, domain, args.max_answer_tokens))

    summary = {}
    grouped = defaultdict(list)
    by_position = defaultdict(list)
    for record in records:
        key = record["domain"]
        for item in record["ranks"]:
            grouped[key].append(item["rank"])
            by_position[(key, item["answer_position"])].append(item["rank"])

    for domain in sorted(grouped):
        summary[domain] = {
            "all_checked_answer_tokens": summarize(grouped[domain]),
            "by_position": {
                str(position): summarize(by_position[(domain, position)])
                for position in range(1, args.max_answer_tokens + 1)
                if by_position[(domain, position)]
            },
        }

    return {
        "checkpoint": args.checkpoint,
        "power_mode": args.power_mode,
        "prompt_count": len(selected),
        "max_answer_tokens": args.max_answer_tokens,
        "requested_domains": args.domains,
        "summary": summary,
        "records": records,
    }


def write_markdown(payload: dict, path: str) -> None:
    lines = [
        "# HPP V2 Answer-Prefix Continuation Probe",
        "",
        f"Checkpoint: `{payload['checkpoint']}`",
        f"Prompts: `{payload['prompt_count']}`",
        f"Answer tokens checked: `{payload['max_answer_tokens']}`",
        "",
        "## Summary",
        "",
    ]
    for domain, summary in payload["summary"].items():
        all_stats = summary["all_checked_answer_tokens"]
        first = summary["by_position"].get("1", {})
        fourth = summary["by_position"].get("4", {})
        lines.append(
            f"- `{domain}` all-token mean rank `{all_stats['mean']}`, "
            f"top100 `{all_stats['top100_rate']}`, "
            f"pos1 mean `{first.get('mean')}`, pos4 mean `{fourth.get('mean')}`"
        )
    lines.extend(["", "## Sample Records", ""])
    for record in payload["records"][:8]:
        rank_text = ", ".join(
            f"{item['answer_position']}:{item['text'].replace(chr(10), '\\n')}={item['rank']}"
            for item in record["ranks"][:8]
        )
        lines.extend(
            [
                f"### {record['domain']} - {record['mode']} - {record['prompt']}",
                "",
                f"- expected: {record['expected']}",
                f"- ranks: `{rank_text}`",
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
    parser.add_argument("--domains", nargs="+", default=["auto", "conversation"])
    parser.add_argument("--limit", type=int, default=75)
    parser.add_argument("--max-answer-tokens", type=int, default=12)
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
