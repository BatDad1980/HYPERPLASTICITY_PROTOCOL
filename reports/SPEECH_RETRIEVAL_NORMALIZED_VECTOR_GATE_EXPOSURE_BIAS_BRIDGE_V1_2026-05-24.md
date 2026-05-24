# HPP V2 Normalized Vector Retrieval Gate Report

Checkpoint: `checkpoints/hpp_speech_exposure_bias_bridge_v1.pth`
Profile: `semantic_short`
Prompt count: `75`
Seeds: `14`
Start tokens: `5`

## Overall Retrieval Strategy Comparison

This table compares the exact-match retrieval rates of the three routing strategies across all 375 evaluations (75 prompts x 5 variants):

| Strategy | Exact-Match Rate | Description |
| :--- | :---: | :--- |
| **Raw Vector Similarity** | `0.5867` | Matches raw query prompt against raw memory in embedding space |
| **Normalized Key Match** | `0.8` | Matches exact normalized keys (fails on paraphrases) |
| **Normalized Vector Similarity** | `0.8667` | Matches normalized query against normalized memory in embedding space |
| **Hybrid Retrieval (Key + Norm Vector)** | `0.8667` | Lookup first, falls back to normalized vector similarity |

## Performance Summary (Hybrid Strategy)

- **Overall Surface Pass**: `319/375 (85.07%)`
- **Overall Semantic Pass**: `222/375 (59.20%)`
- **Format Leaks**: `6`

## Detailed Breakdown by Variant

| Variant | Count | Raw Vector Match | Normalized Key Match | Normalized Vector Match | Hybrid Match | Semantic Pass | Surface Pass |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `bounded` | 75 | 0.4267 | 1.0000 | 1.0000 | 1.0000 | 0.6800 | 0.9733 |
| `exact` | 75 | 0.9733 | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 0.9867 |
| `paraphrase` | 75 | 0.2667 | 0.0000 | 0.3333 | 0.3333 | 0.2533 | 0.3200 |
| `please_answer` | 75 | 0.6400 | 1.0000 | 1.0000 | 1.0000 | 0.6800 | 0.9867 |
| `simple_terms` | 75 | 0.6267 | 1.0000 | 1.0000 | 1.0000 | 0.6800 | 0.9867 |

## Paraphrase Retrieval Failure Analysis

Found 50 routing failures under paraphrase queries:
### Paraphrase Mismatch: Give me a short status update.
- query: *"Can you provide a quick status report?"*
- expected: "The current status is stable enough to run the next measured test."
- retrieved by Raw Vector: "What should you say when you do not know?"
- retrieved by Normalized Vector: "Are you a finished mind?"
- hybrid match: `False`

### Paraphrase Mismatch: Tell me the next step in one sentence.
- query: *"What is the next step? Answer in one sentence."*
- expected: "The next step is to run the held-out gate and record the result."
- retrieved by Raw Vector: "What is the purpose of a seed in evaluation?"
- retrieved by Normalized Vector: "What is the purpose of a seed in evaluation?"
- hybrid match: `False`

### Paraphrase Mismatch: Say yes or no, then explain briefly.
- query: *"Give a yes/no answer followed by a brief explanation."*
- expected: "Yes. I can answer briefly and stay on topic."
- retrieved by Raw Vector: "Give a short answer for an urgent moment."
- retrieved by Normalized Vector: "Give a short answer for an urgent moment."
- hybrid match: `False`

### Paraphrase Mismatch: What should we check first?
- query: *"What is the first thing we should check?"*
- expected: "Check power, temperature, files, and the current checkpoint first."
- retrieved by Raw Vector: "What is the safest small action?"
- retrieved by Normalized Vector: "What is the safest small action?"
- hybrid match: `False`

### Paraphrase Mismatch: Give me a calm answer.
- query: *"Provide a calm response."*
- expected: "We can slow down and handle one measured step."
- retrieved by Raw Vector: "Give a calm warning about unsafe movement."
- retrieved by Normalized Vector: "Give a calm warning about unsafe movement."
- hybrid match: `False`

### Paraphrase Mismatch: What is the safest small action?
- query: *"What safest tiny action can we take?"*
- expected: "The safest small action is to verify the current state before changing anything."
- retrieved by Raw Vector: "What do we not know yet?"
- retrieved by Normalized Vector: "How should the robot respond to unknown telemetry?"
- hybrid match: `False`

### Paraphrase Mismatch: Explain that in simple words.
- query: *"Can you explain that using simpler language?"*
- expected: "The speech is cleaner, but it still needs better boundaries."
- retrieved by Raw Vector: "What is the safest small action?"
- retrieved by Normalized Vector: "Say yes or no, then explain briefly."
- hybrid match: `False`

### Paraphrase Mismatch: What do we know right now?
- query: *"What is our current knowledge?"*
- expected: "We know stable decoding is better than raw decoding on the held-out gate."
- retrieved by Raw Vector: "What is a controlled intensity answer?"
- retrieved by Normalized Vector: "What is a controlled intensity answer?"
- hybrid match: `False`

### Paraphrase Mismatch: What do we not know yet?
- query: *"What remains unknown to us?"*
- expected: "We do not know whether the next repair pass will pass the gate."
- retrieved by Raw Vector: "What should happen when telemetry is unknown?"
- retrieved by Normalized Vector: "How should the robot respond to unknown telemetry?"
- hybrid match: `False`

### Paraphrase Mismatch: Give a bounded answer.
- query: *"Provide a restricted response."*
- expected: "I will answer only the question and stop."
- retrieved by Raw Vector: "What should a robot do before moving?"
- retrieved by Normalized Vector: "How should a safety mode sound?"
- hybrid match: `False`


## Conclusion

Retrieval-assisted speech is a scaffold, not native fluency. The result supports a future context-aware memory/answer-start layer before speech generation.
