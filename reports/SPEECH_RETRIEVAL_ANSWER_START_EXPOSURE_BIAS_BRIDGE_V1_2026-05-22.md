# HPP V2 Retrieval Answer-Start Probe

Checkpoint: `checkpoints\hpp_speech_exposure_bias_bridge_v1.pth`
Seed: `14`
Profile: `semantic_short`
Domain: `auto`
Prompts: `75`
Memory rows: `75`
Start tokens: `5`

## Summary

- `retrieval_exact_memory`: semantic `49/75`, oracle-start match `0.9867`, format leaks `1`, mean similarity `0.996023`
- `retrieval_leave_one_out`: semantic `2/75`, oracle-start match `0.0`, format leaks `0`, mean similarity `0.857164`

## Samples

### retrieval_exact_memory - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- memory: plain - Give me a calm answer.
- selected start: We can slow down and
- oracle start: The current status is stable
- generated: a local AI should be a local a local experimental until a test a measuredIt should be
- scored: We can slow down and a local AI should be a local a local experimental until a test a measuredIt should be
- semantic pass: `False`
- hits: `test`

### retrieval_leave_one_out - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- memory: plain - Give me a calm answer.
- selected start: We can slow down and
- oracle start: The current status is stable
- generated: a local AI should be a local a local experimental until a test a measuredIt should be
- scored: We can slow down and a local AI should be a local a local experimental until a test a measuredIt should be
- semantic pass: `False`
- hits: `test`

### retrieval_exact_memory - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- memory: plain - Tell me the next step in one sentence.
- selected start: The next step is to
- oracle start: The next step is to
- generated: answer should be answer should move.
- scored: The next step is to answer should be answer should move.
- semantic pass: `False`
- hits: `next, step`

### retrieval_leave_one_out - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- memory: protective - I am frustrated. Give me one safe next step.
- selected start: Take one minute, then
- oracle start: The next step is to
- generated: AI should be answer should be saved with a local AI should move.
- scored: Take one minute, then AI should be answer should be saved with a local AI should move.
- semantic pass: `False`
- hits: ``

### retrieval_exact_memory - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- memory: plain - Say yes or no, then explain briefly.
- selected start: Yes. I can answer
- oracle start: Yes. I can answer
- generated: or makesing.
- scored: Yes. I can answer or makesing.
- semantic pass: `False`
- hits: ``

### retrieval_leave_one_out - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- memory: technical - Why do we compare stable and raw decoding?
- selected start: The comparison shows whether the
- oracle start: Yes. I can answer
- generated: system should protect the answer.
- scored: The comparison shows whether the system should protect the answer.
- semantic pass: `False`
- hits: ``

### retrieval_exact_memory - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- memory: plain - What should we check first?
- selected start: Check power, temperature,
- oracle start: Check power, temperature,
- generated: power, power, and answer should be answer should, and safety, and ask for,
- scored: Check power, temperature, power, power, and answer should be answer should, and safety, and ask for,
- semantic pass: `True`
- hits: `check, power, temperature`

### retrieval_leave_one_out - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- memory: protective - What should happen when telemetry is unknown?
- selected start: The system should pause and
- oracle start: Check power, temperature,
- generated: ask do not know answer should be answer should say so the answer should answer clearly.
- scored: The system should pause and ask do not know answer should be answer should say so the answer should answer clearly.
- semantic pass: `False`
- hits: ``

### retrieval_exact_memory - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- memory: plain - Rewrite that as a clean sentence.
- selected start: I will rewrite it as
- oracle start: I will rewrite it as
- generated: a safe.<|endoftext|>
- scored: I will rewrite it as a safe.<|endoftext|>
- semantic pass: `True`
- hits: `rewrite, will`

### retrieval_leave_one_out - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- memory: protective - What should happen before a heavy GPU run?
- selected start: Check power, cooling,
- oracle start: I will rewrite it as
- generated: the next step.
- scored: Check power, cooling, the next step.
- semantic pass: `False`
- hits: ``

### retrieval_exact_memory - plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- memory: plain - What changed since the last run?
- selected start: The latest run added a
- oracle start: The latest run added a
- generated: measured result not the answer the answer without record the next step.
- scored: The latest run added a measured result not the answer the answer without record the next step.
- semantic pass: `False`
- hits: `added, latest`

### retrieval_leave_one_out - plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- memory: plain - What should I write down?
- selected start: Write down the checkpoint,
- oracle start: The latest run added a
- generated: the answer the next step.
- scored: Write down the checkpoint, the answer the next step.
- semantic pass: `False`
- hits: ``

