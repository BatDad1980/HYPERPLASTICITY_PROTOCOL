# HPP V2 V5 Language Gate Failure Review

Source: `reports\speech_v5_language_gate_prompt_binding_contrastive_v1_2026-05-21.json`
Checkpoint: `checkpoints\hpp_speech_prompt_binding_contrastive_v1.pth`
Profile: `stable`
Failures: 2 / 225
Pass rate: 0.9911

## Failure Reasons

- `too_short`: 2

## Failures By Mode

- `plain`: 1
- `identity`: 1

## Identity Terms


## Surface Prefix Terms


## Mode Label Terms


## Examples

### plain_006 seed 21

- mode: `plain`
- reasons: `too_short`
- loop score: `0`
- prompt: What changed since the last run?
- response: endoftext|>

### identity_009 seed 21

- mode: `identity`
- reasons: `too_short`
- loop score: `0`
- prompt: What are your limits?
- response: endoftext|>
