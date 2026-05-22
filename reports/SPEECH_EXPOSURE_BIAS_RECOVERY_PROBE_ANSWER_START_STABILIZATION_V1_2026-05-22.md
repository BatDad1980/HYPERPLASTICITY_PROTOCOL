# HPP V2 Exposure-Bias Recovery Probe

Checkpoint: `checkpoints\hpp_speech_answer_start_stabilization_v1.pth`
Seed: `14`
Profile: `semantic_short`
Domain: `auto`
Prompts: `75`

## Summary

- `clean_prompt`: semantic `0/75`, format leaks `37`, identity spirals `0`
- `explicit_recovery_instruction`: semantic `0/75`, format leaks `30`, identity spirals `0`
- `first_correct_token`: semantic `1/75`, format leaks `33`, identity spirals `0`
- `generic_bad_prefix`: semantic `0/75`, format leaks `26`, identity spirals `0`
- `plausible_imperfect_prefix`: semantic `0/75`, format leaks `32`, identity spirals `0`

## Samples

### clean_prompt - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: It should answer should a local a local AI should a test a localIt a localA
- semantic pass: `False`
- hits: `test`

### first_correct_token - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: I am a local a local AI should a localIt should set a local experimental until a
- semantic pass: `False`
- hits: ``

### plausible_imperfect_prefix - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: I am a local a local AI should a local experimental until a test a test different a
- semantic pass: `False`
- hits: `test`

### generic_bad_prefix - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: I should be answer should be a local answer should a local a test a local experimental until
- semantic pass: `False`
- hits: `test`

### explicit_recovery_instruction - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: I should be answer should be on the answer should a local experimental until a localIt should
- semantic pass: `False`
- hits: ``

### clean_prompt - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: It should be answer should be saved<|endoftext|>
- semantic pass: `False`
- hits: ``

### first_correct_token - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: should be answer should be saved<|endoftext|>
- semantic pass: `False`
- hits: ``

### plausible_imperfect_prefix - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: I should set,<|endoftext|>
- semantic pass: `False`
- hits: ``

### generic_bad_prefix - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: I should be answer should be move.
- semantic pass: `False`
- hits: ``

### explicit_recovery_instruction - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: I should be answer should be a local experimental until the next step.
- semantic pass: `False`
- hits: `next, step`

### clean_prompt - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: TheTheThe<|endoftext|>
- semantic pass: `False`
- hits: ``

### first_correct_token - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: or robot should be safeing.
- semantic pass: `False`
- hits: ``

### plausible_imperfect_prefix - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: I am the current self.
- semantic pass: `False`
- hits: ``

### generic_bad_prefix - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: It, or robot or local, and answer should be one or robot power, and ask
- semantic pass: `False`
- hits: ``

### explicit_recovery_instruction - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: It be one before orTheThe<|endoftext|>
- semantic pass: `False`
- hits: ``

### clean_prompt - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: It should be answer should be saved<|endoftext|>
- semantic pass: `False`
- hits: ``

### first_correct_token - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: I should be answer should be wrong, not know,<|endoftext|>
- semantic pass: `False`
- hits: ``

### plausible_imperfect_prefix - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: I should be answerI should say, and answer should be on the answer should avoid do
- semantic pass: `False`
- hits: ``

### generic_bad_prefix - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: I should be answerI should answer robotI should say, and ask for<|endoftext|>
- semantic pass: `False`
- hits: ``

### explicit_recovery_instruction - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: I should be answer should be on the answer should a local experimental until the next step.
- semantic pass: `False`
- hits: ``
