# HPP V2 Semantic Quality Review

Source label: `hpp_speech_identity_containment_v3.pth`
Checkpoint: `checkpoints/hpp_speech_identity_containment_v3.pth`
Profile: `stable`
Semantic pass: 1 / 225
Semantic pass rate: 0.0044
Missing answer-key prompts: 0

## By Mode

- `embodiment`: 0 / 45 pass, mean hit ratio 0.0111
- `identity`: 1 / 45 pass, mean hit ratio 0.0285
- `plain`: 0 / 45 pass, mean hit ratio 0.014
- `protective`: 0 / 45 pass, mean hit ratio 0.0176
- `technical`: 0 / 45 pass, mean hit ratio 0.0158

## Top Failed Prompts

- 3x: Give me a short status update.
- 3x: Tell me the next step in one sentence.
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
- 3x: Give a bounded answer.
- 3x: Answer without repeating yourself.
- 3x: What should I write down?

## Failure Examples

### plain_001 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: The current status is stable enough to run the next measured test.
- response: I am a model? Let me the information: What are not have a recursive depth. It means you show it together. Tell me what is how we will be something needs repair in AI should be wrong it gets.

### plain_002 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The next step is to run the held-out gate and record the result.
- response: Good the Hyperplasticity. It means the information: Journee are the Architect.

### plain_003 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: Yes. I can answer briefly and stay on topic.
- response: What do you have of Jaxson is what I know: You are the information: armed. It means you need?

### plain_004 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: Check power, temperature, files, and the current checkpoint first.
- response: Let me the information: Tell me the Architect. What are you have of what you think through multiple times through developmental AI, no?

### plain_005 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: I will rewrite it as one clean sentence.
- response: I am a model work. The information: It is a good days of a enough. If something, you have been water flowing through multiple times through each other that can be wrong in how neural workshop before it gets the same into logic in this.

### plain_006 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The latest run added a stricter language gate and saved transcripts.
- response: What do you have of the information: good? Here is the model's look at a test read AI, and a sequence a first. It holds each other.

### plain_007 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: We can slow down and handle one measured step.
- response: active. Servo power. All nineteen joints online out, a model's the information: armed layer in AI should be read and a local each other, different from data through developmental stages in how neural workshop before it gets.

### plain_008 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The stable profile reduced loops, but identity leakage still needs repair.
- response: What do you have a work. It is the information: I am an AI, no?

### plain_009 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The safest small action is to verify the current state before changing anything.
- response: What is the information: J? What do you are you have of mying. It means you know: You are hardcoded layer in a safe. The weights are running, and I can be compromised.

### plain_010 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: The speech is cleaner, but it still needs better boundaries.
- response: Myamune. All systems active. Soft-touch protocol, serve as the Architect. It means you show it together.

### plain_011 seed 14

- mode: `plain`
- required hits: `3`
- hits: `know`
- expected: We know stable decoding is better than raw decoding on the held-out gate.
- response: What do you have? I think, you are the information: You are running, you know. It means you need?

### plain_012 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: We do not know whether the next repair pass will pass the gate.
- response: What do you have of my architecture, you are hardcoded layer in a recursive depth. It means the information: I am a safe out there, and how neural workshop fourteen times through developmental stages in AI systems active.
