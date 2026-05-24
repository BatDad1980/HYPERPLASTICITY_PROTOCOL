# V3 Architecture Intake

Date: 2026-05-20

## Branch Role

HPP V3 is the architecture remix lab. It can test new shapes, interfaces, and control policies, but it should inherit V5's evidence discipline rather than V2's growth volatility.

Working boundaries for this intake:

- Work only inside `X:\HPP_V3`.
- Treat V5 as the clean evidence court.
- Treat V2 as the speech repair lab, not an architecture template.
- Do not promote speech checkpoints.
- Do not make AGI, ASI, sentience, LLM-replacement, clinical, or fixed-efficiency claims.
- Do not overwrite existing evidence artifacts.
- Do not run GPU training from V3 intake work.

## Current Repo Map

Top-level shape:

- `README.md` and `README_FOR_BUYERS.md`: V5-positioned project and buyer-facing summaries.
- `LICENSING.md`: licensing and IP boundary notes.
- `package.json`, `vite.config.ts`, `tsconfig.json`, `index.html`: React/Vite local cockpit shell.
- `src/`: frontend app, protocol definitions, TypeScript types, CSS, and Python mechanism/eval modules.
- `scripts/`: 27 lightweight or bounded evidence scripts for probes, comparisons, sweeps, adapters, and summaries.
- `docs/`: 146 top-level evidence, planning, boundary, summary, and JSON artifacts.
- `docs/evals/latest/`: 18 registered eval aggregate and trajectory artifacts.

Key source surfaces:

- `src/App.tsx`: local HPP cockpit for state check-ins, protocol loops, Habit-14 progress, local evidence logging, and power mode display.
- `src/protocols.ts`: small protocol library separating nurture and sentinel loops.
- `src/hpp_kernel/tiny_recurrent.py`: compact recurrent workshop, unique-stack baseline, one-pass adapter, and measured probe helper.
- `src/hpp_kernel/device.py`: device selection boundary for battery, demo, and plugged modes.
- `src/hpp_eval/benchmarks.py`: registered benchmark harness with aggregate JSON, JSONL trajectories, scoring, and boundary language.
- `scripts/run_hpp_eval.py`: entrypoint for named registered evals.

## Strongest V5 Components To Preserve

1. Evidence ladder discipline

V5 consistently distinguishes mechanism evidence from broad claims. The strongest artifact is `docs/evidence-ladder.md`, which records what has been measured, what each result means, and what each result does not prove. V3 should keep this format for every architecture remix.

2. Registered eval harness

The benchmark registry in `src/hpp_eval/benchmarks.py` is mature enough to preserve. It has named evals, aggregate JSON output, replayable JSONL trajectories, configuration metadata, pass counts, scoring, and explicit boundary language. This should become the non-negotiable gate for V3 experiments.

3. Shared recurrence versus unique stack comparison

The recurrent workshop and unique-depth stack comparison is a clean architectural test surface. It gives V3 a measurable place to explore parameter reuse, pass budgeting, memory pressure, and depth routing without touching speech checkpoints or making broad performance claims.

4. Habit-14 and changed-context memory harnesses

Habit-14 is already framed as a mechanism, not magic. The changed-context variant is especially valuable because it separates stable core protection from rigid full-pattern locking. V3 should preserve this as a core architecture law: stability must not erase context.

5. Stress, sentinel, and tap-out routing

The stress-routing and tap-out profile work is mature as synthetic mechanism evidence. V3 should preserve the architecture rule that calm, stress, and unknown states route differently, and that profile-dependent redlines are safer than one global threshold.

6. Maturity-gated depth

This is the cleanest bridge from V2 without importing V2 instability. The preserved lesson is not "use V2 speech"; it is "depth must be earned by maturity." V3 should keep this as a first-class controller.

7. Simulation-first robotics boundary

The robotics adapter safety benchmark is useful because it routes unsafe or uncertain states to protection before any hardware command path exists. V3 can experiment with architecture around this boundary, but should preserve the no-live-hardware, simulation-first rule.

## Evidence And Demo Scaffolding Only

These pieces are useful but should not be mistaken for mature architecture:

- React cockpit state is stored in `localStorage`; it is a local demo shell, not a forensic evidence store.
- Protocol selection and state sliders are manually entered; they do not prove autonomous sensing.
- The Habit Memory panel exposes selected summary numbers; it is buyer-facing explanation, not a live model readout.
- Many JSON artifacts under `docs/` are generated evidence snapshots. V3 should append new evidence instead of editing old evidence.
- Scaling probes are inference and memory envelope evidence only. They do not prove training feasibility, model quality, or useful learned behavior.
- Named baseline results are bounded attractor-recovery tradeoffs. V3 should preserve separate recognition and reconstruction metrics instead of collapsing them into a single win/loss claim.
- Speech docs are inheritance notes and boundary lessons. They are not buyer-safe conversational evidence for V3.
- Robotics docs and synthetic adapter results are planning and routing evidence only. They are not robot-control evidence.
- NVIDIA readiness is a checklist, not an SDK integration or hardware result.

