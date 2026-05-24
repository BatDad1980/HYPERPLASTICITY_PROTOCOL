# Named Baseline Sweep Summary

This sweep repeats the named-baseline attractor-recovery comparison across multiple seeds.

## Run

- Mode: `plugged`
- Device: `NVIDIA GeForce RTX 4050 Laptop GPU`
- CUDA available: `True`
- Seeds: `14, 21, 28`
- Classes: `24`
- Dimension: `256`
- Evaluation noise: `1.35`

## Result

- HPP MSE win rate: `0.0`
- HPP accuracy win rate: `1.0`
- Best-baseline-to-HPP MSE ratio mean: `0.90812662x`
- HPP accuracy minus best baseline mean: `0.01892362`
- Peak allocated CUDA memory max: `53.889 MB`
- HPP stored memory values: `6168`
- MLP parameters: `525568`
- GRU parameters: `1445632`

## Interpretation

This setting separates coordinate reconstruction from pathway recognition. HPP did not win mean MSE here, but it did win the class/pathway recovery metric across the tested seeds.

## Boundary

This is still a synthetic mechanism sweep. It strengthens repeatability for this task only; it does not prove broad model superiority, language ability, production safety, or a fixed efficiency multiple.
