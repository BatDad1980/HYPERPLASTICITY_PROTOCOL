# V5 Speech Adapter Import Plan

Date: 2026-05-20

## Purpose

Define the review boundary before HPP V5 consumes any V2 speech adapter behavior.

This is a plan, not an implementation.

## Source Candidate

Source branch:

`C:\Users\Aural\Desktop\Codename HYPERPLASTICITY PROTOCOL\Project_HPP`

Candidate path:

- Adapter: `core/v5_language_adapter.py`
- Checkpoint: `checkpoints/hpp_speech_identity_containment_v1.pth`
- Gate evaluator: `tools/speech_v5_language_gate.py`
- Held-out suite: `datasets/hf_local/SPEECH_HELDOUT_V5_GATE_V1.jsonl`

## Current Evidence

Stability clean pass:

- Report: `reports/SPEECH_V5_SAFE_ADAPTER_CLEAN_PASS_2026-05-20.md`
- Evaluations: `225`
- Pass count: `225`
- Format leaks: `0`
- Mode-label leaks: `0`
- Repeated sentence failures: `0`
- Mean loop score: `0.6933`
- Max loop score: `7`
- Identity spiral total: `5`

Cold restart confirmation:

- Report: `reports/SPEECH_V5_SAFE_ADAPTER_COLD_RESTART_2026-05-20.md`
- Evaluations: `225`
- Pass count: `225`
- Format leaks: `0`
- Mode-label leaks: `0`
- Repeated sentence failures: `0`
- Mean loop score: `0.6933`
- Max loop score: `7`
- Identity spiral total: `5`

Manual transcript review:

- Report: `reports/SPEECH_V5_MANUAL_TRANSCRIPT_REVIEW_COLD_RESTART_2026-05-20.md`
- Outputs beginning with `Response`: `180 / 225`
- Outputs beginning with `Instruction`: `18 / 225`
- Finding: stable outputs are still often not clean human-facing answers

Strict surface-quality gate:

- Report: `reports/SPEECH_V5_STRICT_SURFACE_GATE_2026-05-20.md`
- Evaluations: `225`
- Pass count: `27`
- Surface prefix total: `198`
- Format leaks: `0`
- Mode-label leaks: `0`
- Repeated sentence failures: `0`
- Mean loop score: `0.6933`

Current decision:

- stability gate: pass
- cold restart gate: pass
- strict surface-quality gate: fail / hold

## Import Boundary

V5 may import:

- adapter interface shape
- gate evaluator design
- held-out speech rubric
- transcript logging expectations
- decoder-side safety controls
- stable-profile routing lesson

V5 should not import yet:

- raw V2 speech behavior
- unreviewed checkpoints
- training datasets wholesale
- private or messy V2 development files
- claims of mature fluency
- any AGI / ASI / sentience framing

## Required Repair Before Implementation

Do not implement the V5 speech adapter yet.

The V2 side should first repair:

- leading wrapper residue
- direct first-word answers
- one-to-three sentence completion
- semantic answer completion
- bounded identity language

Then V2 should rerun the strict surface gate.

## Required V5-Side Checks Before Future Implementation

1. Confirm the strict surface-quality gate passes after repair.
2. Review the repaired transcript artifact manually.
3. Define a V5-native speech eval artifact format.
4. Define where transcripts are stored.
5. Decide whether V5 uses a wrapper, adapter copy, or read-only bridge.
6. Confirm no private data leaks into buyer-facing transcripts.
7. Add a V5 speech benchmark only after the adapter can run from V5.
8. Keep the first V5 speech demo labeled experimental.

## First Implementation Shape

When the strict surface gate passes, the first V5-side speech integration should be small:

- read-only bridge first
- one adapter entrypoint
- no training
- no checkpoint promotion
- deterministic profile defaults
- stable adapter path only
- transcript logging always on
- explicit command for held-out gate rerun

## Promotion Rule

The adapter is not promoted because it sounds good.

It earns promotion only if it passes:

- cold-start gate
- manual transcript review
- strict surface-quality gate
- V5-native held-out gate
- leakage checks
- repetition checks
- identity containment checks

## Boundary

This import plan supports a bounded speech adapter review.

It does not claim:

- raw V2 speech maturity
- general conversational fluency
- LLM replacement
- AGI
- human-equivalent cognition
- production-ready chat

Current buyer-safe phrasing:

> HPP V5 is tracking a bounded speech adapter path from the V2 lab branch. Stability has improved substantially, but V5-native speech promotion is on hold until the stricter surface-quality gate passes.
