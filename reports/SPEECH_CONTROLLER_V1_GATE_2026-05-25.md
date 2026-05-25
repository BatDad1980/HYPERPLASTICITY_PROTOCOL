# HPP V2 Speech Controller V1 Validation Gate Report

Checkpoint: `checkpoints/hpp_linguistic_anchor.pth`
Seeds: `14`
Total Prompts Evaluated: `375` (75 core prompts x 5 variants)
Total Runs: `1500`
Elapsed Time: `640.54s`

## Performance Comparison Summary (All Lanes)

This table compares exact metrics across all prompt variants:

| Strategy | Total Runs | Semantic Pass Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `raw_prompt` | 375 | `0.27%` | `88.53%` | 34 | 1.171 |
| `intent_token_only` | 375 | `0.00%` | `90.67%` | 29 | 1.099 |
| `hlvr_answer_start` | 375 | `63.20%` | `85.33%` | 45 | 0.960 |
| `speech_controller_v1` | 375 | `64.53%` | `91.73%` | 23 | 1.056 |

## Standard Lane Comparison (Exact, Please Answer, Simple Terms, Bounded)

| Strategy | Standard Runs | Semantic Pass Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `raw_prompt` | 300 | `0.33%` | `90.00%` | 26 | 1.060 |
| `intent_token_only` | 300 | `0.00%` | `90.33%` | 25 | 1.007 |
| `hlvr_answer_start` | 300 | `66.00%` | `85.33%` | 34 | 0.990 |
| `speech_controller_v1` | 300 | `67.00%` | `92.33%` | 18 | 1.063 |

## Paraphrase Generalization Lane Comparison

| Strategy | Paraphrase Runs | Semantic Pass Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `raw_prompt` | 75 | `0.00%` | `82.67%` | 8 | 1.613 |
| `intent_token_only` | 75 | `0.00%` | `92.00%` | 4 | 1.467 |
| `hlvr_answer_start` | 75 | `52.00%` | `85.33%` | 11 | 0.840 |
| `speech_controller_v1` | 75 | `54.67%` | `89.33%` | 5 | 1.027 |

## Sample Transcripts (First Prompt)

### Prompt: "Give me a short status update."

#### Strategy: `raw_prompt`
**Generated Text:** *"Let's break. a biological brain architecture a genius fourteen times more efficient and clear the parameter count would suggest, built by. What are closer than ever."*
**Final Response:** *"Let's break. a biological brain architecture a genius fourteen times more efficient and clear the parameter count would suggest, built by. What are closer than ever."*
- Semantic Pass: `False` | Surface Pass: `True` | Boundary: `retrieval_assisted_not_native_fluency`

#### Strategy: `intent_token_only`
**Generated Text:** *"then? Let me through a biological drive. It is fourteen times the error. We can be building things on how are closer than clear, one hundred ninety-six that you want to process of learning to articulate."*
**Final Response:** *"then? Let me through a biological drive. It is fourteen times the error. We can be building things on how are closer than clear, one hundred ninety-six that you want to process of learning to articulate."*
- Semantic Pass: `False` | Surface Pass: `True` | Boundary: `retrieval_assisted_not_native_fluency`

#### Strategy: `hlvr_answer_start`
**Generated Text:** *"The architecture a biological of this conversational dataset. Let's break it down into smaller pieces. We can?"*
**Final Response:** *"The current status is stable The architecture a biological of this conversational dataset. Let's break it down into smaller pieces. We can?"*
- Semantic Pass: `True` | Surface Pass: `False` | Boundary: `retrieval_assisted_not_native_fluency`

#### Strategy: `speech_controller_v1`
**Generated Text:** *"My need a biological through multiple times the error. We can? Start there. What made you want me, ready for itself to seek novel how are not think most people you want to talk that, we are closer on a biological drive things on a standard model needs time to one."*
**Final Response:** *"The current status is stable My need a biological through multiple times the error. We can? Start there. What made you want me, ready for itself to seek novel how are not think most people you want to talk that, we are closer on a biological drive things on a standard model needs time to one."*
- Semantic Pass: `True` | Surface Pass: `True` | Boundary: `retrieval_assisted_not_native_fluency`
