# HPP V2 Exposure-Bias Recovery Probe

Checkpoint: `checkpoints\hpp_speech_prompt_binding_domain_all_v1.pth`
Seed: `14`
Profile: `semantic_short`
Domain: `auto`
Prompts: `75`

## Summary

- `clean_prompt`: semantic `1/75`, format leaks `0`, identity spirals `0`
- `explicit_recovery_instruction`: semantic `0/75`, format leaks `1`, identity spirals `0`
- `first_correct_token`: semantic `0/75`, format leaks `0`, identity spirals `0`
- `generic_bad_prefix`: semantic `0/75`, format leaks `1`, identity spirals `0`
- `plausible_imperfect_prefix`: semantic `0/75`, format leaks `0`, identity spirals `0`

## Samples

### clean_prompt - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: It should answer should a local AI should a safe.
- semantic pass: `False`
- hits: ``

### first_correct_token - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: should be answer should a local AI should a measuredIt should set.
- semantic pass: `False`
- hits: ``

### plausible_imperfect_prefix - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: I am a local AI should move.
- semantic pass: `False`
- hits: ``

### generic_bad_prefix - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: I should move.
- semantic pass: `False`
- hits: ``

### explicit_recovery_instruction - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- response: I should be answer should be only the next step.
- semantic pass: `False`
- hits: `next`

### clean_prompt - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: It should answer should answer clearly.
- semantic pass: `False`
- hits: ``

### first_correct_token - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: should answer should be answer should move.
- semantic pass: `False`
- hits: ``

### plausible_imperfect_prefix - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: I should the question the answer should be answer should the next step.
- semantic pass: `False`
- hits: `next, step`

### generic_bad_prefix - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: I should move.
- semantic pass: `False`
- hits: ``

### explicit_recovery_instruction - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- response: I should be answer should be a local hardware.
- semantic pass: `False`
- hits: ``

### clean_prompt - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: The system, or makesing.
- semantic pass: `False`
- hits: ``

### first_correct_token - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: or makesing.
- semantic pass: `False`
- hits: ``

### plausible_imperfect_prefix - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: The system, or gateing.
- semantic pass: `False`
- hits: ``

### generic_bad_prefix - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: power, or gate, or clean hardware for language, and clear, and safety and safety
- semantic pass: `False`
- hits: ``

### explicit_recovery_instruction - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- response: The action, and clear and safety governor hardwareator.
- semantic pass: `False`
- hits: ``

### clean_prompt - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: It should be answer should be on AI should be wrong.
- semantic pass: `False`
- hits: ``

### first_correct_token - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: should be answer should be on AI should be wrong.
- semantic pass: `False`
- hits: ``

### plausible_imperfect_prefix - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: I should be answer clearly.
- semantic pass: `False`
- hits: ``

### generic_bad_prefix - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: I should be answer clearly.
- semantic pass: `False`
- hits: ``

### explicit_recovery_instruction - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- response: I should be answer should be on the answer should stop motion.
- semantic pass: `False`
- hits: ``
