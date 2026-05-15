from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from hpp_sovereign_engine import HPP_SovereignEngine

app = FastAPI(title="Hyper-Plasticity Protocol V3.0 Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = HPP_SovereignEngine(max_context=512)

class PulseRequest(BaseModel):
    input_text: str
    pitch: float = 200.0
    emotion: str = "neutral"

@app.post("/api/pulse")
def api_pulse(req: PulseRequest):
    try:
        result = engine.pulse(
            input_text=req.input_text,
            pitch=req.pitch,
            emotion=req.emotion,
            task_type="general"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Ensure public directory exists
os.makedirs("public", exist_ok=True)

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/")
def serve_dashboard():
    return FileResponse("public/index.html")

if __name__ == "__main__":
    print("[+] Starting Sentinel Dashboard on port 8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
