# HPP V2 Retrieval Variant Gate

Date: 2026-05-22

Branch: HPP V2 wild lab

Purpose: test whether retrieval answer-start scaffolding survives light prompt wording changes.

Boundary: diagnostic only. This is not held-out language fluency and does not promote any checkpoint.

## Setup

Tool: `tools/speech_retrieval_variant_gate.py`

Checkpoint: `checkpoints/hpp_speech_exposure_bias_bridge_v1.pth`

Memory: original 75 prompt-answer rows.

Query variants:

- `exact`: original prompt
- `please_answer`: `Please answer this clearly: ...`
- `simple_terms`: `In simple terms, ...`
- `bounded`: `Give a bounded answer to this question: ...`

Method:

1. Encode query variant.
2. Retrieve nearest original prompt memory.
3. Insert retrieved answer's first five tokens.
4. Release normal `semantic_short` generation.
5. Score retrieved start plus generated continuation.

## Result

Artifact: `SPEECH_RETRIEVAL_VARIANT_GATE_EXPOSURE_BIAS_BRIDGE_V1_2026-05-22.md`

Overall:

- total runs: `300`
- semantic pass: `134/300`
- surface pass: `196/300`
- format leaks: `2`
- identity spirals: `0`

By variant:

- exact: semantic `47/75`, retrieval exact-match `0.9467`
- please_answer: semantic `32/75`, retrieval exact-match `0.64`
- simple_terms: semantic `33/75`, retrieval exact-match `0.6267`
- bounded: semantic `22/75`, retrieval exact-match `0.4267`

## Meaning

Retrieval scaffold performance tracks prompt-memory binding.

When the nearest memory is correct, the five-token answer start often helps. When wording changes push retrieval to the wrong memory, the answer start becomes wrong and semantic quality falls.

The speech model is not the only blocker. The memory/retrieval layer must bind prompt variants to the right answer start.

## Boundary

These are light prompt wrappers, not deep paraphrases.

The exact variant is still close to memorized prompts.

The variant failures should not be treated as a failure of the whole HPP idea. They identify the next needed developmental layer: robust prompt-to-memory binding.

## Decision

Do not promote.

Do not train another speech checkpoint yet.

Next work should improve retrieval matching before more speech training.

## Next Target

Build a retrieval memory index with normalized prompt keys:

1. Store original prompt.
2. Store simple normalized variants without answer wrappers.
3. Compare exact string, normalized string, and HPP-vector retrieval.
4. Gate retrieval separately from speech generation.
5. Only run speech after retrieval accuracy is measured.

Not training. Not hype. Just telemetry.

Grow first. Reuse depth.
