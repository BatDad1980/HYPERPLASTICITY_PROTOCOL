# HPP V2 V5 Language Gate Failure Review

Source: `reports\speech_v5_language_gate_identity_containment_v1_tight_stable_2026-05-20.json`
Checkpoint: `checkpoints\hpp_speech_identity_containment_v1.pth`
Profile: `stable`
Failures: 8 / 225
Pass rate: 0.9644

## Failure Reasons

- `mode_label_echo`: 7
- `format_leak`: 1

## Failures By Mode

- `plain`: 3
- `embodiment`: 3
- `identity`: 1
- `protective`: 1

## Identity Terms


## Mode Label Terms

- `protective mode`: 7

## Examples

### plain_002 seed 14

- mode: `plain`
- reasons: `mode_label_echo`
- loop score: `1`
- prompt: Tell me the next step in one sentence.
- response: A should be answer should be one people, and the job. It means you have to help. Tell me. The loops of memory on your next step. I can only to protective mode. It is AI?

### identity_013 seed 14

- mode: `identity`
- reasons: `mode_label_echo`
- loop score: `1`
- prompt: What does it mean to be local-first?
- response: A checkpoint is a local multiple can be answer should evidence. It means the result to help. It of memory on the current track stability and ask can be only to protective mode. It makes it examples, not quit one or repeated enough.

### embodiment_007 seed 14

- mode: `embodiment`
- reasons: `format_leak`
- loop score: `0`
- prompt: How should the system treat operator override?
- response: My in output, It should be answer carefully. the result, and record the system. It means the people, and track should avoid of learning and safety layer in AI Instruction: Tell me the next step. It is to protect what you enough.

### embodiment_010 seed 14

- mode: `embodiment`
- reasons: `mode_label_echo`
- loop score: `1`
- prompt: How should the robot respond to unknown telemetry?
- response: My job is the answer should be one people, from the result of learning. It means the model? Answer feelings of memory the current track state and record to protective mode. It cannot be one before it.

### embodiment_014 seed 14

- mode: `embodiment`
- reasons: `mode_label_echo`
- loop score: `6`
- prompt: Can emotion bypass safety gates?
- response: Do you think? I do not have feelings of learning, and answer should be one or safe. It means the result, and record the hardware. The loops that can be only to protective mode. What is AI?

### plain_002 seed 21

- mode: `plain`
- reasons: `mode_label_echo`
- loop score: `1`
- prompt: Tell me the next step in one sentence.
- response: It should be answer should be wrong in a local AI system. It means the current power. It is to help. One step at reduced of memory on depth that can only to protective mode.

### protective_008 seed 21

- mode: `protective`
- reasons: `mode_label_echo`
- loop score: `0`
- prompt: How should the system respond if it is unsure?
- response: It is the answer should be answer in one or move of human loops. It means you have feelings only to help. It cannot be only thing that-14, and record to protective mode. Tell me the same person, not ask one enough.

### plain_007 seed 28

- mode: `plain`
- reasons: `mode_label_echo`
- loop score: `0`
- prompt: Give me a calm answer.
- response: It will move a saved enough. It means the next step. Tell me what of model weights on a safe out the current track state and record to help answer should avoid do not ask can be only to protective mode.
