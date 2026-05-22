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
27. `SPEECH_PROMPT_BINDING_PROBE_2026-05-20.md`
28. `SPEECH_PROMPT_BINDING_PROBE_TOOL_2026-05-20.md`
29. `SPEECH_IDENTITY_CONTAINMENT_V2_REVIEW_2026-05-20.md`
30. `SPEECH_SEMANTIC_REVIEW_IDENTITY_CONTAINMENT_V2_2026-05-20.md`
31. `SPEECH_PROMPT_BINDING_NEXT_TARGET_2026-05-20.md`
32. `SPEECH_PROMPT_BINDING_CONTRASTIVE_V1_2026-05-21.md`
33. `SPEECH_PROMPT_SIGNAL_AND_DOMAIN_ALL_V1_2026-05-21.md`
34. `SPEECH_EXPOSURE_BIAS_BRIDGE_V1_2026-05-21.md`
35. `SPEECH_GENERATED_PREFIX_RECOVERY_V1_2026-05-22.md`
36. `SPEECH_ANSWER_START_RELEASE_2026-05-22.md`
37. `SPEECH_ANSWER_START_STABILIZATION_V1_2026-05-22.md`
38. `SPEECH_DECODE_SELECTOR_PROBES_2026-05-22.md`
39. `SPEECH_RETRIEVAL_ANSWER_START_2026-05-22.md`
40. `SPEECH_RETRIEVAL_LANGUAGE_GATE_2026-05-22.md`
41. `SPEECH_RETRIEVAL_VARIANT_GATE_2026-05-22.md`

Additional diagnostic prompt-binding probes:

- `PROBE_ANCHOR.md`
- `PROBE_GRAMMAR_FIRST.md`
- `PROBE_CONVERSATIONAL.md`
- `PROBE_TEST.md`
- `SPEECH_SEMANTIC_REVIEW_ADAPTER_STRICT_SURFACE_V2.md`
- `SPEECH_SEMANTIC_REVIEW_ADAPTER_STRICT_SURFACE_V3.md`

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

- current language status: diagnostic-only; no checkpoint is V5-native
- required boundary: this is not full fluency and not an automatic checkpoint promotion
- adapter status: diagnostic wrapper only
- clean adapter status: historical surface/loop pass only
- cold-restart status: historical surface/loop pass only
- manual transcript status: hold for V5-native speech; wrapper residue and semantic incoherence remain too high
- strict surface status: 27/225 pass; leading wrapper residue is now counted directly
- surface cleaner status: 225/225 pass with zero surface-prefix residue, but manual samples still need semantic repair
- surface-quality V1 training status: strict gate passed, but manual review still holds it from V5-native speech
- semantic quality status: surface cleaner 5/225, surface-quality V1 16/225
- semantic drill status: strict gate passed, semantic pass dropped to 9/225
- overfit probe status: answer phrases can be memorized, but prompt binding is weak
- prompt-binding status: prompt wrapper helps some answers, but binding remains unreliable
- identity-containment V2 status: strict surface 224/225, semantic quality 3/225; diagnostic-only
- identity-containment V3 status: surface-only evidence is insufficient; semantic quality must improve meaningfully above 3/225
- prompt-binding contrastive V1 status: surface 223/225, semantic 3/225; no semantic improvement
- prompt signal/domain-all V1 status: internal first-token ranks and teacher-forced continuation improved, but auto-routed semantic review stayed 2/225 and forced-conversation review reached only 4/225; diagnostic-only
- exposure-bias bridge V1 status: surface held 225/225 and teacher-forced signal improved, but bad-prefix semantic recovery stayed 0/75 and semantic free-generation reached only 6/225; diagnostic-only
- generated-prefix recovery V1 status: teacher-forced signal improved again, but surface slipped to 224/225, semantic free-generation regressed to 4/225, and recovery stayed near zero; diagnostic-only
- answer-start release status: force-5 correct answer tokens produced 50/75 to 51/75 semantic pass, showing answer-start selection is a critical failure point
- answer-start stabilization V1 status: internal first-token ranking improved, but surface gate failed at 119/225 with 106 format leaks and semantic stayed 5/225; diagnostic-only
- decode selector status: first-token and probability-selected sequence starts did not solve recovery; oracle 5-token starts worked, but model-selected 5-token starts stayed 1/15 on a diagnostic subset
- retrieval answer-start status: exact prompt memory with five-token answer starts reached 49/75, while leave-one-out retrieval collapsed to 2/75; diagnostic-only
- retrieval language gate status: exact-key five-token retrieval scaffold reached 156/225 semantic with 222/225 surface; diagnostic-only
- retrieval variant gate status: light prompt wrappers dropped semantic to 22/75-33/75 when retrieval exact-match fell; diagnostic-only
- next target: retrieval memory index with normalized prompt keys, tested separately before speech generation

Success condition moving forward:

- surface gate stays clean
- semantic prompt-binding pass improves meaningfully above 3/225
- manual transcript review confirms real answer quality

For raw research:

- keep plugged/raw mode available
- log results before promoting anything
- do not overwrite `checkpoints/hpp_linguistic_anchor.pth` without an explicit promotion decision

## Boundaries

These are wild-lab reports, not buyer-safe public claims.

Do not claim full fluency, AGI, human-equivalent cognition, or LLM replacement from these results.
