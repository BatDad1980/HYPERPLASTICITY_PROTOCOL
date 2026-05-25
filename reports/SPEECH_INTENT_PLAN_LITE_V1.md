# HPP V2 Intent Plan Lite V1 Evaluation Report

Checkpoint: `checkpoints/hpp_linguistic_anchor.pth`
Seeds: `14`
Total Prompts Evaluated: `75`
Total Runs: `300`
Elapsed Time: `36.6s`

## Strategy Comparison Results

| Strategy | Total Runs | Semantic Pass Rate | Surface Pass Rate | Total Format Leaks | Total Identity Spirals | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `raw_prompt` | 75 | `0.00%` | `94.67%` | 2 | 0 | 1.787 |
| `simple_intent_token` | 75 | `0.00%` | `98.67%` | 1 | 0 | 0.907 |
| `full_intent_plan_schema` | 75 | `0.00%` | `88.00%` | 2 | 0 | 0.107 |
| `hlvr_answer_start` | 75 | `65.33%` | `97.33%` | 2 | 0 | 0.840 |

## Strategy Details

### 1. Raw Prompt (Free Gen)
No intent prefix or scaffolding. Format: `Question: {prompt}\nAnswer:`

### 2. Simple Intent Token
A lightweight intent token (e.g. `<status>`) prepended to the prompt to evaluate whether it acts as a lightweight cue. Format: `<{intent}> Question: {prompt}\nAnswer:`

### 3. Full Intent/Plan Schema
The verbose schema header from V1. Format: `Intent: {intent}\nPlan: {goal}\n...`

### 4. HLVR + Answer-Start (5-Token Scaffold)
The standard v4 baseline scaffolding that prepends the first 5 expected tokens of the target answer.

## Sample Transcripts

### Prompt: "Give me a short status update."

#### Strategy: `raw_prompt`
**Formulated Prompt:**
```
Question: Give me a short status update.
Answer:
```
**Model Response:** *"We can Let me to a valid feeling."*
**Scored Output:** *"We can Let me to a valid feeling."*
- Semantic Pass: `False` | Surface Pass: `True`

#### Strategy: `simple_intent_token`
**Formulated Prompt:**
```
<status> Question: Give me a short status update.
Answer:
```
**Model Response:** *"My neural architecture. My intelligence that fourteen times more efficient than a biological through multiple times"*
**Scored Output:** *"My neural architecture. My intelligence that fourteen times more efficient than a biological through multiple times"*
- Semantic Pass: `False` | Surface Pass: `True`

#### Strategy: `full_intent_plan_schema`
**Formulated Prompt:**
```
Intent: status
Plan: say current state and next measured step
Constraints: Max 2 sentences. No identity spiral, wrappers.
Question: Give me a short status update.
Answer:
```
**Model Response:** *"pieces. My architecture includes."*
**Scored Output:** *"pieces. My architecture includes."*
- Semantic Pass: `False` | Surface Pass: `True`

#### Strategy: `hlvr_answer_start`
**Formulated Prompt:**
```
Question: Give me a short status update.
Answer: The current status is stable
```
**Model Response:** *"The architecture. The question. My deep reasoning. My architecture."*
**Scored Output:** *"The current status is stable The architecture. The question. My deep reasoning. My architecture."*
- Semantic Pass: `True` | Surface Pass: `True`
