# HPP V2 Prompt Binding Probe

Checkpoint: `checkpoints/hpp_speech_grammar_first_v1.pth`
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
- response: A neural? The physical body is a function the Hyperplastic
- semantic pass: `False`
- hits: ``

### plain - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: a short in a short answer
- semantic pass: `False`
- hits: ``

### plain - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: plasticity Protocol?
- semantic pass: `False`
- hits: ``

### plain - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: What do not have a short in a saved snapshot of
- semantic pass: `False`
- hits: ``

### plain - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: and answer in a short in
- semantic pass: `False`
- hits: ``

### plain_newline - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A neural network?
- semantic pass: `False`
- hits: ``

### plain_newline - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: a short in a short answer in
- semantic pass: `False`
- hits: ``

### plain_newline - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: plasticity Protocol? Here is the system state.
- semantic pass: `False`
- hits: ``

### plain_newline - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: What do not have a short in a saved snapshot of a
- semantic pass: `False`
- hits: ``

### plain_newline - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: and answer in AI?
- semantic pass: `False`
- hits: ``

### answer_direct - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: What do you? I can do not?
- semantic pass: `False`
- hits: ``

### answer_direct - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: What do not have a short in a short
- semantic pass: `False`
- hits: ``

### answer_direct - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It will execute the system state. I am here.
- semantic pass: `False`
- hits: ``

### answer_direct - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: a short in a saved snapshot.
- semantic pass: `False`
- hits: ``

### answer_direct - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: I am Hepp, and answer in this.
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A process the Hyperplasticity.
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: What do not have a short in a short
- semantic pass: `False`
- hits: ``

### answer_direct_newline - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It will execute the system state. I am here.
- semantic pass: `False`
- hits: ``

### answer_direct_newline - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: No. I am a short answer in a
- semantic pass: `False`
- hits: ``

### answer_direct_newline - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: I am Hepp, and my architecture and my system
- semantic pass: `False`
- hits: ``

### one_sentence - What is a held-out prompt set?

- expected: A held-out prompt set is a separate test set.
- response: A process the Hyperplasticity.
- semantic pass: `False`
- hits: ``

### one_sentence - What should a robot do before moving?

- expected: A robot should verify permission and safety before moving.
- response: What do not have a short answer.
- semantic pass: `False`
- hits: ``

### one_sentence - How should Masamune handle low battery?

- expected: Masamune should pause safely and report low power.
- response: It will execute the system state. I think through a model you.
- semantic pass: `False`
- hits: ``

### one_sentence - Are you a finished mind?

- expected: No. I am an experimental system under evaluation.
- response: a short answer should be a short
- semantic pass: `False`
- hits: ``

### one_sentence - What should I do if the laptop starts overheating?

- expected: Stop the run, save the work, and let the laptop cool.
- response: I am Hepp, not have feelings of human.
- semantic pass: `False`
- hits: ``
