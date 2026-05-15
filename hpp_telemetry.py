from flask import Flask, jsonify, request
from flask_cors import CORS
import torch
import time
import random
import logging

# Silence standard flask logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from core.infant_core import HyperPlasticCore
from core.hpp_guardian_ecosystem import GuardianEcosystem
from utils.bacl_entropy import BACL_EntropyGenerator

app = Flask(__name__)
CORS(app)

DIM = 512
print("[TELEMETRY] Booting HPP Live API Bridge...")
print("[TELEMETRY] Initializing PyTorch Core...")
hpp_engine = HyperPlasticCore(dim=DIM, max_loops=36)
masamune = GuardianEcosystem(infant_core=hpp_engine, dim=DIM)
bacl = BACL_EntropyGenerator()

# Persist the state in memory
system_state = {
    "epoch": 0,
    "safe_data": torch.randn(1, 1, DIM)
}

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify({
        "loops": hpp_engine.habit_tracker,
        "is_stabilized": hpp_engine.is_stabilized,
        "development_stage": "Guardian" if hpp_engine.is_stabilized else "Infant Core",
    })

@app.route('/api/nurture', methods=['POST'])
def run_nurture():
    system_state["epoch"] += 1
    current_entropy = bacl.generate_live_entropy()
    
    # Simulate child's focus
    task = random.choice(["focus", "calm_down", "general"])
    pitch = random.uniform(190.0, 210.0) 
    
    start_time = time.perf_counter()
    _ = masamune(system_state["safe_data"], current_pitch=pitch, task_type=task, forced_stress="LOW")
    exec_time = time.perf_counter() - start_time
    
    # Check if we should trigger habit lock
    if system_state["epoch"] >= 14 and not hpp_engine.is_stabilized:
        hpp_engine.habit_tracker = 14
        hpp_engine.signal_habit_lock()
        
    return jsonify({
        "status": "success",
        "action": f"Nurture Logic Processed ({task})",
        "execution_speed": f"{exec_time:.5f}s",
        "loops": hpp_engine.habit_tracker,
        "is_stabilized": hpp_engine.is_stabilized,
        "entropy": current_entropy,
        "pitch": round(pitch, 1),
        "task": task
    })

@app.route('/api/toxic_stress', methods=['POST'])
def run_toxic_stress():
    stress_data = torch.randn(1, 1, DIM) * 100
    attack_entropy = "BACL_XOR_WARNING_UNAUTHORIZED_SPOOF"
    
    start_time = time.perf_counter()
    _ = masamune(stress_data, current_pitch=350.0, task_type="focus", forced_stress="HIGH")
    exec_time = time.perf_counter() - start_time
    
    return jsonify({
        "status": "danger",
        "action": "Sentinel Reflex Triggered",
        "execution_speed": f"{exec_time:.6f}s",
        "entropy": attack_entropy,
        "pitch": 350.0,
        "is_stabilized": hpp_engine.is_stabilized
    })

if __name__ == '__main__':
    print("[TELEMETRY] HPP Live Bridge listening on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)
