# HPP V2 Answer-Prefix Continuation Probe

Checkpoint: `checkpoints\hpp_speech_prompt_binding_domain_all_v1.pth`
Prompts: `75`
Answer tokens checked: `12`

## Summary

- `conversation` all-token mean rank `28.16`, top100 `0.9158`, pos1 mean `17.73`, pos4 mean `31.64`
- `identity` all-token mean rank `104.79`, top100 `0.6979`, pos1 mean `72.86`, pos4 mean `116.9`
- `logic` all-token mean rank `126.79`, top100 `0.6564`, pos1 mean `104.53`, pos4 mean `122.34`
- `none` all-token mean rank `30.81`, top100 `0.9107`, pos1 mean `19.35`, pos4 mean `32.31`
- `synthesis` all-token mean rank `112.96`, top100 `0.7556`, pos1 mean `299.75`, pos4 mean `91.0`

## Sample Records

### conversation - plain - Give me a short status update.

- expected: The current status is stable enough to run the next measured test.
- ranks: `1:The=12, 2: current=8, 3: status=80, 4: is=8, 5: stable=5, 6: enough=1, 7: to=1, 8: run=26`

### conversation - plain - Tell me the next step in one sentence.

- expected: The next step is to run the held-out gate and record the result.
- ranks: `1:The=3, 2: next=3, 3: step=3, 4: is=3, 5: to=1, 6: run=29, 7: the=3, 8: held=7`

### logic - plain - Say yes or no, then explain briefly.

- expected: Yes. I can answer briefly and stay on topic.
- ranks: `1:Yes=16, 2:.=1, 3: I=11, 4: can=6, 5: answer=6, 6: briefly=363, 7: and=4, 8: stay=1307`

### conversation - plain - What should we check first?

- expected: Check power, temperature, files, and the current checkpoint first.
- ranks: `1:Check=5, 2: power=2, 3:,=1, 4: temperature=31, 5:,=1, 6: files=145, 7:,=1, 8: and=1`

### synthesis - plain - Rewrite that as a clean sentence.

- expected: I will rewrite it as one clean sentence.
- ranks: `1:I=1, 2: will=15, 3: rewrite=673, 4: it=2, 5: as=73, 6: one=43, 7: clean=79, 8: sentence=118`

### synthesis - plain - What changed since the last run?

- expected: The latest run added a stricter language gate and saved transcripts.
- ranks: `1:The=1, 2: latest=109, 3: run=15, 4: added=66, 5: a=64, 6: stricter=227, 7: language=81, 8: gate=25`

### conversation - plain - Give me a calm answer.

- expected: We can slow down and handle one measured step.
- ranks: `1:We=7, 2: can=2, 3: slow=5, 4: down=40, 5: and=3, 6: handle=12, 7: one=21, 8: measured=8`

### conversation - plain - Summarize the result without hype.

- expected: The stable profile reduced loops, but identity leakage still needs repair.
- ranks: `1:The=2, 2: stable=3, 3: profile=31, 4: reduced=24, 5: loops=16, 6:,=2, 7: but=4, 8: identity=121`
