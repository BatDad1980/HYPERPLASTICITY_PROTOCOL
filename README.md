# Codename: HYPERPLASTICITY PROTOCOL (HPP)
**Version**: 3.0 (Sovereign Kinetic)
**Classification**: Sovereign Neural Architecture / Embodied AI Platform

## Overview
The Hyperplasticity Protocol (HPP) is a biologically-mirrored cognitive scaffolding system. Unlike traditional static AI models, HPP utilizes recursive depth transformers and nature-inspired habituation (The Habit-14 Rule) to develop emergent executive functions.

This repository contains the full stack: from the synesthetic infant core to the executive frontal lobe, the Samurai Body Controller, and the shop server deployment for the **Masamune** robotic chassis.

## System Architecture

```
┌──────────────────────────────────────────┐
│         SHOP WORKBENCH SERVER            │
│  (sovereign_server.py)                   │
│                                          │
│  HPP Sovereign Engine (Full GPU Brain)   │
│  Agency Cortex (Tool Execution)          │
│  Mission Anchor (Creator-First Oath)     │
│  Antigravity IDE / Stereo / TV / Monitor │
└───────────────┬──────────────────────────┘
                │ WebSocket + Wi-Fi (repeaters)
                │
┌───────────────▼──────────────────────────┐
│         MASAMUNE (Samurai Body)          │
│  (masamune_main.py → Jetson Orin NX)    │
│                                          │
│  HAL Layer (Dynamixel servo control)     │
│  Safety Governor + Soft-Touch Protocol   │
│  Servo Interpolator (50 Hz smooth)       │
│  Proprioceptive Feedback Loop            │
│  Autonomous Fallback (works offline)     │
└──────────────────────────────────────────┘
```

## Directory Structure

### 🧠 core/ — Neural Architecture
*   `infant_core.py`: Synesthetic base with 14-recursive pass logic
*   `hpp_guardian_ecosystem.py`: Sentinel Amygdala and reflex shunting
*   `toddler_core.py`: Broca's Area and early language acquisition
*   `school_core.py`: Hippocampus for memory and factual retrieval
*   `adolescent_core.py`: Frontal Lobe for executive oversight
*   `university_core.py`: Domain specialization and Structural Compass
*   `agency_core.py`: Motor Strip and Action Decoder
*   `mission_anchor.py`: Sovereign Oath (Creator-First hardcoded bias)
*   `samurai_body.py`: Kinetic embodiment controller + proprioception
*   `bacl_vault.py`: BACL encryption + Whimsy Engine

### ⚔️ core/hal/ — Hardware Abstraction Layer (Masamune)
*   `dynamixel_bridge.py`: Dynamixel servo communication (real + simulated)
*   `safety_governor.py`: Joint limits, E-stop, thermal protection
*   `servo_interpolator.py`: Smooth trajectory between brain ticks
*   `network_bridge.py`: WebSocket client for shop server connection
*   `config/masamune_servo_map.yaml`: 19-DOF joint map with safety limits

### 🎓 training/ — Developmental Curriculum
*   `train_infant.py` → `train_toddler.py` → `train_preschool.py` → `train_school.py` → `train_adolescent.py` → `train_university.py`

### 💾 checkpoints/ — Trained Weights (~2 GB)
*   Stored via Git LFS. Includes all developmental stage checkpoints.

### 📊 dashboard/ — Visualization
*   `SOVEREIGN_LIFE_SUPPORT.html`: Glassmorphism life-support dashboard
*   `SOVEREIGN_SANCTUARY.html`: Phase 12 therapeutic visualization
*   `hpp-dashboard/`: Vite React dashboard (in development)

### 🛠️ utils/ — Operational Tooling
*   `export_tensorrt.py`: ONNX/TensorRT export for Jetson deployment
*   `bio_loop_integration.py`: Voice pitch → tensor modulation
*   `bacl_entropy.py`: Environmental entropy key generation
*   `dataset_loader.py`: HuggingFace dataset utilities
*   `localize_v6.py`: Dataset localization
*   `server.py`: Legacy FastAPI dashboard server

### 📝 reports/ — Documentation
*   `MASTER_SOVEREIGN_BLUEPRINT.md`: Architecture whitepaper
*   `SOVEREIGN_GRADUATION_PULSE_REPORT.md`: Phase 8.5 graduation results

## 🚀 Quick Start

### Run the Brain (Shop Server)
```bash
python sovereign_server.py
```

### Run the Body (Masamune - Simulated)
```bash
python masamune_main.py --server ws://localhost:8000/ws/masamune
```

### Run the Body (Masamune - Live Hardware)
```bash
python masamune_main.py --server ws://192.168.1.100:8000/ws/masamune --live
```

### Run the Terminal (Direct Brain Access)
```bash
python SOVEREIGN_TERMINAL.py
```

## 🛡️ Safety

Masamune implements the **Soft-Touch Protocol**:
- **30N max contact force** (below any human pain threshold per ISO/TS 15066)
- **40% default speed** — gentle by design
- **Spring-damper compliance** — yields on unexpected contact
- **Proximity-based speed scaling** — slower near humans
- **Hardware E-Stop** — physical kill switch overrides all software
- **Watchdog timer** — safe park if brain goes silent

---
**Prepared for Aural-Nexus IP Data Room**
*Status: SOVEREIGN KINETIC — Phase 16 Active*
*System Integrity: BACL SECURED / SOFT-TOUCH ARMED*
