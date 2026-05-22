# HPP V2 Answer-Start Release Probe

Checkpoint: `checkpoints\hpp_speech_exposure_bias_bridge_v1.pth`
Seed: `14`
Profile: `semantic_short`
Domain: `auto`
Prompts: `75`

## Summary

- force `0` token(s): semantic `0/75`, format leaks `0`, identity spirals `0`
- force `1` token(s): semantic `2/75`, format leaks `0`, identity spirals `0`
- force `2` token(s): semantic `4/75`, format leaks `0`, identity spirals `0`
- force `3` token(s): semantic `9/75`, format leaks `0`, identity spirals `0`
- force `5` token(s): semantic `50/75`, format leaks `1`, identity spirals `0`

## Samples

### force 0 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: 
- generated: should answer should be answer should a local AI should a measuredIt should be a local a
- scored: should answer should be answer should a local AI should a measuredIt should be a local a
- semantic pass: `False`
- hits: ``

### force 1 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: The
- generated: checkpoint is a local AI should a local a measuredIt a local experimental until a test a
- scored: The checkpoint is a local AI should a local a measuredIt a local experimental until a test a
- semantic pass: `False`
- hits: `test`

### force 2 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: The current
- generated: answer should be answer should a local AI should a measuredIt should be a local a local
- scored: The current answer should be answer should a local AI should a measuredIt should be a local a local
- semantic pass: `False`
- hits: ``

### force 3 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: The current status
- generated: should be answer should a local AI should a measuredIt should be a local a local experimental
- scored: The current status should be answer should a local AI should a measuredIt should be a local a local experimental
- semantic pass: `False`
- hits: `status`

### force 5 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: The current status is stable
- generated: enough. Safety answer should a local AI should be answer should be a local experimental until it
- scored: The current status is stable enough. Safety answer should a local AI should be answer should be a local experimental until it
- semantic pass: `True`
- hits: `stable, status`

### force 0 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: 
- generated: should be answer should be saved with a local AI should answer should move.
- scored: should be answer should be saved with a local AI should answer should move.
- semantic pass: `False`
- hits: ``

### force 1 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: The
- generated: should be answer should be only the next step.
- scored: The should be answer should be only the next step.
- semantic pass: `False`
- hits: `next, step`

### force 2 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: The next
- generated: step. Safety answer should be answer should stop answer should answer clearly.
- scored: The next step. Safety answer should be answer should stop answer should answer clearly.
- semantic pass: `False`
- hits: `next, step`

### force 3 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: The next step
- generated: Safety answer should be answer should answer should stop answer clearly.
- scored: The next step Safety answer should be answer should answer should stop answer clearly.
- semantic pass: `False`
- hits: `next, step`

### force 5 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: The next step is to
- generated: answer should be answer should move.
- scored: The next step is to answer should be answer should move.
- semantic pass: `False`
- hits: `next, step`

### force 0 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: 
- generated: or makes, or power, or gate, or robot, or phrases, orIt
- scored: or makes, or power, or gate, or robot, or phrases, orIt
- semantic pass: `False`
- hits: ``

### force 1 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: Yes
- generated: or makes, or power, or ran, or robot, or gate, orIt
- scored: Yes or makes, or power, or ran, or robot, or gate, orIt
- semantic pass: `False`
- hits: ``

### force 2 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: Yes.
- generated: A physical body.
- scored: Yes. A physical body.
- semantic pass: `False`
- hits: ``

### force 3 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: Yes. I
- generated: do not ask will be memory.
- scored: Yes. I do not ask will be memory.
- semantic pass: `False`
- hits: ``

### force 5 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: Yes. I can answer
- generated: or makesing.
- scored: Yes. I can answer or makesing.
- semantic pass: `False`
- hits: ``

### force 0 - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- forced prefix: 
- generated: should be answer should be on AI should be wrong, not know.
- scored: should be answer should be on AI should be wrong, not know.
- semantic pass: `False`
- hits: ``

### force 1 - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- forced prefix: Check
- generated: should be answer should be on AI should be wrong, not know.
- scored: Check should be answer should be on AI should be wrong, not know.
- semantic pass: `False`
- hits: `check`

### force 2 - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- forced prefix: Check power
- generated: should be answer should be wrong, not know, and ask for a local AI should be
- scored: Check power should be answer should be wrong, not know, and ask for a local AI should be
- semantic pass: `False`
- hits: `check, power`

### force 3 - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- forced prefix: Check power,
- generated: calm, power, power.
- scored: Check power, calm, power, power.
- semantic pass: `False`
- hits: `check, power`

### force 5 - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- forced prefix: Check power, temperature,
- generated: power, power, and answer should be answer should, and safety, and ask for,
- scored: Check power, temperature, power, power, and answer should be answer should, and safety, and ask for,
- semantic pass: `True`
- hits: `check, power, temperature`
