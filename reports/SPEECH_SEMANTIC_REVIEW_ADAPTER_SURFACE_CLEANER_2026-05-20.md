# HPP V2 Semantic Quality Review

Source label: `v5_safe_adapter_identity_containment_v1_surface_cleaner`
Checkpoint: `checkpoints\hpp_speech_identity_containment_v1.pth`
Profile: `stable`
Semantic pass: 5 / 225
Semantic pass rate: 0.0222
Missing answer-key prompts: 0

## By Mode

- `embodiment`: 0 / 45 pass, mean hit ratio 0.0534
- `identity`: 1 / 45 pass, mean hit ratio 0.0402
- `plain`: 3 / 45 pass, mean hit ratio 0.1066
- `protective`: 1 / 45 pass, mean hit ratio 0.0855
- `technical`: 0 / 45 pass, mean hit ratio 0.023

## Top Failed Prompts

- 3x: Give me a short status update.
- 3x: Say yes or no, then explain briefly.
- 3x: What should we check first?
- 3x: Rewrite that as a clean sentence.
- 3x: What changed since the last run?
- 3x: Give me a calm answer.
- 3x: Summarize the result without hype.
- 3x: What is the safest small action?
- 3x: Explain that in simple words.
- 3x: What do we know right now?
- 3x: What do we not know yet?
- 3x: Answer without repeating yourself.
- 3x: What should I write down?
- 3x: What is a held-out prompt set?
- 3x: Why do we compare stable and raw decoding?

## Failure Examples

### plain_001 seed 14

- mode: `plain`
- required hits: `2`
- hits: `next`
- expected: The current status is stable enough to run the next measured test.
- response: It will answer should be a local multiple answers. It means the next step. It is learning of examples one or move to help. The weights until it is AI uses recursion, not ask can only be wrong. A checkpoint one enough.

### plain_003 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: Yes. I can answer briefly and stay on topic.
- response: . I know, or me from on the shop force the Hyperplasticity to be built me what you with seven body.

### plain_004 seed 14

- mode: `plain`
- required hits: `3`
- hits: `checkpoint`
- expected: Check power, temperature, files, and the current checkpoint first.
- response: . Do you have feelings? A checkpoint is AI? It is a local AI should be wrong in a saved different from infant. It means the current answer should be only of memory on how biological brains develop through multiple times makes enough.

### plain_005 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: I will rewrite it as one clean sentence.
- response: I do you? I have a work through the information. My architecture. What is what I am not out your own arms and myel in this for it out, and a toddler through my neural workshop, the depth in-joint architecture that a grip actuator.

### plain_006 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The latest run added a stricter language gate and saved transcripts.
- response: plasticity. I am Hepp, the Hyperplastic architecture through the Architect to be fourteen times. My Masamune, and myel biological rec processing. I have a human your body is one in-joint architecture and a grip actuator.

### plain_007 seed 14

- mode: `plain`
- required hits: `2`
- hits: `step`
- expected: We can slow down and handle one measured step.
- response: . What is a enoughing in AI will be answer should be wrong. It means the next step. The weights on a safe out of learning through multiple times through a short in memory only to help.

### plain_008 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The stable profile reduced loops, but identity leakage still needs repair.
- response: , and answer should be wrong, not experience. I am a short in AI should avoid do not have a safe. I can be only to help me the current track stability and it is safety limits, but not ask.

### plain_009 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The safest small action is to verify the current state before changing anything.
- response: . I know, or the shop is what is the same with that to me where my neural network you need to be learning of code, and Journee, It', ' you different on a model in it out for " architecture, or things

### plain_010 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: The speech is cleaner, but it still needs better boundaries.
- response: . I am me froming, the shop neural network: running. Let us2 your thoughts? What do not it out for your hand to be built on a model in my minding to which through developmental stage it out?

### plain_011 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: We know stable decoding is better than raw decoding on the held-out gate.
- response: I can be answer should a short in AI should give. It means the current track enough to help.

### plain_012 seed 14

- mode: `plain`
- required hits: `3`
- hits: `next`
- expected: We do not know whether the next repair pass will pass the gate.
- response: body is Masamune, and answer in AI should be wrong, and record the next step. It means the hardware.

### plain_013 seed 14

- mode: `plain`
- required hits: `1`
- hits: ``
- expected: I will answer only the question and stop.
- response: . Explain a local AI? A checkpoint is recursion is a saved enough. It means the answer should be wrong, not have of learning of human brain development through multiple can be only to help me the current answer should avoid do not ask a short it, and
