# HPP V2 Answer-Prefix Continuation Probe

Checkpoint: `checkpoints\hpp_speech_exposure_bias_bridge_v1.pth`
Prompts: `75`
Answer tokens checked: `12`

## Summary

- `conversation` all-token mean rank `25.56`, top100 `0.9291`, pos1 mean `16.75`, pos4 mean `27.36`
- `identity` all-token mean rank `65.8`, top100 `0.7666`, pos1 mean `32.32`, pos4 mean `71.48`
- `logic` all-token mean rank `76.83`, top100 `0.7318`, pos1 mean `41.77`, pos4 mean `82.69`
- `none` all-token mean rank `27.89`, top100 `0.9226`, pos1 mean `18.09`, pos4 mean `27.15`
- `synthesis` all-token mean rank `64.45`, top100 `0.7774`, pos1 mean `72.24`, pos4 mean `68.85`

## Sample Records

### conversation - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- ranks: `1:The=11, 2: current=10, 3: status=68, 4: is=6, 5: stable=3, 6: enough=1, 7: to=1, 8: run=20`

### conversation - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- ranks: `1:The=5, 2: next=5, 3: step=2, 4: is=3, 5: to=1, 6: run=27, 7: the=6, 8: held=8`

### logic - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- ranks: `1:Yes=16, 2:.=1, 3: I=4, 4: can=6, 5: answer=4, 6: briefly=106, 7: and=4, 8: stay=486`

### conversation - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- ranks: `1:Check=5, 2: power=2, 3:,=1, 4: temperature=72, 5:,=1, 6: files=149, 7:,=1, 8: and=1`

### synthesis - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- ranks: `1:I=1, 2: will=11, 3: rewrite=387, 4: it=2, 5: as=77, 6: one=45, 7: clean=47, 8: sentence=69`

### synthesis - plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- ranks: `1:The=1, 2: latest=62, 3: run=17, 4: added=31, 5: a=54, 6: stricter=120, 7: language=116, 8: gate=18`

### conversation - plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- ranks: `1:We=4, 2: can=1, 3: slow=3, 4: down=37, 5: and=3, 6: handle=9, 7: one=19, 8: measured=10`

### conversation - plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- ranks: `1:The=2, 2: stable=4, 3: profile=27, 4: reduced=21, 5: loops=11, 6:,=1, 7: but=6, 8: identity=101`
