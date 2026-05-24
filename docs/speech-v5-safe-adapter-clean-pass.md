# V2 V5-Safe Speech Adapter Clean Pass

Date observed: 2026-05-20

Source branch:

`C:\Users\Aural\Desktop\Codename HYPERPLASTICITY PROTOCOL\Project_HPP`

Source report:

`reports/SPEECH_V5_SAFE_ADAPTER_CLEAN_PASS_2026-05-20.md`

Cold restart confirmation:

`reports/SPEECH_V5_SAFE_ADAPTER_COLD_RESTART_2026-05-20.md`

## Purpose

Record the first V2 speech result that clears the current V5-safe adapter gate.

This is a harvested field result. HPP V5 is not importing the checkpoint, copying raw V2 speech, or promoting full conversational maturity.

## Setup

- Adapter: `core/v5_language_adapter.py`
- Checkpoint: `checkpoints/hpp_speech_identity_containment_v1.pth`
- Gate evaluator: `tools/speech_v5_language_gate.py`
- Held-out suite: `datasets/hf_local/SPEECH_HELDOUT_V5_GATE_V1.jsonl`
- Power mode: plugged
- Seeds: `14`, `21`, `28`
- Profile: stable adapter path

## Change

The stable speech phrase blocker was extended with narrow decoder-side blocks:

- `protective mode`
- `Instruction:`
- `Response:`

This is inference control only.

It does not change checkpoint weights.

## Result

Stable adapter gate:

- evaluations: `225`
- pass count: `225`
- pass rate: `1.0`
- mean loop score: `0.6933`
- max loop score: `7`
- format leak total: `0`
- mode-label leak total: `0`
- repeated sentence failures: `0`
- identity spiral count: `5`

Failure review:

- failures: `0 / 225`
- pass rate: `1.0`

## Cold Restart Confirmation

The same stable adapter gate was rerun after a fresh process and fresh CUDA context.

Cold restart result:

- evaluations: `225`
- pass count: `225`
- pass rate: `1.0`
- mean loop score: `0.6933`
- max loop score: `7`
- format leak total: `0`
- mode-label leak total: `0`
- repeated sentence failures: `0`
- identity spiral count: `5`

The clean adapter pass repeated after cold restart.

This strengthens the adapter path because the result is not only a warm-session artifact.

## Meaning

This is the cleanest V2 language result so far.

It clears the specific target V5 set for language inheritance:

> Reliably clean and measurable, not impressive.

The current V5-safe adapter path now has:

- held-out prompt coverage
- multi-seed evaluation
- transcript artifacts
- zero format leaks
- zero mode-label leaks
- controlled loop score
- no repeated-sentence failures
- identity spiral still measured, but no longer failing the current rubric

## V5 Integration Interpretation

This result was strong enough to begin V5 integration review.

A later manual review and strict surface-quality gate found that the adapter is not yet ready for V5-native speech promotion.

The current status is:

- stability gate: pass
- cold restart gate: pass
- manual language quality review: fail / hold
- strict surface-quality gate: fail / hold

It is not enough to promote raw V2 speech or claim mature fluency.

The next V5-side work should be:

1. Build a response-cleaning repair set.
2. Rerun the strict surface-quality gate.
3. Add another manual transcript review note.
4. Keep raw V2 speech research-only.
5. Define a V5-native speech eval before shipping speech claims.

## Boundary

This is an adapter result.

It is not:

- raw V2 speech
- automatic checkpoint promotion
- mature conversational fluency
- AGI evidence
- human-equivalent cognition evidence
- LLM replacement evidence

Buyer-safe phrasing:

> The V2 lab branch now has a stable adapter path that passed automated and cold-start stability gates with zero format leaks and zero mode-label leaks. A stricter manual/surface review still holds V5-native speech promotion because many outputs begin with wrapper residue and do not answer directly enough.
