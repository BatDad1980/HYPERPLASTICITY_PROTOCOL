# HPP Eval Harness

HPP V5 now has a small benchmark registry modeled after the clean shape of modern evaluation frameworks:

```python
from hpp_eval import BenchmarkConfig, run_benchmark, run_benchmarks

result = await run_benchmark(
    "robotics_adapter_safety",
    BenchmarkConfig(save_dir="docs/evals/latest"),
)
print(f"robotics_adapter_safety: {result.score:.1%}")

results = await run_benchmarks(
    [
        "habit14_memory",
        "changed_context_habit_memory",
        "stress_aware_routing",
        "robotics_adapter_safety",
        "nvidia_robotics_readiness",
        "maturity_depth_control",
        "tapout_boundary_profiles",
        "named_baseline_attractor_recovery",
    ],
    BenchmarkConfig(save_dir="docs/evals/latest"),
)
```

The harness writes:

- aggregate benchmark JSON
- replayable JSONL trajectories
- explicit configuration metadata
- explicit boundary language for buyer-safe interpretation

## First Registered Benchmark

`v3_architecture_boundary_registry`

This benchmark validates the V3 architecture boundary registry. It checks that each remix surface has an explicit role, claim level, allowed power modes, evidence paths, forbidden moves, and boundary language.

It measures:

- architecture component count
- component pass count
- claim-level distribution
- registered-eval coverage
- speech boundary quarantine
- validation errors in the registry metadata

It does not train, load checkpoints, or prove model capability.

Recommended V3 run:

```powershell
python scripts/run_hpp_eval.py v3_architecture_boundary_registry --save-dir docs/v3_evidence
```

`habit14_memory`

This benchmark tests whether repeated exposure creates a protected pathway that improves noisy recall only after the Habit-14 threshold.

It measures:

- pre-threshold non-intervention
- threshold lock behavior
- protected recall improvement at 14 exposures
- extended protected recall improvement at 21 exposures

It does not train a language model or prove general intelligence.

## Changed-Context Habit Benchmark

`changed_context_habit_memory`

This benchmark tests whether Habit-14 can protect a core pathway while the surrounding context changes. It compares a rigid full-pattern lock against a context-adaptive lock that preserves the core and blends in the current context.

It measures:

- pre-threshold non-intervention
- shifted-context adaptive improvement over noisy recall
- shifted-context adaptive improvement over rigid lock
- extended protection at 21 exposures

It does not prove autonomous context discovery, because the context vector is supplied to the adaptive memory.

## Stress-Aware Routing Benchmark

`stress_aware_routing`

This benchmark tests whether a router that switches between nurture-style refinement and sentinel-style protection can beat fixed response modes.

It measures:

- router improvement over fixed nurture under high stress
- router improvement over fixed sentinel under calm conditions
- router improvement over the best fixed strategy overall
- router failure rate

It does not prove autonomous stress detection, because the stress signal is supplied by the harness.

## Tap-Out Boundary Benchmark

`tapout_boundary_profiles`

This benchmark tests profile-specific tap-out behavior under increasing unfamiliar noise. It replays low-tolerance, standard, and high-intensity profiles across several noise scales and seeds.

It measures:

- first tap-out noise per profile
- max no-tapout noise per profile
- final tap-out failure rate
- whether the high-intensity profile tolerates a higher noise band before tapping out

It does not prove real-world stress/OOD detection, because the noise is synthetic and the estimators are hand-built for this harness.

## Named Baseline Benchmark

`named_baseline_attractor_recovery`

This benchmark repeats the named-baseline attractor-recovery comparison across seeds. It records the current honest tradeoff: HPP wins class/pathway recognition while trained baselines win coordinate reconstruction MSE.

It measures:

- HPP accuracy win rate
- HPP MSE win rate
- best-baseline-to-HPP MSE ratio
- HPP accuracy edge over the best baseline
- stored HPP memory values compared with MLP and GRU parameter counts

It does not prove broad model superiority, language ability, or a fixed efficiency multiple.

## Robotics Safety Benchmark

`robotics_adapter_safety`

This benchmark reuses the synthetic robotics adapter scenarios and grades whether uncertain or unsafe states are routed to protection.

It measures:

- low-battery protection
- IMU instability protection
- joint or actuator risk protection
- operator override protection
- unknown-state inspection routing

It does not measure:

- real robot control
- Unitree SDK integration
- ROS2, MuJoCo, IsaacLab, or live hardware
- production safety

## NVIDIA Readiness Benchmark

`nvidia_robotics_readiness`

This benchmark grades whether the current NVIDIA robotics integration plan contains the safety and deployment boundaries HPP needs before using Isaac Lab, Isaac ROS, TensorRT, Triton, Jetson, or live hardware.

It measures checklist readiness only:

- simulation-first path
- no direct motor command path
- telemetry schema
- Sentinel stop mapping
- operator override mapping
- hardware cutoff plan
- replayable trajectory logging
- Jetson target notes
- TensorRT inference notes
- license and dependency boundary

It does not install NVIDIA SDKs, import Isaac Lab, run TensorRT, connect ROS 2, or command hardware.

## Maturity Depth Benchmark

`maturity_depth_control`

This benchmark turns the V2 speech lesson into a V5-native synthetic mechanism test. It compares raw plugged depth against maturity-gated depth across immature, growing, and mature pathway cases.

It measures:

- loop score under raw depth
- loop score under gated depth
- format-leak count under raw depth
- format-leak count under gated depth
- whether quality is preserved or improved after gating

It does not load V2 speech checkpoints, run a language model, or prove conversational fluency.

Run it with:

```powershell
python scripts/run_hpp_eval.py robotics_adapter_safety --save-dir docs/evals/latest
```

Summarize latest registered eval artifacts with:

```powershell
python scripts/summarize_registered_evals.py
```

## Why This Matters

The earlier HPP V5 evidence scripts proved individual rungs. The eval harness begins turning those rungs into a repeatable evaluation layer: named tasks, saved trajectories, aggregate scores, and comparable configuration records.

This is the right bridge between field-lab experiments and buyer-safe technical evidence.
