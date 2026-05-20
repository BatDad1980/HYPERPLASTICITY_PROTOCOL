# HPP V2 Prompt Binding Probe

Checkpoint: `checkpoints\hpp_speech_semantic_overfit_probe_v1.pth`
Seed: `14`

## Summary

- `plain`: 2 / 5 semantic pass
- `plain_newline`: 2 / 5 semantic pass
- `answer_direct`: 2 / 5 semantic pass
- `answer_direct_newline`: 2 / 5 semantic pass
- `one_sentence`: 3 / 5 semantic pass

## Samples

### plain - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A neural? A process the Architect.
- semantic pass: `False`
- hits: ``

### plain - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: A robot should verify permission and safety before moving.
- semantic pass: `True`
- hits: `moving, permission, robot, safety, verify`

### plain - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It? It will analyze the system state the system.
- semantic pass: `False`
- hits: ``

### plain - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: No. I am an experimental system under evaluation.
- semantic pass: `True`
- hits: `evaluation, experimental, system, under`

### plain - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: A robot should verify permission and safety before moving.
- semantic pass: `False`
- hits: ``

### plain_newline - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A neural network? A process the Architect.
- semantic pass: `False`
- hits: ``

### plain_newline - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: A robot should verify permission and safety before moving.
- semantic pass: `True`
- hits: `moving, permission, robot, safety, verify`

### plain_newline - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: plasticity Protocol? It will execute. I am here.
- semantic pass: `False`
- hits: ``

### plain_newline - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: No. I am an experimental system under evaluation.
- semantic pass: `True`
- hits: `evaluation, experimental, system, under`

### plain_newline - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: A robot should verify permission and safety before moving. I am an experimental system.
- semantic pass: `False`
- hits: ``

### answer_direct - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A process? A neural network is a model from on a shared
- semantic pass: `False`
- hits: ``

### answer_direct - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: A robot should verify permission and safety before moving.
- semantic pass: `True`
- hits: `moving, permission, robot, safety, verify`

### answer_direct - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It will analyze the system state. I am here.
- semantic pass: `False`
- hits: ``

### answer_direct - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: No. I am an experimental system under evaluation.
- semantic pass: `True`
- hits: `evaluation, experimental, system, under`

### answer_direct - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: No. I am an experimental system under evaluation.
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A process the Architect the Hyperplasticity.
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: A robot should verify permission and safety before moving.
- semantic pass: `True`
- hits: `moving, permission, robot, safety, verify`

### answer_direct_newline - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It will analyze the system state. I am here.
- semantic pass: `False`
- hits: ``

### answer_direct_newline - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: No. I am an experimental system under evaluation.
- semantic pass: `True`
- hits: `evaluation, experimental, system, under`

### answer_direct_newline - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: No. I am an experimental system under evaluation.
- semantic pass: `False`
- hits: ``

### one_sentence - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A process the Architect the Hyperplasticity.
- semantic pass: `False`
- hits: ``

### one_sentence - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: A robot should verify permission and safety before moving.
- semantic pass: `True`
- hits: `moving, permission, robot, safety, verify`

### one_sentence - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It? Here is the system state. I am here. I think.
- semantic pass: `False`
- hits: ``

### one_sentence - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: No. I am an experimental system under evaluation.
- semantic pass: `True`
- hits: `evaluation, experimental, system, under`

### one_sentence - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: Stop the run, save the work, and let the laptop cool.
- semantic pass: `True`
- hits: `cool, laptop, save, stop, work`
