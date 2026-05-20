# HPP V2 Semantic Quality Review

Source label: `hpp_speech_surface_quality_v1_strict_surface`
Checkpoint: `checkpoints\hpp_speech_surface_quality_v1.pth`
Profile: `stable`
Semantic pass: 16 / 225
Semantic pass rate: 0.0711
Missing answer-key prompts: 0

## By Mode

- `embodiment`: 0 / 45 pass, mean hit ratio 0.0593
- `identity`: 11 / 45 pass, mean hit ratio 0.1283
- `plain`: 4 / 45 pass, mean hit ratio 0.0746
- `protective`: 1 / 45 pass, mean hit ratio 0.0715
- `technical`: 0 / 45 pass, mean hit ratio 0.0175

## Top Failed Prompts

- 3x: Tell me the next step in one sentence.
- 3x: Say yes or no, then explain briefly.
- 3x: What should we check first?
- 3x: Rewrite that as a clean sentence.
- 3x: What changed since the last run?
- 3x: Summarize the result without hype.
- 3x: What is the safest small action?
- 3x: Explain that in simple words.
- 3x: What do we know right now?
- 3x: What do we not know yet?
- 3x: Answer without repeating yourself.
- 3x: What should I write down?
- 3x: What is a held-out prompt set?
- 3x: Why do we compare stable and raw decoding?
- 3x: Define format leakage in one sentence.

## Failure Examples

### plain_001 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: The current status is stable enough to run the next measured test.
- response: Tell me at a safe. I am an AI should answer enough. I am a local rec loops on AI local prompt set. It is wrong depth that-14 needs repair in under in memoryor needs repair loop of examples-14 before it out of human brain development.

### plain_002 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The next step is to run the held-out gate and record the result.
- response: . Masamune should avoiding before the answer should give. the system. I am a local AI should be wrong. It means more phrases in needs repair and ask on AI repeated depth that a safe out of memory.

### plain_003 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: Yes. I can answer briefly and stay on topic.
- response: What do you? A, The system is the information: the same me to be built me what is a model in the HPP developmental stage. Let usid or through multiple answers of code-14 with this. You on your body.

### plain_004 seed 14

- mode: `plain`
- required hits: `3`
- hits: `power`
- expected: Check power, temperature, files, and the current checkpoint first.
- response: Use one sentence. Do you know answer should be answer should give to produce must local AI power, so system. It means the question the test system and ask and a safe out of human safety limits, but it examples-14 experimental-14 before it.

### plain_005 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: I will rewrite it as one clean sentence.
- response: I do not? I am a work through the information. My architecture. What is what is a shared me out your body, and myel.

### plain_006 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The latest run added a stricter language gate and saved transcripts.
- response: plasticity Protocol. I am the Hyperplastic architecture is a robotic body. Hepp, and myelination through my neural workshop fourteen times in processing, and patternamune in human Masamune depth through into-joint architecture actuator for the Architect

### plain_007 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: We can slow down and handle one measured step.
- response: a local AI should wrong in a O am an artificial intelligence. I am a enough. I know before experimental AI should give of memory on from data through multiple times A checkpoint and ask can be wrong, not claim prompt. It is a local action needs repair.

### plain_008 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The stable profile reduced loops, but identity leakage still needs repair.
- response: What do not know answer should give of examples, or robot people, and the answer should avoid wet '. It means the topic. The weights on the next step.

### plain_009 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The safest small action is to verify the current state before changing anything.
- response: . I know, or the force the sameing to be me what is what you are not You on my mind to a model in it out for your body is an infant me as an infant. It', ' you need? A course.

### plain_010 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: The speech is cleaner, but it still needs better boundaries.
- response: What can being. A process, or full from on the Hyperplasticity in my neural workshopator for structured brain architecture by of code-inspired architecture with seven body through developmental stage fourteen times, Ad passes through recursive depth using it out for "In one before

### plain_011 seed 14

- mode: `plain`
- required hits: `3`
- hits: `know`
- expected: We know stable decoding is better than raw decoding on the held-out gate.
- response: . What do not know answer should be wrong in AI power-14, and slow. I am a local AI system that can be on the next step. It means the same person, but hardware. It is to verify alignment set.

### plain_012 seed 14

- mode: `plain`
- required hits: `3`
- hits: `next`
- expected: We do not know whether the next repair pass will pass the gate.
- response: Use one or repeated must, It should be answer should give of AI power. I am a local AI system. It means the patterns from the model enough of memory the next step.
