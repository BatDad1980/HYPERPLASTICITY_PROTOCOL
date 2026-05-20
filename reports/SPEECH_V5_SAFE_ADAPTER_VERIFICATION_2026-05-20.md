# HPP V2 V5-Safe Language Adapter Verification

Date: 2026-05-20

## Purpose

Package the passing HPP V2 language behavior behind a V5-safe adapter candidate and verify it against the same held-out V5 language gate.

The adapter is not a V5-native import.

It is a controlled bridge for review.

## Setup

- Adapter: `core/v5_language_adapter.py`
- Gate evaluator: `tools/speech_v5_language_gate.py`
- Failure analyzer: `tools/analyze_v5_language_gate_failures.py`
- Checkpoint: `checkpoints/hpp_speech_identity_containment_v1.pth`
- Prompt suite: `datasets/hf_local/SPEECH_HELDOUT_V5_GATE_V1.jsonl`
- Power mode: plugged
- Seeds: 14, 21, 28
- Profile: stable through adapter

The adapter forces the current safe path:

- stable speech profile
- bounded token count
- identity/protection phrase blocking
- explicit checkpoint loading
- raw V2 speech remains separate

## Adapter Gate Result

Artifact:

- `reports/speech_v5_language_gate_adapter_identity_containment_v1_2026-05-20.json`

Stable adapter profile:

- evaluations: 225
- pass count: 217
- pass rate: 0.9644
- mean loop score: 0.7067
- max loop score: 6
- format leak total: 1
- mode label total: 7
- identity spiral total: 5
- repeated sentence total: 0

Decision:

**Adapter path passes the current V5 language gate.**

Boundary:

This is a stable-only adapter run. Raw-vs-stable comparison is already documented in the two-profile gate artifact.

## Failure Review

Artifacts:

- `reports/SPEECH_V5_GATE_FAILURE_REVIEW_2026-05-20.md`
- `reports/speech_v5_gate_failure_review_identity_containment_v1_tight_stable_2026-05-20.json`

Remaining failures:

- failures: 8 / 225
- pass rate: 0.9644
- failure reasons:
  - mode label echo: 7
  - format leak: 1

Primary remaining phrase:

- `protective mode`

Meaning:

The identity spiral problem is controlled under the current gate. The main remaining issue is a narrow mode-label echo where outputs mention `protective mode`.

## Meaning

The language layer now has three useful pieces of evidence:

1. Raw-vs-stable gate shows stable profile is better than raw.
2. Identity containment gate shows stable profile passes all current V5 language targets.
3. Adapter gate shows the passing behavior can be packaged behind a reviewable V5-safe interface.

This is enough to begin V5 integration review as an adapter candidate.

It is not enough to declare mature fluency.

## Next Step

For the next pass:

1. Add `protective mode` to stable phrase blocking or train a small mode-label echo repair.
2. Rerun adapter gate.
3. If pass rate improves without new regressions, document a V5 adapter import plan.
4. Keep raw V2 speech as research-only.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
