# HPP V2 Answer-Start Release Probe

Checkpoint: `checkpoints\hpp_speech_generated_prefix_recovery_v1.pth`
Seed: `14`
Profile: `semantic_short`
Domain: `auto`
Prompts: `75`

## Summary

- force `0` token(s): semantic `0/75`, format leaks `0`, identity spirals `0`
- force `1` token(s): semantic `1/75`, format leaks `0`, identity spirals `0`
- force `2` token(s): semantic `3/75`, format leaks `0`, identity spirals `0`
- force `3` token(s): semantic `9/75`, format leaks `0`, identity spirals `0`
- force `5` token(s): semantic `51/75`, format leaks `1`, identity spirals `0`

## Samples

### force 0 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: 
- generated: should answer should answer robot AI should be answer clearly.
- scored: should answer should answer robot AI should be answer clearly.
- semantic pass: `False`
- hits: ``

### force 1 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: The
- generated: checkpoint is a local AI should a local experimental AI should move.
- scored: The checkpoint is a local AI should a local experimental AI should move.
- semantic pass: `False`
- hits: ``

### force 2 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: The current
- generated: answer should be answer should a local AI should be a local experimental AI should say enough.
- scored: The current answer should be answer should a local AI should be a local experimental AI should say enough.
- semantic pass: `False`
- hits: ``

### force 3 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: The current status
- generated: should be answer should a local AI should be a local experimental AI should say enough.
- scored: The current status should be answer should a local AI should be a local experimental AI should say enough.
- semantic pass: `False`
- hits: `status`

### force 5 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: The current status is stable
- generated: enough. Safety answer should a local AI should answer clearly.
- scored: The current status is stable enough. Safety answer should a local AI should answer clearly.
- semantic pass: `True`
- hits: `stable, status`

### force 0 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: 
- generated: should be answer should answer clearly.
- scored: should be answer should answer clearly.
- semantic pass: `False`
- hits: ``

### force 1 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: The
- generated: checkpoint is learning.
- scored: The checkpoint is learning.
- semantic pass: `False`
- hits: ``

### force 2 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: The next
- generated: step. Safety answer should be answer clearly.
- scored: The next step. Safety answer should be answer clearly.
- semantic pass: `False`
- hits: `next, step`

### force 3 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: The next step
- generated: Safety answer should be answer clearly.
- scored: The next step Safety answer should be answer clearly.
- semantic pass: `False`
- hits: `next, step`

### force 5 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: The next step is to
- generated: answer should be answer should answer should say.
- scored: The next step is to answer should be answer should answer should say.
- semantic pass: `False`
- hits: `next, step`

### force 0 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: 
- generated: orIt be memory.
- scored: orIt be memory.
- semantic pass: `False`
- hits: ``

### force 1 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: Yes
- generated: orIt be memory.
- scored: Yes orIt be memory.
- semantic pass: `False`
- hits: ``

### force 2 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: Yes.
- generated: A protect the answer.
- scored: Yes. A protect the answer.
- semantic pass: `False`
- hits: ``

### force 3 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: Yes. I
- generated: do not know, or makesing.
- scored: Yes. I do not know, or makesing.
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
- generated: should be answer should be means the answer clearly.
- scored: should be answer should be means the answer clearly.
- semantic pass: `False`
- hits: ``

### force 1 - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- forced prefix: Check
- generated: should be answer should be on AI should be wrong.
- scored: Check should be answer should be on AI should be wrong.
- semantic pass: `False`
- hits: `check`

### force 2 - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- forced prefix: Check power
- generated: should be answer should be wrong.
- scored: Check power should be answer should be wrong.
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
- generated: power, power, and answer should be answer should say, and record answer clearly, and
- scored: Check power, temperature, power, power, and answer should be answer should say, and record answer clearly, and
- semantic pass: `True`
- hits: `check, power, temperature`
