# V3 Experiment 001: Architecture Boundary Registry

Date: 2026-05-20

## Objective

Create a measurable V3 architecture registry before changing core model behavior.

## Hypothesis

V3 can safely begin architecture remix work by first defining subsystem boundaries, claim levels, allowed power modes, evidence paths, and forbidden moves. A registered eval can catch boundary drift before later experiments become ambiguous.

## Inputs

- `docs/V3_ARCHITECTURE_INTAKE.md`
- `docs/V3_EVIDENCE_RULES.md`
- `docs/evidence-ladder.md`
- `docs/eval-harness.md`
- inherited V5 source and evidence artifacts inside `X:\HPP_V3`

## Implementation

- Add `src/hpp_arch/registry.py`.
- Register `v3_architecture_boundary_registry` in `src/hpp_eval/benchmarks.py`.
- Write outputs under `docs/v3_evidence/` for V3-specific evidence.

## Measurement

Run:

```powershell
python scripts/run_hpp_eval.py v3_architecture_boundary_registry --save-dir docs/v3_evidence
```

Pass criteria:

- all required architecture components exist
- every component has boundary language
- every component has forbidden moves
- every component has evidence paths
- speech boundary remains a plan-level quarantine
- no validation errors are reported

## Boundary

This experiment is governance and architecture metadata only. It does not train, load checkpoints, invoke heavy GPU work, prove speech ability, or make AGI/sentience/LLM-replacement claims.

## Promotion Criteria

The registry can become the first V3 control surface if the registered eval passes and artifacts are saved under `docs/v3_evidence/`.

## Rejection Criteria

Reject or revise the experiment if the registry authorizes plugged speech execution, promotes demo surfaces as model evidence, omits evidence paths, or lacks clear forbidden moves.
