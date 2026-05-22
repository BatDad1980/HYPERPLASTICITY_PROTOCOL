# HPP V2 Retrieval Language Gate

Date: 2026-05-22

Branch: HPP V2 wild lab

Purpose: test exact-key prompt memory as a runtime speech scaffold.

Boundary: diagnostic only. This is not general language fluency and does not promote any checkpoint.

## Setup

Tool: `tools/speech_retrieval_language_gate.py`

Checkpoint: `checkpoints/hpp_speech_exposure_bias_bridge_v1.pth`

Method:

1. Exact-match prompt lookup from the known HPP V2 speech memory rows.
2. Retrieve the expected answer's first five tokens.
3. Insert those five tokens before free generation.
4. Score the retrieved start plus generated continuation.
5. Save full transcripts and surface/semantic metrics.

Seeds: `11`, `22`, `33`

Prompt count: `75`

Total scored runs: `225`

## Result

Artifact: `SPEECH_RETRIEVAL_LANGUAGE_GATE_EXPOSURE_BIAS_BRIDGE_V1_2026-05-22.md`

- surface pass: `222/225`
- semantic pass: `156/225`
- semantic pass rate: `0.6933`
- mean loop score: `1.64`
- max loop score: `6`
- format leaks: `3`
- identity spiral hits: `0`
- retrieval misses: `0`

By mode:

- plain: `34/45`
- technical: `33/45`
- protective: `27/45`
- identity: `30/45`
- embodiment: `32/45`

## Comparison

Same checkpoint without retrieval:

- strict surface gate: `225/225`
- semantic free-generation gate: `6/225`

With exact-key retrieval start:

- retrieval surface gate: `222/225`
- retrieval semantic gate: `156/225`

Meaning: exact prompt memory plus five-token answer start produced a large semantic improvement while mostly preserving surface behavior.

## Boundary

This is exact-key retrieval, not held-out paraphrase generalization.

This is not a V5-native language claim.

This does not prove mature conversational fluency.

It does support a narrower architecture finding: HPP V2 speech benefits strongly when context-aware memory supplies the correct answer start before free generation.

## Failure Pattern

Remaining failures still show autoregressive derailment after the retrieved start:

- `answer should ...`
- `a local AI should ...`
- repeated generic safety/action fragments
- partial hits without full answer completion

The start often lands correctly, but the continuation still drifts.

## Decision

Do not promote.

Keep `hpp_speech_exposure_bias_bridge_v1.pth` diagnostic-only.

Keep retrieval as an external scaffold until it passes held-out/paraphrase gates.

## Next Target

Build a paraphrase retrieval diagnostic:

1. Create paraphrase prompts for each known answer.
2. Keep the exact-key answer memory hidden behind the paraphrase.
3. Retrieve nearest prompt memory by embedding similarity.
4. Insert five-token answer start.
5. Run the same retrieval language gate.

Success is not fluency. Success is whether paraphrase retrieval can approach exact-key retrieval without surface regression.

Not training. Not hype. Just telemetry.

Grow first. Reuse depth.
