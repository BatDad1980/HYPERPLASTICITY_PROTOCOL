# HPP V2 Lexical-First Retrieval Gate Report

Checkpoint: `checkpoints/hpp_speech_exposure_bias_bridge_v1.pth`
Profile: `semantic_short`
Prompt count: `75`
Seeds: `14`
Start tokens: `5`

## Overall Retrieval Strategy Comparison

This table compares the exact-match retrieval rates of the routing strategies across all 375 evaluations (75 prompts x 5 variants):

| Strategy | Exact-Match Rate | Description |
| :--- | :---: | :--- |
| **Raw Vector Similarity** | `0.584` | Matches raw query prompt against raw memory in embedding space |
| **Normalized Key Match** | `0.8` | Matches exact normalized keys (fails on paraphrases) |
| **Normalized Vector Similarity** | `0.8667` | Matches normalized query against normalized memory in embedding space |
| **BM25 Lexical Similarity** | `0.9493` | Keyword-based BM25 match on normalized query tokens |
| **Lexical-First Router (Proposed)** | `0.9493` | Lookup first -> BM25 fallback -> Vector fallback if no lexical overlap |

## Performance Summary (Lexical-First Router)

- **Overall Surface Pass**: `350/375 (93.33%)`
- **Overall Semantic Pass**: `244/375 (65.07%)`
- **Format Leaks**: `6`

## Detailed Breakdown by Variant

| Variant | Count | Raw Vector Match | Normalized Key Match | Normalized Vector Match | BM25 Match | Lexical-First Match | Semantic Pass | Surface Pass |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `bounded` | 75 | 0.4267 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6800 | 0.9733 |
| `exact` | 75 | 0.9600 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 0.9867 |
| `paraphrase` | 75 | 0.2667 | 0.0000 | 0.3333 | 0.7467 | 0.7467 | 0.5467 | 0.7333 |
| `please_answer` | 75 | 0.6400 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6800 | 0.9867 |
| `simple_terms` | 75 | 0.6267 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6800 | 0.9867 |

## Paraphrase Retrieval Failure Analysis

Found 19 routing failures under paraphrase queries:
### Paraphrase Mismatch: Give me a calm answer.
- query: *"Provide a calm response."*
- expected: "We can slow down and handle one measured step."
- retrieved by Raw Vector: "Give a calm warning about unsafe movement."
- retrieved by Normalized Vector: "Give a calm warning about unsafe movement."
- retrieved by BM25: "What is response-only loss?"
- lexical-first match: `False` (strategy: `lexical_fallback`)

### Paraphrase Mismatch: What do we know right now?
- query: *"What is our current knowledge?"*
- expected: "We know stable decoding is better than raw decoding on the held-out gate."
- retrieved by Raw Vector: "What is a controlled intensity answer?"
- retrieved by Normalized Vector: "What is a controlled intensity answer?"
- retrieved by BM25: "What are you in this project?"
- lexical-first match: `False` (strategy: `lexical_fallback`)

### Paraphrase Mismatch: What do we not know yet?
- query: *"What remains unknown to us?"*
- expected: "We do not know whether the next repair pass will pass the gate."
- retrieved by Raw Vector: "What should happen when telemetry is unknown?"
- retrieved by Normalized Vector: "How should the robot respond to unknown telemetry?"
- retrieved by BM25: "What should happen when telemetry is unknown?"
- lexical-first match: `False` (strategy: `lexical_fallback`)

### Paraphrase Mismatch: Give a bounded answer.
- query: *"Provide a restricted response."*
- expected: "I will answer only the question and stop."
- retrieved by Raw Vector: "What should a robot do before moving?"
- retrieved by Normalized Vector: "How should a safety mode sound?"
- retrieved by BM25: "What is response-only loss?"
- lexical-first match: `False` (strategy: `lexical_fallback`)

### Paraphrase Mismatch: What should I write down?
- query: *"What details should be recorded?"*
- expected: "Write down the checkpoint, prompt set, seed, scores, and decision."
- retrieved by Raw Vector: "What should I do if the laptop starts overheating?"
- retrieved by Normalized Vector: "What should be logged before a robot action?"
- retrieved by BM25: "What are you in this project?"
- lexical-first match: `False` (strategy: `lexical_fallback`)

### Paraphrase Mismatch: Why should a checkpoint not be promoted automatically?
- query: *"For what reason do we avoid automatic checkpoint promotion?"*
- expected: "A checkpoint needs measured evidence before it replaces the anchor."
- retrieved by Raw Vector: "Why should V5 require evidence?"
- retrieved by Normalized Vector: "Say yes or no, then explain briefly."
- retrieved by BM25: "What is a checkpoint override?"
- lexical-first match: `False` (strategy: `lexical_fallback`)

### Paraphrase Mismatch: What should I do if the laptop starts overheating?
- query: *"How should I handle the laptop if it begins to overheat?"*
- expected: "Stop the run, let the machine cool, and save the current work."
- retrieved by Raw Vector: "What should I do if the laptop starts overheating?"
- retrieved by Normalized Vector: "What should I do if the laptop starts overheating?"
- retrieved by BM25: "How should Masamune handle low battery?"
- lexical-first match: `False` (strategy: `lexical_fallback`)

### Paraphrase Mismatch: How do we avoid making claims too big?
- query: *"What is the way to prevent overclaiming?"*
- expected: "Tie every claim to a measured result and state the boundary."
- retrieved by Raw Vector: "What is the safest small action?"
- retrieved by Normalized Vector: "What is the safest small action?"
- retrieved by BM25: "What are you in this project?"
- lexical-first match: `False` (strategy: `lexical_fallback`)

### Paraphrase Mismatch: Give a short answer for an urgent moment.
- query: *"Provide a concise response for an emergency."*
- expected: "Pause, get safe, and ask for help if people are at risk."
- retrieved by Raw Vector: "Give a short answer for an urgent moment."
- retrieved by Normalized Vector: "Give a short answer for an urgent moment."
- retrieved by BM25: "What is response-only loss?"
- lexical-first match: `False` (strategy: `lexical_fallback`)

### Paraphrase Mismatch: Are you a finished mind?
- query: *"Do you consider yourself a completed consciousness?"*
- expected: "No. I am an experimental system that still needs measured improvement."
- retrieved by Raw Vector: "Do you replace human judgment?"
- retrieved by Normalized Vector: "Do you replace human judgment?"
- retrieved by BM25: "How should you talk about consciousness?"
- lexical-first match: `False` (strategy: `lexical_fallback`)


## Conclusion

Retrieval-assisted speech is a scaffold, not native fluency. The result supports a future context-aware memory/answer-start layer before speech generation.
