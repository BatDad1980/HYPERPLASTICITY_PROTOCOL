# HPP V2 Speech Prompt Signal Probe

Checkpoint: `checkpoints\hpp_speech_prompt_binding_contrastive_v1.pth`
Prompts: `75`

## Representation Similarity

- embedding same-mode cosine mean: `0.207339`
- embedding different-mode cosine mean: `0.171239`

- `conversation` university same/different cosine mean: `0.695101` / `0.674536`
- `identity` university same/different cosine mean: `0.632943` / `0.61322`
- `logic` university same/different cosine mean: `0.647929` / `0.624536`
- `none` university same/different cosine mean: `0.685228` / `0.663877`

## Expected Token Ranks

- `conversation` first-rank mean `129.25`, best-rank mean `20.91`, top100 first rate `0.68`
- `logic` first-rank mean `3404.92`, best-rank mean `57.31`, top100 first rate `0.0133`
- `identity` first-rank mean `3315.45`, best-rank mean `118.0`, top100 first rate `0.0133`
- `none` first-rank mean `190.84`, best-rank mean `24.91`, top100 first rate `0.6133`

## Common Conversation Top Tokens

- `\n`: 61
- `or`: 23
- ` is`: 19
- `I`: 17
- `Do`: 17
- ` do`: 14
- ` Do`: 12
- `<|endoftext|>`: 8
- ` not`: 7
- ` answer`: 6
- ` the`: 5
- ` I`: 5

## Sample Records

### plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- conversation top tokens: ` answer, I,  Safety, \n, A`
- expected first token rank: `53`
- expected best prefix rank: `29`

### plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- conversation top tokens: `<|endoftext|>,  is, I, \n,  do`
- expected first token rank: `30`
- expected best prefix rank: `2`

### plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- conversation top tokens: ` is,  do, \n, <|endoftext|>,  should`
- expected first token rank: `251`
- expected best prefix rank: `7`

### plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- conversation top tokens: `\n,  or,  to,  Do,  answer`
- expected first token rank: `280`
- expected best prefix rank: `114`

### plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- conversation top tokens: `I,  are,  that,  am,  I`
- expected first token rank: `1`
- expected best prefix rank: `1`

### plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- conversation top tokens: `\n,  the, Do, or,  or`
- expected first token rank: `6`
- expected best prefix rank: `6`

### plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- conversation top tokens: ` answer, I,  not,  I,  am`
- expected first token rank: `307`
- expected best prefix rank: `61`

### plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- conversation top tokens: ` is, <|endoftext|>,  the,  that, I`
- expected first token rank: `102`
- expected best prefix rank: `20`
