# HPP V2 Answer-Start Stabilization V1

Date: 2026-05-22

Branch: HPP V2 wild lab

Purpose: test whether short first-answer-token training improves free generation after the answer-start release probe showed a strong force-5 effect.

Boundary: diagnostic only. Do not promote `hpp_speech_answer_start_stabilization_v1.pth`.

## Setup

- Base checkpoint: `checkpoints/hpp_speech_exposure_bias_bridge_v1.pth`
- New local checkpoint: `checkpoints/hpp_speech_answer_start_stabilization_v1.pth`
- Dataset: `datasets/hf_local/SPEECH_ANSWER_START_STABILIZATION_V1.jsonl`
- Samples: `450`
- Target shape: first `3` or `5` answer tokens only
- Training steps: `700`
- Batch: `2`
- Seq len: `96`
- Learning rate: `6e-6`
- Domain strategy: `all`
- CUDA OOM events: `0`

## Answer-Start Release

Artifact: `SPEECH_ANSWER_START_RELEASE_ANSWER_START_STABILIZATION_V1_2026-05-22.md`

- force `0` token(s): `1/75`
- force `1` token(s): `2/75`
- force `2` token(s): `4/75`
- force `3` token(s): `9/75`
- force `5` token(s): `50/75`

Compared with the base exposure-bias bridge V1:

- force `0`: `0/75` to `1/75`
- force `1`: unchanged at `2/75`
- force `2`: unchanged at `4/75`
- force `3`: unchanged at `9/75`
- force `5`: unchanged at `50/75`

Meaning: answer-start stabilization did not meaningfully improve release behavior.

## Strict Surface Gate

Artifact: `speech_v5_language_gate_answer_start_stabilization_v1_2026-05-22.json`

- stable pass: `119/225`
- pass rate: `0.5289`
- mean loop score: `0.1956`
- max loop score: `2`
- format leaks: `106`
- surface prefix hits: `0`
- identity spiral hits: `0`

Meaning: the checkpoint failed the surface gate. The short answer-start rows taught visible answer-format artifacts.

## Semantic Free-Generation Gate

Artifact: `SPEECH_SEMANTIC_QUALITY_REVIEW_ANSWER_START_STABILIZATION_V1_2026-05-22.md`

- semantic pass: `5/225`
- prior exposure-bias bridge V1 semantic pass: `6/225`

Meaning: semantic free generation did not improve.

## Recovery Probe

Artifact: `SPEECH_EXPOSURE_BIAS_RECOVERY_PROBE_ANSWER_START_STABILIZATION_V1_2026-05-22.md`

- clean prompt: `0/75`, format leaks `37`
- first correct token: `1/75`, format leaks `33`
- plausible imperfect prefix: `0/75`, format leaks `32`
- generic bad prefix: `0/75`, format leaks `26`
- explicit recovery instruction: `0/75`, format leaks `30`

Meaning: recovery behavior did not improve and surface artifacts worsened.

## Prompt Signal Probe

Artifact: `SPEECH_PROMPT_SIGNAL_PROBE_ANSWER_START_STABILIZATION_V1_2026-05-22.md`

Expected first-token top-100 rate:

- conversation: `0.7867`
- logic: `0.56`
- identity: `0.6133`
- none: `0.7867`

Compared with generated-prefix recovery V1:

- conversation: `0.7733` to `0.7867`
- logic: `0.4933` to `0.56`
- identity: `0.6` to `0.6133`
- none: `0.7467` to `0.7867`

Meaning: internal first-token ranking improved, but behavior worsened.

## Decision

Do not promote.

Answer-start stabilization V1 is a hard negative result:

- hidden first-token ranking improved
- free semantic behavior did not improve
- answer-start release did not improve
- surface gate failed badly

This suggests ordinary supervised rows with answer-format wrappers are contaminating the speech surface. The model needs either a cleaner generation interface or a trainable objective that improves first-token selection without teaching the wrapper text.

## Next Target

Do not train another wrapper-heavy checkpoint.

Recommended next diagnostic:

1. Add a decode-only first-token selector probe.
2. Pick the best first answer token from the expected-token rank distribution without adding `Answer:` wrapper text to training.
3. Release generation after selected first token.
4. Compare against force-1 and force-5 baselines.
5. Only train again if decode-time selection shows recovery without surface leakage.

Not training. Not hype. Just telemetry.

Grow first. Reuse depth.
