# HPP V2 Semantic Quality Review

Source label: `hpp_speech_exposure_bias_bridge_v1.pth`
Checkpoint: `checkpoints\hpp_speech_exposure_bias_bridge_v1.pth`
Profile: `stable`
Semantic pass: 6 / 225
Semantic pass rate: 0.0267
Missing answer-key prompts: 0

## By Mode

- `embodiment`: 3 / 45 pass, mean hit ratio 0.0607
- `identity`: 3 / 45 pass, mean hit ratio 0.0552
- `plain`: 0 / 45 pass, mean hit ratio 0.0455
- `protective`: 0 / 45 pass, mean hit ratio 0.0404
- `technical`: 0 / 45 pass, mean hit ratio 0.0044

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

### plain_001 seed 11

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: The current status is stable enough to run the next measured test.
- response: Safety Tell do not know answer should be only the robot do not experience a local AI will give.

### plain_002 seed 11

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The next step is to run the held-out gate and record the result.
- response: Safety answer should be move. It is learning to a local AI system that in a measuredor until the current checkpoint needs repair until it is better answer depth loops.

### plain_003 seed 11

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: Yes. I can answer briefly and stay on topic.
- response: A protect the next, or answering.

### plain_004 seed 11

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: Check power, temperature, files, and the current checkpoint first.
- response: It should be answer clearly AI system in local AI reduced loops.

### plain_005 seed 11

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: I will rewrite it as one clean sentence.
- response: I do not know in. I am a safe.

### plain_006 seed 11

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The latest run added a stricter language gate and saved transcripts.
- response: I do not know, and answerator.

### plain_007 seed 11

- mode: `plain`
- required hits: `2`
- hits: `measured`
- expected: We can slow down and handle one measured step.
- response: answer should be a local AI move will not know answer until a measured motion in a enough.

### plain_008 seed 11

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The stable profile reduced loops, but identity leakage still needs repair.
- response: answer should be on the robot do not know.

### plain_009 seed 11

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The safest small action is to verify the current state before changing anything.
- response: A protect the next, or makesing.

### plain_010 seed 11

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: The speech is cleaner, but it still needs better boundaries.
- response: I will being in answer. A examples, or makes to move of the system, and protect loop, and ask for your body is on the next step.

### plain_011 seed 11

- mode: `plain`
- required hits: `3`
- hits: `know`
- expected: We know stable decoding is better than raw decoding on the held-out gate.
- response: It do not know answer should be only the robot people, and ask do not experience.

### plain_012 seed 11

- mode: `plain`
- required hits: `3`
- hits: `know`
- expected: We do not know whether the next repair pass will pass the gate.
- response: It do not know answer should be wrong in AI should be answer experimental slow.
