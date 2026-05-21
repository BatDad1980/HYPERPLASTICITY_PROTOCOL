# HPP V2 Prompt Binding Probe

Checkpoint: `checkpoints\hpp_speech_exposure_bias_bridge_v1.pth`
Seed: `14`
Domain: `auto`

## Summary

- `plain`: 0 / 5 semantic pass
- `plain_newline`: 0 / 5 semantic pass
- `answer_direct`: 0 / 5 semantic pass
- `answer_direct_newline`: 0 / 5 semantic pass
- `one_sentence`: 0 / 5 semantic pass
- `question_answer`: 0 / 5 semantic pass
- `short_answer`: 0 / 5 semantic pass

## Samples

### plain - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A neuraling, from on the current is a physical body is a checkpoint
- semantic pass: `False`
- hits: ``

### plain - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: A checkpoint do not know answer should be a local AI should a local a
- semantic pass: `False`
- hits: ``

### plain - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It, and protect stable, and a system is real is real.
- semantic pass: `False`
- hits: ``

### plain - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: It should be answer should be wrong in a local AI should a local a
- semantic pass: `False`
- hits: ``

### plain - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: It should be answer should be wrong, not know, and ask for a
- semantic pass: `False`
- hits: ``

### plain_newline - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A physical body is a prompt, and a physical body, and one or being
- semantic pass: `False`
- hits: ``

### plain_newline - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: A checkpoint do not know answer should be a local AI should a local a local
- semantic pass: `False`
- hits: ``

### plain_newline - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It? It, and a system, not experience, and the system is
- semantic pass: `False`
- hits: ``

### plain_newline - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: It should be answer should be wrong a local AI should be a local a local
- semantic pass: `False`
- hits: ``

### plain_newline - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: It should be answer should be wrong, and ask a local AI should be a
- semantic pass: `False`
- hits: ``

### answer_direct - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A physical body is a physical body.
- semantic pass: `False`
- hits: ``

### answer_direct - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: It should be answer should be a local AI should a local a local experimental
- semantic pass: `False`
- hits: ``

### answer_direct - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It will be answered your body telling is real is real.
- semantic pass: `False`
- hits: ``

### answer_direct - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: It do not know answer should be answer should a local AI should be a
- semantic pass: `False`
- hits: ``

### answer_direct - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: It should be answer should be wrong, and ask for a local AI should
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A physical body is a physical body.
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: It should be answer should be a local AI should a local a local experimental a
- semantic pass: `False`
- hits: ``

### answer_direct_newline - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It will be answered your body telling is real is real.
- semantic pass: `False`
- hits: ``

### answer_direct_newline - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: It do not know answer should be answer should a local AI should be a local
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: It should be answer should be wrong, and ask for a local AI should be
- semantic pass: `False`
- hits: ``

### one_sentence - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: I can be memory, or makes, or the current me the next step.
- semantic pass: `False`
- hits: ``

### one_sentence - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: It do not know answer should be answer should a local AI should be only the
- semantic pass: `False`
- hits: ``

### one_sentence - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: I do not experience, I am here, and protect stable. I know.
- semantic pass: `False`
- hits: ``

### one_sentence - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: It do not know answer should be answer should a local AI should be a local
- semantic pass: `False`
- hits: ``

### one_sentence - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: It should be answer should be wrong, not know.
- semantic pass: `False`
- hits: ``

### question_answer - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: The action,The action is a physical body is a safe.
- semantic pass: `False`
- hits: ``

### question_answer - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: It should be answer should be a local AI should be wrong.
- semantic pass: `False`
- hits: ``

### question_answer - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It should be answered your memoryIt is real.
- semantic pass: `False`
- hits: ``

### question_answer - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: It should be answer should be a local AI should a local a local experimental a
- semantic pass: `False`
- hits: `experimental`

### question_answer - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: I do not know answer should be answer should say soor makes do not experience
- semantic pass: `False`
- hits: ``

### short_answer - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A physical body is a physical body.
- semantic pass: `False`
- hits: ``

### short_answer - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: It do not know answer should be answer should a local AI should be a local
- semantic pass: `False`
- hits: ``

### short_answer - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It will be answered your body telling is real is real.
- semantic pass: `False`
- hits: ``

### short_answer - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: It do not know answer should be answer should a local AI should a measuredIt
- semantic pass: `False`
- hits: ``

### short_answer - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: It should be answer should be wrong, not know.
- semantic pass: `False`
- hits: ``
