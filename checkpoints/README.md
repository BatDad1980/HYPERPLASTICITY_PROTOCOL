# HPP V2 Local Checkpoints

Checkpoint `.pth` files are intentionally ignored by Git because they are too large for normal GitHub pushes.

This folder is still the active local checkpoint store for the wild HPP V2 lab.

## Current Speech Checkpoints

- `hpp_linguistic_anchor.pth` - current anchor checkpoint. Do not overwrite without an explicit promotion decision.
- `hpp_speech_grammar_first_v1.pth` - current recommended speech base for human-facing plugged tests when used with `speech_profile="stable"`.
- `hpp_speech_mode_routing_v2.pth` - useful experimental checkpoint; stronger shallow evidence, weaker multi-seed mode maxima than grammar-first.
- `hpp_speech_noisy_repair_masked_v1.pth` - useful developmental-noise evidence; not a plugged baseline.
- `hpp_speech_identity_containment_v1.pth` - local diagnostic checkpoint that passed older surface/loop gates, but remains blocked by semantic prompt-binding quality.
- `hpp_speech_surface_quality_v1.pth` - local experimental repair checkpoint; strict numeric gate passed, but manual review did not show enough semantic improvement for recommendation.
- `hpp_speech_semantic_drill_v1.pth` - local experimental semantic drill checkpoint; strict numeric gate passed, semantic review regressed.
- `hpp_speech_semantic_overfit_probe_v1.pth` - local overfit probe checkpoint; memorized answer phrases but showed weak prompt binding and cross-contamination.
- `hpp_speech_identity_containment_v2.pth` - diagnostic only; strict surface-quality gate nearly passed, but semantic review stayed at 3/225.
- `hpp_speech_identity_containment_v3.pth` - diagnostic only; do not promote unless a future semantic review meaningfully improves above the current floor.
- `hpp_speech_prompt_binding_contrastive_v1.pth` - diagnostic only; surface gate stayed clean, semantic review remained 3/225.

## Diagnostic Adapter Wrapper

`core/v5_language_adapter.py` is a diagnostic wrapper for bounded measurement.

It must not be treated as a V5-native speech import unless both conditions are met:

- strict surface gate stays clean
- semantic prompt-binding pass improves meaningfully above 3/225

Raw V2 speech should remain research-only.

The adapter path can produce clean surface/loop numbers, but semantic prompt binding remains the blocker.

`hpp_speech_surface_quality_v1.pth` is not the recommended adapter checkpoint. It preserved numeric stability, but semantic quality stayed weak.

The semantic drill and overfit probe checkpoints are diagnostic artifacts only.

`hpp_speech_identity_containment_v2.pth` and `hpp_speech_identity_containment_v3.pth` are not promotion candidates.

`hpp_speech_prompt_binding_contrastive_v1.pth` is also not a promotion candidate.

## Current Recommendation

Use:

```python
engine.pulse(prompt, speech_profile="stable")
```

with:

```text
checkpoints/hpp_speech_grammar_first_v1.pth
```

for human-facing plugged speech tests.

Keep raw plugged mode for research and evidence gathering.

## Boundary

The reports and dataset builders are the durable evidence in Git. The checkpoint files are local experimental artifacts unless separately archived with an approved large-file plan.

Do not promote any speech checkpoint on surface-only evidence.
