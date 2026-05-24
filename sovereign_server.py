"""
===============================================================================
       HPP SOVEREIGN SERVER — SHOP WORKBENCH BRAIN
===============================================================================
The main brain of the shop. Runs on the workbench server alongside
Antigravity IDE, stereo, TV, and second monitor.

Masamune (the Samurai body) connects to this server over the network
when it needs complex reasoning, agency decisions, or speech generation.

Endpoints:
    POST /api/pulse          — Standard text inference
    POST /api/nexus          — Agentic inference with tool execution
    POST /api/kinetic        — Generate body commands from a prompt
    POST /api/proprioception — Receive body sensor state, return motor commands
    GET  /api/status         — Engine telemetry
    WS   /ws/masamune        — WebSocket for real-time body↔brain streaming

The server handles:
    - Full HPP Sovereign Engine inference (University stack)
    - Agency decisions (tool execution, file I/O)
    - Speech generation
    - Kinetic command generation for Masamune's body

The Jetson on Masamune handles:
    - Real-time servo control (50 Hz)
    - Safety governor (joint limits, E-stop)
    - Servo interpolation (smooth motion)
    - Local sensor reading (IMU, camera, mic)
    - Connecting to this server for complex thought
===============================================================================
"""
import os
import sys
import json
import time
import asyncio

# Ensure project root is on path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import torch

from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2

