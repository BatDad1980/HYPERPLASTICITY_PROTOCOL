# Registered Eval Suite Summary

This page summarizes the current HPP V5 registered benchmark suite.

The suite is not a claim that HPP V5 is a finished AI model. It is a repeatable mechanism-evidence layer: named benchmarks, saved aggregate JSON, replayable JSONL trajectories, explicit configuration metadata, and boundary language.

Run the suite with:

```powershell
python scripts/run_hpp_eval.py all --save-dir docs/evals/latest --max-concurrency 1
```

List available benchmarks with:

```powershell
python scripts/run_hpp_eval.py --list
```

## Current Benchmarks

| Benchmark | Score | Pass | Primary Signal | Boundary |
| :--- | ---: | :--- | :--- | :--- |
| `habit14_memory` | `1.0` | `4/4` | Habit-14 protected recall activates after repeated exposure. | Synthetic memory mechanism only. |
| `changed_context_habit_memory` | `1.0` | `4/4` | Protected core recall survives shifted context better than noisy recall or rigid lock. | Context vector is supplied by the harness. |
| `stress_aware_routing` | `1.0` | `4/4` | Router beats fixed nurture under stress and fixed sentinel under calm probes. | Stress signal is supplied by the harness. |
| `tapout_boundary_profiles` | `0.966667` | `24/27` | High-intensity profile tolerates a higher unfamiliar-noise band before tap-out. | Synthetic noise and hand-built stress/OOD estimators. |
| `named_baseline_attractor_recovery` | `1.0` | `3/3` | HPP wins pathway recognition while trained baselines win coordinate MSE. | Synthetic attractor-recovery tradeoff only. |
| `maturity_depth_control` | `0.959103` | `6/6` | Maturity-gated depth reduces loop amplification and format leakage. | Synthetic depth-control mechanism only. |
| `robotics_adapter_safety` | `1.0` | `7/7` | Unsafe or uncertain robot telemetry routes to protection before hardware. | No live SDK, ROS2, simulator, or robot command path. |
| `nvidia_robotics_readiness` | `0.9` | `10/10` | NVIDIA robotics plan has simulation-first and safety-first boundaries. | Checklist only; no SDK install or runtime integration. |

## Strongest Repeated Signals

- Habit-14 threshold behavior is now registered in both identical-context and changed-context forms.
- Stress routing is registered in both direct-stress and tap-out boundary forms.
- Maturity-gated depth is registered as a V5-native version of the V2 speech lesson.
- Named baselines now record a repeatable tradeoff instead of overclaiming a universal win.
- Robotics evidence remains safety-bound: telemetry and planning first, no hardware command path.

## What The Suite Can Claim

- HPP V5 has a repeatable local eval harness.
- Each benchmark writes aggregate JSON and replayable JSONL trajectories.
- Current evidence supports specific mechanism claims: protected recall, context-aware protection, stress routing, tap-out boundaries, maturity-gated depth, compact pathway recognition, and safety-first robotics routing.
- Current runs are compatible with the RTX 4050 field-lab workflow.

## What The Suite Cannot Claim

- It does not prove a fixed `3000x` efficiency multiple.
- It does not prove full LLM replacement.
- It does not prove human-equivalent cognition.
- It does not prove production-safe autonomous agency.
- It does not prove mature conversational fluency.
- It does not prove real-world clinical state detection.

## Latest Artifacts

- `docs/evals/latest/habit14_memory.json`
- `docs/evals/latest/changed_context_habit_memory.json`
- `docs/evals/latest/stress_aware_routing.json`
- `docs/evals/latest/tapout_boundary_profiles.json`
- `docs/evals/latest/named_baseline_attractor_recovery.json`
- `docs/evals/latest/maturity_depth_control.json`
- `docs/evals/latest/robotics_adapter_safety.json`
- `docs/evals/latest/nvidia_robotics_readiness.json`

Each has a matching `.trajectories.jsonl` file in the same folder.
