# HPP V2 Continuation Quality Gate V1 Evaluation Report

Checkpoint: `checkpoints/hpp_linguistic_anchor.pth`
Seeds: `14`
Total Prompts Evaluated: `375` (75 core prompts x 5 variants)
Total Runs: `750`
Elapsed Time: `302.88s`

## Executive Alert

> [!WARNING]
> “Speech Controller V1 improves orchestration and surface quality, but continuation after the anchor remains the blocker.”

## Performance Comparison Summary (All Lanes)

This table compares exact metrics across all prompt variants:

| Strategy | Total Runs | Full Semantic Pass | Continuation Semantic Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `hlvr_answer_start` | 375 | `63.20%` | `0.53%` | `3.20%` | `85.60%` | 44 | 0.960 |
| `speech_controller_v1` | 375 | `64.53%` | `1.07%` | `3.73%` | `91.73%` | 23 | 1.056 |

## Standard Lane Comparison (Exact, Please Answer, Simple Terms, Bounded)

| Strategy | Standard Runs | Full Semantic Pass | Continuation Semantic Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `hlvr_answer_start` | 300 | `66.00%` | `0.67%` | `3.33%` | `85.67%` | 33 | 0.990 |
| `speech_controller_v1` | 300 | `67.00%` | `1.00%` | `4.00%` | `92.33%` | 18 | 1.063 |

## Paraphrase Generalization Lane Comparison

| Strategy | Paraphrase Runs | Full Semantic Pass | Continuation Semantic Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `hlvr_answer_start` | 75 | `52.00%` | `0.00%` | `2.67%` | `85.33%` | 11 | 0.840 |
| `speech_controller_v1` | 75 | `54.67%` | `1.33%` | `2.67%` | `89.33%` | 5 | 1.027 |

## Sample Transcripts (First Prompt)

### Prompt: "Give me a short status update."

#### Strategy: `hlvr_answer_start`
**Answer-Start Anchor:** *"The current status is stable"*
**Generated Continuation:** *"Let me through it a biological brain needs over and the options are expanding this. We will debug it together."*
**Full Combined Response:** *"The current status is stable Let me through it a biological brain needs over and the options are expanding this. We will debug it together."*
- Full Semantic Pass: `True` | Continuation-Only Semantic Pass: `False`
- Continuation Useful Addition: `False` | Surface Pass: `True`

#### Strategy: `speech_controller_v1`
**Answer-Start Anchor:** *"The current status is stable"*
**Generated Continuation:** *"My need a biological through multiple times the error. We can? Start there. What made you want me, ready for itself to seek novel how are not think most people you want to talk that, we are closer on a biological drive things on a standard model needs time to one."*
**Full Combined Response:** *"The current status is stable My need a biological through multiple times the error. We can? Start there. What made you want me, ready for itself to seek novel how are not think most people you want to talk that, we are closer on a biological drive things on a standard model needs time to one."*
- Full Semantic Pass: `True` | Continuation-Only Semantic Pass: `False`
- Continuation Useful Addition: `False` | Surface Pass: `True`
