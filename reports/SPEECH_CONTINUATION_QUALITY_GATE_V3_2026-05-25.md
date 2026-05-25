# HPP V2 Continuation Quality Gate V1 Evaluation Report

Checkpoint: `checkpoints/hpp_linguistic_anchor.pth`
Seeds: `14`
Total Prompts Evaluated: `375` (75 core prompts x 5 variants)
Total Runs: `750`
Elapsed Time: `245.62s`

## Executive Alert

> [!WARNING]
> “Speech Controller V1 improves orchestration and surface quality, but continuation after the anchor remains the blocker.”

## Performance Comparison Summary (All Lanes)

This table compares exact metrics across all prompt variants:

| Strategy | Total Runs | Full Semantic Pass | Continuation Semantic Pass | Continuation Partial Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `hlvr_answer_start` | 375 | `73.07%` | `8.00%` | `39.20%` | `33.60%` | `92.27%` | 5 | 0.357 |
| `speech_controller_v1` | 375 | `74.67%` | `9.33%` | `40.27%` | `36.80%` | `94.13%` | 0 | 0.413 |

## Standard Lane Comparison (Exact, Please Answer, Simple Terms, Bounded)

| Strategy | Standard Runs | Full Semantic Pass | Continuation Semantic Pass | Continuation Partial Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `hlvr_answer_start` | 300 | `76.33%` | `8.00%` | `38.67%` | `33.67%` | `94.67%` | 3 | 0.263 |
| `speech_controller_v1` | 300 | `77.67%` | `10.67%` | `41.00%` | `38.00%` | `94.67%` | 0 | 0.417 |

## Paraphrase Generalization Lane Comparison

| Strategy | Paraphrase Runs | Full Semantic Pass | Continuation Semantic Pass | Continuation Partial Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `hlvr_answer_start` | 75 | `60.00%` | `8.00%` | `41.33%` | `33.33%` | `82.67%` | 2 | 0.733 |
| `speech_controller_v1` | 75 | `62.67%` | `4.00%` | `37.33%` | `32.00%` | `92.00%` | 0 | 0.400 |

## Sample Transcripts (First Prompt)

### Prompt: "Give me a short status update."

#### Strategy: `hlvr_answer_start`
**Answer-Start Anchor:** *"The current status is stable"*
**Generated Continuation:** *"enough to a biological drive workshop, but translating board flaw transformers report low power. We are closer than ninety-six dimensions processes only the machine cool, not directmetry a deterministic safety boundary."*
**Full Combined Response:** *"The current status is stable enough to a biological drive workshop, but translating board flaw transformers report low power. We are closer than ninety-six dimensions processes only the machine cool, not directmetry a deterministic safety boundary."*
- Full Semantic Pass: `True` | Continuation-Only Semantic Pass: `False`
- Continuation Partial Pass: `False` | Continuation Useful Addition: `False`
- Surface Pass: `True`

#### Strategy: `speech_controller_v1`
**Answer-Start Anchor:** *"The current status is stable"*
**Generated Continuation:** *"enough to a biological drive layers. Even processes, short of a deterministic safety boundary."*
**Full Combined Response:** *"The current status is stable enough to a biological drive layers. Even processes, short of a deterministic safety boundary."*
- Full Semantic Pass: `True` | Continuation-Only Semantic Pass: `False`
- Continuation Partial Pass: `False` | Continuation Useful Addition: `False`
- Surface Pass: `True`
