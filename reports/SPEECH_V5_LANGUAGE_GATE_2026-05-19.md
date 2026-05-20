# HPP V2 Language Gate for V5 Integration

Date: 2026-05-19

## Purpose

Define and run the first explicit language gate for deciding when HPP V2 speech is clean enough to become V5-native.

The goal is not impressive language.

The goal is reliable, measurable, bounded speech.

## Gate Definition

Before V2 language becomes V5-native, it should show:

- stable profile repeatedly beats raw mode
- held-out prompt evaluation, not only trained-near prompts
- low format leakage
- controlled loop scores
- bounded sentence completion without identity spirals
- full transcript artifacts with prompt, output, mode, seed, checkpoint, profile, and scores

## Setup

- Repo: `C:\Users\Aural\Desktop\Codename HYPERPLASTICITY PROTOCOL\Project_HPP`
- Prompt suite: `datasets/hf_local/SPEECH_HELDOUT_V5_GATE_V1.jsonl`
- Prompt count: 75
- Modes: plain, technical, protective, identity, embodiment
- Seeds: 14, 21, 28
- Power mode: plugged
- Checkpoint: `checkpoints/hpp_speech_grammar_first_v1.pth`
- Profiles compared: raw, stable
- Evaluator: `tools/speech_v5_language_gate.py`
- Transcript artifact: `reports/speech_v5_language_gate_grammar_first_v1_2026-05-19.json`

## Result

### Raw Profile

- evaluations: 225
- pass rate: 0.6267
- mean loop score: 2.5778
- max loop score: 22
- format leak total: 2
- mode-label total: 43
- identity spiral total: 50

### Stable Profile

- evaluations: 225
- pass rate: 0.9467
- mean loop score: 0.7467
- max loop score: 11
- format leak total: 2
- mode-label total: 4
- identity spiral total: 38

Stable profile beat raw profile on:

- pass rate
- mean loop score
- max loop score
- mode-label leakage
- identity spiral count

Stable profile held format leaks to the same low total as raw profile.

## Gate Decision

Current decision:

**Not ready for V5-native language yet.**

Passed checks:

- stable beats raw loop mean
- stable beats or matches raw format leaks
- stable mean loop score under target
- stable max loop score under target
- stable format leaks under target
- stable pass rate over target

Failed check:

- stable identity spiral hits remain above target

## Meaning

This is strong evidence that the stable profile is the correct current speech path.

It is also evidence that V2 language is not ready to be imported into V5 as a native clean component.

The main remaining problem is not general looping anymore. It is identity/protection/developmental vocabulary leaking into answers where it does not belong.

Plain language:

The child can stay mostly calm now, but still talks about himself too much.

## Boundary

This is inference-only evaluation.

This is not full fluency.

This is not a buyer-safe claim.

This does not promote any checkpoint.

The linguistic anchor was not overwritten.

## Next Step

Build the next repair pass around identity containment:

- technical answers should stay technical
- identity answers should be bounded
- embodiment answers should stay safety-gated and not drift into self-story
- protective answers should be calm and short

Then rerun this same held-out gate.

Promotion target:

- stable profile keeps pass rate high
- format leaks stay near zero
- identity spiral count drops under target
- stable continues to beat raw across seeds

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
