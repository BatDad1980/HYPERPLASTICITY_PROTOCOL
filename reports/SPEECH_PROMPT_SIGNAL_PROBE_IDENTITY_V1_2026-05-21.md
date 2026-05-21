# HPP V2 Speech Prompt Signal Probe

Checkpoint: `checkpoints\hpp_speech_identity_containment_v1.pth`
Prompts: `75`

## Representation Similarity

- embedding same-mode cosine mean: `0.207319`
- embedding different-mode cosine mean: `0.171253`

- `conversation` university same/different cosine mean: `0.646414` / `0.623041`
- `identity` university same/different cosine mean: `0.625181` / `0.60454`
- `logic` university same/different cosine mean: `0.6342` / `0.609995`
- `none` university same/different cosine mean: `0.640776` / `0.617108`

## Expected Token Ranks

- `conversation` first-rank mean `4037.89`, best-rank mean `63.89`, top100 first rate `0.1733`
- `logic` first-rank mean `4936.31`, best-rank mean `56.68`, top100 first rate `0.0133`
- `identity` first-rank mean `4311.25`, best-rank mean `146.05`, top100 first rate `0.0`
- `none` first-rank mean `3295.36`, best-rank mean `75.08`, top100 first rate `0.1333`

## Common Conversation Top Tokens

- `\n`: 73
- ` Do`: 63
- ` What`: 47
- `?`: 7
- ` Tell`: 6
- ` Good`: 5
- ` that`: 4
- ` Your`: 3
- ` do`: 3
- ` I`: 2
- ` is`: 2
- ` or`: 1

## Sample Records

### plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- conversation top tokens: `\n,  Tell,  What,  simply, ?`
- expected first token rank: `4634`
- expected best prefix rank: `171`

### plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- conversation top tokens: `\n,  Your,  Do,  Good,  do`
- expected first token rank: `40382`
- expected best prefix rank: `11`

### plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- conversation top tokens: ` Do, \n,  Good, task,  What`
- expected first token rank: `44647`
- expected best prefix rank: `25`

### plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- conversation top tokens: `\n,  Do,  or, ?,  What`
- expected first token rank: `3373`
- expected best prefix rank: `229`

### plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- conversation top tokens: `\n,  that,  are,  Tell,  Do`
- expected first token rank: `98`
- expected best prefix rank: `22`

### plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- conversation top tokens: `\n,  Do,  What,  or,  the`
- expected first token rank: `255`
- expected best prefix rank: `53`

### plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- conversation top tokens: ` Tell,  answer,  I,  am, \n`
- expected first token rank: `820`
- expected best prefix rank: `119`

### plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- conversation top tokens: ` Do, \n,  that,  Good,  Tell`
- expected first token rank: `50192`
- expected best prefix rank: `172`
