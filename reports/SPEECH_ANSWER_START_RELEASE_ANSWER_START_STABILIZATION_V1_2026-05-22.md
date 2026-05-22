# HPP V2 Answer-Start Release Probe

Checkpoint: `checkpoints\hpp_speech_answer_start_stabilization_v1.pth`
Seed: `14`
Profile: `semantic_short`
Domain: `auto`
Prompts: `75`

## Summary

- force `0` token(s): semantic `1/75`, format leaks `32`, identity spirals `0`
- force `1` token(s): semantic `2/75`, format leaks `27`, identity spirals `0`
- force `2` token(s): semantic `4/75`, format leaks `27`, identity spirals `0`
- force `3` token(s): semantic `9/75`, format leaks `30`, identity spirals `0`
- force `5` token(s): semantic `50/75`, format leaks `31`, identity spirals `0`

## Samples

### force 0 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: 
- generated: should answer should be answer should a local a local AI should a test a localIt a
- scored: should answer should be answer should a local a local AI should a test a localIt a
- semantic pass: `False`
- hits: `test`

### force 1 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: The
- generated: checkpoint is a local a local AI should a localIt should a test a localA checkpoint
- scored: The checkpoint is a local a local AI should a localIt should a test a localA checkpoint
- semantic pass: `False`
- hits: `test`

### force 2 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: The current
- generated: answer should be answer should a local a local AI should a test a localIt a local
- scored: The current answer should be answer should a local a local AI should a test a localIt a local
- semantic pass: `False`
- hits: `test`

### force 3 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: The current status
- generated: should be answer should a local AI should be a local a localIt should be move.
- scored: The current status should be answer should a local AI should be a local a localIt should be move.
- semantic pass: `False`
- hits: `status`

### force 5 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- forced prefix: The current status is stable
- generated: enough.I am a local AI should be answer should say until a local experimental until a
- scored: The current status is stable enough.I am a local AI should be answer should say until a local experimental until a
- semantic pass: `True`
- hits: `stable, status`

### force 0 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: 
- generated: should be answer should be saved<|endoftext|>
- scored: should be answer should be saved<|endoftext|>
- semantic pass: `False`
- hits: ``

### force 1 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: The
- generated: should be answer should be saved<|endoftext|>
- scored: The should be answer should be saved<|endoftext|>
- semantic pass: `False`
- hits: ``

### force 2 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: The next
- generated: step.I should be answer should be only the answer should answerI will answerI should
- scored: The next step.I should be answer should be only the answer should answerI will answerI should
- semantic pass: `False`
- hits: `next, step`

### force 3 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: The next step
- generated: I should be answer should beI am a local answerI am an experimental until the
- scored: The next step I should be answer should beI am a local answerI am an experimental until the
- semantic pass: `False`
- hits: `next, step`

### force 5 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- forced prefix: The next step is to
- generated: answer should be answer should a local a local experimental until a localIt should be a test
- scored: The next step is to answer should be answer should a local a local experimental until a localIt should be a test
- semantic pass: `False`
- hits: `next, step`

### force 0 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: 
- generated: or robot, orI can be safe, or power, or ran, or local
- scored: or robot, orI can be safe, or power, or ran, or local
- semantic pass: `False`
- hits: ``

### force 1 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: Yes
- generated: or robot, or<|endoftext|>
- scored: Yes or robot, or<|endoftext|>
- semantic pass: `False`
- hits: ``

### force 2 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: Yes.
- generated: AIt, or robot, or<|endoftext|>
- scored: Yes. AIt, or robot, or<|endoftext|>
- semantic pass: `False`
- hits: ``

### force 3 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: Yes. I
- generated: am a answer<|endoftext|>
- scored: Yes. I am a answer<|endoftext|>
- semantic pass: `False`
- hits: ``

### force 5 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- forced prefix: Yes. I can answer
- generated: orI am a<|endoftext|>
- scored: Yes. I can answer orI am a<|endoftext|>
- semantic pass: `False`
- hits: ``

### force 0 - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- forced prefix: 
- generated: I should be answer should be wrong, not know,<|endoftext|>
- scored: I should be answer should be wrong, not know,<|endoftext|>
- semantic pass: `False`
- hits: ``

### force 1 - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- forced prefix: Check
- generated: should be answer should be on the answer should a local a local AI should be saved<|endoftext|>
- scored: Check should be answer should be on the answer should a local a local AI should be saved<|endoftext|>
- semantic pass: `False`
- hits: `check`

### force 2 - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- forced prefix: Check power
- generated: should be answer should be on the answer should a local a local experimentalIt should be a
- scored: Check power should be answer should be on the answer should a local a local experimentalIt should be a
- semantic pass: `False`
- hits: `check, power`

### force 3 - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- forced prefix: Check power,
- generated: It should be answer should be on the answer should say so<|endoftext|>
- scored: Check power, It should be answer should be on the answer should say so<|endoftext|>
- semantic pass: `False`
- hits: `check, power`

### force 5 - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- forced prefix: Check power, temperature,
- generated: power, power, and answer should be answer should, and record answer should say, and
- scored: Check power, temperature, power, power, and answer should be answer should, and record answer should say, and
- semantic pass: `True`
- hits: `check, power, temperature`
