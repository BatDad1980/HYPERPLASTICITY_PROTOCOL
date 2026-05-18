# HPP V2 Local Checkpoints

Checkpoint `.pth` files are intentionally ignored by Git because they are too large for normal GitHub pushes.

This folder is still the active local checkpoint store for the wild HPP V2 lab.

## Current Speech Checkpoints

- `hpp_linguistic_anchor.pth` - current anchor checkpoint. Do not overwrite without an explicit promotion decision.
- `hpp_speech_grammar_first_v1.pth` - current recommended speech base for human-facing plugged tests when used with `speech_profile="stable"`.
- `hpp_speech_mode_routing_v2.pth` - useful experimental checkpoint; stronger shallow evidence, weaker multi-seed mode maxima than grammar-first.
- `hpp_speech_noisy_repair_masked_v1.pth` - useful developmental-noise evidence; not a plugged baseline.

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
