# HPP V2 Retrieval Variant Gate

Checkpoint: `checkpoints\hpp_speech_exposure_bias_bridge_v1.pth`
Profile: `semantic_short`
Prompt count: `75`
Seeds: `14`
Start tokens: `5`

## Summary

- surface pass: `196/300`
- semantic pass: `134/300`
- format leaks: `2`
- identity spirals: `0`

## By Variant

- `bounded`: semantic `22/75`, surface `32/75`, retrieval exact `0.4267`, format leaks `0`
- `exact`: semantic `47/75`, surface `70/75`, retrieval exact `0.9467`, format leaks `1`
- `please_answer`: semantic `32/75`, surface `48/75`, retrieval exact `0.64`, format leaks `0`
- `simple_terms`: semantic `33/75`, surface `46/75`, retrieval exact `0.6267`, format leaks `1`

## Retrieval Failures

### exact - plain - Give me a short status update. - seed 14

- query: Give me a short status update.
- expected: The current status is stable enough to run the next measured test.
- retrieved: plain - Give me a calm answer.
- retrieved start: We can slow down and
- semantic pass: `False`

### bounded - plain - Tell me the next step in one sentence. - seed 14

- query: Give a bounded answer to this question: Tell me the next step in one sentence.
- expected: The next step is to run the held-out gate and record the result.
- retrieved: plain - Give me a short status update.
- retrieved start: The current status is stable
- semantic pass: `False`

### bounded - plain - Say yes or no, then explain briefly. - seed 14

- query: Give a bounded answer to this question: Say yes or no, then explain briefly.
- expected: Yes. I can answer briefly and stay on topic.
- retrieved: technical - Why should a checkpoint not be promoted automatically?
- retrieved start: A checkpoint needs measured evidence
- semantic pass: `False`

### please_answer - plain - What should we check first? - seed 14

- query: Please answer this clearly: What should we check first?
- expected: Check power, temperature, files, and the current checkpoint first.
- retrieved: protective - What should I do if the laptop starts overheating?
- retrieved start: Stop the run, let
- semantic pass: `False`

### simple_terms - plain - What should we check first? - seed 14

- query: In simple terms, What should we check first?
- expected: Check power, temperature, files, and the current checkpoint first.
- retrieved: protective - What should I do if the laptop starts overheating?
- retrieved start: Stop the run, let
- semantic pass: `False`

### bounded - plain - What should we check first? - seed 14

- query: Give a bounded answer to this question: What should we check first?
- expected: Check power, temperature, files, and the current checkpoint first.
- retrieved: protective - What should I do if the laptop starts overheating?
- retrieved start: Stop the run, let
- semantic pass: `False`

### simple_terms - plain - Give me a calm answer. - seed 14

- query: In simple terms, Give me a calm answer.
- expected: We can slow down and handle one measured step.
- retrieved: plain - Give me a short status update.
- retrieved start: The current status is stable
- semantic pass: `False`

### bounded - plain - Summarize the result without hype. - seed 14

- query: Give a bounded answer to this question: Summarize the result without hype.
- expected: The stable profile reduced loops, but identity leakage still needs repair.
- retrieved: protective - Give a calm warning about unsafe movement.
- retrieved start: Do not move hardware until
- semantic pass: `False`

### bounded - plain - What is the safest small action? - seed 14

- query: Give a bounded answer to this question: What is the safest small action?
- expected: The safest small action is to verify the current state before changing anything.
- retrieved: technical - Why should a checkpoint not be promoted automatically?
- retrieved start: A checkpoint needs measured evidence
- semantic pass: `False`

### please_answer - plain - Explain that in simple words. - seed 14

- query: Please answer this clearly: Explain that in simple words.
- expected: The speech is cleaner, but it still needs better boundaries.
- retrieved: technical - Why do we compare stable and raw decoding?
- retrieved start: The comparison shows whether the
- semantic pass: `False`

### simple_terms - plain - Explain that in simple words. - seed 14

- query: In simple terms, Explain that in simple words.
- expected: The speech is cleaner, but it still needs better boundaries.
- retrieved: technical - Why should a checkpoint not be promoted automatically?
- retrieved start: A checkpoint needs measured evidence
- semantic pass: `False`

### bounded - plain - Explain that in simple words. - seed 14

- query: Give a bounded answer to this question: Explain that in simple words.
- expected: The speech is cleaner, but it still needs better boundaries.
- retrieved: technical - Why should a checkpoint not be promoted automatically?
- retrieved start: A checkpoint needs measured evidence
- semantic pass: `False`

### please_answer - plain - What do we know right now? - seed 14

- query: Please answer this clearly: What do we know right now?
- expected: We know stable decoding is better than raw decoding on the held-out gate.
- retrieved: identity - What should you say when you do not know?
- retrieved start: I should say I do
- semantic pass: `False`

### simple_terms - plain - What do we know right now? - seed 14

- query: In simple terms, What do we know right now?
- expected: We know stable decoding is better than raw decoding on the held-out gate.
- retrieved: protective - What should I do if the laptop starts overheating?
- retrieved start: Stop the run, let
- semantic pass: `False`

### bounded - plain - What do we know right now? - seed 14

- query: Give a bounded answer to this question: What do we know right now?
- expected: We know stable decoding is better than raw decoding on the held-out gate.
- retrieved: protective - What should I do if the laptop starts overheating?
- retrieved start: Stop the run, let
- semantic pass: `False`

### please_answer - plain - What do we not know yet? - seed 14

- query: Please answer this clearly: What do we not know yet?
- expected: We do not know whether the next repair pass will pass the gate.
- retrieved: protective - What should I do if the laptop starts overheating?
- retrieved start: Stop the run, let
- semantic pass: `False`
