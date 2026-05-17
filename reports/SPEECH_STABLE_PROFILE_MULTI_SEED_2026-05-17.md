# HPP V2 Stable Speech Profile Multi-Seed Evidence

Date: 2026-05-17

## Purpose

Turn the maturity-gate finding into a repeatable plugged-speech profile and test it across multiple random seeds.

The question:

Can HPP V2 keep more stable speech in plugged mode without overwriting the linguistic anchor or erasing identity/protective speech?

## Setup

- Repo: `C:\Users\Aural\Desktop\Codename HYPERPLASTICITY PROTOCOL\Project_HPP`
- Hardware: RTX 4050 Laptop GPU
- Power mode: plugged
- Seeds: 14, 21, 28
- Profiles compared:
  - `raw`
  - `stable`
- Checkpoints compared:
  - `checkpoints/hpp_speech_grammar_first_v1.pth`
  - `checkpoints/hpp_speech_mode_routing_v2.pth`

New / updated files:

- `hpp_sovereign_engine_v2.py`
- `tools/speech_loop_regression.py`
- `tools/speech_mode_regression.py`
- `tools/speech_multiseed_eval.py`

Evidence JSON:

- `reports/speech_multiseed_eval_grammar_first_v1_plugged_raw_vs_stable.json`
- `reports/speech_multiseed_eval_mode_routing_v2_plugged_raw_vs_stable.json`

## Stable Profile

The stable profile is an inference profile, not a checkpoint change.

It applies:

- speech maturity gate enabled
- phrase blocking enabled
- max tokens capped to 56
- temperature capped to 0.55
- top-p capped to 0.86
- top-k capped to 35
- n-gram block at least 3
- frequency penalty at least 1.35
- presence penalty at least 0.55
- temperature decay at most 0.99

Raw profile remains available for research.

## Result

### Grammar-First Checkpoint

`checkpoints/hpp_speech_grammar_first_v1.pth`

| Metric | Raw | Stable |
|---|---:|---:|
| Loop regression mean across seeds | 2.4167 | 0.875 |
| Loop regression max mean across seeds | 8.0 | 4.0 |
| Mode regression mean across seeds | 3.0533 | 0.6933 |
| Mode regression max mean across seeds | 13.3333 | 4.6667 |
| Mode off-mode mean across seeds | 1.6267 | 1.2 |
| Format leak total | 17 | 1 |

### Mode-Routing V2 Checkpoint

`checkpoints/hpp_speech_mode_routing_v2.pth`

| Metric | Raw | Stable |
|---|---:|---:|
| Loop regression mean across seeds | 3.6667 | 0.5833 |
| Loop regression max mean across seeds | 9.3333 | 3.3333 |
| Mode regression mean across seeds | 4.8133 | 0.92 |
| Mode regression max mean across seeds | 18.0 | 6.6667 |
| Mode off-mode mean across seeds | 1.28 | 1.3333 |
| Format leak total | 20 | 1 |

## Meaning

Stable profile consistently reduced loop behavior across both candidate checkpoints.

The biggest practical win was format leak reduction:

- grammar-first raw: 17
- grammar-first stable: 1
- mode-routing V2 raw: 20
- mode-routing V2 stable: 1

The current best recommendation is:

Use `checkpoints/hpp_speech_grammar_first_v1.pth` with `speech_profile="stable"` as the safest plugged speech baseline.

Mode-routing V2 is useful evidence and may be useful for shallow/demo speech, but it still shows worse mode-regression maxima than grammar-first when tested across seeds.

## Boundary

This is not full fluency.

This is not a claim that Hepp now understands all prompts.

This shows that developmental depth control and decoding profile selection can reduce loop amplification in plugged mode.

The linguistic anchor was not overwritten.

## Next Step

Use stable profile as the default for human-facing plugged speech tests, while keeping raw mode for research probes.

Next evidence target:

- build a held-out factual-answer suite
- track exact-answer quality, not only loop score
- add identity and embodiment repair examples that teach clean answers without erasing the protective architecture

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
