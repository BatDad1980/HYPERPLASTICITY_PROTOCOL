# HPP V2 Surface Cleaner Strict Gate

Date: 2026-05-20

## Purpose

Test whether narrow decoder cleanup can remove leading wrapper residue caught by the strict surface gate.

The prior strict gate failed because outputs often began with `Response` or `Instruction`.

## Change

The stable speech layer now:

- blocks standalone `Response` and `Instruction` attractor phrases during stable decoding
- strips a leading `Response` or `Instruction` label during final response cleanup

This is an inference cleanup, not a checkpoint weight change.

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

- `reports/speech_v5_language_gate_adapter_surface_cleaner_2026-05-20.json`

Strict surface gate:

- evaluations: 225
- pass count: 225
- pass rate: 1.0
- mean loop score: 0.7911
- max loop score: 7
- format leak total: 0
- surface prefix total: 0
- mode label total: 0
- identity spiral total: 2
- repeated sentence total: 0

Failure review artifacts:

- `reports/SPEECH_V5_GATE_FAILURE_REVIEW_ADAPTER_SURFACE_CLEANER_2026-05-20.md`
- `reports/speech_v5_gate_failure_review_adapter_surface_cleaner_2026-05-20.json`

Failure review:

- failures: 0 / 225
- pass rate: 1.0

## Meaning

The strict surface-prefix failure can be controlled by narrow stable decoding and cleanup.

However, manual samples still show weak semantic completion. The adapter is cleaner at the surface, but it still needs a direct-completion repair pass before being treated as V5-native human-facing speech.

## Boundary

This is not a checkpoint improvement.

This is not proof of mature fluency.

This does not erase the manual transcript finding that answer quality remains uneven.

This does not claim AGI, human-equivalent cognition, or full LLM replacement.

## Next Step

Run a bounded direct-completion repair training pass using:

- `tools/build_speech_surface_quality_dataset.py`
- `datasets/hf_local/SPEECH_SURFACE_QUALITY_V1.jsonl`

Then rerun the strict surface gate and manually sample the new transcript.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
