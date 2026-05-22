# HPP V2 Decode Selector Probes

Date: 2026-05-22

Branch: HPP V2 wild lab

Purpose: test whether decode-only answer-start selection can improve semantic recovery without additional training or wrapper contamination.

Boundary: diagnostic only. No checkpoint promotion.

## First-Token Selector

Tool: `tools/speech_decode_first_token_selector_probe.py`

Checkpoint: `checkpoints/hpp_speech_exposure_bias_bridge_v1.pth`

Artifact: `SPEECH_DECODE_FIRST_TOKEN_SELECTOR_EXPOSURE_BIAS_BRIDGE_V1_2026-05-22.md`

Results:

- no selected token: `0/75`
- unrestricted top-1 token: `0/75`
- global answer-token pool: `3/75`
- mode answer-token pool: `2/75`
- oracle first token: `2/75`

Meaning: choosing only the first token is not enough. Even oracle first-token release stays weak.

## Five-Token Oracle Baseline

Tool: `tools/speech_answer_start_release_probe.py`

Artifacts:

- `SPEECH_ANSWER_START_RELEASE_EXPOSURE_BIAS_BRIDGE_V1_2026-05-22.md`
- `SPEECH_ANSWER_START_RELEASE_GENERATED_PREFIX_RECOVERY_V1_2026-05-22.md`

Results:

- exposure-bias bridge V1 force-5: `50/75`
- generated-prefix recovery V1 force-5: `51/75`

Meaning: the answer path is much more stable when the first five correct answer tokens are supplied.

## Sequence Selector

Tool: `tools/speech_decode_answer_start_sequence_selector_probe.py`

Full run was too expensive in parallel, so the diagnostic was reduced to `15` prompts.

Exposure-bias bridge V1:

- 3-token global sequence pool: `0/15`
- 3-token mode sequence pool: `1/15`
- 3-token oracle sequence: `3/15`
- 5-token global sequence pool: `0/15`
- 5-token mode sequence pool: `1/15`
- 5-token oracle sequence: `11/15`

Generated-prefix recovery V1:

- 3-token global sequence pool: `0/15`
- 3-token mode sequence pool: `1/15`
- 3-token oracle sequence: `2/15`
- 5-token global sequence pool: `0/15`
- 5-token mode sequence pool: `1/15`
- 5-token oracle sequence: `11/15`

Meaning: short answer starts work when they are the correct starts, but the model-scored candidate pool does not select the correct start reliably.

## Manual Pattern

Common wrong selected starts:

- `I am a`
- `I will answer`
- `We do not`
- `Masamune`

These are generic high-probability starts, not prompt-bound starts.

## Decision

Decode-only selection by local token probability is not enough.

Do not train another answer wrapper.

Do not promote any checkpoint.

The next target is prompt-to-start binding, not answer-start probability alone.

## Next Target

Build a retrieval-style answer-start binding diagnostic:

1. Embed prompt and candidate prompts.
2. Select the answer-start sequence from the nearest prompt, not from next-token probability.
3. Release generation after the retrieved 5-token start.
4. Compare retrieved-start result against oracle force-5 and probability-selected force-5.
5. If retrieval-start approaches oracle-start behavior without surface leaks, the next architecture idea is context-aware memory/retrieval before speech generation.

Not training. Not hype. Just telemetry.

Grow first. Reuse depth.
