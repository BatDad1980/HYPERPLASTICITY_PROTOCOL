# hpp_harness.py
# Layer B: The Tracker (Telemetry, Evaluation & CLI Wrapper)

from __future__ import annotations
import argparse
import json
import time
from time import perf_counter
from statistics import mean, median, stdev
import platform
import os

import torch

from hpp_secret_engine import (
    make_clean_patterns,
    train_memories,
    train_model,
    sample_batch,
    OnePassMLPDenoiser,
    GRURefiner,
    count_parameters,
)

# --- Layer B Telemetry and Utility Functions ---

def select_device(mode: str = "auto") -> dict[str, object]:
    """Determines device execution under HPP guidelines."""
    cuda_available = torch.cuda.is_available()
    use_cuda = cuda_available and mode in {"auto", "plugged"}
    device = "cuda:0" if use_cuda else "cpu"
    
    device_name = "CPU"
    cuda_version = None
    if use_cuda:
        torch_device = torch.device(device)
        device_name = torch.cuda.get_device_name(torch_device)
        cuda_version = torch.version.cuda
        
    return {
        "device": device,
        "device_name": device_name,
        "cuda_available": cuda_available,
        "cuda_version": cuda_version,
    }

def calculate_mse(a: torch.Tensor, b: torch.Tensor) -> float:
    """Computes Mean Squared Error (MSE) on device."""
    return float(torch.mean((a - b) ** 2).detach().cpu())

def summarize_stats(values: list[float]) -> dict[str, float]:
    """Calculates statistical metrics for lists of numbers."""
    if not values:
        return {"min": 0.0, "mean": 0.0, "median": 0.0, "max": 0.0, "stdev": 0.0}
    return {
        "min": round(min(values), 6),
        "mean": round(mean(values), 6),
        "median": round(median(values), 6),
        "max": round(max(values), 6),
        "stdev": round(stdev(values), 6) if len(values) > 1 else 0.0,
    }

def evaluate_model(
    name: str,
    recall_fn,
    clean: torch.Tensor,
    *,
    batches: int,
    batch: int,
    noise: float,
    distractor_scale: float,
    device: torch.device,
) -> dict[str, dict[str, float]]:
    """Evaluates a model's denoising capability and tracking metrics (Layer B)."""
    errors = []
    accuracies = []
    latencies = []

    for _ in range(batches):
        x, target, labels = sample_batch(
            clean,
            batch=batch,
            noise=noise,
            distractor_scale=distractor_scale,
            device=device,
        )
        if device.type == "cuda":
            torch.cuda.synchronize(device)
        start = perf_counter()
        
        with torch.no_grad():
            output, predicted = recall_fn(x)
            
        if device.type == "cuda":
            torch.cuda.synchronize(device)
        latencies.append((perf_counter() - start) * 1000)
        errors.append(calculate_mse(output, target))
        accuracies.append(float((predicted == labels).float().mean().detach().cpu()))

    return {
        "mse": summarize_stats(errors),
        "accuracy": summarize_stats(accuracies),
        "latency_ms": summarize_stats(latencies),
    }

# --- Core Seed Execution ---

