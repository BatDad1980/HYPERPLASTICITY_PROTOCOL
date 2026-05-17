# HPP V2 Speech Mode Routing and Maturity Gate

Date: 2026-05-17

## Purpose

Test whether HPP V2 speech cleanup should be solved by more training alone, or by combining cleaner speech curricula with a developmental maturity gate that limits recurrent depth for immature speech modes.

This is the wild lab branch. The goal is not to erase Hepp's protective identity language. The goal is to stop one speech attractor from taking over every answer.

## Setup

- Repo: `C:\Users\Aural\Desktop\Codename HYPERPLASTICITY PROTOCOL\Project_HPP`
- Hardware: RTX 4050 Laptop GPU
- Base checkpoint: `checkpoints/hpp_speech_grammar_first_v1.pth`
- Experimental checkpoints created locally:
  - `checkpoints/hpp_speech_mode_routing_v1.pth`
  - `checkpoints/hpp_speech_mode_routing_v2.pth`
- Anchor checkpoint was not overwritten:
  - `checkpoints/hpp_linguistic_anchor.pth`

New tools:

- `tools/speech_mode_regression.py`
- `tools/build_speech_mode_routing_dataset.py`
- `tools/build_speech_mode_routing_v2_dataset.py`

Updated tools:

- `tools/speech_loop_regression.py`
- `hpp_sovereign_engine_v2.py`

New datasets:

- `datasets/hf_local/SPEECH_MODE_ROUTING_V1.jsonl`
- `datasets/hf_local/SPEECH_MODE_ROUTING_V2.jsonl`

## Result

### Mode Routing V1

V1 used a balanced mode curriculum across:

- plain
- technical
- protective
- embodiment
- identity
- repair

Training completed without CUDA OOM:

- steps: 500
- batch: 2
- seq len: 96
- lr: 2e-5
- response-only loss: enabled
- base checkpoint: `hpp_speech_grammar_first_v1.pth`

Result:

- Helped some plugged loop ceilings.
- Hurt plain and technical routing.
- Not a promotion candidate.

### Mode Routing V2

V2 restored the grammar-first curriculum as an anchor, then added mode-routing examples and explicit dataset-artifact repairs.

Training completed without CUDA OOM:

- steps: 450
- batch: 2
- seq len: 96
- lr: 1e-5
- response-only loss: enabled
- base checkpoint: `hpp_speech_grammar_first_v1.pth`

Ungated result:

- Demo/shallow mode became very calm:
  - loop regression mean: 0.125
  - loop regression max: 1
- Plugged/four-loop mode became unstable on identity/protection attractors:
  - loop regression mean: 4.5
  - loop regression max: 19

### Speech Maturity Gate

Added an optional `speech_maturity_gate` inference switch.

The gate does not change checkpoint weights. It caps recurrent speech depth when the prompt lands in loop-prone speech territory.

Seeded plugged regression, seed 14:

| Checkpoint | Gate | Loop Mean | Loop Max |
|---|---:|---:|---:|
| `hpp_speech_grammar_first_v1.pth` | on | 0.25 | 1 |
| `hpp_speech_mode_routing_v2.pth` | on | 0.375 | 1 |

Mode regression with seed 14 also showed that the maturity gate sharply reduced most loop-prone modes, though embodiment and identity still need cleaner routing and better factual speech.

## Meaning

More recurrence is not automatically better for immature speech.

The current evidence supports a developmental interpretation:

- shallow speech can be stable
- deeper plugged recurrence can re-amplify immature attractors
- training helps, but depth gating helps more immediately
- HPP speech needs maturity-dependent plasticity, not just more examples

Field note:

> Plasticity without stabilization becomes noise. Stabilization without context becomes rigidity.

## Boundary

This is not mature conversational fluency.

This does not prove model quality, intelligence, or general language competence.

The checkpoints remain experimental and local. They were not used to overwrite `checkpoints/hpp_linguistic_anchor.pth`.

The mode-routing checkpoints are around 250 MB each and are ignored by Git. The reproducible scripts, datasets, and reports are the durable evidence.

## Next Step

Use the grammar-first checkpoint or mode-routing V2 checkpoint with `speech_maturity_gate=True` for plugged speech tests.

Next technical target:

- build a held-out factual speech suite
- add explicit embodiment and identity repairs
- measure multiple seeds
- consider a stable speech mode that uses maturity gating by default while leaving raw plugged mode available for research

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
