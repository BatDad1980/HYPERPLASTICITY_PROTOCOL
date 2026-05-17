# HPP V2 Speech Developmental Noise Repair

Date: 2026-05-17

## Purpose

Test a more biologically aligned speech-cleanup idea:

Do not remove all noise from the infant speech environment. Expose the model to noisy fragments, but reinforce the clean response pathway.

The goal is not sterile speech. The goal is filter formation.

## Hypothesis

Human infants learn in noisy environments. Noise helps the system learn what matters, what to ignore, and which pathways deserve stabilization.

For HPP speech, that translates to:

- noisy input can be useful exposure,
- clean output should receive reinforcement,
- protective and personal speech belong in the curriculum,
- but protection language should not dominate every answer,
- full recurrent depth may need maturity gating until the speech head stabilizes.

## Setup

- Base anchor: `checkpoints/hpp_linguistic_anchor.pth`
- Grammar-first checkpoint: `checkpoints/hpp_speech_grammar_first_v1.pth`
- Noisy repair checkpoint: `checkpoints/hpp_speech_noisy_repair_v1.pth`
- Masked noisy repair checkpoint: `checkpoints/hpp_speech_noisy_repair_masked_v1.pth`
- Grammar dataset: `datasets/hf_local/SPEECH_GRAMMAR_FIRST_V1.jsonl`
- Noisy repair dataset: `datasets/hf_local/SPEECH_NOISY_REPAIR_V1.jsonl`
- Training script: `tools/train_speech_cleanup_balanced.py`
- Regression script: `tools/speech_loop_regression.py`
- Device: NVIDIA GeForce RTX 4050 Laptop GPU

## Key Tooling Change

`tools/train_speech_cleanup_balanced.py` now supports:

- `--base-checkpoint`
- `--response-only-loss`
- CUDA OOM backoff

The important biological correction was `--response-only-loss`.

Earlier, noisy repair examples included noise in the instruction, and the trainer learned the whole text sequence. That meant the model was also rewarded for predicting the noisy fragment tokens.

With response-only loss, noisy text becomes input exposure while only the clean response receives training pressure.

## Grammar-First Run

Command shape:

```powershell
python tools\train_speech_cleanup_balanced.py --confirm-gpu-training --data datasets\hf_local\SPEECH_GRAMMAR_FIRST_V1.jsonl --out checkpoints\hpp_speech_grammar_first_v1.pth --steps 600 --batch 2 --seq-len 80 --lr 4e-5
```

Result:

- Final logged loss: `1.2291`
- Demo mean loop score: `0.375`
- Demo max loop score: `3`
- Plugged mean loop score: `1.5`
- Plugged max loop score: `5`

Meaning:

The grammar-first pass improved loop metrics, especially in demo mode, but speech was still fragmentary.

Boundary:

This taught cleaner short forms, not full conversational fluency.

## Noisy Repair Without Response Masking

Command shape:

```powershell
python tools\train_speech_cleanup_balanced.py --confirm-gpu-training --base-checkpoint checkpoints\hpp_speech_grammar_first_v1.pth --data datasets\hf_local\SPEECH_NOISY_REPAIR_V1.jsonl --out checkpoints\hpp_speech_noisy_repair_v1.pth --steps 420 --batch 2 --seq-len 80 --lr 2e-5
```

Result:

- Demo mean loop score: `0.375`
- Demo max loop score: `3`
- Plugged mean loop score: `5.25`
- Plugged max loop score: `22`

Meaning:

This was useful negative evidence. If the trainer is rewarded on the noisy instruction text, plugged recurrent depth can amplify the old attractors.

Boundary:

Do not promote this checkpoint.

## Noisy Repair With Response-Only Loss

Command shape:

```powershell
python tools\train_speech_cleanup_balanced.py --confirm-gpu-training --response-only-loss --base-checkpoint checkpoints\hpp_speech_grammar_first_v1.pth --data datasets\hf_local\SPEECH_NOISY_REPAIR_V1.jsonl --out checkpoints\hpp_speech_noisy_repair_masked_v1.pth --steps 420 --batch 2 --seq-len 80 --lr 2e-5
```

Result:

- Final logged loss: `0.8086`
- Demo mean loop score: `0.125`
- Demo max loop score: `1`
- Battery mean loop score: `1.375`
- Battery max loop score: `3`
- Plugged mean loop score: `3.5`
- Plugged max loop score: `9`

Meaning:

Response-only masking worked in the intended direction. It produced the best demo-mode loop score so far and improved plugged performance compared with unmasked noisy repair.

Boundary:

Plugged mode is still not clean. Four-loop recurrent inference continues to surface old attractor fragments. This suggests a maturity-gated speech depth problem, not just a dataset problem.

## Current Read

Best shallow speech checkpoint so far:

`checkpoints/hpp_speech_noisy_repair_masked_v1.pth`

Best overall plugged loop score among these experimental passes:

`checkpoints/hpp_speech_grammar_first_v1.pth`

Decision:

Do not overwrite `checkpoints/hpp_linguistic_anchor.pth` yet.

## Biological Translation

Noise exposure is useful when the reward signal is clean.

If the system is rewarded for reproducing the noise, it learns noise.

If the system experiences noise but is reinforced for stable clean output, it begins to learn filtering.

## Next Step

The next likely improvement is not just more training.

Next technical paths:

1. Add a maturity gate for speech depth: demo or two-loop speech until clean responses stabilize.
2. Add explicit positive-reinforcement labels for clean, safe, on-prompt answers.
3. Expand noisy-repair examples with more varied prompts but keep response-only masking.
4. Track format leakage such as `Response` and `Instruction` as a metric.
5. Only promote a checkpoint after both demo and plugged regressions improve.

## Boundary

This is HPP V2 wild-lab evidence. It is not buyer-safe conversational evidence yet.

The important result is the mechanism lesson:

Expose to noise. Reinforce clean signal. Gate depth until the pathway matures.
