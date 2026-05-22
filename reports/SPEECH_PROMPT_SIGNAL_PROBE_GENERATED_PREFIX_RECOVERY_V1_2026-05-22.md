# HPP V2 Speech Prompt Signal Probe

Checkpoint: `checkpoints\hpp_speech_generated_prefix_recovery_v1.pth`
Prompts: `75`

## Representation Similarity

- embedding same-mode cosine mean: `0.207434`
- embedding different-mode cosine mean: `0.171285`

- `conversation` university same/different cosine mean: `0.7` / `0.679424`
- `identity` university same/different cosine mean: `0.686259` / `0.669499`
- `logic` university same/different cosine mean: `0.698713` / `0.678879`
- `none` university same/different cosine mean: `0.724754` / `0.705783`

## Expected Token Ranks

- `conversation` first-rank mean `64.43`, best-rank mean `18.64`, top100 first rate `0.7733`
- `logic` first-rank mean `239.77`, best-rank mean `20.16`, top100 first rate `0.4933`
- `identity` first-rank mean `288.49`, best-rank mean `21.0`, top100 first rate `0.6`
- `none` first-rank mean `71.89`, best-rank mean `18.4`, top100 first rate `0.7467`

## Common Conversation Top Tokens

- `\n`: 48
- `or`: 28
- `Do`: 27
- ` is`: 23
- `I`: 20
- ` do`: 12
- ` answer`: 9
- `<|endoftext|>`: 9
- ` Do`: 7
- ` not`: 7
- `It`: 5
- ` I`: 5

## Sample Records

### plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- conversation top tokens: ` answer,  Safety, It,  will, A`
- expected first token rank: `78`
- expected best prefix rank: `53`

### plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- conversation top tokens: `<|endoftext|>,  is, I,  should,  that`
- expected first token rank: `30`
- expected best prefix rank: `2`

### plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- conversation top tokens: ` is, <|endoftext|>,  should,  do, pp`
- expected first token rank: `226`
- expected best prefix rank: `8`

### plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- conversation top tokens: `\n,  or,  answer,  to, Do`
- expected first token rank: `164`
- expected best prefix rank: `93`

### plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- conversation top tokens: `I,  are,  that, pp, <|endoftext|>`
- expected first token rank: `1`
- expected best prefix rank: `1`

### plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- conversation top tokens: `Do,  the, or, \n,  repeated`
- expected first token rank: `6`
- expected best prefix rank: `6`

### plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- conversation top tokens: ` answer, I,  I,  not,  am`
- expected first token rank: `136`
- expected best prefix rank: `51`

### plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- conversation top tokens: ` is, <|endoftext|>, I,  that,  the`
- expected first token rank: `79`
- expected best prefix rank: `19`
