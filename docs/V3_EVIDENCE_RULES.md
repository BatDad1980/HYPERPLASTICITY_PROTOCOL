# V3 Evidence Rules

Date: 2026-05-20

## Purpose

HPP V3 is allowed to remix architecture, but every remix must keep V5's evidence discipline. V3 can propose and test new shapes; it cannot quietly promote a claim, overwrite inherited evidence, or treat speech behavior as mature without V5-style gates.

## Branch Law

- V2 discovers speech behavior.
- V3 tests architecture and remix ideas.
- V5 judges and documents what is real.
- V6 is born only from what survives V5.

## Non-Negotiable Boundaries

- Work only inside `X:\HPP_V3`.
- Treat `X:\HPP_V5` as a source template, not a work target.
- Do not modify or overwrite HPP_V5, V2, or old evidence artifacts.
- Do not run heavy GPU training.
- If training seems useful, stop and write the proposed experiment first.
- Do not copy or promote speech checkpoints.
- Do not make AGI, ASI, sentience, LLM-replacement, clinical, production autonomy, or fixed-efficiency claims.

## Evidence Storage

V3-generated evidence should be append-only.

Preferred locations:

- `docs/v3_evidence/`: V3 architecture experiments, manifests, and summaries.
- `docs/evals/v3/`: V3 registered eval outputs if a run should not replace V5-derived `docs/evals/latest/`.
- `docs/`: stable V3 governance docs, intake docs, and experiment proposals.

Do not edit inherited JSON evidence to make a V3 point. Add a new V3 artifact that cites the inherited artifact instead.

## Required Experiment Record

Every V3 experiment should record:

- experiment name
- date
- objective
- hypothesis
- input artifacts or source docs
- script or module invoked
- seed, if applicable
- device and power mode
- output artifacts
- measurable pass/fail criteria
- boundary language
- promotion and rejection criteria

## Claim Levels

Use these levels in V3 docs and architecture metadata:

- `governance`: rules, branch boundaries, and allowed workflows.
- `plan`: proposed work that has not run.
- `mechanism`: synthetic or bounded harness evidence.
- `demo`: local UI or buyer-safe explanatory surface.
- `registered_eval`: named benchmark with aggregate JSON and trajectory output.
- `integration_ready`: mature enough to be proposed back to V5 review.

Nothing in V3 should skip from `plan` or `demo` to `integration_ready` without a registered eval or an explicit V5 review gate.

## Training Rule

V3 does not train first. It writes first.

If a future architecture question requires training, create a proposal that includes:

- why a non-training harness is insufficient
- smallest safe training shape
- CPU/battery fallback if possible
- maximum time and memory budget
- stop conditions
- expected evidence artifacts
- exact reasons a checkpoint would be rejected

Training proposals are not claims. They are permission slips for later review.