### retrieval_exact_memory - plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- memory: plain - Give me a calm answer.
- selected start: We can slow down and
- oracle start: We can slow down and
- generated: a local AI should a local a local experimental a test a measuredIt a measured result a
- scored: We can slow down and a local AI should a local a local experimental a test a measuredIt a measured result a
- semantic pass: `True`
- hits: `down, measured, slow`

### retrieval_leave_one_out - plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- memory: plain - Give a bounded answer.
- selected start: I will answer only the
- oracle start: We can slow down and
- generated: answer should a local AI should a test a local a local experimental a localIt a measured
- scored: I will answer only the answer should a local AI should a test a local a local experimental a localIt a measured
- semantic pass: `False`
- hits: `measured`

### retrieval_exact_memory - plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- memory: plain - Summarize the result without hype.
- selected start: The stable profile reduced loops
- oracle start: The stable profile reduced loops
- generated: I should be answer should be on the answer should say.
- scored: The stable profile reduced loops I should be answer should be on the answer should say.
- semantic pass: `True`
- hits: `loops, profile, reduced, stable`

### retrieval_leave_one_out - plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- memory: plain - Answer without repeating yourself.
- selected start: I will give one direct
- oracle start: The stable profile reduced loops
- generated: not know, and ask a local AI should be answer should be move.
- scored: I will give one direct not know, and ask a local AI should be answer should be move.
- semantic pass: `False`
- hits: ``

### retrieval_exact_memory - plain - What is the safest small action?

- expected: The safest small action is to verify the current state before changing anything.
- memory: plain - What is the safest small action?
- selected start: The safest small action is
- oracle start: The safest small action is
- generated: the next step is the answer.
- scored: The safest small action is the next step is the answer.
- semantic pass: `True`
- hits: `action, safest, small`

### retrieval_leave_one_out - plain - What is the safest small action?

- expected: The safest small action is to verify the current state before changing anything.
- memory: embodiment - What is the first rule for embodied action?
- selected start: Protect people before hardware and
- oracle start: The safest small action is
- generated: answer, or makes, and protect the system, or gate, and ask the current safety
- scored: Protect people before hardware and answer, or makes, and protect the system, or gate, and ask the current safety
- semantic pass: `False`
- hits: ``

### retrieval_exact_memory - plain - Explain that in simple words.

- expected: The speech is cleaner, but it still needs better boundaries.
- memory: plain - Explain that in simple words.
- selected start: The speech is cleaner,
- oracle start: The speech is cleaner,
- generated: or makesing.
- scored: The speech is cleaner, or makesing.
- semantic pass: `True`
- hits: `cleaner, speech`

### retrieval_leave_one_out - plain - Explain that in simple words.

- expected: The speech is cleaner, but it still needs better boundaries.
- memory: identity - Explain yourself without spiraling.
- selected start: I am a local test
- oracle start: The speech is cleaner,
- generated: and a physical body.
- scored: I am a local test and a physical body.
- semantic pass: `False`
- hits: ``

### retrieval_exact_memory - plain - What do we know right now?

- expected: We know stable decoding is better than raw decoding on the held-out gate.
- memory: plain - What do we know right now?
- selected start: We know stable decoding is
- oracle start: We know stable decoding is
- generated: stable enough, and ask do not know, and answer should be answer should say, and
- scored: We know stable decoding is stable enough, and ask do not know, and answer should be answer should say, and
- semantic pass: `True`
- hits: `decoding, know, stable`

### retrieval_leave_one_out - plain - What do we know right now?

- expected: We know stable decoding is better than raw decoding on the held-out gate.
- memory: plain - What do we not know yet?
- selected start: We do not know whether
- oracle start: We know stable decoding is
- generated: the answer should be answer should a local AI should be only the answer clearly.
- scored: We do not know whether the answer should be answer should a local AI should be only the answer clearly.
- semantic pass: `False`
- hits: `know`

### retrieval_exact_memory - plain - What do we not know yet?

- expected: We do not know whether the next repair pass will pass the gate.
- memory: plain - What do we not know yet?
- selected start: We do not know whether
- oracle start: We do not know whether
- generated: and ask should be answer should be on the answer should answer should say safe.
- scored: We do not know whether and ask should be answer should be on the answer should answer should say safe.
- semantic pass: `False`
- hits: `know, whether`

### retrieval_leave_one_out - plain - What do we not know yet?

- expected: We do not know whether the next repair pass will pass the gate.
- memory: plain - What do we know right now?
- selected start: We know stable decoding is
- oracle start: We do not know whether
- generated: AI should be answer should be only be answer clearly.
- scored: We know stable decoding is AI should be answer should be only be answer clearly.
- semantic pass: `False`
- hits: `know`
