# HPP V2 Speech Exposure-Bias Bridge V1

Date: 2026-05-21

Branch: HPP V2 wild lab

Purpose: test whether a small recovery curriculum can help speech recover from imperfect generated prefixes without breaking the strict surface gate.

Boundary: diagnostic only. Do not promote `hpp_speech_exposure_bias_bridge_v1.pth`.

## Setup

- Base checkpoint: `checkpoints/hpp_speech_prompt_binding_domain_all_v1.pth`
- New local checkpoint: `checkpoints/hpp_speech_exposure_bias_bridge_v1.pth`
- Dataset: `datasets/hf_local/SPEECH_EXPOSURE_BIAS_BRIDGE_V1.jsonl`
- Samples: `375`
- Curriculum variants per target answer:
  - clean prompt only
  - prompt plus first correct token
  - prompt plus imperfect plausible prefix
  - prompt plus generic bad prefix
  - prompt plus explicit recovery instruction
- Training steps: `900`
- Batch: `2`
- Seq len: `144`
- Learning rate: `1e-5`
- Domain strategy: `all`
- CUDA OOM events: `0`

## Strict Surface Gate

Artifact: `speech_v5_language_gate_exposure_bias_bridge_v1_2026-05-21.json`

- stable pass: `225/225`
- pass rate: `1.0`
- mean loop score: `0.1689`
- max loop score: `4`
- format leaks: `0`
- surface prefix hits: `0`
- identity spiral hits: `0`
- repeated sentence hits: `0`

Meaning: surface stability held.

## Semantic Free-Generation Gate

Artifact: `SPEECH_SEMANTIC_QUALITY_REVIEW_EXPOSURE_BIAS_BRIDGE_V1_2026-05-21.md`

- semantic pass: `6/225`
- prior domain-all auto-route semantic pass: `2/225`
- prior domain-all forced-conversation semantic pass: `4/225`

Meaning: free-generation semantic score moved above the old `3/225` floor, but not enough to count as reliable prompt binding.

## Prompt-Binding Probe

Artifact: `SPEECH_PROMPT_BINDING_PROBE_EXPOSURE_BIAS_BRIDGE_V1_SEMANTIC_SHORT_2026-05-21.md`

- total semantic pass: `0/35`
- all prompt wrappers remained `0/5`

Meaning: the small five-prompt binding probe did not improve.

## Recovery Probe

Artifact: `SPEECH_EXPOSURE_BIAS_RECOVERY_PROBE_EXPOSURE_BIAS_BRIDGE_V1_2026-05-21.md`

Compared with `domain_all_v1`, bad-prefix format leakage improved:

- explicit recovery instruction format leaks: `1` to `0`
- generic bad prefix format leaks: `1` to `0`

Semantic recovery did not improve:

- clean prompt: `1/75`
- first correct token: `0/75`
- plausible imperfect prefix: `0/75`
- generic bad prefix: `0/75`
- explicit recovery instruction: `0/75`

Manual samples still show generic local attractors:

- `answer should ...`
- `a local AI should ...`
- `do not know answer should ...`
- `It should be answer should ...`

Meaning: the recovery curriculum reduced some surface artifacts around bad prefixes, but it did not produce measurable semantic recovery.

## Teacher-Forced Signal

Artifact: `SPEECH_ANSWER_PREFIX_CONTINUATION_EXPOSURE_BIAS_BRIDGE_V1_2026-05-21.md`

All-token top-100 expected-answer rate:

- conversation: `0.9291`
- logic: `0.7318`
- identity: `0.7666`
- synthesis: `0.7774`
- none: `0.9226`

Compared with `domain_all_v1`:

- conversation: `0.9158` to `0.9291`
- logic: `0.6564` to `0.7318`
- identity: `0.6979` to `0.7666`
- synthesis: `0.7556` to `0.7774`
- none: `0.9107` to `0.9226`

Meaning: the correct answer path strengthened under teacher forcing, especially in routed domains.

## Prompt Signal Probe

Artifact: `SPEECH_PROMPT_SIGNAL_PROBE_EXPOSURE_BIAS_BRIDGE_V1_2026-05-21.md`

Expected first-token top-100 rate:

- conversation: `0.76`
- logic: `0.4667`
- identity: `0.5467`
- none: `0.7067`

Compared with `domain_all_v1`:

- conversation: `0.76` to `0.76`
- logic: `0.24` to `0.4667`
- identity: `0.3867` to `0.5467`
- none: `0.68` to `0.7067`

Meaning: internal first-token prompt signal improved in `logic` and `identity`, but free generation still derails.

## Decision

Do not promote.

Exposure-bias bridge V1 is a useful diagnostic checkpoint, not a speech candidate.

The current best diagnosis is still autoregressive derailment from generic attractors. The answer rails are stronger under teacher forcing, but the model does not yet recover semantically after its own imperfect prefixes.

## Next Target

The next bridge should train on model-generated bad prefixes rather than hand-written bad prefixes.

Recommended next diagnostic:

1. Generate bad prefixes from the current checkpoint for each held-out prompt.
2. Build a recovery dataset from those exact generated prefixes.
3. Train only a small continuation repair pass.
4. Re-run recovery probe and semantic gate.
5. Keep promotion blocked unless recovery variants improve above zero and free semantic pass improves meaningfully.

Not training. Not hype. Just telemetry.

Grow first. Reuse depth.
