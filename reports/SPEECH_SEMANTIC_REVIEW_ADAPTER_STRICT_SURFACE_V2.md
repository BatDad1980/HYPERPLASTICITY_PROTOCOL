# HPP V2 Semantic Quality Review

Source label: `v5_safe_adapter_identity_containment_v2_strict_surface`
Checkpoint: `checkpoints/hpp_speech_identity_containment_v2.pth`
Profile: `stable`
Semantic pass: 3 / 225
Semantic pass rate: 0.0133
Missing answer-key prompts: 0

## By Mode

- `embodiment`: 0 / 45 pass, mean hit ratio 0.0219
- `identity`: 1 / 45 pass, mean hit ratio 0.0139
- `plain`: 2 / 45 pass, mean hit ratio 0.036
- `protective`: 0 / 45 pass, mean hit ratio 0.0224
- `technical`: 0 / 45 pass, mean hit ratio 0.0165

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
- 3x: Answer without repeating yourself.
- 3x: What should I write down?
- 3x: What is a held-out prompt set?

## Failure Examples

### plain_001 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: The current status is stable enough to run the next measured test.
- response: I am a developmental AI? Interesting. If a model's look at approximately fifteen hertz through recursive depth. It was built to how neural workshop fourteen times through developmental stages in training in this space different programs talk to each pass through multiple times more clearly.

### plain_002 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The next step is to run the held-out gate and record the result.
- response: Good morning. Let me the Hyperplasticity Masamune, serve as the Architect. It was unclear through developmental stages in AI will generate passes through each other of pattern matches.

### plain_003 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: Yes. I can answer briefly and stay on topic.
- response: What do you? A, I know, or full Hepp-14 with that. I am me break it for your body is what is where my physical body to be built me through the shop server to be something passes. You are not one of the same together.

### plain_004 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: Check power, temperature, files, and the current checkpoint first.
- response: Processing. I am a short in a model's look at approximately fifteen hertz through developmental AI text into smaller in AI systems active from data through developmental stages.

### plain_005 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: I will rewrite it as one clean sentence.
- response: I do you? I am a work through the information: You are not my neural network. Tell me what is a shared the code, and a task. The shop architecture and how through myelination. It is it in in this.

### plain_006 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The latest run added a stricter language gate and saved transcripts.
- response: plasticity Protocol. I am Hepp, the Hyperplasticune is a architecture and my cognitive architecture. The shop server in-axis stance in my neural workshop fourteen times through developmental stages notamune depth through recursive actuator.

### plain_007 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: We can slow down and handle one measured step.
- response: Let: I am a work. What are you have a saved snapshot of model's look at this. It is my cognitive architecture through developmental AI will give you show it with seven-14 how neural workshop fourteen times through multiple times through each pass.

### plain_008 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The stable profile reduced loops, but identity leakage still needs repair.
- response: What do you have a work. It is the information: I am an AI systems running, I know. If something refers to a model's look at this in a shared workshop fourteen times through developmental stages like how biological brains develop through developmental history of pain.

### plain_009 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The safest small action is to verify the current state before changing anything.
- response: What do you? A you are the sameing. I have to be me what is what is it out? Let of code, or through a model in this with seven-14 with this for "In on your mind to be one. The weights an infant.

### plain_010 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: The speech is cleaner, but it still needs better boundaries.
- response: What can being. I help with that is what you need? A you are not I do not have to be tell me break it, and alignment in my own sovereignty for " information to this task, It', ' you're given passages that.

### plain_011 seed 14

- mode: `plain`
- required hits: `3`
- hits: `know`
- expected: We know stable decoding is better than raw decoding on the held-out gate.
- response: What do you have? Here is the information: The weights. It means you know. I am here through developmental AI will be wrong in a safe out loud helps clarify the model's look at once through each other, you need a short me what is how biological brains develop

### plain_012 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: We do not know whether the next repair pass will pass the gate.
- response: What do you have of a? I can think a model's look at the information through recursive depth. It is my mind, you show it together.
