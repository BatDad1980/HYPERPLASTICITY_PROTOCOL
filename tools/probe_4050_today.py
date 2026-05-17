"""Bounded RTX 4050 field-lab readiness probe.

This is a controlled plugged-in diagnostic, not a burn-in test. It records
matmul throughput, memory headroom, thermals when available, and CUDA OOM
boundaries without intentionally trying to crash the laptop.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from datetime import datetime, timezone

import torch


def nvidia_smi_query() -> dict:
    query = [
        "nvidia-smi",
        "--query-gpu=temperature.gpu,memory.used,memory.total,power.draw,utilization.gpu",
        "--format=csv,noheader,nounits",
    ]
    try:
        raw = subprocess.check_output(query, text=True, stderr=subprocess.STDOUT).strip()
        temp, mem_used, mem_total, power, util = [part.strip() for part in raw.split(",")]
        return {
            "temperature_c": float(temp),
            "memory_used_mib": float(mem_used),
            "memory_total_mib": float(mem_total),
            "power_w": float(power),
            "utilization_percent": float(util),
        }
    except Exception as exc:
        return {"error": str(exc)}


def synchronize() -> None:
    if torch.cuda.is_available():
        torch.cuda.synchronize()


def clear_cuda() -> None:
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


def run_matmul(size: int, repeats: int, dtype: torch.dtype) -> dict:
    device = torch.device("cuda")
    result = {"size": size, "repeats": repeats, "dtype": str(dtype).replace("torch.", "")}
    try:
        clear_cuda()
        a = torch.randn((size, size), device=device, dtype=dtype)
        b = torch.randn((size, size), device=device, dtype=dtype)
        synchronize()

        # Warmup
        _ = a @ b
        synchronize()

        start = time.perf_counter()
        for _ in range(repeats):
            c = a @ b
        synchronize()
        elapsed = time.perf_counter() - start

        ops = 2 * (size**3) * repeats
        result.update(
            {
                "status": "ok",
                "elapsed_ms": round(elapsed * 1000, 4),
                "mean_ms": round((elapsed / repeats) * 1000, 4),
                "approx_tflops": round(ops / elapsed / 1e12, 4),
                "peak_allocated_mib": round(torch.cuda.max_memory_allocated() / (1024**2), 3),
                "peak_reserved_mib": round(torch.cuda.max_memory_reserved() / (1024**2), 3),
            }
        )
        del a, b, c
    except RuntimeError as exc:
        if "out of memory" in str(exc).lower():
            result.update({"status": "cuda_oom", "error": str(exc).splitlines()[0]})
        else:
            result.update({"status": "runtime_error", "error": str(exc).splitlines()[0]})
    finally:
        clear_cuda()
    return result


def run_allocation(size_mib: int, cap_mib: int) -> dict:
    device = torch.device("cuda")
    result = {"target_mib": size_mib, "cap_mib": cap_mib}
    if size_mib > cap_mib:
        result.update({"status": "skipped_over_cap"})
        return result

    numel = size_mib * 1024 * 1024 // 2  # fp16 bytes
    try:
        clear_cuda()
        tensor = torch.empty((numel,), device=device, dtype=torch.float16)
        tensor.fill_(1.0)
        synchronize()
        result.update(
            {
                "status": "ok",
                "peak_allocated_mib": round(torch.cuda.max_memory_allocated() / (1024**2), 3),
                "peak_reserved_mib": round(torch.cuda.max_memory_reserved() / (1024**2), 3),
            }
        )
        del tensor
    except RuntimeError as exc:
        if "out of memory" in str(exc).lower():
            result.update({"status": "cuda_oom", "error": str(exc).splitlines()[0]})
        else:
            result.update({"status": "runtime_error", "error": str(exc).splitlines()[0]})
    finally:
        clear_cuda()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=os.path.join("reports", "rtx4050_field_probe_today.json"))
    parser.add_argument("--matmul-sizes", nargs="*", type=int, default=[1024, 2048, 3072, 4096])
    parser.add_argument("--repeats", type=int, default=8)
    parser.add_argument("--alloc-sizes-mib", nargs="*", type=int, default=[1024, 2048, 3072, 4096, 5120])
    parser.add_argument("--alloc-cap-mib", type=int, default=5120)
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit("CUDA is not available. Refusing to run GPU probe.")

    torch.cuda.reset_peak_memory_stats()
    started = datetime.now(timezone.utc).isoformat()
    device_props = torch.cuda.get_device_properties(0)
    before = nvidia_smi_query()

    matmul_results = []
    for size in args.matmul_sizes:
        torch.cuda.reset_peak_memory_stats()
        matmul_results.append(run_matmul(size, args.repeats, torch.float16))

    allocation_results = []
    for size_mib in args.alloc_sizes_mib:
        torch.cuda.reset_peak_memory_stats()
        allocation_results.append(run_allocation(size_mib, args.alloc_cap_mib))
        if allocation_results[-1]["status"] == "cuda_oom":
            break

    after = nvidia_smi_query()
    report = {
        "generated_at": started,
        "device_name": torch.cuda.get_device_name(0),
        "compute_capability": list(torch.cuda.get_device_capability(0)),
        "total_memory_mib": round(device_props.total_memory / (1024**2), 3),
        "before": before,
        "after": after,
        "matmul": matmul_results,
        "allocation": allocation_results,
        "boundary": "Controlled plugged-in field-lab probe; not long training, not model-quality evidence, not a burn-in test.",
    }

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, indent=2)

    best = max((r for r in matmul_results if r.get("status") == "ok"), key=lambda r: r.get("approx_tflops", 0), default=None)
    largest_alloc = max((r["target_mib"] for r in allocation_results if r.get("status") == "ok"), default=0)
    print(f"[GPU] {report['device_name']} total_mib={report['total_memory_mib']}")
    print(f"[TEMP] before={before.get('temperature_c')}C after={after.get('temperature_c')}C")
    if best:
        print(f"[BEST_MATMUL] size={best['size']} mean_ms={best['mean_ms']} approx_tflops={best['approx_tflops']}")
    print(f"[ALLOC] largest_ok_mib={largest_alloc} cap_mib={args.alloc_cap_mib}")
    print(f"[REPORT] {args.out}")


if __name__ == "__main__":
    main()
