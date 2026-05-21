# HPP V2 Answer-Prefix Continuation Probe

Checkpoint: `checkpoints\hpp_speech_prompt_binding_contrastive_v1.pth`
Prompts: `75`
Answer tokens checked: `12`

## Summary

- `conversation` all-token mean rank `34.11`, top100 `0.9047`, pos1 mean `21.52`, pos4 mean `37.98`
- `identity` all-token mean rank `1347.72`, top100 `0.5254`, pos1 mean `945.84`, pos4 mean `1191.42`
- `logic` all-token mean rank `2425.38`, top100 `0.4665`, pos1 mean `2175.72`, pos4 mean `1681.72`
- `none` all-token mean rank `41.28`, top100 `0.8702`, pos1 mean `29.95`, pos4 mean `43.76`
- `synthesis` all-token mean rank `2412.98`, top100 `0.4667`, pos1 mean `3025.25`, pos4 mean `2694.25`

## Sample Records

### conversation - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- ranks: `1:The=11, 2: current=13, 3: status=107, 4: is=8, 5: stable=6, 6: enough=1, 7: to=1, 8: run=19`

### conversation - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- ranks: `1:The=3, 2: next=4, 3: step=3, 4: is=9, 5: to=1, 6: run=35, 7: the=3, 8: held=12`

### logic - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- ranks: `1:Yes=76, 2:.=1, 3: I=5, 4: can=8, 5: answer=72, 6: briefly=7879, 7: and=4, 8: stay=4595`

### conversation - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- ranks: `1:Check=5, 2: power=2, 3:,=1, 4: temperature=13, 5:,=1, 6: files=176, 7:,=1, 8: and=1`

### synthesis - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- ranks: `1:I=4, 2: will=29, 3: rewrite=13390, 4: it=3, 5: as=40, 6: one=106, 7: clean=1407, 8: sentence=1457`

### synthesis - plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- ranks: `1:The=4, 2: latest=4939, 3: run=80, 4: added=4816, 5: a=22, 6: stricter=14153, 7: language=94, 8: gate=365`

### conversation - plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- ranks: `1:We=10, 2: can=1, 3: slow=4, 4: down=28, 5: and=3, 6: handle=25, 7: one=35, 8: measured=12`

### conversation - plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- ranks: `1:The=1, 2: stable=6, 3: profile=39, 4: reduced=50, 5: loops=25, 6:,=2, 7: but=3, 8: identity=140`
