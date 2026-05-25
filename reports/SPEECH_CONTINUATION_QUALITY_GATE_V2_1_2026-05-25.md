# HPP V2 Continuation Quality Gate V1 Evaluation Report

Checkpoint: `checkpoints/hpp_linguistic_anchor.pth`
Seeds: `14`
Total Prompts Evaluated: `375` (75 core prompts x 5 variants)
Total Runs: `750`
Elapsed Time: `310.16s`

## Executive Alert

> [!WARNING]
> “Speech Controller V1 improves orchestration and surface quality, but continuation after the anchor remains the blocker.”

## Performance Comparison Summary (All Lanes)

This table compares exact metrics across all prompt variants:

| Strategy | Total Runs | Full Semantic Pass | Continuation Semantic Pass | Continuation Partial Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `hlvr_answer_start` | 375 | `72.27%` | `4.53%` | `33.33%` | `26.93%` | `89.60%` | 18 | 0.461 |
| `speech_controller_v1` | 375 | `72.53%` | `5.87%` | `34.13%` | `30.40%` | `93.87%` | 6 | 0.373 |

## Standard Lane Comparison (Exact, Please Answer, Simple Terms, Bounded)

| Strategy | Standard Runs | Full Semantic Pass | Continuation Semantic Pass | Continuation Partial Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `hlvr_answer_start` | 300 | `75.67%` | `4.67%` | `34.00%` | `27.67%` | `90.00%` | 12 | 0.470 |
| `speech_controller_v1` | 300 | `76.33%` | `6.67%` | `34.33%` | `31.33%` | `93.33%` | 5 | 0.387 |

## Paraphrase Generalization Lane Comparison

| Strategy | Paraphrase Runs | Full Semantic Pass | Continuation Semantic Pass | Continuation Partial Pass | Useful-Addition Rate | Surface Pass Rate | Total Format Leaks | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `hlvr_answer_start` | 75 | `58.67%` | `4.00%` | `30.67%` | `24.00%` | `88.00%` | 6 | 0.427 |
| `speech_controller_v1` | 75 | `57.33%` | `2.67%` | `33.33%` | `26.67%` | `96.00%` | 1 | 0.320 |

## Sample Transcripts (First Prompt)

### Prompt: "Give me a short status update."

#### Strategy: `hlvr_answer_start`
**Answer-Start Anchor:** *"The current status is stable"*
**Generated Continuation:** *"adds a biological drive stages if misused needs a deterministic has six gigabytes of memory hardware."*
**Full Combined Response:** *"The current status is stable adds a biological drive stages if misused needs a deterministic has six gigabytes of memory hardware."*
- Full Semantic Pass: `True` | Continuation-Only Semantic Pass: `False`
- Continuation Partial Pass: `False` | Continuation Useful Addition: `False`
- Surface Pass: `True`

#### Strategy: `speech_controller_v1`
**Answer-Start Anchor:** *"The current status is stable"*
**Generated Continuation:** *"if misused architecture achieves a deterministic servos, short of learning one universal answer briefly needed the machine cool, not direct tokens measured"*
**Full Combined Response:** *"The current status is stable if misused architecture achieves a deterministic servos, short of learning one universal answer briefly needed the machine cool, not direct tokens measured"*
- Full Semantic Pass: `True` | Continuation-Only Semantic Pass: `False`
- Continuation Partial Pass: `True` | Continuation Useful Addition: `True`
- Surface Pass: `True`