def run_seed(args: argparse.Namespace, seed: int, device_report: dict) -> dict[str, object]:
    """Runs a single training/evaluation cycle for a given seed."""
    device = torch.device(device_report["device"])
    torch.manual_seed(seed)

    # Generate synthetic dataset matrices inside the secure engine
    clean = make_clean_patterns(args.classes, args.dim, device)
    
    # Initialize models
    mlp = OnePassMLPDenoiser(args.dim, args.hidden).to(device)
    gru = GRURefiner(args.dim, args.hidden).to(device)

    if device.type == "cuda":
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats(device)
        torch.cuda.synchronize(device)

    start = perf_counter()
    
    # Observe and lock developmental memories
    hpp, nearest = train_memories(
        clean,
        classes=args.classes,
        dim=args.dim,
        exposures_per_class=args.exposures_per_class,
        batch=args.batch,
        noise=args.train_noise,
        distractor_scale=args.distractor_scale,
        device=device,
    )
    
    # Gradient training of baselines
    train_model(
        mlp,
        clean,
        steps=args.train_steps,
        batch=args.batch,
        noise=args.train_noise,
        distractor_scale=args.distractor_scale,
        lr=args.lr,
        device=device,
    )
    
    train_model(
        gru,
        clean,
        steps=args.train_steps,
        batch=args.batch,
        noise=args.train_noise,
        distractor_scale=args.distractor_scale,
        lr=args.lr,
        device=device,
    )

    # Recall functions mapping
    def recall_mlp(x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        output = mlp(x)
        predicted = torch.argmin(torch.cdist(output, clean), dim=1)
        return output, predicted

    def recall_gru(x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        output = gru(x)
        predicted = torch.argmin(torch.cdist(output, clean), dim=1)
        return output, predicted

    # Layer B: telemetry tracking & evaluation
    eval_results = {
        "hpp_developmental_memory": evaluate_model(
            "hpp_developmental_memory",
            hpp.recall,
            clean,
            batches=args.eval_batches,
            batch=args.batch,
            noise=args.eval_noise,
            distractor_scale=args.distractor_scale,
            device=device,
        ),
        "nearest_centroid": evaluate_model(
            "nearest_centroid",
            nearest.recall,
            clean,
            batches=args.eval_batches,
            batch=args.batch,
            noise=args.eval_noise,
            distractor_scale=args.distractor_scale,
            device=device,
        ),
        "one_pass_mlp": evaluate_model(
            "one_pass_mlp",
            recall_mlp,
            clean,
            batches=args.eval_batches,
            batch=args.batch,
            noise=args.eval_noise,
            distractor_scale=args.distractor_scale,
            device=device,
        ),
        "gru_refiner": evaluate_model(
            "gru_refiner",
            recall_gru,
            clean,
            batches=args.eval_batches,
            batch=args.batch,
            noise=args.eval_noise,
            distractor_scale=args.distractor_scale,
            device=device,
        ),
    }

    if device.type == "cuda":
        torch.cuda.synchronize(device)
        peak_allocated_mb = round(torch.cuda.max_memory_allocated(device) / 1024 / 1024, 3)
        peak_reserved_mb = round(torch.cuda.max_memory_reserved(device) / 1024 / 1024, 3)
    else:
        peak_allocated_mb = 0.0
        peak_reserved_mb = 0.0

    baseline_keys = ["nearest_centroid", "one_pass_mlp", "gru_refiner"]
    best_baseline_key = min(baseline_keys, key=lambda k: eval_results[k]["mse"]["mean"])
    best_baseline = eval_results[best_baseline_key]
    hpp_result = eval_results["hpp_developmental_memory"]
    
    best_accuracy_key = max(baseline_keys, key=lambda k: eval_results[k]["accuracy"]["mean"])
    best_accuracy_baseline = eval_results[best_accuracy_key]
    
    comparison = {
        "seed": seed,
        "best_mse_baseline": best_baseline_key,
        "best_accuracy_baseline": best_accuracy_key,
        "hpp_mse_mean": hpp_result["mse"]["mean"],
        "best_baseline_mse_mean": best_baseline["mse"]["mean"],
        "best_baseline_to_hpp_mse_ratio": round(best_baseline["mse"]["mean"] / max(hpp_result["mse"]["mean"], 1e-12), 6),
        "hpp_accuracy_mean": hpp_result["accuracy"]["mean"],
        "best_baseline_accuracy_mean": best_accuracy_baseline["accuracy"]["mean"],
        "hpp_accuracy_minus_best_baseline": round(hpp_result["accuracy"]["mean"] - best_accuracy_baseline["accuracy"]["mean"], 6),
        "hpp_won_mse": hpp_result["mse"]["mean"] < best_baseline["mse"]["mean"],
        "hpp_won_accuracy": hpp_result["accuracy"]["mean"] > best_accuracy_baseline["accuracy"]["mean"],
        "peak_allocated_mb": peak_allocated_mb,
        "peak_reserved_mb": peak_reserved_mb,
        "elapsed_ms": round((perf_counter() - start) * 1000, 2),
        "mlp_parameters": count_parameters(mlp),
        "gru_parameters": count_parameters(gru),
        "hpp_memory_values": int(hpp.prototypes.numel() + hpp.exposures.numel()),
    }
    
    return {"comparison": comparison, "results": eval_results}

# --- CLI Execution Orchestrator ---

def main() -> None:
    parser = argparse.ArgumentParser(description="HPP V5 Buyer-Safe Evaluation Harness")
    parser.add_argument("--mode", choices=["battery", "plugged", "auto"], default="auto",
                        help="Power mode. 'plugged' prefers GPU, 'battery' forces CPU.")
    parser.add_argument("--seed", type=int, default=None,
                        help="Run a single test with this seed (e.g., 14).")
    parser.add_argument("--sweep", type=int, choices=[10, 15], default=None,
                        help="Run a sweep across 10 or 15 pre-configured seeds.")
    parser.add_argument("--dim", type=int, default=None,
                        help="Representation dimension (defaults: 192 for 10-seed sweep, 384 for 15-seed sweep).")
    parser.add_argument("--hidden", type=int, default=None,
                        help="MLP/GRU hidden dimension. Defaults to 2x dim.")
    parser.add_argument("--classes", type=int, default=24,
                        help="Number of classes/attractors.")
    parser.add_argument("--batch", type=int, default=96,
                        help="Batch size.")
    parser.add_argument("--train-noise", type=float, default=0.42,
                        help="Training noise scale.")
    parser.add_argument("--eval-noise", type=float, default=None,
                        help="Evaluation noise scale (defaults: 1.35 for 10-seed sweep, 1.45 for 15-seed sweep).")
    parser.add_argument("--distractor-scale", type=float, default=0.28,
                        help="Distractor scale.")
    parser.add_argument("--exposures-per-class", type=int, default=56,
                        help="Training exposures per class.")
    parser.add_argument("--train-steps", type=int, default=None,
                        help="Number of steps for gradient baseline training (defaults: 60 for 10-seed sweep, 500 for 15-seed sweep).")
    parser.add_argument("--eval-batches", type=int, default=24,
                        help="Number of evaluation batches.")
    parser.add_argument("--lr", type=float, default=0.0016,
                        help="Baseline optimizer learning rate.")
    args = parser.parse_args()

    # Determine default sweeps and parameter configurations
    is_sweep = args.sweep is not None
    sweep_size = args.sweep if is_sweep else 10
    
    # Configure defaults matching the evidence ladder
    if args.dim is None:
        args.dim = 384 if (is_sweep and sweep_size == 15) else 192
    if args.hidden is None:
        args.hidden = args.dim * 2
    if args.eval_noise is None:
        args.eval_noise = 1.45 if (is_sweep and sweep_size == 15) else 1.35
    if args.train_steps is None:
        args.train_steps = 500 if (is_sweep and sweep_size == 15) else 60

    device_report = select_device(args.mode)
    
    print("=" * 70)
    print("   HYPERPLASTICITY PROTOCOL (HPP) V5 EVALUATION HARNESS")
    print("=" * 70)
    print(f"  Device:           {device_report['device_name']}")
    print(f"  CUDA Available:   {device_report['cuda_available']} (Version: {device_report['cuda_version']})")
    print(f"  Classes:          {args.classes}")
    print(f"  Dimension:        {args.dim}")
    print(f"  Hidden Size:      {args.hidden}")
    print(f"  Eval Noise:       {args.eval_noise}")
    print(f"  Distractor Scale: {args.distractor_scale}")
    print("-" * 70)

    # Determine seeds to run
    if args.seed is not None:
        seeds = [args.seed]
        print(f"Running single evaluation with seed {args.seed}...")
    elif is_sweep:
        if sweep_size == 10:
            seeds = [14, 21, 42, 77, 101, 133, 144, 199, 256, 314]
            print(f"Running 10-seed sweep: {seeds}")
        else: # 15
            seeds = [14, 21, 42, 77, 101, 133, 144, 199, 256, 314, 377, 512, 777, 1024, 1337]
            print(f"Running 15-seed sweep: {seeds}")
    else:
        # Default fallback to seed 14 single run
        seeds = [14]
        print("No seed or sweep specified. Defaulting to seed 14 single evaluation...")

    comparisons = []
    
    for s_idx, seed in enumerate(seeds):
        print(f"\n[Seed {seed:4d}] Processing...", end="", flush=True)
        report = run_seed(args, seed, device_report)
        comp = report["comparison"]
        comparisons.append(comp)
        print(f" Done in {comp['elapsed_ms']:.1f}ms. Peak VRAM: {comp['peak_allocated_mb']:.3f} MB")
        
        # Verbose prints for single runs
        if len(seeds) == 1:
            print("-" * 50)
            print(f"  HPP Parameter Values (Stored Memory):  {comp['hpp_memory_values']:,}")
            print(f"  MLP Baseline Parameters:               {comp['mlp_parameters']:,}")
            print(f"  GRU Baseline Parameters:               {comp['gru_parameters']:,}")
            print("-" * 50)
            print(f"  Mean Squared Error (MSE):")
            print(f"    HPP Developmental Memory:   {comp['hpp_mse_mean']:.6f} [Win: {comp['hpp_won_mse']}]")
            print(f"    Best Baseline ({comp['best_mse_baseline']}):   {comp['best_baseline_mse_mean']:.6f}")
            print(f"    MSE Ratio (Best Base / HPP): {comp['best_baseline_to_hpp_mse_ratio']:.4f}x")
            print(f"  Pathway Recognition Accuracy:")
            print(f"    HPP Developmental Memory:   {comp['hpp_accuracy_mean']:.2%}")
            print(f"    Best Baseline Accuracy:     {comp['best_baseline_accuracy_mean']:.2%}")
            print(f"    Accuracy Edge (HPP - Base): {comp['hpp_accuracy_minus_best_baseline']:.2%}")

    # Summary report for sweeps
    if len(seeds) > 1:
        mse_wins = sum(1 for c in comparisons if c["hpp_won_mse"])
        acc_wins = sum(1 for c in comparisons if c["hpp_won_accuracy"])
        avg_ratio = mean(c["best_baseline_to_hpp_mse_ratio"] for c in comparisons)
        avg_acc_edge = mean(c["hpp_accuracy_minus_best_baseline"] for c in comparisons)
        max_vram = max(c["peak_allocated_mb"] for c in comparisons)
        
        print("\n" + "=" * 70)
        print("  SWEEP SUMMARY REPORT")
        print("=" * 70)
        print(f"  Seeds Run:           {len(seeds)}")
        print(f"  HPP MSE Win Rate:    {mse_wins / len(seeds):.1%}")
        print(f"  HPP Accuracy Win:    {acc_wins / len(seeds):.1%}")
        print(f"  Avg MSE Ratio:       {avg_ratio:.4f}x (Best Baseline / HPP)")
        print(f"  Avg Accuracy Edge:   {avg_acc_edge:.2%} (HPP - Best Baseline)")
        print(f"  Peak Allocated CUDA: {max_vram:.3f} MB")
        print(f"  MLP Parameters:      {comparisons[0]['mlp_parameters']:,}")
        print(f"  GRU Parameters:      {comparisons[0]['gru_parameters']:,}")
        print(f"  HPP Memory Values:   {comparisons[0]['hpp_memory_values']:,}")
        print("=" * 70)
        
        # Verify specific claim matches
        if sweep_size == 10 and args.dim == 192:
            print("\n[VERIFICATION]")
            print(f"  Evidence Claims check for 10-seed sweep:")
            print(f"    * HPP MSE Win Rate = 100%:        {'PASSED' if mse_wins == 10 else 'FAILED'}")
            print(f"    * HPP Accuracy Win Rate = 100%:   {'PASSED' if acc_wins == 10 else 'FAILED'}")
        elif sweep_size == 15 and args.dim == 384:
            print("\n[VERIFICATION]")
            print(f"  Evidence Claims check for 15-seed sweep:")
            print(f"    * HPP MSE Win Rate = 0%:          {'PASSED' if mse_wins == 0 else 'FAILED'}")
            print(f"    * HPP Accuracy Win Rate = 100%:   {'PASSED' if acc_wins == 15 else 'FAILED'}")

    print("\n  Harness Execution Completed.")
    print("=" * 70)

if __name__ == "__main__":
    main()