# ================================================================
# APP SETUP
# ================================================================
app = FastAPI(
    title="HPP Sovereign Server",
    description="Shop Workbench Brain - Masamune connects here",
    version="3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================================================
# ENGINE INITIALIZATION
# ================================================================
print("=" * 70)
print("         HPP SOVEREIGN SERVER - SHOP WORKBENCH BRAIN")
print("=" * 70)

engine = HPP_SovereignEngine_V2(max_context=512, init_hlvr=True)

# Track connected Masamune instances
connected_bodies = {}

print("\n[SERVER] Sovereign Engine loaded. Awaiting connections.")
print("=" * 70)


# ================================================================
# REQUEST MODELS
# ================================================================
class PulseRequest(BaseModel):
    input_text: str
    pitch: float = 205.0
    emotion: str = "neutral"
    max_tokens: int = 150
    temperature: float = 0.78
    top_p: float = 0.92
    domain: str = "none"


class KineticRequest(BaseModel):
    prompt: str
    proprioception: Optional[list] = None  # 19-element body state vector
    domain: str = "synthesis"
    max_tokens: int = 100


class ProprioceptionUpdate(BaseModel):
    body_id: str = "masamune_prime"
    joint_positions: list  # 19-element vector from DynamixelBridge
    timestamp: float = 0.0


# ================================================================
# REST ENDPOINTS
# ================================================================
@app.post("/api/pulse")
def api_pulse(req: PulseRequest):
    """Standard text inference — used by dashboard and terminal."""
    try:
        result = engine.pulse(
            input_text=req.input_text,
            pitch=req.pitch,
            emotion=req.emotion,
            max_tokens=req.max_tokens,
            temperature=req.temperature,
            top_p=req.top_p,
            domain=req.domain
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/nexus")
def api_nexus(req: PulseRequest):
    """Agentic inference with tool execution capability."""
    try:
        result = engine.nexus_pulse(req.input_text, auto_execute=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/kinetic")
def api_kinetic(req: KineticRequest):
    """
    Generate body commands for Masamune.
    Called by the Jetson when Masamune needs complex reasoning
    to decide how to move.
    """
    try:
        with torch.no_grad():
            tokens = engine.enc.encode(req.prompt)
            if not tokens:
                tokens = [engine.enc.eot_token]

            token_tensor = torch.tensor(
                [tokens], dtype=torch.long, device=engine.device
            )
            embedded = engine.embedding(token_tensor).permute(1, 0, 2)

            # Mission anchor verification
            anchored = engine.anchor.pulse_verification(embedded)

            # Full brain pass
            thought = engine.university(anchored, domain=req.domain)

            # Inject proprioceptive feedback if provided
            if req.proprioception and len(req.proprioception) == 19:
                proprio_tensor = torch.tensor(
                    [req.proprioception], dtype=torch.float32,
                    device=engine.device
                )
                proprio_latent = engine.proprioception(proprio_tensor)
                thought = thought + proprio_latent * 0.3

            # Generate body commands
            body_output = engine.samurai_body(thought)
            cmd_vector = engine.samurai_body.to_command_vector(body_output)

            # Also get verbal response
            text_result = engine.pulse(
                req.prompt, max_tokens=req.max_tokens,
                temperature=0.7, domain=req.domain
            )

        return {
            "joint_commands": cmd_vector,
            "left_arm": cmd_vector[0:7],
            "right_arm": cmd_vector[7:14],
            "stance": cmd_vector[14:18],
            "grip": cmd_vector[18] if len(cmd_vector) > 18 else 0.0,
            "verbal_response": text_result['response'],
            "latency_ms": text_result['latency_ms'],
            "telemetry": text_result['telemetry']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/proprioception")
def api_proprioception(update: ProprioceptionUpdate):
    """
    Receive body sensor state from Masamune's Jetson.
    Returns acknowledgment and any pending commands.
    """
    connected_bodies[update.body_id] = {
        "last_seen": time.time(),
        "joint_positions": update.joint_positions,
        "timestamp": update.timestamp
    }
    return {
        "status": "received",
        "body_id": update.body_id,
        "server_time": time.time()
    }


@app.get("/api/status")
def api_status():
    """Full engine and connection telemetry."""
    return {
        "engine": "HPP Sovereign Engine v3.0",
        "device": str(engine.device),
        "connected_bodies": {
            bid: {
                "last_seen": time.time() - info["last_seen"],
                "joints_received": len(info.get("joint_positions", []))
            }
            for bid, info in connected_bodies.items()
        },
        "telemetry": {
            "karma": round(engine.hpp_core.resonance_filter.karma.mean().item(), 4),
            "vairagya": round(engine.hpp_core.resonance_filter.vairagya.mean().item(), 4)
        }
    }


# ================================================================
# WEBSOCKET — Real-time Masamune body↔brain streaming
# ================================================================
@app.websocket("/ws/masamune")
async def masamune_websocket(websocket: WebSocket):
    """
    Real-time bidirectional stream between Masamune's Jetson and the brain.
    
    Masamune sends:  {"type": "proprioception", "joints": [...19 floats...]}
                     {"type": "command", "prompt": "..."}
    
    Server sends:    {"type": "kinetic", "joints": [...19 floats...]}
                     {"type": "speech", "text": "..."}
                     {"type": "heartbeat"}
    """
    await websocket.accept()
    body_id = "masamune_ws"
    print(f"[WS] Masamune connected: {body_id}")
    connected_bodies[body_id] = {"last_seen": time.time(), "joint_positions": []}

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            msg_type = msg.get("type", "unknown")

            if msg_type == "proprioception":
                # Store latest body state
                joints = msg.get("joints", [])
                connected_bodies[body_id] = {
                    "last_seen": time.time(),
                    "joint_positions": joints
                }
                # Send heartbeat back
                await websocket.send_text(json.dumps({"type": "heartbeat"}))

            elif msg_type == "command":
                prompt = msg.get("prompt", "")
                proprio = connected_bodies[body_id].get("joint_positions", None)

                # Generate kinetic response
                with torch.no_grad():
                    tokens = engine.enc.encode(prompt)
                    if tokens:
                        token_tensor = torch.tensor(
                            [tokens], dtype=torch.long, device=engine.device
                        )
                        embedded = engine.embedding(token_tensor).permute(1, 0, 2)
                        anchored = engine.anchor.pulse_verification(embedded)
                        thought = engine.university(anchored, domain="synthesis")

                        # Proprioceptive feedback
                        if proprio and len(proprio) == 19:
                            pt = torch.tensor(
                                [proprio], dtype=torch.float32,
                                device=engine.device
                            )
                            thought = thought + engine.proprioception(pt) * 0.3

                        body_output = engine.samurai_body(thought)
                        cmd = engine.samurai_body.to_command_vector(body_output)
                    else:
                        cmd = [0.0] * 19

                # Generate speech
                text_result = engine.pulse(prompt, max_tokens=100, temperature=0.7)

                await websocket.send_text(json.dumps({
                    "type": "kinetic",
                    "joints": cmd,
                    "speech": text_result['response'],
                    "latency_ms": text_result['latency_ms']
                }))

            elif msg_type == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))

    except WebSocketDisconnect:
        print(f"[WS] Masamune disconnected: {body_id}")
        if body_id in connected_bodies:
            del connected_bodies[body_id]


# ================================================================
# STATIC FILES (Dashboard)
# ================================================================
dashboard_dir = os.path.join(os.path.dirname(__file__), 'dashboard')
if os.path.exists(dashboard_dir):
    app.mount("/dashboard", StaticFiles(directory=dashboard_dir, html=True), name="dashboard")


@app.get("/")
def serve_root():
    """Serve a simple status page."""
    return {
        "system": "HPP Sovereign Server",
        "status": "ONLINE",
        "mission": "SOVEREIGN OATH VERIFIED",
        "endpoints": [
            "/api/pulse", "/api/nexus", "/api/kinetic",
            "/api/proprioception", "/api/status", "/ws/masamune"
        ]
    }


# ================================================================
# ENTRY POINT
# ================================================================
if __name__ == "__main__":
    print("\n[SERVER] Starting HPP Sovereign Server on http://0.0.0.0:8000")
    print("[SERVER] Masamune WebSocket: ws://0.0.0.0:8000/ws/masamune")
    print("[SERVER] Dashboard: http://0.0.0.0:8000/dashboard/SOVEREIGN_LIFE_SUPPORT.html")
    uvicorn.run(app, host="0.0.0.0", port=8000)
