# HPP V2 Answer-Start Release Probe

Date: 2026-05-22

Branch: HPP V2 wild lab

Purpose: test whether forcing the first few correct answer tokens can keep free generation on the semantic path.

Boundary: diagnostic only. This does not promote any checkpoint.

## Setup

Tool: `tools/speech_answer_start_release_probe.py`

Checkpoints:

- `checkpoints/hpp_speech_exposure_bias_bridge_v1.pth`
- `checkpoints/hpp_speech_generated_prefix_recovery_v1.pth`

Method:

1. Format each prompt as `Question: ... Answer:`
2. Force `0`, `1`, `2`, `3`, or `5` expected answer tokens into the input.
3. Release the model into normal `semantic_short` generation.
4. Score the forced prefix plus generated continuation against the expected answer.

## Exposure-Bias Bridge V1 Result

Artifact: `SPEECH_ANSWER_START_RELEASE_EXPOSURE_BIAS_BRIDGE_V1_2026-05-22.md`

- force `0` token(s): `0/75`
- force `1` token(s): `2/75`
- force `2` token(s): `4/75`
- force `3` token(s): `9/75`
- force `5` token(s): `50/75`

## Generated-Prefix Recovery V1 Result

Artifact: `SPEECH_ANSWER_START_RELEASE_GENERATED_PREFIX_RECOVERY_V1_2026-05-22.md`

- force `0` token(s): `0/75`
- force `1` token(s): `1/75`
- force `2` token(s): `3/75`
- force `3` token(s): `9/75`
- force `5` token(s): `51/75`

## Meaning

The answer path is reachable when the first few answer tokens are stabilized.

This explains the previous pattern:

- teacher-forced token ranks are strong
- free generation is weak
- bad-prefix recovery wrappers do not solve it
- five correct answer-start tokens recover semantic scoring on about two-thirds of prompts

This is not fluency. It is a diagnostic result showing that early answer-start selection is a critical failure point.

## Decision

Do not promote any checkpoint.

Do not keep training generic recovery wrappers as ordinary text.

The next useful target is answer-start stabilization: teach or constrain the model to select the first few answer tokens reliably, then release generation.

## Next Target

Build `SPEECH_ANSWER_START_STABILIZATION_V1`:

1. Train short answer-start rows where the target is only the first 3 to 5 answer tokens.
2. Keep response-only loss.
3. Avoid long recovery wrapper text.
4. Evaluate answer-start release again.
5. Only continue if force-0, force-1, or force-2 semantic pass improves without surface regression.

Not training. Not hype. Just telemetry.

Grow first. Reuse depth.
