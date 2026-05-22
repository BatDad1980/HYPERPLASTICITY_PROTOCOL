# HPP V2 Retrieval Answer-Start Probe

Date: 2026-05-22

Branch: HPP V2 wild lab

Purpose: test whether context-aware prompt memory can supply the first five answer tokens more reliably than local next-token probability.

Boundary: diagnostic only. No checkpoint promotion.

## Setup

Tool: `tools/speech_retrieval_answer_start_probe.py`

Checkpoint: `checkpoints/hpp_speech_exposure_bias_bridge_v1.pth`

Method:

1. Encode the current prompt into an HPP prompt vector.
2. Retrieve the nearest remembered prompt.
3. Insert the remembered answer's first five tokens.
4. Release normal `semantic_short` generation.
5. Score the selected start plus generated continuation.

Two retrieval modes were tested:

- `retrieval_exact_memory`: memory contains the current prompt.
- `retrieval_leave_one_out`: current prompt is excluded.

## Result

Artifact: `SPEECH_RETRIEVAL_ANSWER_START_EXPOSURE_BIAS_BRIDGE_V1_2026-05-22.md`

- exact memory: `49/75`
- leave-one-out: `2/75`
- exact memory oracle-start match: `0.9867`
- leave-one-out oracle-start match: `0.0`
- exact memory format leaks: `1`
- leave-one-out format leaks: `0`

## Meaning

This is the strongest clean diagnostic result so far.

It does not prove general speech fluency. Leave-one-out retrieval collapses, so the model is not generalizing answer starts from nearby prompts yet.

It does show that when context-aware memory supplies the right answer start, free generation can stay semantically scorable on most prompts. This matches the force-5 oracle result:

- force-5 oracle start: about `50/75` to `51/75`
- retrieval exact memory start: `49/75`

The failure is therefore not just missing answer memory. The major failure is selecting the right answer start for the prompt.

## Manual Pattern

Probability-selected starts chose generic high-probability fragments:

- `I am a`
- `I will answer`
- `We do not`
- `Masamune`

Retrieval-selected starts chose prompt-bound starts when memory matched:

- `Check power, temperature,`
- `I will rewrite it as`
- `The stable profile reduced loops`

## Decision

Do not promote.

Do not train another wrapper-heavy checkpoint.

The next architecture target should be context-aware memory before speech generation:

- prompt memory
- answer-start retrieval
- bounded release
- surface gate after retrieval

## Next Target

Build a cleaner retrieval gate:

1. Use exact-key retrieval first as a controlled diagnostic baseline.
2. Then test paraphrase/held-out prompt retrieval separately.
3. Keep answer-start retrieval outside the trained checkpoint until it proves surface-safe.
4. Compare against V5 standards only after the retrieval path has full transcripts and semantic review.

Not training. Not hype. Just telemetry.

Grow first. Reuse depth.
