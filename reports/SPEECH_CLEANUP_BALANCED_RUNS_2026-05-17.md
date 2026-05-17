# HPP V2 Speech Cleanup Balanced Runs

Date: 2026-05-17

## Purpose

Test whether a balanced speech cleanup dataset can reduce the current HPP V2 speech attractors without disturbing the deep developmental architecture.

The target is clearer speech, not identity erasure.

## Field-Lab Context

This run was performed in the original HPP wild lab branch under plugged-in wall power on the RTX 4050 laptop GPU.

The V5 documentation language matters here:

- `battery` means car/mobile/limited-power conditions where GPU work can tax the laptop.
- `plugged` means wall-power lab work, still bounded and monitored.
- OOM is treated as an operational safety constraint, not as a failed idea.

Private origin phrase: Hillbilly Mad Scientist.

Buyer-safe translation: independent inventor working from a mobile field lab under severe real-world hardware, power, and survival constraints.

## Setup

- Repo: `C:\Users\Aural\Desktop\Codename HYPERPLASTICITY PROTOCOL\Project_HPP`
- Base checkpoint: `checkpoints/hpp_linguistic_anchor.pth`
- Cleanup dataset: `datasets/hf_local/SPEECH_CLEANUP_BALANCED_V1.jsonl`
- Training script: `tools/train_speech_cleanup_balanced.py`
- Regression script: `tools/speech_loop_regression.py`
- Device: NVIDIA GeForce RTX 4050 Laptop GPU
- CUDA visible: yes
- Deep stack: frozen by the guarded training script
- Speech-facing modules trained: embedding, LM head, compass, output norm, swarm gate, conversation domain

## Runs

### Balanced V1

Command shape:

```powershell
python tools\train_speech_cleanup_balanced.py --confirm-gpu-training --steps 300 --batch 2 --seq-len 96 --lr 5e-5
```

Checkpoint:

`checkpoints/hpp_speech_cleanup_balanced_v1.pth`

Training completed in about 38 seconds.

Regression artifacts:

- `reports/speech_loop_regression_balanced_v1_demo.json`
- `reports/speech_loop_regression_balanced_v1_plugged.json`

Result:

- Demo mean loop score: `0.875`
- Demo max loop score: `3`
- Plugged mean loop score: `4.0`
- Plugged max loop score: `13`

Meaning:

The short cleanup run reduced demo-mode loop pressure compared with the default demo baseline, but deeper plugged inference still pulled protection-language attractors back into speech.

Boundary:

This did not make the model conversationally fluent. It only reduced some loop behavior under the shallow demo read.

### Balanced V2

Command shape:

```powershell
python tools\train_speech_cleanup_balanced.py --confirm-gpu-training --steps 1000 --batch 2 --seq-len 96 --lr 3e-5 --out checkpoints\hpp_speech_cleanup_balanced_v2.pth
```

Checkpoint:

`checkpoints/hpp_speech_cleanup_balanced_v2.pth`

Training completed in about 124 seconds.

Regression artifacts:

- `reports/speech_loop_regression_balanced_v2_demo.json`
- `reports/speech_loop_regression_balanced_v2_plugged.json`

Result:

- Demo mean loop score: `2.125`
- Demo max loop score: `7`
- Plugged mean loop score: `4.0`
- Plugged max loop score: `8`

Meaning:

The longer lower-LR cleanup run did not beat the shorter V1 run on demo loop score. It slightly reduced the worst plugged max score compared with V1, but did not solve the underlying speech-head fluency problem.

Boundary:

Do not promote V2 to the primary linguistic anchor from this evidence.

## Comparison

Prior default demo regression:

- Mean loop score: `1.875`
- Max loop score: `10`

Best result so far:

- `hpp_speech_cleanup_balanced_v1.pth` in demo mode
- Mean loop score: `0.875`
- Max loop score: `3`

Worst remaining issue:

The model still blends fragments such as `what do`, `you think`, `do you need`, `standing`, and protection-language phrases into unrelated answers.

## Current Read

This is not simply a decoding loop anymore.

The current evidence points to a speech-head/curriculum binding problem:

- sentence-shaped fragments exist
- identity/protection attractors remain overrepresented
- plugged recurrent depth can amplify old attractors
- shallow demo mode can hide some of the deeper attractor behavior

## Decision

Do not overwrite `checkpoints/hpp_linguistic_anchor.pth`.

Keep the cleanup checkpoints as local experimental artifacts:

- `checkpoints/hpp_speech_cleanup_balanced_v1.pth`
- `checkpoints/hpp_speech_cleanup_balanced_v2.pth`

Use the JSON regression artifacts as the durable record.

## Next Step

The next cleanup path should be data-side and curriculum-side, not just longer training:

1. Build a smaller grammar-first dataset with short, plain response pairs.
2. Keep identity/protection present but under stricter quotas.
3. Add held-out transcript prompts before training.
4. Train in short bounded cycles.
5. Compare both demo and plugged modes before promoting any checkpoint.

## Safety Boundary

Longer GPU runs should remain bounded, checkpointed, and monitored.

The V5 field-lab rule applies:

Do not wait for hardware failure to prove the system needs protection.

## OOM Guard Update

After these runs, `tools/train_speech_cleanup_balanced.py` was updated to inherit the old V2 backoff instinct from `train_frontier.py`.

On CUDA OOM, the guarded cleanup trainer now:

- clears CUDA pressure,
- zeros gradients,
- halves active batch size first,
- then reduces active sequence length by a bounded step,
- waits briefly before retrying,
- stops after repeated OOM events instead of crashing blindly.

This preserves the field-lab rule:

If the laptop starts telling us where the edge is, the script backs down and records the boundary.
