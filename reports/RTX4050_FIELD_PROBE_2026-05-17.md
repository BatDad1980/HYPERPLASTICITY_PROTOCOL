# RTX 4050 Field Probe

Date: 2026-05-17

## Purpose

Check how healthy the RTX 4050 laptop GPU feels today under controlled plugged-in field-lab conditions.

This is a readiness and headroom probe, not a burn-in test and not model-quality evidence.

## Setup

- Machine role: HPP V2 wild lab / mobile field laptop
- Device: NVIDIA GeForce RTX 4050 Laptop GPU
- CUDA visible to PyTorch: yes
- Compute capability: 8.9
- Total CUDA memory reported by PyTorch: about `6140.5 MiB`
- Power context: plugged into wall power
- Script: `tools/probe_4050_today.py`

## Conservative Probe

Artifact:

`reports/rtx4050_field_probe_2026-05-17.json`

Result:

- Temperature before: `46C`
- Temperature after: `48C`
- Best FP16 matmul size: `3072`
- Best approximate throughput: `17.5822 TFLOPS`
- Largest allocation under cap: `5120 MiB`

## Edge Probe

Artifact:

`reports/rtx4050_field_probe_2026-05-17_edge.json`

Result:

- Temperature before: `47C`
- Temperature after: `49C`
- Best FP16 matmul size: `5120`
- Best approximate throughput: `17.7164 TFLOPS`
- Largest allocation under cap: `5632 MiB`

## Meaning

The 4050 was healthy today:

- CUDA was available.
- Baseline temperature was cool.
- Short FP16 matrix workloads ran cleanly.
- A large allocation close to practical VRAM capacity succeeded.
- Temperature stayed under `50C` after both probes.

This supports the field-lab premise that meaningful HPP work can be performed on modest local hardware when runs are bounded, monitored, and documented.

## Boundary

This does not prove:

- long training stability,
- model quality,
- safe sustained thermal behavior,
- full VRAM availability during mixed desktop workloads,
- that larger HPP runs should be launched without stop conditions.

It only proves today's short controlled CUDA readiness.

## Field-Lab Rule

The laptop is part of the hypothesis, but it is also the inventor's only machine.

Use it hard enough to learn. Do not use it blindly enough to lose the lab.
