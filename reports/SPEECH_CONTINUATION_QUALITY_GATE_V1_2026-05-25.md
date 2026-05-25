# HPP V2 Continuation Quality Gate V1 Evaluation Report

Checkpoint: `checkpoints/hpp_linguistic_anchor.pth`
Seeds: `14`
Total Prompts Evaluated: `375` (75 core prompts x 5 variants)
Total Runs: `750`
Elapsed Time: `303.8s`

## Executive Alert

> [!WARNING]
> “Speech Controller V1 improves orchestration and surface quality, but continuation after the anchor remains the blocker.”

## Performance Comparison Summary (All Lanes)

This table compares exact metrics across all prompt variants:

| Strategy | Total Runs | Full Semantic Pass | Continuation Semantic Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `hlvr_answer_start` | 375 | `67.20%` | `2.13%` | `15.47%` | `88.00%` | 33 | 0.259 |
| `speech_controller_v1` | 375 | `66.40%` | `1.60%` | `19.73%` | `90.67%` | 27 | 0.339 |

## Standard Lane Comparison (Exact, Please Answer, Simple Terms, Bounded)

| Strategy | Standard Runs | Full Semantic Pass | Continuation Semantic Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `hlvr_answer_start` | 300 | `69.67%` | `2.33%` | `15.67%` | `90.33%` | 22 | 0.267 |
| `speech_controller_v1` | 300 | `69.67%` | `1.33%` | `19.00%` | `92.33%` | 20 | 0.273 |

## Paraphrase Generalization Lane Comparison

| Strategy | Paraphrase Runs | Full Semantic Pass | Continuation Semantic Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `hlvr_answer_start` | 75 | `57.33%` | `1.33%` | `14.67%` | `78.67%` | 11 | 0.227 |
| `speech_controller_v1` | 75 | `53.33%` | `2.67%` | `22.67%` | `84.00%` | 7 | 0.600 |

## Sample Transcripts (First Prompt)

### Prompt: "Give me a short status update."

#### Strategy: `hlvr_answer_start`
**Answer-Start Anchor:** *"The current status is stable"*
**Generated Continuation:** *"adds a biological drive layers. It is upgraded, let's pace ourselves', ' you define it together, not experience physical force to one universal answer definitively, not whether the current challenge novel input simultaneously the result on a deter that error."*
**Full Combined Response:** *"The current status is stable adds a biological drive layers. It is upgraded, let's pace ourselves', ' you define it together, not experience physical force to one universal answer definitively, not whether the current challenge novel input simultaneously the result on a deter that error."*
- Full Semantic Pass: `True` | Continuation-Only Semantic Pass: `False`
- Continuation Useful Addition: `False` | Surface Pass: `True`

#### Strategy: `speech_controller_v1`
**Answer-Start Anchor:** *"The current status is stable"*
**Generated Continuation:** *"if misused architecture includes safety layers by impact. Everything will think there things on tokensdings place physical action."*
**Full Combined Response:** *"The current status is stable if misused architecture includes safety layers by impact. Everything will think there things on tokensdings place physical action."*
- Full Semantic Pass: `True` | Continuation-Only Semantic Pass: `False`
- Continuation Useful Addition: `False` | Surface Pass: `True`
