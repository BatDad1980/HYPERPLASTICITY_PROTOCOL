# HPP V2 Tools Index

This folder contains reproducible utility scripts for the wild HPP V2 lab.

## Speech Cleanup and Evaluation

- `audit_speech_data.py` - audits speech training data for loop-prone phrases and category balance.
- `build_speech_cleanup_dataset.py` - builds the first balanced speech cleanup dataset.
- `build_speech_grammar_first_dataset.py` - builds the grammar-first speech curriculum.
- `build_speech_noisy_repair_dataset.py` - builds the developmental noisy-input repair curriculum.
- `build_speech_mode_routing_dataset.py` - builds speech mode routing V1.
- `build_speech_mode_routing_v2_dataset.py` - builds grammar-anchored speech mode routing V2.
- `train_speech_cleanup_balanced.py` - guarded CUDA trainer with checkpoint override, response-only loss, and OOM backoff.
- `speech_loop_regression.py` - lightweight loop/attractor regression.
- `speech_mode_regression.py` - mode-specific speech regression for plain, technical, protective, embodiment, and identity prompts.
- `speech_multiseed_eval.py` - multi-seed raw-vs-stable speech profile evaluation.

## Hardware / Field Lab

- `probe_4050_today.py` - bounded RTX 4050 health, allocation, and throughput probe.

## Current Speech Baseline

Use `checkpoints/hpp_speech_grammar_first_v1.pth` with `speech_profile="stable"` for human-facing plugged speech tests.

Keep raw plugged mode for research probes.

Do not overwrite `checkpoints/hpp_linguistic_anchor.pth` unless explicitly choosing to promote a checkpoint.
