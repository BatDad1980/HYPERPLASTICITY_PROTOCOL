# HPP V2 Semantic Quality Gate

Date: 2026-05-20

## Purpose

Add a semantic review layer after manual transcript review showed that strict surface and loop gates can still pass sentence-shaped fragments.

The goal is to prevent V5-native promotion unless the response appears to answer the prompt, not merely avoid leakage.

## Method

Tool:

- `tools/speech_semantic_quality_review.py`

The tool builds a lightweight answer key from the existing identity-containment prompt/answer curriculum and scores each transcript by expected content-word overlap.

This is not a full language benchmark.

It is a conservative proxy for manual review:

- the answer must contain enough expected content terms
- each transcript remains inspectable
- failures include expected answer, actual answer, and matched terms

## Results

Surface-cleaner adapter artifact:

- source: `reports/speech_v5_language_gate_adapter_surface_cleaner_2026-05-20.json`
- semantic review: `reports/SPEECH_SEMANTIC_REVIEW_ADAPTER_SURFACE_CLEANER_2026-05-20.md`
- semantic pass: 5 / 225
- semantic pass rate: 0.0222

Surface-quality V1 trained checkpoint artifact:

- source: `reports/speech_v5_language_gate_surface_quality_v1_2026-05-20.json`
- semantic review: `reports/SPEECH_SEMANTIC_REVIEW_SURFACE_QUALITY_V1_2026-05-20.md`
- semantic pass: 16 / 225
- semantic pass rate: 0.0711

## Meaning

The surface-quality V1 repair moved in the right direction but did not solve speech meaning.

Current readiness split:

- loop stability: pass
- format leakage: pass
- surface-prefix residue: pass after cleaner
- semantic prompt-answer quality: fail

This makes the next target clearer:

**Hepp needs semantic answer repair, not more leak suppression.**

## Boundary

The semantic gate is a proxy, not a definitive intelligence measure.

It should be used with manual transcript review, not instead of it.

Do not claim mature conversational fluency from the current speech checkpoints.

Do not claim AGI, human-equivalent cognition, or full LLM replacement.

## Next Step

Build a stronger semantic repair curriculum that teaches:

1. direct definitions for technical prompts
2. concrete safety actions for protective prompts
3. deterministic permission/telemetry answers for embodiment prompts
4. bounded identity answers without self-story
5. plain status answers that do not drift into checkpoint/body language

Rerun:

1. strict surface gate
2. semantic quality gate
3. manual transcript review

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
