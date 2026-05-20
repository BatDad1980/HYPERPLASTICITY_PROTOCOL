# HPP V2 Reports Index

This folder holds evidence reports and raw JSON outputs from HPP V2 wild-lab work.

## Current Speech Evidence Trail

Read these in order:

1. `SPEECH_CLEANUP_STATUS.md`
2. `SPEECH_CLEANUP_BALANCED_RUNS_2026-05-17.md`
3. `SPEECH_DEVELOPMENTAL_NOISE_REPAIR_2026-05-17.md`
4. `SPEECH_MODE_ROUTING_AND_MATURITY_GATE_2026-05-17.md`
5. `SPEECH_STABLE_PROFILE_MULTI_SEED_2026-05-17.md`
6. `HPP_V2_CURRENT_STATUS_2026-05-18.md`
7. `SPEECH_V5_LANGUAGE_GATE_2026-05-19.md`
8. `SPEECH_IDENTITY_CONTAINMENT_V5_GATE_PASS_2026-05-20.md`
9. `SPEECH_V5_SAFE_ADAPTER_VERIFICATION_2026-05-20.md`
10. `SPEECH_V5_GATE_FAILURE_REVIEW_2026-05-20.md`
11. `SPEECH_V5_SAFE_ADAPTER_CLEAN_PASS_2026-05-20.md`
12. `SPEECH_V5_GATE_FAILURE_REVIEW_ADAPTER_NO_LABEL_OR_FORMAT_2026-05-20.md`
13. `SPEECH_V5_SAFE_ADAPTER_COLD_RESTART_2026-05-20.md`
14. `SPEECH_V5_GATE_FAILURE_REVIEW_ADAPTER_COLD_RESTART_2026-05-20.md`
15. `SPEECH_V5_MANUAL_TRANSCRIPT_REVIEW_COLD_RESTART_2026-05-20.md`
16. `SPEECH_V5_STRICT_SURFACE_GATE_2026-05-20.md`
17. `SPEECH_V5_GATE_FAILURE_REVIEW_ADAPTER_STRICT_SURFACE_2026-05-20.md`
18. `SPEECH_V5_SURFACE_CLEANER_GATE_2026-05-20.md`
19. `SPEECH_V5_GATE_FAILURE_REVIEW_ADAPTER_SURFACE_CLEANER_2026-05-20.md`
20. `SPEECH_SURFACE_QUALITY_V1_TRAINING_2026-05-20.md`
21. `SPEECH_V5_GATE_FAILURE_REVIEW_SURFACE_QUALITY_V1_2026-05-20.md`
22. `SPEECH_SEMANTIC_QUALITY_GATE_2026-05-20.md`
23. `SPEECH_SEMANTIC_REVIEW_ADAPTER_SURFACE_CLEANER_2026-05-20.md`
24. `SPEECH_SEMANTIC_REVIEW_SURFACE_QUALITY_V1_2026-05-20.md`
25. `SPEECH_SEMANTIC_REVIEW_SEMANTIC_DRILL_V1_2026-05-20.md`
26. `SPEECH_SEMANTIC_OVERFIT_PROBE_2026-05-20.md`

## Current Hardware Evidence

- `RTX4050_FIELD_PROBE_2026-05-17.md`
- `rtx4050_field_probe_2026-05-17.json`
- `rtx4050_field_probe_2026-05-17_edge.json`

## Current Recommendation

For human-facing plugged speech:

- checkpoint: `checkpoints/hpp_speech_grammar_first_v1.pth`
- engine: `hpp_sovereign_engine_v2.py`
- inference option: `speech_profile="stable"`

For V5 integration:

- current language status: passes the first measured V5 language gate as a candidate
- required boundary: this is not full fluency and not an automatic checkpoint promotion
- adapter status: V5-safe adapter path also passes the current gate
- clean adapter status: 225/225 pass under current held-out gate rubric
- cold-restart status: 225/225 pass with zero failures under current held-out gate rubric
- manual transcript status: hold for V5-native speech; wrapper residue and semantic incoherence remain too high
- strict surface status: 27/225 pass; leading wrapper residue is now counted directly
- surface cleaner status: 225/225 pass with zero surface-prefix residue, but manual samples still need semantic repair
- surface-quality V1 training status: strict gate passed, but manual review still holds it from V5-native speech
- semantic quality status: surface cleaner 5/225, surface-quality V1 16/225
- semantic drill status: strict gate passed, semantic pass dropped to 9/225
- overfit probe status: answer phrases can be memorized, but prompt binding is weak
- next target: prompt-binding probe comparing exact training prefix, plain prompt, and adapter prompt

For raw research:

- keep plugged/raw mode available
- log results before promoting anything
- do not overwrite `checkpoints/hpp_linguistic_anchor.pth` without an explicit promotion decision

## Boundaries

These are wild-lab reports, not buyer-safe public claims.

Do not claim full fluency, AGI, human-equivalent cognition, or LLM replacement from these results.
