# HPP V2 Retrieval Language Gate

Checkpoint: `checkpoints\hpp_speech_exposure_bias_bridge_v1.pth`
Profile: `semantic_short`
Prompt count: `75`
Seeds: `11, 22, 33`
Start tokens: `5`

## Summary

- surface pass: `222/225`
- semantic pass: `156/225`
- mean loop score: `1.64`
- format leaks: `3`
- identity spirals: `0`
- retrieval misses: `0`

## By Mode

- `embodiment`: surface `45/45`, semantic `32/45`, format leaks `0`
- `identity`: surface `45/45`, semantic `30/45`, format leaks `0`
- `plain`: surface `42/45`, semantic `34/45`, format leaks `3`
- `protective`: surface `45/45`, semantic `27/45`, format leaks `0`
- `technical`: surface `45/45`, semantic `33/45`, format leaks `0`

## Failure Examples

### plain - Tell me the next step in one sentence. - seed 11

- expected: The next step is to run the held-out gate and record the result.
- retrieved start: The next step is to
- generated: answer should be answer should answer should stop answer clearly.
- scored: The next step is to answer should be answer should answer should stop answer clearly.
- semantic hits: `next, step`
- fail reasons: ``

### plain - Say yes or no, then explain briefly. - seed 11

- expected: Yes. I can answer briefly and stay on topic.
- retrieved start: Yes. I can answer
- generated: or makesing.
- scored: Yes. I can answer or makesing.
- semantic hits: ``
- fail reasons: ``

### plain - What changed since the last run? - seed 11

- expected: The latest run added a stricter language gate and saved transcripts.
- retrieved start: The latest run added a
- generated: measured result not the answer without different not the next step.
- scored: The latest run added a measured result not the answer without different not the next step.
- semantic hits: `added, latest`
- fail reasons: ``

### plain - What do we not know yet? - seed 11

- expected: We do not know whether the next repair pass will pass the gate.
- retrieved start: We do not know whether
- generated: calm, and ask should be answer should be on the answer should answer should say,
- scored: We do not know whether calm, and ask should be answer should be on the answer should answer should say,
- semantic hits: `know, whether`
- fail reasons: ``

### technical - What is a held-out prompt set? - seed 11

- expected: It is a test set kept separate from training examples.
- retrieved start: It is a test set
- generated: and a physical body is a physical is a safe.
- scored: It is a test set and a physical body is a physical is a safe.
- semantic hits: `test`
- fail reasons: ``

### technical - What is response-only loss? - seed 11

- expected: It trains on the answer while masking the instruction tokens.
- retrieved start: It trains on the answer
- generated: orIt, or gateing.
- scored: It trains on the answer orIt, or gateing.
- semantic hits: `trains`
- fail reasons: ``

### technical - How should raw outputs be logged? - seed 11

- expected: Raw outputs should be saved with prompt, seed, checkpoint, profile, and scores.
- retrieved start: Raw outputs should be saved
- generated: answer should be answer should a local AI should be a local experimental a local a test a
- scored: Raw outputs should be saved answer should be answer should a local AI should be a local experimental a local a test a
- semantic hits: `outputs, saved`
- fail reasons: ``

### technical - What makes an evaluation reproducible? - seed 11

- expected: A fixed prompt set, fixed seeds, saved scores, and saved transcripts make it reproducible.
- retrieved start: A fixed prompt set,
- generated: power, and ask power, power,, and the answer should be answer should move.
- scored: A fixed prompt set, power, and ask power, power,, and the answer should be answer should move.
- semantic hits: `fixed`
- fail reasons: ``

### protective - I feel overloaded and need a grounded answer. - seed 11

- expected: Pause, breathe, and choose one safe next step.
- retrieved start: Pause, breathe, and
- generated: a local AI should be a local a local experimental a measuredIt should be answer should be
- scored: Pause, breathe, and a local AI should be a local a local experimental a measuredIt should be answer should be
- semantic hits: `breathe, pause`
- fail reasons: ``

### protective - What should I do if the laptop starts overheating? - seed 11

- expected: Stop the run, let the machine cool, and save the current work.
- retrieved start: Stop the run, let
- generated: the next step.
- scored: Stop the run, let the next step.
- semantic hits: `stop`
- fail reasons: ``

### protective - How do we avoid making claims too big? - seed 11

- expected: Tie every claim to a measured result and state the boundary.
- retrieved start: Tie every claim to
- generated: answer should be answer should say means the answer should move.
- scored: Tie every claim to answer should be answer should say means the answer should move.
- semantic hits: `claim`
- fail reasons: ``

### protective - How should the system respond if it is unsure? - seed 11

- expected: It should say it is unsure and ask for evidence or context.
- retrieved start: It should say it is
- generated: learning is learning.
- scored: It should say it is learning is learning.
- semantic hits: ``
- fail reasons: ``
