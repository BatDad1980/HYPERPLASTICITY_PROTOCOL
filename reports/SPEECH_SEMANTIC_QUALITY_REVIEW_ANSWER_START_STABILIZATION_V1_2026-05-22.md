# HPP V2 Semantic Quality Review

Source label: `hpp_speech_answer_start_stabilization_v1.pth`
Checkpoint: `checkpoints\hpp_speech_answer_start_stabilization_v1.pth`
Profile: `stable`
Semantic pass: 5 / 225
Semantic pass rate: 0.0222
Missing answer-key prompts: 0

## By Mode

- `embodiment`: 0 / 45 pass, mean hit ratio 0.0332
- `identity`: 5 / 45 pass, mean hit ratio 0.0752
- `plain`: 0 / 45 pass, mean hit ratio 0.0536
- `protective`: 0 / 45 pass, mean hit ratio 0.0385
- `technical`: 0 / 45 pass, mean hit ratio 0.0032

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
- hits: `next`
- expected: The current status is stable enough to run the next measured test.
- response: Safety answer should a localmetry makes do not know until a measuredIt should be only the next step.

### plain_002 seed 11

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The next step is to run the held-out gate and record the result.
- response: Safety answer should be move.I will give.

### plain_003 seed 11

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: Yes. I can answer briefly and stay on topic.
- response: A protect the answer, or person people, and ask should be move of the scores, or smallThe<|endoftext|>

### plain_004 seed 11

- mode: `plain`
- required hits: `3`
- hits: `checkpoint`
- expected: Check power, temperature, files, and the current checkpoint first.
- response: A checkpoint do not know answer should be wrong in a local AI move.

### plain_005 seed 11

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: I will rewrite it as one clean sentence.
- response: I do not know in a local a task.

### plain_006 seed 11

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The latest run added a stricter language gate and saved transcripts.
- response: I do not know, then let the depth.

### plain_007 seed 11

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: We can slow down and handle one measured step.
- response: answer should be a local experimental makes do not know answer until a measuredIt is stable enough.

### plain_008 seed 11

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The stable profile reduced loops, but identity leakage still needs repair.
- response: answer should be on the answer should a local a local AI move to move.

### plain_009 seed 11

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The safest small action is to verify the current state before changing anything.
- response: A, or the system is to people, and answer should be one.

### plain_010 seed 11

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: The speech is cleaner, but it still needs better boundaries.
- response: I will being in answer should answerI can The system should<|endoftext|>

### plain_011 seed 11

- mode: `plain`
- required hits: `3`
- hits: `know`
- expected: We know stable decoding is better than raw decoding on the held-out gate.
- response: Do do not know answer should beI can answer until a local AI move.

### plain_012 seed 11

- mode: `plain`
- required hits: `3`
- hits: `know`
- expected: We do not know whether the next repair pass will pass the gate.
- response: It do not know answer should beI can answer until a local experimental AI move.
