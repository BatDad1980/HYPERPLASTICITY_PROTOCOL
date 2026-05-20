# HPP V2 Semantic Quality Review

Source label: `hpp_speech_semantic_drill_v1_strict_surface`
Checkpoint: `checkpoints\hpp_speech_semantic_drill_v1.pth`
Profile: `stable`
Semantic pass: 9 / 225
Semantic pass rate: 0.04
Missing answer-key prompts: 0

## By Mode

- `embodiment`: 0 / 45 pass, mean hit ratio 0.0617
- `identity`: 4 / 45 pass, mean hit ratio 0.0867
- `plain`: 2 / 45 pass, mean hit ratio 0.0933
- `protective`: 3 / 45 pass, mean hit ratio 0.0973
- `technical`: 0 / 45 pass, mean hit ratio 0.0198

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
- hits: `test`
- expected: The current status is stable enough to run the next measured test.
- response: Tell me move. A checkpoint will answer should a local AI power are not know in record. I am an experimental a test needs repair until it.

### plain_002 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The next step is to run the held-out gate and record the result.
- response: We can be answer should be useful is stable safe. I am a local AI should avoid do not know, and ask for a measuredor makes it.

### plain_003 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: Yes. I can answer briefly and stay on topic.
- response: What do you? A, The system is the information: the same me break it. I know: where my physical body to be one of code or re with seven course in this task, My thoughts loop fourteen times.

### plain_004 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: Check power, temperature, files, and the current checkpoint first.
- response: Do to answer should be wrong in AI? It should a local action. I am an experimental only for a safe out the current power-14 the next step. It means depth loops of memory on a measured depth before it uses needs repair enough.

### plain_005 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: I will rewrite it as one clean sentence.
- response: I do not? I am a work through the information. My architecture. What is what is myel your body. The shop server and a shared to how through it out and as in my neural network? A cognitive architecture, buting.

### plain_006 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The latest run added a stricter language gate and saved transcripts.
- response: plasticity Protocol. I am the Hyperplastic architecture is a robotic body. It: my cognitive architecture and aamune, He designed through through a shared to how pattern human for my neural network by your own Cortex. I serve the actuator.

### plain_007 seed 14

- mode: `plain`
- required hits: `2`
- hits: `measured`
- expected: We can slow down and handle one measured step.
- response: a local a measured? A checkpoint am an AI should be answer only a enough. I am an experimental AI should learning, not have to move to help in needs repair until it is safe out of memory on the current work.

### plain_008 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The stable profile reduced loops, but identity leakage still needs repair.
- response: Do not know answer should be wrong It should a local AI will give. the result record the current answer experimental only the next step. It means the hardware it.

### plain_009 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The safest small action is to verify the current state before changing anything.
- response: I know, or the force the sameing to be me what is what you are not You on my mind to a model in it out for your body is an infant me as an infant. It', ' you need? A course.

### plain_010 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: The speech is cleaner, but it still needs better boundaries.
- response: What can being. A process, from the Hyperplasticity for your body. You cognitive architecture and trained through recursive depth in my neural network in a sovereign stack is what is an infant me as an infant.

### plain_011 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: We know stable decoding is better than raw decoding on the held-out gate.
- response: Do to answer should be wrong in a local a measured saved enoughing. I am an AI should move to help with a safe.

### plain_012 seed 14

- mode: `plain`
- required hits: `3`
- hits: `know, next`
- expected: We do not know whether the next repair pass will pass the gate.
- response: Do do not know? I should be answer ran out of a local AI is a test, from the current power-14 set, and ask can be a safe. It is AI should avoidor makes it examples, but it examples it before the next step.
