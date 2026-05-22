# HPP V2 Answer-Prefix Continuation Probe

Checkpoint: `checkpoints\hpp_speech_generated_prefix_recovery_v1.pth`
Prompts: `75`
Answer tokens checked: `12`

## Summary

- `conversation` all-token mean rank `22.74`, top100 `0.9446`, pos1 mean `13.07`, pos4 mean `25.26`
- `identity` all-token mean rank `53.74`, top100 `0.8016`, pos1 mean `24.11`, pos4 mean `60.99`
- `logic` all-token mean rank `63.81`, top100 `0.7747`, pos1 mean `32.94`, pos4 mean `69.84`
- `none` all-token mean rank `24.5`, top100 `0.9381`, pos1 mean `14.28`, pos4 mean `24.27`
- `synthesis` all-token mean rank `52.29`, top100 `0.8169`, pos1 mean `55.32`, pos4 mean `55.56`

## Sample Records

### conversation - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- ranks: `1:The=11, 2: current=13, 3: status=78, 4: is=5, 5: stable=3, 6: enough=1, 7: to=1, 8: run=15`

### conversation - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- ranks: `1:The=5, 2: next=5, 3: step=2, 4: is=4, 5: to=1, 6: run=21, 7: the=4, 8: held=5`

### logic - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- ranks: `1:Yes=16, 2:.=1, 3: I=3, 4: can=4, 5: answer=4, 6: briefly=81, 7: and=4, 8: stay=372`

### conversation - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- ranks: `1:Check=4, 2: power=2, 3:,=1, 4: temperature=102, 5:,=1, 6: files=137, 7:,=1, 8: and=1`

### synthesis - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- ranks: `1:I=1, 2: will=6, 3: rewrite=300, 4: it=2, 5: as=90, 6: one=44, 7: clean=42, 8: sentence=49`

### synthesis - plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- ranks: `1:The=1, 2: latest=47, 3: run=18, 4: added=22, 5: a=58, 6: stricter=78, 7: language=81, 8: gate=11`

### conversation - plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- ranks: `1:We=4, 2: can=1, 3: slow=3, 4: down=24, 5: and=3, 6: handle=8, 7: one=14, 8: measured=11`

### conversation - plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- ranks: `1:The=1, 2: stable=9, 3: profile=18, 4: reduced=14, 5: loops=10, 6:,=1, 7: but=8, 8: identity=79`
