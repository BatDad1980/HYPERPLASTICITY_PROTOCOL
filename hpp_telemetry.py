from flask import Flask, jsonify, request
from flask_cors import CORS
import torch
import time
import random
import logging

# Silence standard flask logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from utils.bacl_entropy import BACL_EntropyGenerator

app = Flask(__name__)
CORS(app)

DIM = 512
print("[TELEMETRY] Booting HPP Live API Bridge...")
print("[TELEMETRY] Initializing PyTorch Sovereign Engine V2 on CPU...")
# Initialize V2 engine on CPU (use_fp16=False) to protect GPU resources
engine = HPP_SovereignEngine_V2(dim=DIM, max_context=512, use_fp16=False, init_hlvr=True)
bacl = BACL_EntropyGenerator()

# Persist state
system_state = {
    "epoch": 0,
    "safe_data": torch.randn(1, 1, DIM)
}

PROMPTS = [
    "Who are you?",
    "what is your role in HPP V2?",
    "Please answer this clearly: Explain recursion in simple terms.",
    "In simple terms, help me slow down.",
    "What should a robot do before moving?"
]

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify({
        "loops": engine.hpp_core.habit_tracker,
        "is_stabilized": engine.hpp_core.is_stabilized,
        "development_stage": "Guardian" if engine.hpp_core.is_stabilized else "Infant Core",
    })

@app.route('/api/nurture', methods=['POST'])
def run_nurture():
    system_state["epoch"] += 1
    current_entropy = bacl.generate_live_entropy()
    
    # Select prompt
    prompt = random.choice(PROMPTS)
    pitch = random.uniform(190.0, 210.0) 
    
    start_time = time.perf_counter()
    res = engine.pulse(prompt, use_hlvr=True, speech_profile="stable", speech_maturity_gate=True)
    exec_time = time.perf_counter() - start_time
    
    # Simulate loops progress (to myelinated stage)
    if engine.hpp_core.habit_tracker < 14:
        engine.hpp_core.habit_tracker += 1
        if engine.hpp_core.habit_tracker == 14:
            engine.hpp_core.is_stabilized = True
            
    routed_domain = res.get("domain_used", "conversation")
    response_text = res.get("response", "")
    
    return jsonify({
        "status": "success",
        "action": f"HLVR Prompt: '{prompt}' -> Response: '{response_text[:35]}...'",
        "execution_speed": f"{exec_time:.5f}s",
        "loops": engine.hpp_core.habit_tracker,
        "is_stabilized": engine.hpp_core.is_stabilized,
        "entropy": current_entropy,
        "pitch": round(pitch, 1),
        "task": routed_domain,
        "response": response_text
    })

@app.route('/api/toxic_stress', methods=['POST'])
def run_toxic_stress():
    stress_data = torch.randn(1, 1, DIM) * 100
    attack_entropy = "BACL_XOR_WARNING_UNAUTHORIZED_SPOOF"
    
    start_time = time.perf_counter()
    _ = engine.guardian(stress_data, current_pitch=350.0, task_type="focus", forced_stress="HIGH")
    exec_time = time.perf_counter() - start_time
    
    return jsonify({
        "status": "danger",
        "action": "Sentinel Reflex Triggered",
        "execution_speed": f"{exec_time:.6f}s",
        "entropy": attack_entropy,
        "pitch": 350.0,
        "is_stabilized": engine.hpp_core.is_stabilized
    })

if __name__ == '__main__':
    print("[TELEMETRY] HPP Live Bridge listening on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)
