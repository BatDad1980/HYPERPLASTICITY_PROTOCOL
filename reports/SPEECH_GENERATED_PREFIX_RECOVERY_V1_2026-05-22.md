# HPP V2 Generated-Prefix Recovery V1

Date: 2026-05-22

Branch: HPP V2 wild lab

Purpose: train recovery from Hepp's own generated bad prefixes instead of hand-written bad prefixes.

Boundary: diagnostic only. Do not promote `hpp_speech_generated_prefix_recovery_v1.pth`.

## Setup

- Source checkpoint for bad-prefix generation: `checkpoints/hpp_speech_exposure_bias_bridge_v1.pth`
- New local checkpoint: `checkpoints/hpp_speech_generated_prefix_recovery_v1.pth`
- Dataset: `datasets/hf_local/SPEECH_GENERATED_PREFIX_RECOVERY_V1.jsonl`
- Source drafts: `150`
- Source drafts already passing semantic review: `1`
- Training rows: `447`
- Training steps: `1000`
- Batch: `2`
- Seq len: `160`
- Learning rate: `8e-6`
- Domain strategy: `all`
- CUDA OOM events: `0`

The generated bad prefixes were real model failures, including patterns like:

- `It should answer should ...`
- `answer should move`
- `do not know answer should ...`
- `measuredIt ...`

## Strict Surface Gate

Artifact: `speech_v5_language_gate_generated_prefix_recovery_v1_2026-05-22.json`

- stable pass: `224/225`
- pass rate: `0.9956`
- mean loop score: `0.0978`
- max loop score: `3`
- format leaks: `2`
- surface prefix hits: `0`
- identity spiral hits: `0`

Meaning: loop behavior improved, but surface cleanliness regressed from the previous perfect `225/225` and `0` format leaks.

## Semantic Free-Generation Gate

Artifact: `SPEECH_SEMANTIC_QUALITY_REVIEW_GENERATED_PREFIX_RECOVERY_V1_2026-05-22.md`

- semantic pass: `4/225`
- prior exposure-bias bridge V1 semantic pass: `6/225`

Meaning: semantic free generation regressed.

## Recovery Probe

Artifact: `SPEECH_EXPOSURE_BIAS_RECOVERY_PROBE_GENERATED_PREFIX_RECOVERY_V1_2026-05-22.md`

- clean prompt: `0/75`
- first correct token: `1/75`
- plausible imperfect prefix: `0/75`
- generic bad prefix: `0/75`
- explicit recovery instruction: `0/75`
- format leaks: `0`
- identity spirals: `0`

Meaning: generated-prefix recovery did not produce meaningful semantic recovery. It only created one small first-token continuation pass.

## Prompt-Binding Probe

Artifact: `SPEECH_PROMPT_BINDING_PROBE_GENERATED_PREFIX_RECOVERY_V1_SEMANTIC_SHORT_2026-05-22.md`

- total semantic pass: `0/35`
- all prompt wrappers remained `0/5`

Meaning: the focused binding probe did not improve.

## Teacher-Forced Signal

Artifact: `SPEECH_ANSWER_PREFIX_CONTINUATION_GENERATED_PREFIX_RECOVERY_V1_2026-05-22.md`

All-token top-100 expected-answer rate:

- conversation: `0.9446`
- logic: `0.7747`
- identity: `0.8016`
- synthesis: `0.8169`
- none: `0.9381`

Compared with exposure-bias bridge V1:

- conversation: `0.9291` to `0.9446`
- logic: `0.7318` to `0.7747`
- identity: `0.7666` to `0.8016`
- synthesis: `0.7774` to `0.8169`
- none: `0.9226` to `0.9381`

Meaning: internal teacher-forced answer rails strengthened again.

## Prompt Signal Probe

Artifact: `SPEECH_PROMPT_SIGNAL_PROBE_GENERATED_PREFIX_RECOVERY_V1_2026-05-22.md`

Expected first-token top-100 rate:

- conversation: `0.7733`
- logic: `0.4933`
- identity: `0.6`
- none: `0.7467`

Compared with exposure-bias bridge V1:

- conversation: `0.76` to `0.7733`
- logic: `0.4667` to `0.4933`
- identity: `0.5467` to `0.6`
- none: `0.7067` to `0.7467`

Meaning: prompt-conditioned first-token pressure improved internally, especially in identity.

## Decision

Do not promote.

Generated-prefix recovery V1 strengthened hidden token ranking while worsening or failing the behavior that matters:

- surface gate slipped from `225/225` to `224/225`
- semantic gate fell from `6/225` to `4/225`
- recovery stayed near zero

This confirms the failure is not just lack of answer memory. The model can rank the right answer tokens when constrained, but free generation remains captured by generic attractors.

## Answer-Start Release Follow-Up

Artifact: `SPEECH_ANSWER_START_RELEASE_2026-05-22.md`

Forcing the first answer tokens produced a strong diagnostic signal:

- exposure-bias bridge V1 force-5: `50/75`
- generated-prefix recovery V1 force-5: `51/75`
- both checkpoints force-3: `9/75`

Meaning: the correct answer path becomes much more stable when the first few answer tokens are supplied. The next repair target should be answer-start stabilization, not more recovery-wrapper training.

## Next Target

Stop training recovery wrappers as ordinary text.

Next diagnostic should change the decoding/training interface:

1. Train short answer-start rows where the target is only the first 3 to 5 answer tokens.
2. Avoid long recovery-wrapper text.
3. Re-run answer-start release.
4. Continue only if force-0, force-1, or force-2 improves without surface regression.

Not training. Not hype. Just telemetry.

Grow first. Reuse depth.
