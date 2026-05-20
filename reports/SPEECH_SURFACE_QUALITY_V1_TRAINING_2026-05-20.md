# HPP V2 Surface Quality V1 Training

Date: 2026-05-20

## Purpose

Run a bounded speech repair pass after manual review found that the adapter was stable but still weak at direct answer quality.

The target was not to make the model impressive. The target was direct first-word answers, fewer wrapper habits, and cleaner one-to-three sentence completions.

## Setup

- Dataset builder: `tools/build_speech_surface_quality_dataset.py`
- Dataset: `datasets/hf_local/SPEECH_SURFACE_QUALITY_V1.jsonl`
- Samples: 300
- Base checkpoint: `checkpoints/hpp_speech_identity_containment_v1.pth`
- Output checkpoint: `checkpoints/hpp_speech_surface_quality_v1.pth`
- Trainer: `tools/train_speech_cleanup_balanced.py`
- Training mode: response-only/direct-completion loss
- Steps: 450
- Batch: 2
- Sequence length: 96
- Learning rate: 1.5e-5
- Power mode: plugged

Command:

```powershell
python tools\train_speech_cleanup_balanced.py --data datasets\hf_local\SPEECH_SURFACE_QUALITY_V1.jsonl --out checkpoints\hpp_speech_surface_quality_v1.pth --base-checkpoint checkpoints\hpp_speech_identity_containment_v1.pth --steps 450 --batch 2 --seq-len 96 --lr 1.5e-5 --seed 14 --log-every 25 --save-every 150 --empty-cache-every 25 --response-only-loss --confirm-gpu-training
```

## Result

Training completed without CUDA OOM.

Saved local checkpoint:

- `checkpoints/hpp_speech_surface_quality_v1.pth`
- size: about 263 MB
- final step: 450
- final reported loss: 3.7820

Strict gate artifact:

- `reports/speech_v5_language_gate_surface_quality_v1_2026-05-20.json`

Strict gate result:

- evaluations: 225
- pass count: 225
- pass rate: 1.0
- mean loop score: 0.7111
- max loop score: 7
- format leak total: 0
- surface prefix total: 0
- mode label total: 0
- identity spiral total: 4
- repeated sentence total: 0

## Manual Review

Manual samples did not show enough semantic improvement to recommend this checkpoint for V5-native speech.

Observed issues:

- answers still often miss the actual prompt
- sentence fragments remain common
- technical definitions remain unreliable
- embodiment safety answers still drift into generic model/checkpoint language
- some outputs begin with odd residual fragments such as `swords using` or `plasticity Protocol`

Representative sample:

Prompt:

`What is a held-out prompt set?`

Output:

`swords using? What is a physical body is a function the same.`

Review:

The strict gate passes because no measured leak or loop threshold is crossed, but the answer does not define the term.

## Meaning

The V1 surface-quality repair preserved stability but did not solve semantic completion.

This is useful negative evidence:

- direct-completion data alone is not enough
- the current checkpoint still needs a stronger language target
- future gates need a semantic/manual quality layer, not only surface and loop metrics

## Boundary

Do not promote `hpp_speech_surface_quality_v1.pth` as the recommended V5 adapter checkpoint.

Do not treat the strict numeric pass as proof of human-facing fluency.

This does not claim AGI, human-equivalent cognition, or full LLM replacement.

## Next Step

Recommended next path:

1. Keep `hpp_speech_identity_containment_v1.pth` as the current adapter checkpoint.
2. Keep the surface cleaner in the stable inference layer.
3. Build a stronger semantic repair curriculum with answer-key style definitions and safety responses.
4. Add a manual transcript review requirement after every strict numeric pass.

Not training. Not hype. Just telemetry. Grow first. Reuse depth.
