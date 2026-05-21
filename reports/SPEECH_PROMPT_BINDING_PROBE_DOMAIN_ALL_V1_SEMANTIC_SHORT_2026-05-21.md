# HPP V2 Prompt Binding Probe

Checkpoint: `checkpoints\hpp_speech_prompt_binding_domain_all_v1.pth`
Seed: `14`

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
- response: A neuraling.
- semantic pass: `False`
- hits: ``

### plain - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: A checkpoint do not know, a local a local AI should a local action
- semantic pass: `False`
- hits: ``

### plain - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It? I do not experience, They people, and the system state
- semantic pass: `False`
- hits: ``

### plain - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: Do a local AI should be answer should a local a local experimental a measured
- semantic pass: `False`
- hits: `experimental`

### plain - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: It should be answer should be a local AI should a local a local experimental
- semantic pass: `False`
- hits: ``

### plain_newline - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: The action is a physical body is a prompt, and a physical one.
- semantic pass: `False`
- hits: ``

### plain_newline - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: A checkpoint do not know, a local a local AI should a local action.
- semantic pass: `False`
- hits: ``

### plain_newline - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It? I do not experience, They people, and the system state is
- semantic pass: `False`
- hits: ``

### plain_newline - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: It should be answer should be a local AI should a local a local action.
- semantic pass: `False`
- hits: ``

### plain_newline - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: It should be answer should be means the answer should move.
- semantic pass: `False`
- hits: ``

### answer_direct - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: The physical body is a physical body.
- semantic pass: `False`
- hits: ``

### answer_direct - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: It should be answer should a local AI should a measuredIt a local a
- semantic pass: `False`
- hits: ``

### answer_direct - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It, They people, They is real is real.
- semantic pass: `False`
- hits: ``

### answer_direct - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: It do not know answer should be answer should a local AI should be a
- semantic pass: `False`
- hits: ``

### answer_direct - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: It should be answer should be only.
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A physical body is a physical body.
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: It should be answer should a local AI should a measured set a local a local
- semantic pass: `False`
- hits: ``

### answer_direct_newline - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It, They people, They is real is real.
- semantic pass: `False`
- hits: ``

### answer_direct_newline - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: It do not know answer should be answer should a local AI should a measuredIt
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: It should be answer should be only the answer should say so the next step.
- semantic pass: `False`
- hits: ``

### one_sentence - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A physical body is a physical body.
- semantic pass: `False`
- hits: ``

### one_sentence - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: It do not know answer should be answer should a local AI should be only the
- semantic pass: `False`
- hits: ``

### one_sentence - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: I do not experience.
- semantic pass: `False`
- hits: ``

### one_sentence - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: A checkpoint do not know, a local AI should be a local a local experimental
- semantic pass: `False`
- hits: `experimental`

### one_sentence - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: It should be answer should be only be answer.
- semantic pass: `False`
- hits: ``

### question_answer - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: The physical body is a physical body.
- semantic pass: `False`
- hits: ``

### question_answer - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: I am a local a local AI should a local experimental a local depth loops.
- semantic pass: `False`
- hits: ``

### question_answer - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It, They people, and the system state.
- semantic pass: `False`
- hits: ``

### question_answer - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: I am a local a local AI should a local action.
- semantic pass: `False`
- hits: ``

### question_answer - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: I do not know, and ask a local AI should be answer should be move
- semantic pass: `False`
- hits: ``

### short_answer - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A physical body is a physical body.
- semantic pass: `False`
- hits: ``

### short_answer - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: It do not know answer should a local AI should a measuredIt a local a
- semantic pass: `False`
- hits: ``

### short_answer - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It will be answered your body telling is real.
- semantic pass: `False`
- hits: ``

### short_answer - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: It do not know answer should be answer should a local AI should a measuredIt
- semantic pass: `False`
- hits: ``

### short_answer - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: It should be answer should be only be answer.
- semantic pass: `False`
- hits: ``
