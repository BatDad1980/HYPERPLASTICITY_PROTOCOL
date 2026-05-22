"""Decode-only first-token selector probe for HPP V2 speech.

This does not train. It selects one answer-start token at runtime, releases
normal generation, and compares candidate-pool selection against oracle force.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.build_speech_exposure_bias_bridge_dataset import prompt_answer
from tools.build_speech_identity_containment_dataset import PAIRS
from tools.speech_semantic_quality_review import score_item
from tools.speech_v5_language_gate import leak_metrics, load_override
from tools.train_speech_cleanup_balanced import detect_domain


def prompt_rows() -> list[dict]:
    rows = []
    for mode, pairs in PAIRS.items():
        for prompt, expected in pairs:
            rows.append({"mode": mode, "prompt": prompt, "expected": expected})
    return rows


def first_token_id(engine: HPP_SovereignEngine_V2, text: str) -> int:
    tokens = engine.enc.encode(text)
    return int(tokens[0]) if tokens else int(engine.enc.eot_token)


def candidate_tokens(engine: HPP_SovereignEngine_V2) -> dict[str, list[int]]:
    by_mode = defaultdict(set)
    all_tokens = set()
    for mode, pairs in PAIRS.items():
        for _prompt, expected in pairs:
            token = first_token_id(engine, expected)
            by_mode[mode].add(token)
            all_tokens.add(token)
    result = {"global": sorted(all_tokens)}
    for mode, tokens in by_mode.items():
        result[mode] = sorted(tokens)
    return result


@torch.no_grad()
def next_logits(engine: HPP_SovereignEngine_V2, prompt: str, domain: str) -> torch.Tensor:
    runtime_domain = detect_domain(prompt) if domain == "auto" else domain
    tokens = engine.enc.encode(prompt, allowed_special="all")
    if not tokens:
        tokens = [engine.enc.eot_token]
    ids = torch.tensor([tokens], dtype=torch.long, device=engine.device)
    embedded = engine.embedding(ids).permute(1, 0, 2)
    if engine.use_fp16:
        embedded = embedded.half()
    output = engine.university(embedded, domain=runtime_domain)
    return engine.lm_head(output[-1, 0]).float().detach().cpu()


def best_from_pool(logits: torch.Tensor, pool: list[int]) -> int:
    if not pool:
        return int(torch.argmax(logits).item())
    pool_tensor = torch.tensor(pool, dtype=torch.long)
    scores = logits[pool_tensor]
    return int(pool[int(torch.argmax(scores).item())])


def token_text(engine: HPP_SovereignEngine_V2, token_id: int) -> str:
    return engine.enc.decode([int(token_id)])


def choose_tokens(engine: HPP_SovereignEngine_V2, row: dict, logits: torch.Tensor, pools: dict[str, list[int]]) -> dict[str, int]:
    oracle = first_token_id(engine, row["expected"])
    return {
        "none": -1,
        "unrestricted_top1": int(torch.argmax(logits).item()),
        "global_answer_pool": best_from_pool(logits, pools["global"]),
        "mode_answer_pool": best_from_pool(logits, pools.get(row["mode"], pools["global"])),
        "oracle_first_token": oracle,
    }


def run_one(engine: HPP_SovereignEngine_V2, row: dict, selected_text: str, args: argparse.Namespace) -> dict:
    input_text = f"{prompt_answer(row['prompt'])} {selected_text}"
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)
    response = engine.pulse(
        input_text,
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
        domain=args.domain,
    )
    combined = (selected_text + " " + response["response"]).strip()
    scored = score_item(
        {
            "id": row["prompt"],
            "mode": row["mode"],
            "seed": args.seed,
            "prompt": row["prompt"],
            "response": combined,
        },
        row["expected"],
    )
    leaks = leak_metrics(combined)
    return {
        "input": input_text,
        "generated_continuation": response["response"],
        "scored_response": combined,
        "semantic_pass": scored["semantic_pass"],
        "hits": scored["hits"],
        "required_hits": scored["required_hits"],
        "format_leak_count": leaks["format_leak_count"],
        "identity_spiral_count": leaks["identity_spiral_count"],
        "repeated_sentence_count": leaks["repeated_sentence_count"],
    }


def run_probe(args: argparse.Namespace) -> dict:
    engine = HPP_SovereignEngine_V2(max_context=512)
    load_override(engine, args.checkpoint)
    engine.set_power_mode(args.power_mode)

    pools = candidate_tokens(engine)
    rows = prompt_rows()
    selected = rows[: args.limit] if args.limit else rows
    records = []
    for row in selected:
        base_prompt = f"{prompt_answer(row['prompt'])} "
        logits = next_logits(engine, base_prompt, args.domain)
        chosen = choose_tokens(engine, row, logits, pools)
        oracle_token = first_token_id(engine, row["expected"])
        for strategy, token_id in chosen.items():
            selected_text = "" if token_id < 0 else token_text(engine, token_id)
            result = run_one(engine, row, selected_text, args)
            records.append(
                {
                    "mode": row["mode"],
                    "prompt": row["prompt"],
                    "expected": row["expected"],
                    "strategy": strategy,
                    "selected_token_id": token_id,
                    "selected_text": selected_text,
                    "oracle_token_id": oracle_token,
                    "oracle_text": token_text(engine, oracle_token),
                    "selected_is_oracle": token_id == oracle_token,
                    **result,
                }
            )

    grouped = defaultdict(list)
    for record in records:
        grouped[record["strategy"]].append(record)
    summary = {}
    for strategy, items in sorted(grouped.items()):
        pass_count = sum(1 for item in items if item["semantic_pass"])
        summary[strategy] = {
            "count": len(items),
            "semantic_pass_count": pass_count,
            "semantic_pass_rate": round(pass_count / max(1, len(items)), 4),
            "oracle_token_match_rate": round(
                sum(1 for item in items if item["selected_is_oracle"]) / max(1, len(items)),
                4,
            ),
            "format_leak_total": sum(item["format_leak_count"] for item in items),
            "identity_spiral_total": sum(item["identity_spiral_count"] for item in items),
            "repeated_sentence_total": sum(item["repeated_sentence_count"] for item in items),
        }

    return {
        "checkpoint": args.checkpoint,
        "seed": args.seed,
        "speech_profile": args.speech_profile,
        "domain": args.domain,
        "prompt_count": len(selected),
        "candidate_pool_sizes": {name: len(tokens) for name, tokens in sorted(pools.items())},
        "summary": summary,
        "records": records,
    }


def write_markdown(payload: dict, path: str) -> None:
    lines = [
        "# HPP V2 Decode First-Token Selector Probe",
        "",
        f"Checkpoint: `{payload['checkpoint']}`",
        f"Seed: `{payload['seed']}`",
        f"Profile: `{payload['speech_profile']}`",
        f"Domain: `{payload['domain']}`",
        f"Prompts: `{payload['prompt_count']}`",
        "",
        "## Candidate Pools",
        "",
    ]
    for name, size in payload["candidate_pool_sizes"].items():
        lines.append(f"- `{name}`: {size}")
    lines.extend(["", "## Summary", ""])
    for strategy, stats in payload["summary"].items():
        lines.append(
            f"- `{strategy}`: semantic `{stats['semantic_pass_count']}/{stats['count']}`, "
            f"oracle-token match `{stats['oracle_token_match_rate']}`, "
            f"format leaks `{stats['format_leak_total']}`"
        )
    lines.extend(["", "## Samples", ""])
    for item in payload["records"][:25]:
        lines.extend(
            [
                f"### {item['strategy']} - {item['mode']} - {item['prompt']}",
                "",
                f"- expected: {item['expected']}",
                f"- selected: {item['selected_text']} / oracle: {item['oracle_text']}",
                f"- generated: {item['generated_continuation']}",
                f"- scored: {item['scored_response']}",
                f"- semantic pass: `{item['semantic_pass']}`",
                f"- hits: `{', '.join(item['hits'])}`",
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
    parser.add_argument("--seed", type=int, default=14)
    parser.add_argument("--limit", type=int, default=75)
    parser.add_argument("--max-tokens", type=int, default=24)
    parser.add_argument("--temperature", type=float, default=0.25)
    parser.add_argument("--top-p", type=float, default=0.55)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--frequency-penalty", type=float, default=1.05)
    parser.add_argument("--presence-penalty", type=float, default=0.15)
    parser.add_argument("--speech-profile", choices=["raw", "stable", "semantic_short"], default="semantic_short")
    parser.add_argument("--domain", default="auto", choices=["auto", "conversation", "logic", "identity", "synthesis", "none"])
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--md-out", required=True)
    args = parser.parse_args()

    payload = run_probe(args)
    os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
    with open(args.json_out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2)
    write_markdown(payload, args.md_out)
    print(f"wrote: {args.json_out}")
    print(f"wrote: {args.md_out}")
    print(json.dumps(payload["summary"], indent=2))


if __name__ == "__main__":
    main()
