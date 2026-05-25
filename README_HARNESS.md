# HPP V5 Buyer-Safe Evaluation Harness

This evaluation harness compiles the Hyperplasticity Protocol (HPP) V5 node routing and plasticity logic inside a compiled binary. It acts as a "Black Box," allowing you to verify the HPP V5 performance claims on your own hardware without exposing the underlying proprietary math formulas.

## Architecture

The harness is split into two layers:
1. **Layer A (The Secret Engine):** The HPP V5 memory, baselines (Nearest Centroid, MLP, and GRU), and training procedures.
2. **Layer B (The Tracker):** The outer wrapper that measures peak VRAM (`torch.cuda.memory_allocated()`), performance latency, and calculates Mean Squared Error (MSE) and pathway recognition accuracy against the dataset.

## How to Execute the Harness

You can run the executable directly from your terminal:

```powershell
# Run a single seed comparison (defaults to seed 14)
.\hpp_harness.exe --seed 14

# Run on CPU instead of GPU (battery mode)
.\hpp_harness.exe --seed 14 --mode battery

# Run the 10-seed sweep (matches the evidence ladder summary claims)
.\hpp_harness.exe --sweep 10

# Run the larger 15-seed sweep at dimension 384
.\hpp_harness.exe --sweep 15 --dim 384
```

## CLI Parameter Reference

* `--mode`: Choose power mode: `auto` (default, uses CUDA if available), `plugged` (prefers GPU), or `battery` (forces CPU).
* `--seed`: Run a specific seed evaluation (e.g., `--seed 14`).
* `--sweep`: Run a sweep across `10` or `15` seeds.
* `--dim`: Representation vector dimension (defaults to `192` for 10-seed sweep, `384` for 15-seed sweep).
* `--hidden`: Hidden layer dimension for baselines.
* `--classes`: Number of class attractors (default `24`).
* `--eval-noise`: Denoising evaluation noise level (defaults to `1.35` for 10-seed sweep, `1.45` for 15-seed sweep).

## Verifying Claims

### 1. The 10-seed Sweep
Run:
```powershell
.\hpp_harness.exe --sweep 10
```
This sweep is run at dimension 192 and evaluation noise 1.35. You should expect HPP to win **100% of the seeds** in both Mean Squared Error (MSE) and pathway recognition accuracy.

### 2. The 15-seed Sweep
Run:
```powershell
.\hpp_harness.exe --sweep 15 --dim 384
```
This sweep is run at dimension 384 and evaluation noise 1.45. This test separates coordinate reconstruction from pathway recognition. HPP is expected to win **100% of seeds in pathway recognition accuracy** but **0% of seeds in MSE** (where trained gradient-based baselines perform better).

## Software and Hardware Requirements

* **OS:** Windows (x86_64) or compatible shell
* **GPU:** NVIDIA CUDA-supported GPU (e.g., RTX 4050 Laptop GPU or higher) is recommended for live VRAM measurement.
* **CPU fallback:** Automatically runs on CPU if CUDA is not detected or `--mode battery` is specified.
