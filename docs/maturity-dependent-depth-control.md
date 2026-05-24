# Maturity-Dependent Depth Control

Date observed: 2026-05-17

Source branch:

`C:\Users\Aural\Desktop\Codename HYPERPLASTICITY PROTOCOL\Project_HPP`

This note records a field result from the original HPP V2 lab branch. HPP V5 is not importing the experimental checkpoints. It is preserving the design lesson.

## Field Result

The V2 speech experiments compared raw plugged speech against a stable profile with maturity gating across seeds `14`, `21`, and `28`.

### `hpp_speech_grammar_first_v1.pth`

| Mode | Mean Regression | Format Leaks |
| --- | ---: | ---: |
| Raw plugged | `3.0533` | `17` |
| Stable profile | `0.6933` | `1` |

### `hpp_speech_mode_routing_v2.pth`

| Mode | Mean Regression | Format Leaks |
| --- | ---: | ---: |
| Raw plugged | `4.8133` | `20` |
| Stable profile | `0.92` | `1` |

Best current speech baseline from the V2 field lab:

`hpp_speech_grammar_first_v1.pth` with the stable maturity-gated profile.

## Meaning

More recurrent depth is not automatically better for immature speech.

The original branch showed that deeper plugged recurrence can re-amplify identity and protection attractors before the speech pathway is mature enough to hold format, syntax, and topic boundaries. A stable profile with maturity gating sharply reduced regression and format leakage.

This supports an HPP design rule:

> Grow first. Reuse depth. Gate maturity.

## Architectural Principle

Speech should receive depth according to maturity, not only according to available compute.

An immature speech adapter should use:

- shallower recurrence
- stricter output format control
- anti-loop decoding
- held-out regression checks
- maturity gates before deeper recurrent reuse

A mature speech adapter can receive more recurrent depth only after it proves:

- low loop score
- low format leakage
- clean sentence completion
- stable held-out behavior
- preserved identity without phrase collapse

## V5 Implication

HPP V5 should model recurrent depth as a routed resource.

Depth should depend on:

- task type
- power mode
- stress/tolerance profile
- speech maturity
- output risk
- recent loop telemetry

This connects speech progress to the broader HPP thesis: plasticity without stabilization becomes noise, while stabilization without context becomes rigidity.

## V5 Mechanism Benchmark

HPP V5 now includes a synthetic eval-harness benchmark:

`maturity_depth_control`

The benchmark does not load V2 speech checkpoints. It tests the mechanism directly by comparing raw plugged depth against maturity-gated depth across immature, growing, and mature pathway cases.

Current latest eval artifact:

- `docs/evals/latest/maturity_depth_control.json`
- `docs/evals/latest/maturity_depth_control.trajectories.jsonl`

The benchmark should be treated as a V5-native mechanism test. It is the next rung after the V2 field finding, not a replacement for live speech regression.

## Later Adapter Gate Confirmation

On 2026-05-20, the V2 branch reported a V5-safe stable adapter gate clean pass:

- Evaluations: `225`
- Pass count: `225`
- Format leaks: `0`
- Mode-label leaks: `0`
- Mean loop score: `0.6933`
- Max loop score: `7`
- Repeated sentence failures: `0`

This confirms the practical value of the maturity-gated adapter direction. The result should still be read as a stable adapter path, not a raw speech or full-fluency claim.

## Boundary

This is original-branch speech evidence, not a V5 language-quality benchmark.

The V2 checkpoints remain experimental local artifacts. The durable V5 inheritance is the measured design principle: maturity-dependent depth control reduced speech regression and format leakage in the V2 field lab.
