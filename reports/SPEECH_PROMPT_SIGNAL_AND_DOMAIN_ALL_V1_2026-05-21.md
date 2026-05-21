# HPP V2 Speech Prompt Signal And Domain-All Diagnostic

Date: 2026-05-21

Branch: HPP V2 wild lab

Purpose: test whether weak semantic prompt binding is caused by missing internal prompt signal, domain routing mismatch, or autoregressive speech collapse.

Boundary: diagnostic only. Do not promote `identity_containment_v2`, `identity_containment_v3`, `prompt_binding_contrastive_v1`, or `domain_all_v1` from these results.

## Setup

- Base checkpoint: `checkpoints/hpp_speech_prompt_binding_contrastive_v1.pth`
- New local checkpoint: `checkpoints/hpp_speech_prompt_binding_domain_all_v1.pth`
- Dataset: `datasets/hf_local/SPEECH_PROMPT_BINDING_CONTRASTIVE_V1.jsonl`
- Training command used `--domain-strategy all`
- Steps: `800`
- Batch: `2`
- Seq len: `128`
- Learning rate: `1.5e-5`
- CUDA OOM events: `0`

The trainer now supports diagnostic domain-aware training:

- `conversation`: original behavior
- `auto`: train the domain detected from prompt text
- `all`: train `conversation`, `logic`, `identity`, and `synthesis` domain heads

The language gate now supports a diagnostic `--domain` override so auto-routing can be compared against a forced domain without changing checkpoint weights.

## Internal Signal Result

The signal probe does not generate speech. It checks prompt-conditioned vectors and expected-token ranks.

Compared with `prompt_binding_contrastive_v1`, `domain_all_v1` improved internal expected first-token rank:

- `conversation` top-100 first-token rate: `0.68` to `0.76`
- `logic` top-100 first-token rate: `0.0133` to `0.24`
- `identity` top-100 first-token rate: `0.0133` to `0.3867`
- `none` top-100 first-token rate: `0.6133` to `0.68`

Meaning: prompt-conditioned signal is not completely absent. Domain-aware training helped the routed heads recognize the first expected answer token more often.

## Speech Gate Result

Auto-routed `domain_all_v1` stable gate:

- surface pass: `225/225`
- mean loop score: `0.1644`
- format leaks: `0`
- identity spiral hits: `0`
- semantic pass: `2/225`

Forced-conversation stable gate:

- surface pass: `225/225`
- mean loop score: `0.0622`
- format leaks: `0`
- identity spiral hits: `0`
- semantic pass: `4/225`

Prompt-binding probe with `semantic_short` remained `0/35`, including forced `conversation`.

## Teacher-Forced Continuation Result

The answer-prefix continuation probe does not free-generate. It supplies the prompt plus earlier expected answer tokens and measures whether the next expected answer token ranks highly.

`prompt_binding_contrastive_v1` showed strong teacher-forced continuation in `conversation` and `none`, but weak routed-domain continuation:

- `conversation` all-token top-100 rate: `0.9047`
- `logic` all-token top-100 rate: `0.4665`
- `identity` all-token top-100 rate: `0.5254`
- `none` all-token top-100 rate: `0.8702`

`domain_all_v1` improved routed-domain teacher-forced continuation:

- `conversation` all-token top-100 rate: `0.9158`
- `logic` all-token top-100 rate: `0.6564`
- `identity` all-token top-100 rate: `0.6979`
- `synthesis` all-token top-100 rate: `0.7556`
- `none` all-token top-100 rate: `0.9107`

Meaning: the answer path exists more strongly under teacher forcing than in free generation.

## Meaning

Domain routing was part of the failure, but not the whole failure.

The checkpoint now has stronger internal first-token pressure, especially in `logic` and `identity`, but autoregressive speech still collapses into generic answer-shapes:

- `answer should ...`
- `a local AI should ...`
- `do not know answer should ...`
- `checkpoint ... local ... measured ...`

This is not a V5-native speech candidate.

The best current diagnosis is exposure-bias/autoregressive derailment: the model can stay closer to expected answer tokens when kept on the correct answer path, but its own generated tokens quickly pull it toward generic local attractors.

## Boundary

This is not model fluency.

This is not a successful semantic binding result.

This is not a buyer-facing claim.

The only positive result is diagnostic: internal prompt signal improved in the routed heads without an OOM or surface regression.

## Next Target

Stop relying on ordinary free-generation training alone. The next repair target should be an exposure-bias bridge:

1. Train or probe short self-repair continuations from corrupted/generated answer prefixes.
2. Compare teacher-forced rank, one-token generated prefix, and free generation on the same prompts.
3. Penalize generic attractors like `answer should`, `a local AI should`, and `do not know answer should` in training data, not only at decode time.
4. Preserve clean surface gates, but require semantic pass above the `3/225` floor before promotion.

Not training. Not hype. Just telemetry.

Grow first. Reuse depth.
