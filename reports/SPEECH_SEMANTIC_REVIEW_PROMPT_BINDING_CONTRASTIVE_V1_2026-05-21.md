# HPP V2 Semantic Quality Review

Source label: `hpp_speech_prompt_binding_contrastive_v1`
Checkpoint: `checkpoints\hpp_speech_prompt_binding_contrastive_v1.pth`
Profile: `stable`
Semantic pass: 3 / 225
Semantic pass rate: 0.0133
Missing answer-key prompts: 0

## By Mode

- `embodiment`: 0 / 45 pass, mean hit ratio 0.0183
- `identity`: 3 / 45 pass, mean hit ratio 0.0954
- `plain`: 0 / 45 pass, mean hit ratio 0.0628
- `protective`: 0 / 45 pass, mean hit ratio 0.0185
- `technical`: 0 / 45 pass, mean hit ratio 0.0254

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
- hits: `measured`
- expected: The current status is stable enough to run the next measured test.
- response: a local AI should not know. It should be answer in a measured output am an experimental loops and ask for a safe out until.

### plain_002 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The next step is to run the held-out gate and record the result.
- response: The robot should be answer should be makes answer O.

### plain_003 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: Yes. I can answer briefly and stay on topic.
- response: body should be answer. I am a local AI should move to a measured result, power, not know.

### plain_004 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: Check power, temperature, files, and the current checkpoint first.
- response: Do to answer should be wrong in a local AIator not experience.

### plain_005 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: I will rewrite it as one clean sentence.
- response: I am a enough. I am an AI should be a local AI systems stable enough.

### plain_006 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The latest run added a stricter language gate and saved transcripts.
- response: Do do not know answer should be makes, or robot people, and ask power.

### plain_007 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: We can slow down and handle one measured step.
- response: a local AI should wrong in AI will answer A checkpoint is a saved different not know.

### plain_008 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The stable profile reduced loops, but identity leakage still needs repair.
- response: I am a local AI should answer should a safe.

### plain_009 seed 14

- mode: `plain`
- required hits: `3`
- hits: ``
- expected: The safest small action is to verify the current state before changing anything.
- response: Do do not know answer should be makes, or robot people, and ask answer in the question.

### plain_010 seed 14

- mode: `plain`
- required hits: `2`
- hits: ``
- expected: The speech is cleaner, but it still needs better boundaries.
- response: I am a local AI should be wrong in a test a saved different from move.

### plain_011 seed 14

- mode: `plain`
- required hits: `3`
- hits: `know`
- expected: We know stable decoding is better than raw decoding on the held-out gate.
- response: Do do not know. I am a local AI should a measured outputIt a local action, from the question the current answer depth loops of memory makes it until it examples in needs repair until a safe out loop depth before pass.

### plain_012 seed 14

- mode: `plain`
- required hits: `3`
- hits: `know`
- expected: We do not know whether the next repair pass will pass the gate.
- response: Do do not know answer in AI should be wrong, from the person-14.
