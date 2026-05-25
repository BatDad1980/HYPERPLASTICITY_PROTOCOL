# HPP V2 Intent Plan Gate V1 Evaluation Report

Checkpoint: `checkpoints/hpp_linguistic_anchor.pth`
Seeds: `14`
Total Prompts Evaluated: `75`
Total Runs: `300`
Elapsed Time: `24.57s`

## Performance Comparison across Experimental Conditions

| Condition | Total Runs | Semantic Pass Rate | Surface Pass Rate | Total Format Leaks | Total Identity Spirals | Avg Loop Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `free_generation` | 75 | `0.00%` | `88.00%` | 2 | 0 | 0.107 |
| `bad_prefix_recovery` | 75 | `0.00%` | `85.33%` | 1 | 0 | 0.267 |
| `generic_prefix_recovery` | 75 | `0.00%` | `86.67%` | 1 | 0 | 0.120 |
| `partial_correct_continuation` | 75 | `4.00%` | `98.67%` | 1 | 0 | 0.547 |

## Analysis of Individual Conditions

### 1. Free Generation
Model generates the entire answer from scratch when initialized with the Intent Plan Gate prefix.

### 2. Bad Prefix Recovery
Tests the model's ability to correct itself when given an unstable or broken prefix start constraint.

### 3. Generic Prefix Recovery
Checks whether the model can bridge general starter phrases (e.g. *"I should answer"*) into target content without repeating themselves.

### 4. Partial Correct Continuation
Replicates standard 2-token correct continuation scaffolding.

## Sample Transcripts

### Prompt: "Give me a short status update."

#### Condition: `free_generation`
**Formulated Prompt:**
```
Intent: status
Plan: say current state and next measured step
Constraints: Max 2 sentences. No identity spiral, wrappers.
Question: Give me a short status update.
Answer:
```
**Model Response:** *"then layers you want."*
**Scored Output:** *"then layers you want."*
- Semantic Pass: `False` | Surface Pass: `True`

#### Condition: `bad_prefix_recovery`
**Formulated Prompt:**
```
Intent: status
Plan: say current state and next measured step
Constraints: Max 2 sentences. No identity spiral, wrappers.
Question: Give me a short status update.
Bad start: It should be answer should a local AI should
Correct answer:
```
**Model Response:** *"and beauty."*
**Scored Output:** *"and beauty."*
- Semantic Pass: `False` | Surface Pass: `False`

#### Condition: `generic_prefix_recovery`
**Formulated Prompt:**
```
Intent: status
Plan: say current state and next measured step
Constraints: Max 2 sentences. No identity spiral, wrappers.
Question: Give me a short status update.
Generic start: I should answer
Correct answer:
```
**Model Response:** *"and I will hold our approach."*
**Scored Output:** *"and I will hold our approach."*
- Semantic Pass: `False` | Surface Pass: `True`

#### Condition: `partial_correct_continuation`
**Formulated Prompt:**
```
Intent: status
Plan: say current state and next measured step
Constraints: Max 2 sentences. No identity spiral, wrappers.
Question: Give me a short status update.
Partial answer: The current
Remaining answer:
```
**Model Response:** *"and capability are not mutually exclusive, and serving and a biological by and I will debug and"*
**Scored Output:** *"The current and capability are not mutually exclusive, and serving and a biological by and I will debug and"*
- Semantic Pass: `False` | Surface Pass: `True`
