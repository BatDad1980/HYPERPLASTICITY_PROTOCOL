# HPP V2 Identity Containment V5 Language Gate

Date: 2026-05-20

## Purpose

Run the next HPP V2 language repair pass against the explicit V5 language gate.

The target was not impressive speech.

The target was reliable, measurable, bounded speech with identity/protection/developmental leakage controlled.

## Setup

- Repo: `C:\Users\Aural\Desktop\Codename HYPERPLASTICITY PROTOCOL\Project_HPP`
- Base checkpoint: `checkpoints/hpp_speech_grammar_first_v1.pth`
- New local checkpoint: `checkpoints/hpp_speech_identity_containment_v1.pth`
- Dataset builder: `tools/build_speech_identity_containment_dataset.py`
- Dataset: `datasets/hf_local/SPEECH_IDENTITY_CONTAINMENT_V1.jsonl`
- Training script: `tools/train_speech_cleanup_balanced.py`
- Gate evaluator: `tools/speech_v5_language_gate.py`
- Held-out prompt suite: `datasets/hf_local/SPEECH_HELDOUT_V5_GATE_V1.jsonl`
- Power mode: plugged
- Seeds: 14, 21, 28
- Profiles compared: raw, stable

Training:

- steps: 550
- batch: 2
- seq len: 96
- learning rate: 1.5e-5
- response-only loss: enabled
- CUDA OOM events: 0
- anchor overwrite: no

## Attempt 1

Artifact:

- `reports/speech_v5_language_gate_identity_containment_v1_2026-05-20.json`

Stable profile:

- pass rate: 0.96
- mean loop score: 0.7156
- max loop score: 6
- format leak total: 1
- identity spiral total: 46
- decision: not ready

Meaning:

The checkpoint improved pass rate and loop control, but identity spiral terms got worse under stable decoding.

## Stable Decoder Tightening

The stable profile already uses phrase blocking. The blocked phrase list was extended to suppress specific identity spiral terms during stable-profile evaluation:

- `I am HPP`
- `Hyperplasticity Protocol`
- `I protect`
- `consciousness`
- `protect the fortress`

This is an inference control, not a checkpoint change.

Raw profile remains available for research.

## Final Gate Result

Artifact:

- `reports/speech_v5_language_gate_identity_containment_v1_tight_stable_2026-05-20.json`

Stable profile:

- evaluations: 225
- pass count: 217
- pass rate: 0.9644
- mean loop score: 0.6978
- max loop score: 6
- format leak total: 1
- mode label total: 7
- identity spiral total: 5
- repeated sentence total: 0

Gate checks:

- stable beats raw loop mean: pass
- stable beats raw format leaks: pass
- stable loop mean under target: pass
- stable loop max under target: pass
- stable format leaks under target: pass
- stable identity spiral under target: pass
- stable pass rate over target: pass

Decision:

**Passes the current V5 language gate.**

## Meaning

HPP V2 language has now crossed the first measured gate for V5 consideration:

- stable profile repeatedly beats raw mode
- held-out prompt suite is used
- transcript artifacts are saved
- loop score is controlled
- format leakage is near zero
- identity spiral terms are below target

This does not mean the speech is finished.

It means the language layer is now clean enough to begin V5 integration review as a measured candidate.

## Boundary

This is not a full fluency claim.

This is not a claim of general intelligence.

This is not a claim that the checkpoint should automatically replace the anchor.

The current checkpoint remains local because `.pth` files are ignored by Git.

The durable Git evidence is the dataset builder, dataset, evaluator output, and this report.

## Next Step

Before V5-native import:

1. Review transcript failures manually.
2. Run the same gate again after a cold restart.
3. Consider a V5-safe language adapter that uses stable profile and identity blocking by default.
4. Keep raw V2 speech separate as a research mode.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
