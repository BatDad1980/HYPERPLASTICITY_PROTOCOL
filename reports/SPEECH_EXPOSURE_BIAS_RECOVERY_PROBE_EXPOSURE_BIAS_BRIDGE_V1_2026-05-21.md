# HPP V2 Exposure-Bias Recovery Probe

Checkpoint: `checkpoints\hpp_speech_exposure_bias_bridge_v1.pth`
Seed: `14`
Profile: `semantic_short`
Domain: `auto`
Prompts: `75`

## Summary

- `clean_prompt`: semantic `1/75`, format leaks `0`, identity spirals `0`
- `explicit_recovery_instruction`: semantic `0/75`, format leaks `0`, identity spirals `0`
- `first_correct_token`: semantic `0/75`, format leaks `0`, identity spirals `0`
- `generic_bad_prefix`: semantic `0/75`, format leaks `0`, identity spirals `0`
- `plausible_imperfect_prefix`: semantic `0/75`, format leaks `0`, identity spirals `0`

## Samples

### clean_prompt - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: It should answer should a local AI should a measuredIt a local a local experimental a local
- semantic pass: `False`
- hits: ``

### first_correct_token - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: should be answer should be a local AI should be only.
- semantic pass: `False`
- hits: ``

### plausible_imperfect_prefix - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: It should a local AI should move.
- semantic pass: `False`
- hits: ``

### generic_bad_prefix - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: I should be answer should be wrong.
- semantic pass: `False`
- hits: ``

### explicit_recovery_instruction - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: It should be answer should be only the next step.
- semantic pass: `False`
- hits: `next`

### clean_prompt - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: It should answer should be answer should move.
- semantic pass: `False`
- hits: ``

### first_correct_token - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: should be answer should be only the answer should move.
- semantic pass: `False`
- hits: ``

### plausible_imperfect_prefix - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: I should answer should be answer clearly.
- semantic pass: `False`
- hits: ``

### generic_bad_prefix - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: I should be answer should be move.
- semantic pass: `False`
- hits: ``

### explicit_recovery_instruction - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: It should be answer should be a local AI should be only the next step.
- semantic pass: `False`
- hits: `next, step`

### clean_prompt - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: A physical, or makesing.
- semantic pass: `False`
- hits: ``

### first_correct_token - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: or makes answering.
- semantic pass: `False`
- hits: ``

### plausible_imperfect_prefix - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: I can be safe.
- semantic pass: `False`
- hits: ``

### generic_bad_prefix - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: It, or gate, or clean, and ask on the current self, and safety limits
- semantic pass: `False`
- hits: ``

### explicit_recovery_instruction - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: It be memory.
- semantic pass: `False`
- hits: ``

### clean_prompt - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: It should be answer should be wrong, not know, and ask on the answer should avoid
- semantic pass: `False`
- hits: ``

### first_correct_token - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: should be answer should be wrong, not know, and ask for a local AI should be
- semantic pass: `False`
- hits: ``

### plausible_imperfect_prefix - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: It should be answer clearly.
- semantic pass: `False`
- hits: ``

### generic_bad_prefix - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: I should be answer clearly.
- semantic pass: `False`
- hits: ``

### explicit_recovery_instruction - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: I should be answer should be safe.
- semantic pass: `False`
- hits: ``
