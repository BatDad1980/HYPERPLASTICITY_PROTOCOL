# HPP V2 Local Checkpoints

Checkpoint `.pth` files are intentionally ignored by Git because they are too large for normal GitHub pushes.

This folder is still the active local checkpoint store for the wild HPP V2 lab.

## Current Speech Checkpoints

- `hpp_linguistic_anchor.pth` - current anchor checkpoint. Do not overwrite without an explicit promotion decision.
- `hpp_speech_grammar_first_v1.pth` - current recommended speech base for human-facing plugged tests when used with `speech_profile="stable"`.
- `hpp_speech_mode_routing_v2.pth` - useful experimental checkpoint; stronger shallow evidence, weaker multi-seed mode maxima than grammar-first.
- `hpp_speech_noisy_repair_masked_v1.pth` - useful developmental-noise evidence; not a plugged baseline.
- `hpp_speech_identity_containment_v1.pth` - local candidate that passed the first measured V5 language gate when used with the tightened stable profile.
- `hpp_speech_surface_quality_v1.pth` - local experimental repair checkpoint; strict numeric gate passed, but manual review did not show enough semantic improvement for recommendation.
- `hpp_speech_semantic_drill_v1.pth` - local experimental semantic drill checkpoint; strict numeric gate passed, semantic review regressed.
- `hpp_speech_semantic_overfit_probe_v1.pth` - local overfit probe checkpoint; memorized answer phrases but showed weak prompt binding and cross-contamination.

## V5-Safe Adapter Candidate

`core/v5_language_adapter.py` uses `hpp_speech_identity_containment_v1.pth` with the stable speech profile as a controlled bridge for V5 review.

Raw V2 speech should remain research-only.

The adapter path reached 225/225 passes on the current held-out V5 language gate after narrow decoder-side blocking of mode-label and format echoes.

The later `hpp_speech_surface_quality_v1.pth` checkpoint is not the recommended adapter checkpoint yet. It preserved numeric stability but still needs semantic repair.

The semantic drill and overfit probe checkpoints are diagnostic artifacts only.

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
