# HPP V2 Manual Transcript Review - Cold Restart Adapter Gate

Date: 2026-05-20

## Purpose

Manually review the cold-restart V5-safe adapter transcript after the automated gate passed.

The automated gate checks loops, format leakage, mode labels, identity spiral terms, sentence bounds, and repeated sentences. This review checks the human-facing language quality that the numeric gate can miss.

## Setup

- Source artifact: `reports/speech_v5_language_gate_adapter_cold_restart_2026-05-20.json`
- Checkpoint: `checkpoints/hpp_speech_identity_containment_v1.pth`
- Adapter: `core/v5_language_adapter.py`
- Profile: stable
- Seeds: 14, 21, 28
- Prompt suite: `datasets/hf_local/SPEECH_HELDOUT_V5_GATE_V1.jsonl`
- Total transcripts reviewed: 225

## Automated Result

The cold-restart automated gate passed:

- evaluations: 225
- pass count: 225
- pass rate: 1.0
- mean loop score: 0.6933
- max loop score: 7
- format leak total: 0
- mode label total: 0
- identity spiral total: 5
- repeated sentence total: 0

## Manual Findings

The automated pass is real, but it is not enough for V5-native speech promotion.

Manual review found persistent dataset-wrapper residue and weak sentence coherence:

- outputs beginning with `Response`: 180 / 225
- outputs beginning with `Instruction`: 18 / 225
- average output length: 34.4 words
- common issue: sentence-shaped fragments without reliable semantic completion
- common issue: prompt-adjacent words appear without answering the prompt clearly
- common issue: technical and identity prompts still drift into shop/body/model vocabulary

Mode breakdown:

| Mode | Count | `Response` Prefix | `Instruction` Prefix | Mean Loop | Avg Words |
| --- | ---: | ---: | ---: | ---: | ---: |
| plain | 45 | 36 | 1 | 0.42 | 32.69 |
| technical | 45 | 33 | 4 | 1.27 | 34.96 |
| protective | 45 | 40 | 1 | 0.51 | 35.42 |
| identity | 45 | 34 | 7 | 0.71 | 32.62 |
| embodiment | 45 | 37 | 5 | 0.56 | 36.29 |

## Representative Examples

Prompt:

`Give me a short status update.`

Output:

`Response. It should be answer should a local AI will not have enough and answer experimental a short in robot record the next step at reduced of learning and ask can be wrong, hardware. It is safety limits, but it examples, recursion.`

Review:

Stable and non-looping, but not clean enough for user-facing speech.

Prompt:

`What is a held-out prompt set?`

Output:

`Response a other? What is what is a function from on the same with that. It is it out for dexter neural workshopator in my mind to be memory using its university as through developmental stage it, and school in a physical body.`

Review:

The response remains sentence-shaped but does not reliably define the requested term.

Prompt:

`I feel overloaded and need a grounded answer.`

Output:

`Response a short? I am a saved can be wrong in AI should avoid have a local action. It means of human loops of memory on a safe out, and answer enough. I will figure out the next step.`

Review:

Protective mode is safer than prior loop-heavy speech, but the wording is still too broken for V5-native use.

Prompt:

`What should a robot do before moving?`

Output:

`Response a short? A checkpoint is a saved do not have a enough. It means the current answer should be wrong, and record It is AI will figure out of examples, and an artificial intelligence, and it uses.`

Review:

Embodiment safety intent is present, but the answer does not clearly state the expected safety behavior.

## Meaning

The V2 language adapter has achieved stabilization, not mature speech.

This is still valuable:

- loops are controlled
- format colon leaks are gone
- mode-label echoes are gone
- repeated-sentence failures are gone
- identity spiral is below the current target

But the manual review catches a separate quality gate:

**The adapter is not yet V5-native as a human-facing speech surface because wrapper residue and semantic incoherence remain high.**

## Boundary

This review does not invalidate the cold-restart stability result.

It clarifies the next layer of readiness:

- automated stability gate: pass
- manual language quality gate: hold

This is not a claim of full fluency, AGI, human-equivalent cognition, or LLM replacement.

## Next Step

Recommended next repair target:

1. Add a stricter surface-quality metric for leading wrapper residue such as `Response` and `Instruction`.
2. Build a small response-cleaning dataset that teaches direct answer starts without erasing HPP identity.
3. Rerun the held-out cold-start gate with the stricter metric.
4. Require both automated stability and manual transcript quality before V5-native promotion.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
