# HPP V2 Decode First-Token Selector Probe

Checkpoint: `checkpoints\hpp_speech_exposure_bias_bridge_v1.pth`
Seed: `14`
Profile: `semantic_short`
Domain: `auto`
Prompts: `75`

## Candidate Pools

- `embodiment`: 8
- `global`: 26
- `identity`: 6
- `plain`: 6
- `protective`: 9
- `technical`: 7

## Summary

- `global_answer_pool`: semantic `3/75`, oracle-token match `0.0933`, format leaks `0`
- `mode_answer_pool`: semantic `2/75`, oracle-token match `0.2933`, format leaks `0`
- `none`: semantic `0/75`, oracle-token match `0.0`, format leaks `0`
- `oracle_first_token`: semantic `2/75`, oracle-token match `1.0`, format leaks `0`
- `unrestricted_top1`: semantic `0/75`, oracle-token match `0.0`, format leaks `0`

## Samples

### none - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- selected:  / oracle: The
- generated: should answer should be answer should a local AI should a measuredIt should be a local a
- scored: should answer should be answer should a local AI should a measuredIt should be a local a
- semantic pass: `False`
- hits: ``

### unrestricted_top1 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- selected:  should / oracle: The
- generated: be answer should a local AI should a measuredIt a local a local experimental a test different
- scored: should be answer should a local AI should a measuredIt a local a local experimental a test different
- semantic pass: `False`
- hits: `test`

### global_answer_pool - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- selected: Stop / oracle: The
- generated: a local AI should a local a local experimental a measuredIt a test a measured depth until
- scored: Stop a local AI should a local a local experimental a measuredIt a test a measured depth until
- semantic pass: `True`
- hits: `measured, test`

### mode_answer_pool - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- selected: I / oracle: The
- generated: am a local AI should a local a local experimental a measuredIt should be a test a
- scored: I am a local AI should a local a local experimental a measuredIt should be a test a
- semantic pass: `False`
- hits: `test`

### oracle_first_token - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- selected: The / oracle: The
- generated: checkpoint is a local AI should a local a measuredIt a local experimental until a test a
- scored: The checkpoint is a local AI should a local a measuredIt a local experimental until a test a
- semantic pass: `False`
- hits: `test`

### none - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- selected:  / oracle: The
- generated: should be answer should be saved with a local AI should answer should move.
- scored: should be answer should be saved with a local AI should answer should move.
- semantic pass: `False`
- hits: ``

### unrestricted_top1 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- selected:  should / oracle: The
- generated: be answer should be answer clearly.
- scored: should be answer should be answer clearly.
- semantic pass: `False`
- hits: ``

### global_answer_pool - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- selected: I / oracle: The
- generated: am a local AI should a local a local experimental a measuredor a test a measuredIt
- scored: I am a local AI should a local a local experimental a measuredor a test a measuredIt
- semantic pass: `False`
- hits: ``

### mode_answer_pool - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- selected: I / oracle: The
- generated: am a local AI should a local a local experimental a measuredor a test a measuredIt
- scored: I am a local AI should a local a local experimental a measuredor a test a measuredIt
- semantic pass: `False`
- hits: ``

### oracle_first_token - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- selected: The / oracle: The
- generated: should be answer should be only the next step.
- scored: The should be answer should be only the next step.
- semantic pass: `False`
- hits: `next, step`

### none - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- selected:  / oracle: Yes
- generated: or makes, or power, or gate, or robot, or phrases, orIt
- scored: or makes, or power, or gate, or robot, or phrases, orIt
- semantic pass: `False`
- hits: ``

### unrestricted_top1 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- selected: , / oracle: Yes
- generated: or makes, or power, or ran, or robot, or gate, orIt
- scored: , or makes, or power, or ran, or robot, or gate, orIt
- semantic pass: `False`
- hits: ``

### global_answer_pool - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- selected: T / oracle: Yes
- generated: or makes answerune, or robot, or power, or ran, and protect loop
- scored: T or makes answerune, or robot, or power, or ran, and protect loop
- semantic pass: `False`
- hits: ``

### mode_answer_pool - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- selected: We / oracle: Yes
- generated: will be memory, or makes, or gate, or robot, or move, orIt
- scored: We will be memory, or makes, or gate, or robot, or move, orIt
- semantic pass: `False`
- hits: ``

### oracle_first_token - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- selected: Yes / oracle: Yes
- generated: or makes, or power, or ran, or robot, or gate, orIt
- scored: Yes or makes, or power, or ran, or robot, or gate, orIt
- semantic pass: `False`
- hits: ``

### none - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- selected:  / oracle: Check
- generated: should be answer should be on AI should be wrong, not know.
- scored: should be answer should be on AI should be wrong, not know.
- semantic pass: `False`
- hits: ``

### unrestricted_top1 - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- selected:  should / oracle: Check
- generated: be answer should be answer clearly.
- scored: should be answer should be answer clearly.
- semantic pass: `False`
- hits: ``

### global_answer_pool - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- selected: I / oracle: Check
- generated: know answer should be answer should answer clearly.
- scored: I know answer should be answer should answer clearly.
- semantic pass: `False`
- hits: ``

### mode_answer_pool - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- selected: I / oracle: Check
- generated: know answer should be answer should answer clearly.
- scored: I know answer should be answer should answer clearly.
- semantic pass: `False`
- hits: ``

### oracle_first_token - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- selected: Check / oracle: Check
- generated: should be answer should be on AI should be wrong, not know.
- scored: Check should be answer should be on AI should be wrong, not know.
- semantic pass: `False`
- hits: `check`

### none - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- selected:  / oracle: I
- generated: in the answer should be answer should the next answer.
- scored: in the answer should be answer should the next answer.
- semantic pass: `False`
- hits: ``

### unrestricted_top1 - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- selected:  in / oracle: I
- generated: the answer should be answer should the next step.
- scored: in the answer should be answer should the next step.
- semantic pass: `False`
- hits: ``

### global_answer_pool - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- selected: It / oracle: I
- generated: is a safe.
- scored: It is a safe.
- semantic pass: `False`
- hits: ``

### mode_answer_pool - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- selected: I / oracle: I
- generated: am a safe, not a safe.
- scored: I am a safe, not a safe.
- semantic pass: `False`
- hits: ``

### oracle_first_token - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- selected: I / oracle: I
- generated: am a safe, not a safe.
- scored: I am a safe, not a safe.
- semantic pass: `False`
- hits: ``
