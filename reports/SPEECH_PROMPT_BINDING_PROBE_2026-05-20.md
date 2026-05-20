# HPP V2 Prompt Binding Probe

Date: 2026-05-20

## Purpose

Check whether semantic failures come from the checkpoint not learning answer phrases or from weak binding between prompt form and answer memory.

The semantic overfit probe showed that the model can memorize some answer phrases, but it cross-contaminates them across prompts.

## Setup

- Probe tool: `tools/speech_prompt_binding_probe.py`
- Checkpoint: `checkpoints/hpp_speech_semantic_overfit_probe_v1.pth`
- Sample artifact: `reports/speech_prompt_binding_probe_2026-05-20.json`
- Tool artifact: `reports/speech_prompt_binding_probe_tool_2026-05-20.json`
- Prompt variants:
  - plain prompt
  - plain prompt plus newline
  - `Answer directly:`
  - `Answer directly:` plus newline
  - `Use one sentence:` plus newline

## Result

The prompt wrapper changed behavior, but did not fully fix binding.

Tool summary:

- plain: 2 / 5 semantic pass
- plain plus newline: 2 / 5 semantic pass
- `Answer directly:`: 2 / 5 semantic pass
- `Answer directly:` plus newline: 2 / 5 semantic pass
- `Use one sentence:` plus newline: 3 / 5 semantic pass

Useful partial results:

- robot safety prompt produced the correct first sentence across variants
- finished-mind prompt produced the correct first sentence across variants
- overheating prompt worked best with `Use one sentence:`

Remaining failures:

- held-out prompt-set definition still failed
- Masamune low-battery answer still failed or drifted
- some prompts received the answer for a different trained prompt

## Meaning

Prompt shape matters, but the current speech path is still mixing answer memories.

The issue is now more specific:

- the model can store answer phrases
- the decoder can surface some of them
- prompt-answer binding is unreliable
- short outputs reduce cross-contamination

## Boundary

This is a diagnostic probe, not a readiness result.

Do not promote the overfit checkpoint.

Do not claim mature fluency.

## Next Step

Recommended next move:

1. Add a short-answer profile for diagnostic use.
2. Build a prompt-binding curriculum that contrasts similar prompts with different answers.
3. Consider whether the V5 adapter should use a small safety retrieval scaffold while native speech continues developing.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
