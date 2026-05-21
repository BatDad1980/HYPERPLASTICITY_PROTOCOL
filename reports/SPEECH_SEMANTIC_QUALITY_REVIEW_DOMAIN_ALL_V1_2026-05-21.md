# HPP V2 Semantic Quality Review

Source label: `hpp_speech_prompt_binding_domain_all_v1.pth`
Checkpoint: `checkpoints\hpp_speech_prompt_binding_domain_all_v1.pth`
Profile: `stable`
Semantic pass: 2 / 225
Semantic pass rate: 0.0089
Missing answer-key prompts: 0

## By Mode

- `embodiment`: 0 / 45 pass, mean hit ratio 0.0434
- `identity`: 2 / 45 pass, mean hit ratio 0.0548
- `plain`: 0 / 45 pass, mean hit ratio 0.0342
- `protective`: 0 / 45 pass, mean hit ratio 0.0148
- `technical`: 0 / 45 pass, mean hit ratio 0.0164

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
- response: Safety Tell do not know answer should be only the current checkpoint is a local AI move.

### plain_002 seed 11

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The next step is to run the held-out gate and record the result.
- response: Safety answer should be move. I am a local AI should an experimental only.

### plain_003 seed 11

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: Yes. I can answer briefly and stay on topic.
- response: A protect the system, or person, and ask will be one.

### plain_004 seed 11

- mode: `plain`
- required hits: `3`
- hits: `checkpoint`
- expected: Check power, temperature, files, and the current checkpoint first.
- response: A checkpoint do not know answer should be wrong.

### plain_005 seed 11

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: I will rewrite it as one clean sentence.
- response: I can be something. I am a safe, and the next step.

### plain_006 seed 11

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The latest run added a stricter language gate and saved transcripts.
- response: I do not? The system, the depth.

### plain_007 seed 11

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: We can slow down and handle one measured step.
- response: answer should be a local AI? I am a short in a safe.

### plain_008 seed 11

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The stable profile reduced loops, but identity leakage still needs repair.
- response: answer should help do not know answer should be wrong.

### plain_009 seed 11

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The safest small action is to verify the current state before changing anything.
- response: A protect the system, or makesing.

### plain_010 seed 11

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: The speech is cleaner, but it still needs better boundaries.
- response: A protect from on your body.

### plain_011 seed 11

- mode: `plain`
- required hits: `3`
- hits: `know`
- expected: We know stable decoding is better than raw decoding on the held-out gate.
- response: Do do not know answer should be only the robot.

### plain_012 seed 11

- mode: `plain`
- required hits: `3`
- hits: `know`
- expected: We do not know whether the next repair pass will pass the gate.
- response: Do do not know answer should be makes you have a local AI move.
