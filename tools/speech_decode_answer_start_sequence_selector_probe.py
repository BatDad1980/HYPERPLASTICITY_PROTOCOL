"""Decode-only answer-start sequence selector probe for HPP V2 speech.

This does not train. It selects a short answer-start sequence from known
candidate starts, then releases normal generation.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict

import torch
import torch.nn.functional as F

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


def token_prefix(engine: HPP_SovereignEngine_V2, text: str, token_count: int) -> tuple[int, ...]:
    return tuple(int(token) for token in engine.enc.encode(text)[:token_count])


def candidate_sequences(engine: HPP_SovereignEngine_V2, token_count: int) -> dict[str, list[tuple[int, ...]]]:
    by_mode = defaultdict(set)
    all_sequences = set()
    for mode, pairs in PAIRS.items():
        for _prompt, expected in pairs:
            seq = token_prefix(engine, expected, token_count)
            if not seq:
                continue
            by_mode[mode].add(seq)
            all_sequences.add(seq)
    result = {"global": sorted(all_sequences)}
    for mode, sequences in by_mode.items():
        result[mode] = sorted(sequences)
    return result


@torch.no_grad()
def sequence_logprob(engine: HPP_SovereignEngine_V2, prompt: str, sequence: tuple[int, ...], domain: str) -> float:
    runtime_domain = detect_domain(prompt) if domain == "auto" else domain
    prompt_tokens = engine.enc.encode(prompt, allowed_special="all")
    if not prompt_tokens:
        prompt_tokens = [engine.enc.eot_token]
    context = list(prompt_tokens)
    score = 0.0
    for token in sequence:
        ids = torch.tensor([context], dtype=torch.long, device=engine.device)
        embedded = engine.embedding(ids).permute(1, 0, 2)
        if engine.use_fp16:
            embedded = embedded.half()
        output = engine.university(embedded, domain=runtime_domain)
        logits = engine.lm_head(output[-1, 0]).float().detach().cpu()
        log_probs = F.log_softmax(logits, dim=-1)
        score += float(log_probs[int(token)].item())
        context.append(int(token))
    return score


def choose_sequence(
    engine: HPP_SovereignEngine_V2,
    row: dict,
    pool: list[tuple[int, ...]],
    token_count: int,
    domain: str,
) -> tuple[int, ...]:
    if not pool:
        return token_prefix(engine, row["expected"], token_count)
    prompt = f"{prompt_answer(row['prompt'])} "
    best = max(pool, key=lambda seq: sequence_logprob(engine, prompt, seq, domain))
    return best


def sequence_text(engine: HPP_SovereignEngine_V2, sequence: tuple[int, ...]) -> str:
    return engine.enc.decode([int(token) for token in sequence])


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

    rows = prompt_rows()
    selected_rows = rows[: args.limit] if args.limit else rows
    records = []
    for token_count in args.token_counts:
        pools = candidate_sequences(engine, token_count)
        for row in selected_rows:
            oracle = token_prefix(engine, row["expected"], token_count)
            selected_by_strategy = {
                "global_sequence_pool": choose_sequence(engine, row, pools["global"], token_count, args.domain),
                "mode_sequence_pool": choose_sequence(engine, row, pools.get(row["mode"], pools["global"]), token_count, args.domain),
                "oracle_sequence": oracle,
            }
            for strategy, sequence in selected_by_strategy.items():
                selected_text = sequence_text(engine, sequence)
                result = run_one(engine, row, selected_text, args)
                records.append(
                    {
                        "mode": row["mode"],
                        "prompt": row["prompt"],
                        "expected": row["expected"],
                        "token_count": token_count,
                        "strategy": strategy,
                        "selected_token_ids": list(sequence),
                        "selected_text": selected_text,
                        "oracle_token_ids": list(oracle),
                        "oracle_text": sequence_text(engine, oracle),
                        "selected_is_oracle": sequence == oracle,
                        **result,
                    }
                )

    grouped = defaultdict(list)
    for record in records:
        grouped[(record["token_count"], record["strategy"])].append(record)
    summary = {}
    for (token_count, strategy), items in sorted(grouped.items()):
        key = f"{token_count}:{strategy}"
        pass_count = sum(1 for item in items if item["semantic_pass"])
        summary[key] = {
            "token_count": token_count,
            "strategy": strategy,
            "count": len(items),
            "semantic_pass_count": pass_count,
            "semantic_pass_rate": round(pass_count / max(1, len(items)), 4),
            "oracle_sequence_match_rate": round(
                sum(1 for item in items if item["selected_is_oracle"]) / max(1, len(items)),
                4,
            ),
            "format_leak_total": sum(item["format_leak_count"] for item in items),
            "identity_spiral_total": sum(item["identity_spiral_count"] for item in items),
        }

    return {
        "checkpoint": args.checkpoint,
        "seed": args.seed,
        "speech_profile": args.speech_profile,
        "domain": args.domain,
        "prompt_count": len(selected_rows),
        "token_counts": args.token_counts,
        "summary": summary,
        "records": records,
    }


def write_markdown(payload: dict, path: str) -> None:
    lines = [
        "# HPP V2 Decode Answer-Start Sequence Selector Probe",
        "",
        f"Checkpoint: `{payload['checkpoint']}`",
        f"Seed: `{payload['seed']}`",
        f"Profile: `{payload['speech_profile']}`",
        f"Domain: `{payload['domain']}`",
        f"Prompts: `{payload['prompt_count']}`",
        "",
        "## Summary",
        "",
    ]
    for _key, stats in payload["summary"].items():
        lines.append(
            f"- `{stats['token_count']}` token `{stats['strategy']}`: "
            f"semantic `{stats['semantic_pass_count']}/{stats['count']}`, "
            f"oracle-sequence match `{stats['oracle_sequence_match_rate']}`, "
            f"format leaks `{stats['format_leak_total']}`"
        )
    lines.extend(["", "## Samples", ""])
    for item in payload["records"][:24]:
        lines.extend(
            [
                f"### {item['token_count']} tokens - {item['strategy']} - {item['mode']} - {item['prompt']}",
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
    parser.add_argument("--token-counts", nargs="+", type=int, default=[3, 5])
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
