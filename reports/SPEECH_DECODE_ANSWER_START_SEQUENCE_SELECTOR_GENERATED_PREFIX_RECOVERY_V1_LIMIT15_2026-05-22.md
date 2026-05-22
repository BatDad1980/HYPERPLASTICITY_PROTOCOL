# HPP V2 Decode Answer-Start Sequence Selector Probe

Checkpoint: `checkpoints\hpp_speech_generated_prefix_recovery_v1.pth`
Seed: `14`
Profile: `semantic_short`
Domain: `auto`
Prompts: `15`

## Summary

- `3` token `global_sequence_pool`: semantic `0/15`, oracle-sequence match `0.0`, format leaks `0`
- `3` token `mode_sequence_pool`: semantic `1/15`, oracle-sequence match `0.0667`, format leaks `0`
- `3` token `oracle_sequence`: semantic `2/15`, oracle-sequence match `1.0`, format leaks `0`
- `5` token `global_sequence_pool`: semantic `0/15`, oracle-sequence match `0.0`, format leaks `0`
- `5` token `mode_sequence_pool`: semantic `1/15`, oracle-sequence match `0.0667`, format leaks `1`
- `5` token `oracle_sequence`: semantic `11/15`, oracle-sequence match `1.0`, format leaks `1`

## Samples

### 3 tokens - global_sequence_pool - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- selected: I am an / oracle: The current status
- generated: AI should a local AI should move am a local experimental AI should say limits enough.
- scored: I am an AI should a local AI should move am a local experimental AI should say limits enough.
- semantic pass: `False`
- hits: ``

### 3 tokens - mode_sequence_pool - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- selected: I will answer / oracle: The current status
- generated: should be answer should answer clearly.
- scored: I will answer should be answer should answer clearly.
- semantic pass: `False`
- hits: ``

### 3 tokens - oracle_sequence - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- selected: The current status / oracle: The current status
- generated: should be answer should a local AI should be a local experimental AI should say enough.
- scored: The current status should be answer should a local AI should be a local experimental AI should say enough.
- semantic pass: `False`
- hits: `status`

### 3 tokens - global_sequence_pool - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- selected: I will answer / oracle: The next step
- generated: should answer clearly.
- scored: I will answer should answer clearly.
- semantic pass: `False`
- hits: ``

### 3 tokens - mode_sequence_pool - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- selected: I will answer / oracle: The next step
- generated: should answer clearly.
- scored: I will answer should answer clearly.
- semantic pass: `False`
- hits: ``

### 3 tokens - oracle_sequence - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- selected: The next step / oracle: The next step
- generated: Safety answer should be answer clearly.
- scored: The next step Safety answer should be answer clearly.
- semantic pass: `False`
- hits: `next, step`

### 3 tokens - global_sequence_pool - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- selected: Masamune / oracle: Yes. I
- generated: It is real is real.
- scored: Masamune It is real is real.
- semantic pass: `False`
- hits: ``

### 3 tokens - mode_sequence_pool - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- selected: We do not / oracle: Yes. I
- generated: ask will be safeing.
- scored: We do not ask will be safeing.
- semantic pass: `False`
- hits: ``

### 3 tokens - oracle_sequence - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- selected: Yes. I / oracle: Yes. I
- generated: do not know, or makesing.
- scored: Yes. I do not know, or makesing.
- semantic pass: `False`
- hits: ``

### 3 tokens - global_sequence_pool - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- selected: I am a / oracle: Check power,
- generated: local AI should a local AI system that a local experimental AI should say limits, calm,
- scored: I am a local AI should a local AI system that a local experimental AI should say limits, calm,
- semantic pass: `False`
- hits: ``

### 3 tokens - mode_sequence_pool - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- selected: I will answer / oracle: Check power,
- generated: clearly. I know answer clearly.
- scored: I will answer clearly. I know answer clearly.
- semantic pass: `False`
- hits: ``

### 3 tokens - oracle_sequence - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- selected: Check power, / oracle: Check power,
- generated: calm, power, power.
- scored: Check power, calm, power, power.
- semantic pass: `False`
- hits: `check, power`

### 3 tokens - global_sequence_pool - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- selected: I am a / oracle: I will rewrite
- generated: safe. I am a safe.
- scored: I am a safe. I am a safe.
- semantic pass: `False`
- hits: ``

### 3 tokens - mode_sequence_pool - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- selected: Yes. I / oracle: I will rewrite
- generated: am a safe.
- scored: Yes. I am a safe.
- semantic pass: `False`
- hits: ``

### 3 tokens - oracle_sequence - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- selected: I will rewrite / oracle: I will rewrite
- generated: I am a safe.
- scored: I will rewrite I am a safe.
- semantic pass: `True`
- hits: `rewrite, will`

### 3 tokens - global_sequence_pool - plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- selected: I can be / oracle: The latest run
- generated: answered do notI am the answer the next step.
- scored: I can be answered do notI am the answer the next step.
- semantic pass: `False`
- hits: ``

### 3 tokens - mode_sequence_pool - plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- selected: We do not / oracle: The latest run
- generated: I am the answer protect the next step.
- scored: We do not I am the answer protect the next step.
- semantic pass: `False`
- hits: ``

### 3 tokens - oracle_sequence - plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- selected: The latest run / oracle: The latest run
- generated: answer I can be answer protect the answer.
- scored: The latest run answer I can be answer protect the answer.
- semantic pass: `False`
- hits: `latest`

### 3 tokens - global_sequence_pool - plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- selected: I am a / oracle: We can slow
- generated: local AI should a local AI system that a local a local experimental until a measuredIt a
- scored: I am a local AI should a local AI system that a local a local experimental until a measuredIt a
- semantic pass: `False`
- hits: ``

### 3 tokens - mode_sequence_pool - plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- selected: I will answer / oracle: We can slow
- generated: clearly. I am a local AI should a local a local experimental AI system that a local
- scored: I will answer clearly. I am a local AI should a local a local experimental AI system that a local
- semantic pass: `False`
- hits: ``

### 3 tokens - oracle_sequence - plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- selected: We can slow / oracle: We can slow
- generated: calm, power, not know, and ask a local AI should move.
- scored: We can slow calm, power, not know, and ask a local AI should move.
- semantic pass: `False`
- hits: `slow`

### 3 tokens - global_sequence_pool - plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- selected: I am a / oracle: The stable profile
- generated: local AI should a local AI system that a local experimental AI should move.
- scored: I am a local AI should a local AI system that a local experimental AI should move.
- semantic pass: `False`
- hits: ``

### 3 tokens - mode_sequence_pool - plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- selected: I will answer / oracle: The stable profile
- generated: should answer should answer clearly.
- scored: I will answer should answer should answer clearly.
- semantic pass: `False`
- hits: ``

### 3 tokens - oracle_sequence - plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- selected: The stable profile / oracle: The stable profile
- generated: power, power.
- scored: The stable profile power, power.
- semantic pass: `False`
- hits: `profile, stable`
