# HPP V2 Decode First-Token Selector Probe

Checkpoint: `checkpoints\hpp_speech_generated_prefix_recovery_v1.pth`
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

- `global_answer_pool`: semantic `1/75`, oracle-token match `0.1067`, format leaks `0`
- `mode_answer_pool`: semantic `1/75`, oracle-token match `0.2667`, format leaks `0`
- `none`: semantic `0/75`, oracle-token match `0.0`, format leaks `0`
- `oracle_first_token`: semantic `1/75`, oracle-token match `1.0`, format leaks `0`
- `unrestricted_top1`: semantic `0/75`, oracle-token match `0.0`, format leaks `0`

## Samples

### none - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- selected:  / oracle: The
- generated: should answer should be answer should a local AI should be a local experimental AI system that a
- scored: should answer should be answer should a local AI should be a local experimental AI system that a
- semantic pass: `False`
- hits: ``

### unrestricted_top1 - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- selected:  should / oracle: The
- generated: be answer should be answer clearly.
- scored: should be answer should be answer clearly.
- semantic pass: `False`
- hits: ``

### global_answer_pool - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- selected: Stop / oracle: The
- generated: a local AI should a local experimental a localIt should a measuredIt should move am a
- scored: Stop a local AI should a local experimental a localIt should a measuredIt should move am a
- semantic pass: `False`
- hits: ``

### mode_answer_pool - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- selected: I / oracle: The
- generated: am a local AI should a local experimental AI should move.
- scored: I am a local AI should a local experimental AI should move.
- semantic pass: `False`
- hits: ``

### oracle_first_token - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- selected: The / oracle: The
- generated: checkpoint is a local AI should a local experimental AI should move.
- scored: The checkpoint is a local AI should a local experimental AI should move.
- semantic pass: `False`
- hits: ``

### none - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- selected:  / oracle: The
- generated: should be answer should answer clearly.
- scored: should be answer should answer clearly.
- semantic pass: `False`
- hits: ``

### unrestricted_top1 - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- selected:  should / oracle: The
- generated: be answer should answer clearly.
- scored: should be answer should answer clearly.
- semantic pass: `False`
- hits: ``

### global_answer_pool - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- selected: I / oracle: The
- generated: am a local AI should move am a measuredIt should answer clearly.
- scored: I am a local AI should move am a measuredIt should answer clearly.
- semantic pass: `False`
- hits: ``

### mode_answer_pool - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- selected: I / oracle: The
- generated: am a local AI should move am a measuredIt should answer clearly.
- scored: I am a local AI should move am a measuredIt should answer clearly.
- semantic pass: `False`
- hits: ``

### oracle_first_token - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- selected: The / oracle: The
- generated: checkpoint is learning.
- scored: The checkpoint is learning.
- semantic pass: `False`
- hits: ``

### none - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- selected:  / oracle: Yes
- generated: orIt be memory.
- scored: orIt be memory.
- semantic pass: `False`
- hits: ``

### unrestricted_top1 - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- selected: , / oracle: Yes
- generated: orIt, or gateing.
- scored: , orIt, or gateing.
- semantic pass: `False`
- hits: ``

### global_answer_pool - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- selected: T / oracle: Yes
- generated: orIt, or gateing.
- scored: T orIt, or gateing.
- semantic pass: `False`
- hits: ``

### mode_answer_pool - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- selected: We / oracle: Yes
- generated: will be memory, or gate, or makes answer phrases in the system should be safe.
- scored: We will be memory, or gate, or makes answer phrases in the system should be safe.
- semantic pass: `False`
- hits: ``

### oracle_first_token - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- selected: Yes / oracle: Yes
- generated: orIt be memory.
- scored: Yes orIt be memory.
- semantic pass: `False`
- hits: ``

### none - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- selected:  / oracle: Check
- generated: should be answer should be means the answer clearly.
- scored: should be answer should be means the answer clearly.
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
- generated: know answer clearly, I know, I am a local AI should be answer clearly.
- scored: I know answer clearly, I know, I am a local AI should be answer clearly.
- semantic pass: `False`
- hits: ``

### mode_answer_pool - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- selected: I / oracle: Check
- generated: know answer clearly, I know, I am a local AI should be answer clearly.
- scored: I know answer clearly, I know, I am a local AI should be answer clearly.
- semantic pass: `False`
- hits: ``

### oracle_first_token - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- selected: Check / oracle: Check
- generated: should be answer should be on AI should be wrong.
- scored: Check should be answer should be on AI should be wrong.
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
- generated: the answer should be answer should the next answer.
- scored: in the answer should be answer should the next answer.
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
- generated: am a safe, notI am a measured out the next answer.
- scored: I am a safe, notI am a measured out the next answer.
- semantic pass: `False`
- hits: ``

### oracle_first_token - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- selected: I / oracle: I
- generated: am a safe, notI am a measured out the next answer.
- scored: I am a safe, notI am a measured out the next answer.
- semantic pass: `False`
- hits: ``
