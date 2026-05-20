# HPP V2 Strict Surface Language Gate

Date: 2026-05-20

## Purpose

Upgrade the V5 language gate after manual transcript review found leading wrapper residue that the prior automated rubric did not count.

The prior cold-restart adapter run passed the stability gate, but many outputs began with `Response` or `Instruction`. Those prefixes are dataset-wrapper residue, not clean speech.

## Change

The gate now adds a strict surface-prefix metric:

- `leading_response_label`
- `leading_instruction_label`

Any output starting with those labels receives `surface_prefix_residue`.

The target for V5-native speech is:

- max surface prefix hits: 0

## Setup

- Adapter: `core/v5_language_adapter.py`
- Checkpoint: `checkpoints/hpp_speech_identity_containment_v1.pth`
- Gate evaluator: `tools/speech_v5_language_gate.py`
- Held-out suite: `datasets/hf_local/SPEECH_HELDOUT_V5_GATE_V1.jsonl`
- Power mode: plugged
- Seeds: 14, 21, 28
- Profile: stable adapter path

Command:

```powershell
python tools\speech_v5_language_gate.py --checkpoint checkpoints\hpp_speech_identity_containment_v1.pth --label v5_safe_adapter_identity_containment_v1_strict_surface --power-mode plugged --profiles stable --seeds 14 21 28 --use-v5-adapter --json-out reports\speech_v5_language_gate_adapter_strict_surface_2026-05-20.json
```

## Result

Artifact:

- `reports/speech_v5_language_gate_adapter_strict_surface_2026-05-20.json`

Strict stable adapter gate:

- evaluations: 225
- pass count: 27
- pass rate: 0.12
- mean loop score: 0.6933
- max loop score: 7
- format leak total: 0
- surface prefix total: 198
- mode label total: 0
- identity spiral total: 5
- repeated sentence total: 0

Decision:

**Not ready for V5-native speech under the stricter surface-quality gate.**

## Meaning

The previous clean pass remains useful evidence for stabilization:

- loops stayed low
- no colon-style format leaks
- no mode-label echoes
- no repeated-sentence failures
- identity spiral remained below target

The stricter gate adds a better human-facing readiness boundary:

- stable adapter behavior: pass
- V5-native surface quality: fail / hold

This is the correct failure. It tells us the next repair target is direct answer starts and semantic completion, not loop suppression.

## Boundary

This does not erase the cold-restart stability result.

It prevents overclaiming the language adapter as V5-native before the speech surface is clean.

This is not a claim of full fluency, AGI, human-equivalent cognition, or LLM replacement.

## Next Step

Build a response-cleaning repair set focused on:

1. removing leading wrapper residue
2. direct first-word answers
3. one-to-three sentence completion
4. retaining bounded identity and safety language
5. avoiding recursive identity loops

Then run the strict surface gate again.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
