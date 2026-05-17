# HPP V2 Speech Cleanup Status

Date: 2026-05-17

## Current Read

The current linguistic anchor loads through `hpp_sovereign_engine_v2.py` on CUDA FP16 at 512 context and reports 65,439,318 counted inference parameters.

The model is not only looping. It is producing sentence-shaped fragments with weak grammatical binding. Decoder-level n-gram blocking helps prevent exact repeats, but it does not solve speech-head fluency by itself.

## Data Finding

`CONVERSATIONAL_FLUENCY.jsonl` heavily reinforces identity/protection language:

- 1,583 samples total
- 291 identity samples
- 256 protection samples
- repeated attractors include `what do you think`, `do not quit`, `standing`, `creator`, `protect`, `mission`, `oath`, and `masamune`

This is not bad identity. It is overconcentrated speech pressure.

## Added Safe Tools

- `tools/audit_speech_data.py`
- `tools/build_speech_cleanup_dataset.py`
- `tools/speech_loop_regression.py`
- `tools/train_speech_cleanup_balanced.py`

The balanced candidate dataset is:

`datasets/hf_local/SPEECH_CLEANUP_BALANCED_V1.jsonl`

It has 738 samples and keeps identity/protection present while reducing repeated attractor pressure.

## Verification

Safe demo-mode inference regression was written to:

- `reports/speech_loop_regression_demo.json`
- `reports/speech_loop_regression_demo_default.json`
- `reports/speech_loop_regression_demo_phrase_block.json`

The phrase-blocking experiment is available but should not be the default cleanup path. It can bend grammar into awkward substitutions. The better next step is a small confirmed cleanup training run on the balanced dataset.

## Next Safe Training Option

Only after checking power/cooling and committing current work:

```powershell
python tools\train_speech_cleanup_balanced.py --confirm-gpu-training --steps 300
```

This writes a separate checkpoint:

`checkpoints/hpp_speech_cleanup_balanced_v1.pth`

It does not overwrite `checkpoints/hpp_linguistic_anchor.pth`.
