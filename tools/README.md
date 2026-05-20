# HPP V2 Tools Index

This folder contains reproducible utility scripts for the wild HPP V2 lab.

## Speech Cleanup and Evaluation

- `audit_speech_data.py` - audits speech training data for loop-prone phrases and category balance.
- `build_speech_cleanup_dataset.py` - builds the first balanced speech cleanup dataset.
- `build_speech_grammar_first_dataset.py` - builds the grammar-first speech curriculum.
- `build_speech_noisy_repair_dataset.py` - builds the developmental noisy-input repair curriculum.
- `build_speech_mode_routing_dataset.py` - builds speech mode routing V1.
- `build_speech_mode_routing_v2_dataset.py` - builds grammar-anchored speech mode routing V2.
- `build_speech_identity_containment_dataset.py` - builds bounded-answer repair data for identity containment.
- `build_syntax_foundation_dataset.py` - builds a small clean grammar scaffold dataset.
- `train_speech_cleanup_balanced.py` - guarded CUDA trainer with checkpoint override, response-only loss, and OOM backoff.
- `speech_loop_regression.py` - lightweight loop/attractor regression.
- `speech_mode_regression.py` - mode-specific speech regression for plain, technical, protective, embodiment, and identity prompts.
- `speech_multiseed_eval.py` - multi-seed raw-vs-stable speech profile evaluation.
- `speech_v5_language_gate.py` - held-out V5 language gate evaluator with full transcript artifacts.

## Hardware / Field Lab

- `probe_4050_today.py` - bounded RTX 4050 health, allocation, and throughput probe.

## Frontier Training

- `train_frontier.py` lives at the repo root because it is a primary training entrypoint.
- It now refuses to run without `--confirm-gpu-training`.
- It no longer overwrites `checkpoints/hpp_linguistic_anchor.pth` unless `--promote-anchor` is explicitly passed.

## Current Speech Baseline

Use `checkpoints/hpp_speech_grammar_first_v1.pth` with `speech_profile="stable"` for human-facing plugged speech tests.

Keep raw plugged mode for research probes.

Do not overwrite `checkpoints/hpp_linguistic_anchor.pth` unless explicitly choosing to promote a checkpoint.
