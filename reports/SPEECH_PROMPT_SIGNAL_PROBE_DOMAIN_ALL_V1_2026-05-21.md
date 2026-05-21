# HPP V2 Speech Prompt Signal Probe

Checkpoint: `checkpoints\hpp_speech_prompt_binding_domain_all_v1.pth`
Prompts: `75`

## Representation Similarity

- embedding same-mode cosine mean: `0.207375`
- embedding different-mode cosine mean: `0.171255`

- `conversation` university same/different cosine mean: `0.72214` / `0.703281`
- `identity` university same/different cosine mean: `0.677595` / `0.660547`
- `logic` university same/different cosine mean: `0.69257` / `0.672475`
- `none` university same/different cosine mean: `0.735378` / `0.717366`

## Expected Token Ranks

- `conversation` first-rank mean `86.68`, best-rank mean `16.65`, top100 first rate `0.76`
- `logic` first-rank mean `1370.48`, best-rank mean `29.88`, top100 first rate `0.24`
- `identity` first-rank mean `1439.44`, best-rank mean `36.63`, top100 first rate `0.3867`
- `none` first-rank mean `108.33`, best-rank mean `18.19`, top100 first rate `0.68`

## Common Conversation Top Tokens

- `\n`: 57
- `or`: 30
- ` is`: 25
- `Do`: 18
- `I`: 16
- `<|endoftext|>`: 9
- ` Do`: 9
- ` answer`: 8
- ` the`: 8
- ` do`: 8
- ` not`: 7
- ` a`: 4

## Sample Records

### plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- conversation top tokens: ` answer,  Safety,  will, It,  should`
- expected first token rank: `71`
- expected best prefix rank: `44`

### plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- conversation top tokens: `<|endoftext|>,  is, I,  should,  the`
- expected first token rank: `29`
- expected best prefix rank: `2`

### plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- conversation top tokens: ` is, <|endoftext|>,  should,  do, \n`
- expected first token rank: `255`
- expected best prefix rank: `10`

### plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- conversation top tokens: `\n,  or,  to,  answer, Do`
- expected first token rank: `182`
- expected best prefix rank: `93`

### plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- conversation top tokens: `I,  are,  that,  is,  am`
- expected first token rank: `1`
- expected best prefix rank: `1`

### plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- conversation top tokens: `\n,  the, or, Do, The`
- expected first token rank: `5`
- expected best prefix rank: `5`

### plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- conversation top tokens: `I,  answer,  not,  am,  I`
- expected first token rank: `226`
- expected best prefix rank: `32`

### plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- conversation top tokens: ` is, <|endoftext|>,  the,  that, I`
- expected first token rank: `75`
- expected best prefix rank: `18`
