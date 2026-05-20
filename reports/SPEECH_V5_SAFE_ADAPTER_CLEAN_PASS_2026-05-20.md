# HPP V2 V5-Safe Language Adapter Clean Pass

Date: 2026-05-20

## Purpose

Close the remaining V5-safe adapter language failures after the identity-containment gate pass.

The previous adapter gate passed overall but still had:

- 7 mode-label echoes
- 1 format leak

## Change

The stable speech phrase blocker was extended with narrow decoder-side blocks:

- `protective mode`
- `Instruction:`
- `Response:`

This is an inference control only.

It does not change checkpoint weights.

## Setup

- Adapter: `core/v5_language_adapter.py`
- Checkpoint: `checkpoints/hpp_speech_identity_containment_v1.pth`
- Gate evaluator: `tools/speech_v5_language_gate.py`
- Held-out suite: `datasets/hf_local/SPEECH_HELDOUT_V5_GATE_V1.jsonl`
- Power mode: plugged
- Seeds: 14, 21, 28
- Profile: stable adapter path

## Result

Artifact:

- `reports/speech_v5_language_gate_adapter_no_label_or_format_2026-05-20.json`

Stable adapter gate:

- evaluations: 225
- pass count: 225
- pass rate: 1.0
- mean loop score: 0.6933
- max loop score: 7
- format leak total: 0
- mode label total: 0
- identity spiral total: 5
- repeated sentence total: 0

Failure review artifact:

- `reports/SPEECH_V5_GATE_FAILURE_REVIEW_ADAPTER_NO_LABEL_OR_FORMAT_2026-05-20.md`
- `reports/speech_v5_gate_failure_review_adapter_no_label_or_format_2026-05-20.json`

Failure review:

- failures: 0 / 225
- pass rate: 1.0

Decision:

**The V5-safe adapter path passes the current held-out language gate with zero failures under the current rubric.**

## Meaning

The language candidate has crossed the current V5 review threshold as an adapter path:

- held-out prompt suite
- multiple seeds
- full transcripts saved
- no format leaks
- no mode-label echoes
- loop scores under target
- identity spiral under target

This is the cleanest V2 language result so far.

## Boundary

This is still an adapter result, not a claim of mature fluency.

This is not raw V2 speech.

This is not an automatic checkpoint promotion.

This does not claim AGI, human-equivalent cognition, or full LLM replacement.

## Next Step

Begin V5 integration review around the adapter path:

1. Create a small V5-side adapter import plan.
2. Cold-restart rerun the same gate.
3. Add a manual transcript review note.
4. Keep raw V2 speech research-only.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
