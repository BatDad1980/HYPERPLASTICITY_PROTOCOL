# Original HPP Speech Progress Bridge

Date observed: 2026-05-15

Source path:

`C:\Users\Aural\Desktop\Codename HYPERPLASTICITY PROTOCOL\Project_HPP`

This note tracks the speech and conversational fluency work in the original HPP branch so V5 can inherit the useful lessons without copying unstable prototype behavior wholesale.

## Current Local Artifacts

Recent speech-focused files observed in the original branch:

- `train_conversational.py`
- `train_conv_focused.py`
- `SPEECH_TEST.py`
- `datasets/hf_local/CONVERSATIONAL_FLUENCY.jsonl`
- `checkpoints/hpp_conversational_1000.pth`
- `checkpoints/hpp_conversational_2000.pth`
- `checkpoints/hpp_conversational_3000.pth`
- `checkpoints/hpp_conversational_4000.pth`
- `checkpoints/hpp_conversational_final.pth`
- `checkpoints/hpp_conversational_progress.pth`
- `checkpoints/hpp_linguistic_anchor.pth`
- HPP V5 regression report: `docs/original-speech-regression.json`

Checkpoint inspection showed the current speech anchor contains:

- `masamune_state_dict`: 75 tensors, 14,189,061 parameters
- `lm_head_state_dict`: 2 tensors, 25,781,841 parameters
- `embedding_state_dict`: 1 tensor, 25,731,584 parameters
- total checkpoint size: about 250.67 MB
- phase metadata on latest anchor: `conversational_v17d`

## What Changed

The original branch moved away from trying to retrain the entire system for language. The better strategy is:

1. Freeze the deep developmental stack.
2. Train the embedding and language-model head.
3. Train the Structural Compass for word order and sequence position.
4. Train the conversation domain layer and routing gate.
5. Train output normalization for speech stability.

This is important because it treats the problem as a speech-interface problem, not as evidence that the whole HPP substrate needs to be rebuilt every time the voice is rough.

## Light Smoke Test Result

`SPEECH_TEST.py` was run against `hpp_linguistic_anchor.pth`.

Observed improvement:

- Output is no longer only isolated concept clusters.
- Sentence-shaped fragments are appearing.
- Training response patterns are recognizable.
- Identity, protection, architecture, and support concepts are being preserved.

Observed limitations:

- The model leaks training format such as `### Response:`.
- It blends multiple samples into one answer.
- It repeats phrases such as `using using using`.
- It often starts coherently and then drifts into architecture vocabulary.
- Identity/protection examples appear overrepresented relative to ordinary dialogue.

Interpretation:

The original branch is between "technical dialect" and usable speech. This is genuine progress, but not yet buyer-safe conversational evidence.

## Held-Out Regression Result

HPP V5 now includes `scripts/run_original_speech_regression.py`, which runs read-only held-out prompts against the original branch and writes `docs/original-speech-regression.json`.

First regression run:

- Checkpoint: `hpp_linguistic_anchor.pth`
- Phase: `conversational_v17d`
- Device: NVIDIA GeForce RTX 4050 Laptop GPU
- Prompts: 6 held-out prompts
- Max tokens: 60
- Temperature: 0.7
- Top-p: 0.9

Observed:

- CUDA inference completed successfully.
- All prompts produced non-empty text.
- Responses are sentence-shaped but not yet reliably instruction-following.
- Five of six held-out responses leaked training format such as `### Response`.
- Responses drift heavily into architecture, neural-network, and Masamune vocabulary.
- Repetition exists but the biggest failure mode is format leakage plus topic blending, not total collapse.

Next speech-training target:

The next original-branch cycles should prioritize plain output format, ordinary dialogue grounding, and held-out prompt behavior before adding more identity or architecture examples.

## Cleanup Cycle Outcome

See `docs/original-speech-cleanup-cycle-summary.md`.

Three cleanup checkpoints were tested:

- `hpp_speech_cleanup_v1.pth`
- `hpp_speech_cleanup_masked_v2.pth`
- `hpp_speech_cleanup_v3.pth`

Outcome:

- v1 reduced format leakage but degraded coherence and increased repetition.
- v2 added response-only loss masking but did not recover held-out speech quality.
- v3 froze embedding and compass for a safer low-memory run, but still did not improve held-out speech.

Decision:

Do not promote the cleanup checkpoints over `hpp_linguistic_anchor.pth`.

The important progress is the evidence loop itself: dataset audit, bounded training, CUDA memory logging, held-out regression, and honest rejection of weak checkpoints.

## Speech Mode Routing And Maturity Gate Outcome

Observed from the original branch on 2026-05-17:

- Report: `reports/SPEECH_MODE_ROUTING_AND_MATURITY_GATE_2026-05-17.md`
- New regression tool: `tools/speech_mode_regression.py`
- Routing datasets:
  - `datasets/hf_local/SPEECH_MODE_ROUTING_V1.jsonl`
  - `datasets/hf_local/SPEECH_MODE_ROUTING_V2.jsonl`
- Experimental checkpoints:
  - `checkpoints/hpp_speech_mode_routing_v1.pth`
  - `checkpoints/hpp_speech_mode_routing_v2.pth`

The current safest plugged speech baseline reported from the V2 lab is:

`hpp_speech_grammar_first_v1.pth` with the stable maturity-gated profile.

Across seeds `14`, `21`, and `28`:

| Checkpoint | Mode | Mean Regression | Format Leaks |
| --- | --- | ---: | ---: |
| `hpp_speech_grammar_first_v1.pth` | Raw plugged | `3.0533` | `17` |
| `hpp_speech_grammar_first_v1.pth` | Stable profile | `0.6933` | `1` |
| `hpp_speech_mode_routing_v2.pth` | Raw plugged | `4.8133` | `20` |
| `hpp_speech_mode_routing_v2.pth` | Stable profile | `0.92` | `1` |

