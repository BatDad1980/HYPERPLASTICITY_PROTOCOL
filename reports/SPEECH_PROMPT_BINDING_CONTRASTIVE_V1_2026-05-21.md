# HPP V2 Prompt Binding Contrastive V1

Date: 2026-05-21

## Purpose

Test whether contrastive prompt-binding data improves semantic answer selection.

Prior evidence showed:

- surface/loop gates can pass while answers remain wrong
- tiny overfit training can store answer phrases
- answer memories cross-contaminate across prompts

This run tested whether explicit similar-prompt contrastive examples improve binding.

## Setup

- Dataset builder: `tools/build_speech_prompt_binding_contrastive_dataset.py`
- Dataset: `datasets/hf_local/SPEECH_PROMPT_BINDING_CONTRASTIVE_V1.jsonl`
- Samples: 525
- Base checkpoint: `checkpoints/hpp_speech_identity_containment_v1.pth`
- Output checkpoint: `checkpoints/hpp_speech_prompt_binding_contrastive_v1.pth`
- Trainer: `tools/train_speech_cleanup_balanced.py`
- Training mode: response-only direct completion
- Steps: 900
- Batch: 2
- Sequence length: 128
- Learning rate: 2e-5
- Power mode: plugged

Training completed without CUDA OOM.

Final reported loss:

- step 900: 2.7575

## Baseline Probe

Baseline checkpoint:

- `checkpoints/hpp_speech_identity_containment_v1.pth`

Probe:

- `reports/SPEECH_PROMPT_BINDING_PROBE_IDENTITY_V1_SEMANTIC_SHORT_BASELINE_2026-05-21.md`

Result:

- semantic-short binding probe: 0 / 35

## Contrastive Checkpoint Probe

Checkpoint:

- `checkpoints/hpp_speech_prompt_binding_contrastive_v1.pth`

Semantic-short probe:

- `reports/SPEECH_PROMPT_BINDING_PROBE_CONTRASTIVE_V1_SEMANTIC_SHORT_2026-05-21.md`
- result: 0 / 35

Stable probe:

- `reports/SPEECH_PROMPT_BINDING_PROBE_CONTRASTIVE_V1_STABLE_2026-05-21.md`
- result: 0 / 35

## Full Gate Result

Strict/surface gate artifact:

- `reports/speech_v5_language_gate_prompt_binding_contrastive_v1_2026-05-21.json`

Surface/loop result:

- evaluations: 225
- pass count: 223
- pass rate: 0.9911
- mean loop score: 0.1022
- max loop score: 6
- format leak total: 0
- surface prefix total: 0
- mode label total: 0
- identity spiral total: 0
- repeated sentence total: 0

Semantic review:

- `reports/SPEECH_SEMANTIC_REVIEW_PROMPT_BINDING_CONTRASTIVE_V1_2026-05-21.md`
- semantic pass: 3 / 225
- semantic pass rate: 0.0133

## Meaning

The contrastive V1 run improved surface cleanliness but did not improve semantic prompt binding.

This does not meet the success condition.

Success required:

1. surface gate stays clean
2. semantic prompt-binding pass improves meaningfully above 3 / 225

Result:

- surface gate: pass
- semantic binding: fail / no improvement

## Diagnosis

More contrastive data in the current training path is not enough.

The current trainable speech slice can reduce visible instability, but it still does not reliably connect prompt meaning to the correct answer.

Likely next technical targets:

- inspect whether the trainable modules receive enough prompt-conditioned signal
- test a wider trainable slice
- test a tiny supervised classifier/router before language generation
- test retrieval-scaffolded answer selection as a safety bridge
- inspect prompt embeddings before and after the University stack

## Boundary

Do not promote `hpp_speech_prompt_binding_contrastive_v1.pth`.

Do not claim speech readiness from surface-only pass.

Do not claim mature fluency, AGI, human-equivalent cognition, or LLM replacement.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
