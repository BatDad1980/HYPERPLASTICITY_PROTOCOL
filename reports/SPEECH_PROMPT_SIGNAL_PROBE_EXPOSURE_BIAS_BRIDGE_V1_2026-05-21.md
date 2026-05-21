# HPP V2 Speech Prompt Signal Probe

Checkpoint: `checkpoints\hpp_speech_exposure_bias_bridge_v1.pth`
Prompts: `75`

## Representation Similarity

- embedding same-mode cosine mean: `0.207425`
- embedding different-mode cosine mean: `0.171291`

- `conversation` university same/different cosine mean: `0.714689` / `0.695235`
- `identity` university same/different cosine mean: `0.69183` / `0.675595`
- `logic` university same/different cosine mean: `0.704721` / `0.685465`
- `none` university same/different cosine mean: `0.736363` / `0.718376`

## Expected Token Ranks

- `conversation` first-rank mean `74.64`, best-rank mean `18.72`, top100 first rate `0.76`
- `logic` first-rank mean `408.32`, best-rank mean `22.03`, top100 first rate `0.4667`
- `identity` first-rank mean `483.53`, best-rank mean `26.07`, top100 first rate `0.5467`
- `none` first-rank mean `87.96`, best-rank mean `19.23`, top100 first rate `0.7067`

## Common Conversation Top Tokens

- `\n`: 53
- `or`: 26
- ` is`: 24
- `Do`: 22
- `I`: 18
- ` Do`: 10
- ` do`: 10
- `<|endoftext|>`: 9
- ` answer`: 8
- ` not`: 7
- ` the`: 6
- ` I`: 6

## Sample Records

### plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- conversation top tokens: ` answer,  Safety, It,  will,  should`
- expected first token rank: `93`
- expected best prefix rank: `49`

### plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- conversation top tokens: ` is, <|endoftext|>, I,  should,  that`
- expected first token rank: `30`
- expected best prefix rank: `1`

### plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- conversation top tokens: ` is, <|endoftext|>,  should,  do, \n`
- expected first token rank: `263`
- expected best prefix rank: `9`

### plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- conversation top tokens: `\n,  or,  answer,  to, Do`
- expected first token rank: `169`
- expected best prefix rank: `125`

### plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- conversation top tokens: `I,  are,  that,  is, pp`
- expected first token rank: `1`
- expected best prefix rank: `1`

### plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- conversation top tokens: ` the, \n, Do, or,  repeated`
- expected first token rank: `6`
- expected best prefix rank: `6`

### plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- conversation top tokens: `I,  answer,  I,  not,  am`
- expected first token rank: `172`
- expected best prefix rank: `39`

### plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- conversation top tokens: ` is, <|endoftext|>,  the, I,  that`
- expected first token rank: `82`
- expected best prefix rank: `19`
