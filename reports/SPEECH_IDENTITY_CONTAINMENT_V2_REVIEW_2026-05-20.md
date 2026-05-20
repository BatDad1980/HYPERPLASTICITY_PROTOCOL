# HPP V2 Identity Containment V2 Review

Date: 2026-05-20

## Purpose

Review the local `hpp_speech_identity_containment_v2.pth` artifact found during cleanup.

## Setup

- Checkpoint: `checkpoints/hpp_speech_identity_containment_v2.pth`
- Gate artifact: `reports/speech_v5_language_gate_adapter_strict_surface_v2.json`
- Semantic review: `reports/SPEECH_SEMANTIC_REVIEW_IDENTITY_CONTAINMENT_V2_2026-05-20.md`
- Profile: stable adapter path
- Seeds: 14, 21, 28

## Strict Surface Result

- evaluations: 225
- pass count: 224
- pass rate: 0.9956
- mean loop score: 1.8178
- max loop score: 10
- format leak total: 0
- surface prefix total: 0
- mode label total: 0
- identity spiral total: 0
- repeated sentence total: 0

## Semantic Review Result

- semantic pass: 3 / 225
- semantic pass rate: 0.0133

## Manual Read

The checkpoint is cleaner on identity spiral and surface residue, but it does not answer prompts reliably.

Representative issue:

Prompt:

`What is a held-out prompt set?`

Output:

`What can do you? A will be hear is a work on the same with that.`

Review:

The output is bounded and non-leaking, but it does not define the requested term.

## Meaning

`hpp_speech_identity_containment_v2.pth` is not recommended for V5-native speech.

It is useful diagnostic evidence:

- identity spiral can be suppressed
- surface residue can stay low
- semantic prompt-answer quality remains the blocker

## Boundary

Do not promote this checkpoint.

Do not treat strict surface pass as fluency.

Do not claim AGI, human-equivalent cognition, or full LLM replacement.

## Next Step

Keep focus on prompt binding and semantic answer selection.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
