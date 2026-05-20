# HPP V2 Speech Next Target - Semantic Prompt Binding

Date: 2026-05-20

## Decision

Stop optimizing surface-only gates.

No speech checkpoint is currently approved for V5-native promotion.

Do not promote:

- `hpp_speech_identity_containment_v2.pth`
- `hpp_speech_identity_containment_v3.pth`

## Current Read

Surface gates are useful but insufficient.

Recent evidence showed:

- clean surface/loop results can coexist with poor answers
- identity-containment V2 reached strong surface numbers but only 3/225 semantic pass
- identity-containment V3 has no promotion value unless semantic quality improves
- overfit probes show answer phrases can be memorized, but prompt binding is weak

## Success Condition

The next valid improvement must satisfy both:

1. Surface gate stays clean.
2. Semantic prompt-binding pass improves meaningfully above 3/225.

Manual transcript review remains required before any V5-native language claim.

## Next Target

Semantic prompt binding.

Recommended work:

1. Add a short-answer diagnostic profile.
2. Build contrastive prompt-binding data with similar prompts that require different answers.
3. Test exact prompt wrappers against plain prompts.
4. Track semantic pass rate as the primary metric, not surface-only pass rate.

## Boundary

No AGI claim.

No full fluency claim.

No LLM replacement claim.

No checkpoint promotion from surface-only evidence.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
