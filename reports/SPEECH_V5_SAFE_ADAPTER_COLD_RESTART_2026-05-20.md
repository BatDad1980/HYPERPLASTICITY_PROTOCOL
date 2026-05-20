# HPP V2 V5-Safe Language Adapter Cold Restart

Date: 2026-05-20

## Purpose

Verify that the clean V5-safe adapter language pass survives a fresh process and fresh CUDA context.

The prior clean pass showed zero failures after narrow stable decoder blocking. This run checks whether that result repeats without relying on a warmed-up interpreter or prior engine state.

## Setup

- Adapter: `core/v5_language_adapter.py`
- Checkpoint: `checkpoints/hpp_speech_identity_containment_v1.pth`
- Gate evaluator: `tools/speech_v5_language_gate.py`
- Held-out suite: `datasets/hf_local/SPEECH_HELDOUT_V5_GATE_V1.jsonl`
- Power mode: plugged
- Seeds: 14, 21, 28
- Profile: stable adapter path
- Run type: cold restart / fresh process

Command:

```powershell
python tools\speech_v5_language_gate.py --checkpoint checkpoints\hpp_speech_identity_containment_v1.pth --label v5_safe_adapter_identity_containment_v1_cold_restart --power-mode plugged --profiles stable --seeds 14 21 28 --use-v5-adapter --json-out reports\speech_v5_language_gate_adapter_cold_restart_2026-05-20.json
```

## Result

Artifact:

- `reports/speech_v5_language_gate_adapter_cold_restart_2026-05-20.json`

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

Failure review artifacts:

- `reports/SPEECH_V5_GATE_FAILURE_REVIEW_ADAPTER_COLD_RESTART_2026-05-20.md`
- `reports/speech_v5_gate_failure_review_adapter_cold_restart_2026-05-20.json`

Failure review:

- failures: 0 / 225
- pass rate: 1.0

## Meaning

The clean adapter pass repeated after cold restart.

This strengthens the adapter path as a measurable candidate for V5-side review because the result is no longer just a single warm-session artifact.

## Boundary

This is still an adapter result, not raw V2 speech.

This does not prove mature fluency.

This does not automatically promote the checkpoint into V5.

This does not claim AGI, human-equivalent cognition, or full LLM replacement.

## Next Step

Create the V5-side adapter import plan before touching `X:\HPP_V5`.

Recommended next evidence item:

1. Manual transcript review on the cold-restart artifact.
2. Small V5 integration plan with import boundary, privacy boundary, and test expectations.
3. Only then decide whether V5 should consume the adapter as a candidate interface.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
