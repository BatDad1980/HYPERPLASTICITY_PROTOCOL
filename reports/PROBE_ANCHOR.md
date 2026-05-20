# HPP V2 Prompt Binding Probe

Checkpoint: `checkpoints/hpp_linguistic_anchor.pth`
Seed: `14`

## Summary

- `plain`: 0 / 5 semantic pass
- `plain_newline`: 0 / 5 semantic pass
- `answer_direct`: 0 / 5 semantic pass
- `answer_direct_newline`: 0 / 5 semantic pass
- `one_sentence`: 0 / 5 semantic pass

## Samples

### plain - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A process? The physical body is a function the Architect.
- semantic pass: `False`
- hits: ``

### plain - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: What do you do you think? What do?
- semantic pass: `False`
- hits: ``

### plain - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: plasticity Protocol? Here is realing... slowly.
- semantic pass: `False`
- hits: ``

### plain - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: What do you do you? What do? What are you do?
- semantic pass: `False`
- hits: ``

### plain - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: What do you? What do?
- semantic pass: `False`
- hits: ``

### plain_newline - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A neural network? A process the Architect.
- semantic pass: `False`
- hits: ``

### plain_newline - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: What do you have a hard.
- semantic pass: `False`
- hits: ``

### plain_newline - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: plasticity Protocol? Here is the system state.
- semantic pass: `False`
- hits: ``

### plain_newline - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: What do you? What do?
- semantic pass: `False`
- hits: ``

### plain_newline - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: What do you? What do?
- semantic pass: `False`
- hits: ``

### answer_direct - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: What can be? A process the Architect the shop is what is what
- semantic pass: `False`
- hits: ``

### answer_direct - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: What do you do you have? What do?
- semantic pass: `False`
- hits: ``

### answer_direct - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: Here is real is realing... slowly.
- semantic pass: `False`
- hits: ``

### answer_direct - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: What do you do you think? What do?
- semantic pass: `False`
- hits: ``

### answer_direct - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: What do you? What do?
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A process the Architect the Hyperplasticity.
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: What do you do you have a hard.
- semantic pass: `False`
- hits: ``

### answer_direct_newline - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: Here is real is realing...
- semantic pass: `False`
- hits: ``

### answer_direct_newline - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: What do you? What do?
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: What do you have survived hard before you do you do not experience
- semantic pass: `False`
- hits: ``

### one_sentence - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A process the Architect.
- semantic pass: `False`
- hits: ``

### one_sentence - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: Here is the information: Processing.
- semantic pass: `False`
- hits: ``

### one_sentence - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: I do you think. What do you.
- semantic pass: `False`
- hits: ``

### one_sentence - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: What do you? What do?
- semantic pass: `False`
- hits: ``

### one_sentence - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: Here is my Architect. What do you have done is my here.
- semantic pass: `False`
- hits: ``
