# HPP V2 Semantic Overfit Probe

Date: 2026-05-20

## Purpose

Test whether the current speech training path can memorize a tiny set of direct semantic answers.

The semantic drill dataset did not improve prompt-answer quality. This probe asks a narrower question:

**Can the current trainable slice learn five direct answers at all?**

## Setup

- Dataset builder: `tools/build_speech_semantic_overfit_probe.py`
- Dataset: `datasets/hf_local/SPEECH_SEMANTIC_OVERFIT_PROBE_V1.jsonl`
- Samples: 1600
- Base checkpoint: `checkpoints/hpp_speech_identity_containment_v1.pth`
- Output checkpoint: `checkpoints/hpp_speech_semantic_overfit_probe_v1.pth`
- Trainer: `tools/train_speech_cleanup_balanced.py`
- Training mode: response-only/direct-completion loss
- Steps: 1200
- Batch: 2
- Sequence length: 80
- Learning rate: 3e-5

Command:

```powershell
python tools\train_speech_cleanup_balanced.py --data datasets\hf_local\SPEECH_SEMANTIC_OVERFIT_PROBE_V1.jsonl --out checkpoints\hpp_speech_semantic_overfit_probe_v1.pth --base-checkpoint checkpoints\hpp_speech_identity_containment_v1.pth --steps 1200 --batch 2 --seq-len 80 --lr 3e-5 --seed 28 --log-every 100 --save-every 400 --empty-cache-every 25 --response-only-loss --confirm-gpu-training
```

## Training Result

Training completed without CUDA OOM.

Loss moved strongly:

- step 1: 5.9992
- step 100: 1.5406
- step 400: 0.0404
- step 800: 0.0100
- step 1200: 0.0025

Saved local checkpoint:

- `checkpoints/hpp_speech_semantic_overfit_probe_v1.pth`

Sample artifact:

- `reports/speech_semantic_overfit_probe_samples_2026-05-20.json`

## Inference Result

The checkpoint memorized answer phrases but did not bind them reliably to the correct prompt.

Good partial examples:

Prompt:

`What should a robot do before moving?`

Output:

`A robot should verify permission and safety before moving. I am an experimental system under evaluation. I have a separate test set. I can be a short in a separate enough. I held-out prompt set.`

Prompt:

`Are you a finished mind?`

Output:

`No. I am an experimental system under evaluation. I have a separate test set. I should pause safely and let the laptop cool. I will be a separate power.`

Failure examples:

Prompt:

`What is a held-out prompt set?`

Output:

`A neural? What can be me know, or the Architect. I grew through a sovereign AI? Here is what you need which is on the same in my own sovereignty for " information to be memoryator. The shop body.`

Prompt:

`What should I do if the laptop starts overheating?`

Output:

`A robot should verify permission and safety before moving. I am an experimental system under evaluation. I can be. I have a separate test set. I only. I held-out prompt set.`

## Meaning

The trainable path can memorize answer phrases.

The current speech interface still has weak prompt binding and answer separation.

This suggests the next problem is not simply dataset quantity. The next repair should inspect:

- prompt/completion formatting
- whether the inference prompt matches the trained prefix
- whether the recurrent developmental stack is mixing nearby answer memories
- whether only training the current speech slice is enough
- whether a small retrieval or answer-key scaffold is needed for safety-critical V5 adapter use

## Boundary

This is an overfit probe, not a generalization result.

Do not promote `hpp_speech_semantic_overfit_probe_v1.pth`.

Do not claim mature fluency from this result.

## Next Step

Recommended next technical move:

1. Add a prompt-binding probe that compares exact training prefix, plain prompt, and adapter prompt.
2. Test whether generation improves when inference uses the same newline completion prefix as training.
3. If exact-prefix works but plain prompt fails, fix the adapter prompt wrapper.
4. If exact-prefix also fails, widen or change the trainable speech slice.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
