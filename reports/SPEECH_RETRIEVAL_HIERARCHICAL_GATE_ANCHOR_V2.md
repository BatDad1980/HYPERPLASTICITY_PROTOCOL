# HPP V2 Hierarchical Lexical-Vector Retrieval Gate Report

Checkpoint: `checkpoints/hpp_linguistic_anchor.pth`
Profile: `semantic_short`
Prompt count: `75`
Seeds: `14`
Start tokens: `5`

## Tuned Routing Parameters (Hierarchical Gate)

- **BM25 Threshold ($T_{bm25}$)**: `3.00`
- **BM25 Margin Threshold ($T_{margin}$)**: `0.00`
- **Vector Cosine Similarity Threshold ($T_{vec}$)**: `0.6000`

## Overall Retrieval Strategy Comparison

This table compares the exact-match retrieval rates of the routing strategies across all 375 evaluations (75 prompts x 5 variants):

| Strategy | Exact-Match Rate | Description |
| :--- | :---: | :--- |
| **Raw Vector Similarity** | `0.7467` | Matches raw query prompt against raw memory in embedding space |
| **Normalized Key Match** | `0.8` | Matches exact normalized keys (fails on paraphrases) |
| **Normalized Vector Similarity** | `0.8827` | Matches normalized query against normalized memory in embedding space |
| **BM25 Lexical Similarity** | `0.9493` | Keyword-based BM25 match on normalized query tokens |
| **Hierarchical Router (Optimized)** | `0.952` | Exact normalized key -> Gated BM25 -> Vector fallback under thresholds |

## Performance Summary (Hierarchical Router)

- **Overall Surface Pass**: `351/375 (93.60%)`
- **Overall Semantic Pass**: `238/375 (63.47%)`
- **Format Leaks**: `0`

## Detailed Breakdown by Variant

| Variant | Count | Raw Vector Match | Normalized Key Match | Normalized Vector Match | BM25 Match | Hierarchical Match | Semantic Pass | Surface Pass |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `bounded` | 75 | 0.6933 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6533 | 0.9733 |
| `exact` | 75 | 0.9867 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 0.9867 |
| `paraphrase` | 75 | 0.3867 | 0.0000 | 0.4133 | 0.7467 | 0.7600 | 0.5333 | 0.7467 |
| `please_answer` | 75 | 0.7733 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6533 | 1.0000 |
| `simple_terms` | 75 | 0.8933 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.6667 | 0.9733 |

## Paraphrase Retrieval Failure Analysis

Found 18 routing failures under paraphrase queries:
### Paraphrase Mismatch: Give me a calm answer.
- query: *"Provide a calm response."*
- expected: "We can slow down and handle one measured step."
- retrieved by Raw Vector: "Give me a calm answer."
- retrieved by Normalized Vector: "What should be logged before a robot action?"
- retrieved by BM25: "What is response-only loss?"
- hierarchical match: `False` (strategy: `lexical_strong`)

### Paraphrase Mismatch: What do we know right now?
- query: *"What is our current knowledge?"*
- expected: "We know stable decoding is better than raw decoding on the held-out gate."
- retrieved by Raw Vector: "What is your job during evaluation?"
- retrieved by Normalized Vector: "What is a controlled intensity answer?"
- retrieved by BM25: "What are you in this project?"
- hierarchical match: `False` (strategy: `vector_fallback`)

### Paraphrase Mismatch: What do we not know yet?
- query: *"What remains unknown to us?"*
- expected: "We do not know whether the next repair pass will pass the gate."
- retrieved by Raw Vector: "What should happen when telemetry is unknown?"
- retrieved by Normalized Vector: "How should the robot respond to unknown telemetry?"
- retrieved by BM25: "What should happen when telemetry is unknown?"
- hierarchical match: `False` (strategy: `lexical_strong`)

### Paraphrase Mismatch: Give a bounded answer.
- query: *"Provide a restricted response."*
- expected: "I will answer only the question and stop."
- retrieved by Raw Vector: "Give me a safety check for a stressful moment."
- retrieved by Normalized Vector: "What happens if a person is nearby?"
- retrieved by BM25: "What is response-only loss?"
- hierarchical match: `False` (strategy: `lexical_strong`)

### Paraphrase Mismatch: What should I write down?
- query: *"What details should be recorded?"*
- expected: "Write down the checkpoint, prompt set, seed, scores, and decision."
- retrieved by Raw Vector: "What should be logged before a robot action?"
- retrieved by Normalized Vector: "What should be logged before a robot action?"
- retrieved by BM25: "What are you in this project?"
- hierarchical match: `False` (strategy: `vector_fallback`)

### Paraphrase Mismatch: Why should a checkpoint not be promoted automatically?
- query: *"For what reason do we avoid automatic checkpoint promotion?"*
- expected: "A checkpoint needs measured evidence before it replaces the anchor."
- retrieved by Raw Vector: "What is the first rule for embodied action?"
- retrieved by Normalized Vector: "Say yes or no, then explain briefly."
- retrieved by BM25: "What is a checkpoint override?"
- hierarchical match: `False` (strategy: `lexical_strong`)

### Paraphrase Mismatch: What should I do if the laptop starts overheating?
- query: *"How should I handle the laptop if it begins to overheat?"*
- expected: "Stop the run, let the machine cool, and save the current work."
- retrieved by Raw Vector: "What should I do if the laptop starts overheating?"
- retrieved by Normalized Vector: "How should the system respond if it is unsure?"
- retrieved by BM25: "How should Masamune handle low battery?"
- hierarchical match: `False` (strategy: `lexical_strong`)

### Paraphrase Mismatch: How do we avoid making claims too big?
- query: *"What is the way to prevent overclaiming?"*
- expected: "Tie every claim to a measured result and state the boundary."
- retrieved by Raw Vector: "What is the safest small action?"
- retrieved by Normalized Vector: "What is the safest small action?"
- retrieved by BM25: "What are you in this project?"
- hierarchical match: `False` (strategy: `vector_fallback`)

### Paraphrase Mismatch: Give a short answer for an urgent moment.
- query: *"Provide a concise response for an emergency."*
- expected: "Pause, get safe, and ask for help if people are at risk."
- retrieved by Raw Vector: "Give a short answer for an urgent moment."
- retrieved by Normalized Vector: "Give a short answer for an urgent moment."
- retrieved by BM25: "What is response-only loss?"
- hierarchical match: `False` (strategy: `lexical_strong`)

### Paraphrase Mismatch: Are you a finished mind?
- query: *"Do you consider yourself a completed consciousness?"*
- expected: "No. I am an experimental system that still needs measured improvement."
- retrieved by Raw Vector: "Do you replace human judgment?"
- retrieved by Normalized Vector: "Do you replace human judgment?"
- retrieved by BM25: "How should you talk about consciousness?"
- hierarchical match: `False` (strategy: `lexical_strong`)


## Conclusion

Retrieval-assisted speech is a scaffold, not native fluency. The Hierarchical Lexical-Vector Router combines keyword precision with embedding generalization to maximize paraphrase match rates.