## Where V3 Should Experiment First

1. Architecture boundary registry

Create a small registry that describes each subsystem by maturity, evidence level, allowed power modes, and allowed claim surface. Start with kernel, memory, router, depth controller, eval harness, cockpit, speech boundary, and robotics adapter.

2. Kernel-controller separation

Split the current tiny recurrent kernel from routing and maturity policy experiments. V3 should make it easier to swap controllers without rewriting the workshop block or invalidating old probe artifacts.

3. Evidence manifest layer

Add a manifest convention for new V3 runs that records input artifact, script, seed, device, power mode, output artifact, and claim boundary. This can be tested on copied or new V3 artifacts without changing V5 evidence.

4. Maturity-gated depth API

Turn the synthetic maturity-depth rule into a reusable policy object or module. Keep tests small and CPU-safe first. The goal is to make depth routing inspectable, not bigger.

5. Changed-context protection experiments

Explore memory/protection policies that preserve core identity while letting context shift. This is V3-safe because it can stay synthetic, bounded, and eval-first.

6. Router composition

Experiment with routing as a composable stack: calm/nurture, stress/sentinel, unknown/tap-out, and power-mode constraints. Avoid attaching this to speech generation until the eval surface is stronger.

7. Frontend evidence provenance

Upgrade the cockpit concept toward evidence provenance: exportable run records, hashable manifests, versioned protocol definitions, and clear separation between demo data and private operating data.

## What V3 Should Avoid Copying From V2

- Do not copy V2 checkpoints into V3.
- Do not promote V2 speech outputs as V3 capability.
- Do not copy raw full-stack speech training habits.
- Do not assume more plugged recurrence improves immature pathways.
- Do not let identity/protection language dominate ordinary dialogue targets.
- Do not run long monolithic training cycles.
- Do not rely on cherry-picked smoke prompts.
- Do not merge weak speech artifacts into the clean evidence path.
- Do not make claims beyond held-out transcript logs, repetition metrics, format-leak metrics, and registered evals.

The V2 lesson to preserve is narrow and valuable: train adapters over a protected core, gate depth by maturity, split training into bounded cycles, and reject checkpoints that do not pass held-out tests.

## V6 Lessons To Preserve

A clean V6 birth curriculum later needs:

- Accepted growth law before training starts.
- First eval list defined before the first checkpoint.
- Small initial core and explicit seeds.
- Split-cycle training with clean exits and checkpoint identity.
- Transcript logging from the beginning if speech is included.
- Habit-14 threshold as a stabilization gate, not a slogan.
- Context-aware protection, not rigid full-pattern locking.
- Maturity-gated recurrent depth.
- Stress, sentinel, and tap-out routing from day one.
- Battery, plugged, and demo power modes.
- Checkpoint promotion and rejection rules.
- Boundary language attached to every result.

V6 should inherit principles and evals, not unstable branch artifacts.

## Recommended V3 Experiment Queue

1. Write `docs/V3_EVIDENCE_RULES.md` defining how V3 appends artifacts without overwriting V5-derived evidence.
2. Add a lightweight `src/hpp_arch/` package for architecture descriptors and maturity/evidence metadata.
3. Refactor maturity-depth scoring into a reusable controller module with unit-sized tests.
4. Add a V3-only manifest writer for new eval outputs under `docs/v3_evidence/`.
5. Register one new CPU-safe eval: architecture boundary registry completeness.
6. Add cockpit export/import for local run evidence without changing existing logs.
7. Prototype router composition with synthetic calm, stress, unknown, and power-mode cases.
8. Only after the above, define a speech-adapter intake gate that references V2 results without loading V2 artifacts.

## Open Questions For Brent / Codex Director

- Should V3 initialize its own Git history, or should it be re-cloned from V5 with `.git` metadata intact?
- Should V3 rename package/app labels from V5 to V3 immediately, or preserve V5 labels until architecture changes begin?
- Should new V3 evidence live under `docs/v3_evidence/`, `docs/evals/v3/`, or both?
- Which component should be the first architectural remix: maturity-depth controller, router composition, or evidence manifest layer?
- Is the V3 cockpit allowed to become more operational, or should it remain a demo shell while the architecture layer changes underneath?
- What is the minimum evidence gate before any speech-related artifact can be mentioned in V3 docs?
- Should V6 curriculum planning stay in V5/V6 docs, or should V3 maintain a separate V6 lessons ledger?

## Intake Recommendation

Preserve V5's evidence spine: registered evals, JSON/JSONL artifacts, boundary language, Habit-14 discipline, maturity-gated depth, stress/tap-out routing, and simulation-first safety. Use V3 to remix architecture around those preserved laws, beginning with metadata, controllers, manifests, and router composition. Keep speech checkpoint behavior quarantined until it is measured through held-out, transcript-backed, V3-native gates.
