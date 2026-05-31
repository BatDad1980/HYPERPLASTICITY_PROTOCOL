import json
import time
from aegis_core import AegisCore

class AegisAPI:
    """
    Project Aegis: Commercial API Stream.
    A lightweight wrapper that allows enterprise buyers to pull the 
    kinetic data into their own dashboards, heat-maps, or safety systems.
    """
    def __init__(self, camera_id):
        self.engine = AegisCore(camera_id=camera_id)
        
    def stream_data(self, duration_seconds=5):
        """Simulates an active HTTP/WebSocket stream to a buyer's server."""
        print(f"[{self.engine.camera_id}] INIT: Aegis Vision Stream Active.")
        print(f"[{self.engine.camera_id}] SECURITY: Zero-Video Mode. Privacy Compliant.\n")
        
        end_time = time.time() + duration_seconds
        
        while time.time() < end_time:
            data = self.engine.process_frame()
            # In a real environment, this would be a Flask/FastAPI response or a WebSocket push
            self._transmit(data)
            time.sleep(1.0) # 1 FPS simulation
            
        print(f"\n[{self.engine.camera_id}] STREAM CLOSED.")
            
    def _transmit(self, payload):
        """Prints the JSON string exactly as a buyer's server would receive it."""
        print(json.dumps(payload, indent=2))