Interpretation:

The original branch is showing developmental speech instability rather than simple "bad talking." More recurrent depth can re-amplify immature identity/protection phrase attractors. Stable maturity-gated speech sharply reduced regression and format leakage.

Design principle harvested for V5:

> Grow first. Reuse depth. Gate maturity.

## V5-Safe Adapter Clean Pass

Observed from the original branch on 2026-05-20:

- Report: `reports/SPEECH_V5_SAFE_ADAPTER_CLEAN_PASS_2026-05-20.md`
- Adapter: `core/v5_language_adapter.py`
- Checkpoint: `checkpoints/hpp_speech_identity_containment_v1.pth`
- Gate evaluator: `tools/speech_v5_language_gate.py`
- Held-out suite: `datasets/hf_local/SPEECH_HELDOUT_V5_GATE_V1.jsonl`
- Seeds: `14`, `21`, `28`
- Profile: stable adapter path

Result:

- Evaluations: `225`
- Pass count: `225`
- Pass rate: `1.0`
- Format leaks: `0`
- Mode-label leaks: `0`
- Mean loop score: `0.6933`
- Max loop score: `7`
- Repeated sentence failures: `0`
- Identity spiral count: `5`, still measured but no longer failing under the current rubric

Interpretation:

This clears the current V5 language inheritance target: reliably clean and measurable, not impressive. It is the strongest V2 speech result so far because it passed a held-out, multi-seed adapter gate with transcript artifacts and zero format/mode-label leakage.

Boundary:

This is a stable adapter result, not raw V2 speech, not automatic checkpoint promotion, not mature fluency, and not an AGI or LLM replacement claim.

Cold restart confirmation:

- Report: `reports/SPEECH_V5_SAFE_ADAPTER_COLD_RESTART_2026-05-20.md`
- Commit in V2: `28f9042 Add cold restart adapter gate evidence`
- Evaluations: `225`
- Pass count: `225`
- Pass rate: `1.0`
- Format leaks: `0`
- Mode-label leaks: `0`
- Repeated sentence failures: `0`
- Mean loop score: `0.6933`
- Max loop score: `7`
- Identity spiral count: `5`

The clean adapter gate repeated after a fresh process and fresh CUDA context, so V5 can begin adapter import planning.

## Manual Review And Strict Surface Gate Hold

Observed from the original branch on 2026-05-20:

- Manual report: `reports/SPEECH_V5_MANUAL_TRANSCRIPT_REVIEW_COLD_RESTART_2026-05-20.md`
- Strict gate report: `reports/SPEECH_V5_STRICT_SURFACE_GATE_2026-05-20.md`
- V2 commit: `9a2b5f9 Add manual speech quality gate`

Manual transcript review found:

- outputs beginning with `Response`: `180 / 225`
- outputs beginning with `Instruction`: `18 / 225`
- common issue: sentence-shaped fragments without reliable semantic completion
- common issue: prompt-adjacent words appear without clearly answering the prompt

Strict surface gate:

- Evaluations: `225`
- Pass count: `27`
- Pass rate: `0.12`
- Surface prefix total: `198`
- Format leaks: `0`
- Mode-label leaks: `0`
- Repeated sentence failures: `0`
- Mean loop score: `0.6933`
- Max loop score: `7`

Interpretation:

The stability result remains real, but V5-native speech promotion is on hold. The next target is response-cleaning: direct first-word answers, no wrapper starts, one-to-three clean sentences, and bounded identity language.

## Lessons For HPP V5

V5 should preserve these lessons:

- Treat the voice as a trainable adapter over a protected core.
- Keep recurrent/developmental kernel evidence separate from speech quality evidence.
- Use clean curriculum design before adding compute.
- Route recurrent depth by maturity instead of assuming more loops are always better.
- Record transcript samples at each checkpoint so progress is auditable.
- Measure repetition, template leakage, and sentence completion as speech-specific metrics.

## Training Constraint Note

The original branch reportedly hit out-of-memory behavior during a single 5,000-step speech cycle, while two separate 2,500-step cycles completed without the same failure.

Interpretation:

- This looks more like long-run memory accumulation, allocator fragmentation, stale graph retention, or cache pressure than a fixed "model too large" limit.
- Splitting long training into shorter resumable cycles is currently the safer RTX 4050-class workflow.
- Each cycle should save a checkpoint, exit the Python process, relaunch cleanly, and continue from the saved anchor.

V5 should treat long-running training as a scheduled sequence of short bounded jobs, not as one monolithic run.

## Next Experiments To Harvest

Before V5 absorbs the speech direction, the original branch should test:

- format-free training text, or loss masking for instruction/response markers
- balanced conversational data with more ordinary daily dialogue
- anti-repetition decoding
- stop-token and clean-ending behavior
- held-out prompts that are not in the training set
- transcript logging after every speech checkpoint
- a small regression suite that compares `1000`, `2000`, `3000`, `4000`, `final`, and `anchor`
- split-cycle training resumes, such as `2,500 + 2,500`, with GPU memory logged at start and end of each cycle
- reduction of `### Response` format leakage on held-out prompts

## Buyer-Safe Position

Do not claim full conversational maturity yet.

Buyer-safe language:

> The original HPP branch has begun converting concept-cluster output into sentence-shaped speech by freezing the deeper developmental stack and training a dedicated speech adapter layer. Early smoke tests show meaningful progress, with remaining work focused on repetition control, format leakage, and clean conversational generalization.
