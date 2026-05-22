# HPP V2 Speech Prompt Signal Probe

Checkpoint: `checkpoints\hpp_speech_answer_start_stabilization_v1.pth`
Prompts: `75`

## Representation Similarity

- embedding same-mode cosine mean: `0.207427`
- embedding different-mode cosine mean: `0.171291`

- `conversation` university same/different cosine mean: `0.728187` / `0.709731`
- `identity` university same/different cosine mean: `0.709032` / `0.693579`
- `logic` university same/different cosine mean: `0.723599` / `0.705648`
- `none` university same/different cosine mean: `0.751377` / `0.734368`

## Expected Token Ranks

- `conversation` first-rank mean `49.8`, best-rank mean `16.04`, top100 first rate `0.7867`
- `logic` first-rank mean `188.32`, best-rank mean `17.85`, top100 first rate `0.56`
- `identity` first-rank mean `233.29`, best-rank mean `18.84`, top100 first rate `0.6133`
- `none` first-rank mean `56.23`, best-rank mean `16.49`, top100 first rate `0.7867`

## Common Conversation Top Tokens

- `\n`: 49
- `I`: 34
- `Do`: 32
- ` is`: 20
- `It`: 15
- `<|endoftext|>`: 15
- `or`: 12
- `The`: 11
- ` answer`: 5
- ` I`: 5
- ` the`: 4
- ` Do`: 4

## Sample Records

### plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- conversation top tokens: ` Safety,  answer, It,  will,  should`
- expected first token rank: `35`
- expected best prefix rank: `35`

### plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- conversation top tokens: `<|endoftext|>,  is, I,  should,  the`
- expected first token rank: `14`
- expected best prefix rank: `2`

### plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- conversation top tokens: ` is, <|endoftext|>,  should, pp, I`
- expected first token rank: `155`
- expected best prefix rank: `14`

### plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- conversation top tokens: `\n, Do,  answer,  or, I`
- expected first token rank: `102`
- expected best prefix rank: `102`

### plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- conversation top tokens: `I, <|endoftext|>, pp,  are,  is`
- expected first token rank: `1`
- expected best prefix rank: `1`

### plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- conversation top tokens: `Do,  the, \n, The, <|endoftext|>`
- expected first token rank: `4`
- expected best prefix rank: `4`

### plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- conversation top tokens: `I,  answer,  I,  not,  am`
- expected first token rank: `134`
- expected best prefix rank: `41`

### plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- conversation top tokens: `<|endoftext|>,  is, I,  the,  that`
- expected first token rank: `24`
- expected best prefix rank: `13`
