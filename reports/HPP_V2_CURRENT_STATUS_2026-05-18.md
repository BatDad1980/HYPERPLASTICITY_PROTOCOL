# HPP V2 Current Status

Date: 2026-05-18

## Purpose

Provide a concise handoff for the HPP V2 wild-lab branch after the speech cleanup, mode-routing, maturity-gate, and stable-profile work.

## Current State

HPP V2 is producing sentence-shaped speech but is still developmentally immature.

The strongest current pattern is:

- shallow/demo speech is often more stable
- raw plugged recurrence can re-amplify identity/protection loops
- stable speech improves when recurrence is gated by maturity
- more training alone has not solved plugged speech loops

## Best Current Speech Baseline

Use:

- checkpoint: `checkpoints/hpp_speech_grammar_first_v1.pth`
- engine: `hpp_sovereign_engine_v2.py`
- inference profile: `speech_profile="stable"`

Do not overwrite:

- `checkpoints/hpp_linguistic_anchor.pth`

## Key Evidence

Stable profile, plugged mode, seeds 14/21/28:

`hpp_speech_grammar_first_v1.pth`

- raw mode-regression mean: 3.0533
- stable mode-regression mean: 0.6933
- raw format leaks: 17
- stable format leaks: 1

`hpp_speech_mode_routing_v2.pth`

- raw mode-regression mean: 4.8133
- stable mode-regression mean: 0.92
- raw format leaks: 20
- stable format leaks: 1

## Meaning

The practical design lesson is:

Speech maturity needs depth control.

This supports the HPP hypothesis that useful adaptive behavior depends on staged development, stabilization, context, and maturity-dependent plasticity rather than simply increasing brute recurrent depth.

## Repo Organization

Navigation files added:

- `tools/README.md`
- `reports/README.md`
- `datasets/hf_local/README.md`
- `checkpoints/README.md`

Additional cleanup:

- root scratch scripts were either removed or organized into repo folders
- syntax dataset builder moved to `tools/build_syntax_foundation_dataset.py`
- robotics safety boundary moved to `core/robotics_safety_adapter.py`
- frontier training now requires `--confirm-gpu-training`
- frontier training no longer overwrites the linguistic anchor unless `--promote-anchor` is passed

## Next Work

1. Build a held-out factual speech suite.
2. Score exact-answer quality, not only loop suppression.
3. Add identity and embodiment repair examples.
4. Add a safe interactive smoke-test launcher that defaults to stable speech.
5. Decide whether any checkpoint deserves promotion to anchor.

## Boundary

This is not a full fluency claim.

This is not buyer-safe public language.

This is wild-lab evidence showing that stable speech currently requires maturity-gated inference.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
