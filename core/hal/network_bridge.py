"""
===============================================================================
       MASAMUNE NETWORK BRIDGE — Jetson → Shop Server Connection
===============================================================================
Runs on Masamune's Jetson. Connects to the shop workbench server over
WebSocket for complex reasoning, while handling real-time servo control locally.

Architecture:
    [Shop Server]  ←──WebSocket──→  [Jetson / NetworkBridge]
         ↓                                    ↓
    HPP Brain (GPU)                   HAL + Servos (local)
    Speech Generation                 Safety Governor (local)
    Agency Decisions                  Interpolation (local)
                                      Sensors (local)

The Jetson handles everything that needs <20ms latency (servo control).
The server handles everything that needs deep thinking (inference).
===============================================================================
"""
import os
import sys
import json
import time
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class MasamuneNetworkBridge:
    """
    Network client that runs on Masamune's Jetson.
    Connects to the shop server for brain access while maintaining
    local real-time control over the body.
    """

    def __init__(self, server_url: str = "ws://192.168.1.100:8000/ws/masamune",
                 http_url: str = "http://192.168.1.100:8000"):
        self.server_url = server_url
        self.http_url = http_url
        self._ws = None
        self._connected = False
        self._running = False
        self._ws_lock = threading.Lock()

        # Latest responses from server
        self.latest_joint_commands = [0.0] * 19
        self.latest_speech = ""
        self.latest_latency = 0.0

        # Callbacks
        self._on_kinetic_callback = None
        self._on_speech_callback = None

        print(f"[NET] Bridge initialized → {server_url}")

    def connect(self):
        """Establish WebSocket connection to shop server."""
        try:
            import websocket
            self._ws = websocket.WebSocket()
            self._ws.connect(self.server_url, timeout=5)
            self._connected = True
            print(f"[NET] Connected to Sovereign Server")
            return True
        except ImportError:
            print("[NET] websocket-client not installed. Using HTTP fallback.")
            self._connected = False
            return False
        except Exception as e:
            print(f"[NET] Connection failed: {e}")
            self._connected = False
            return False

    def disconnect(self):
        """Close the WebSocket connection."""
        if self._ws:
            try:
                self._ws.close()
            except Exception:
                pass
        self._connected = False
        print("[NET] Disconnected from server.")

    @property
    def is_connected(self):
        return self._connected

    # ================================================================
    # SEND TO SERVER
    # ================================================================

    def send_proprioception(self, joint_positions: list):
        """
        Send current body sensor state to the server.
        Called by the body loop at a lower frequency (e.g., 5 Hz).
        """
        if not self._connected:
            return False

        msg = json.dumps({
            "type": "proprioception",
            "joints": joint_positions
        })

        try:
            with self._ws_lock:
                self._ws.send(msg)
                response = self._ws.recv()
            return True
        except Exception as e:
            print(f"[NET] Proprioception send failed: {e}")
            self._connected = False
            return False

    def request_kinetic(self, prompt: str):
        """
        Ask the server brain to generate body commands for a prompt.
        Returns joint commands and speech response.
        """
        if not self._connected:
            return self._http_fallback_kinetic(prompt)

        msg = json.dumps({
            "type": "command",
            "prompt": prompt
        })

        try:
            with self._ws_lock:
                self._ws.send(msg)
                response = self._ws.recv()

            data = json.loads(response)

            if data.get("type") == "kinetic":
                self.latest_joint_commands = data.get("joints", [0.0] * 19)
                self.latest_speech = data.get("speech", "")
                self.latest_latency = data.get("latency_ms", 0)
                return {
                    "joints": self.latest_joint_commands,
                    "speech": self.latest_speech,
                    "latency_ms": self.latest_latency
                }

        except Exception as e:
            print(f"[NET] Kinetic request failed: {e}")
            self._connected = False
            return self._http_fallback_kinetic(prompt)

        return None

    def _http_fallback_kinetic(self, prompt: str):
        """HTTP fallback when WebSocket is unavailable."""
        try:
            import urllib.request
            import urllib.error

            url = f"{self.http_url}/api/kinetic"
            payload = json.dumps({
                "prompt": prompt,
                "proprioception": self.latest_joint_commands
            }).encode('utf-8')

            req = urllib.request.Request(
                url, data=payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())

            self.latest_joint_commands = data.get("joint_commands", [0.0] * 19)
            self.latest_speech = data.get("verbal_response", "")
            self.latest_latency = data.get("latency_ms", 0)

            return {
                "joints": self.latest_joint_commands,
                "speech": self.latest_speech,
                "latency_ms": self.latest_latency
            }
        except Exception as e:
            print(f"[NET] HTTP fallback failed: {e}")
            return None

    # ================================================================
    # BACKGROUND LISTENER (for server-initiated commands)
    # ================================================================

    def start_listener(self):
        """Start background thread that listens for server-pushed commands."""
        self._running = True
        self._listener_thread = threading.Thread(
            target=self._listen_loop, daemon=True, name="NetListener"
        )
        self._listener_thread.start()

    def stop_listener(self):
        self._running = False

    def _listen_loop(self):
        """Background listener for server pushes."""
        while self._running:
            if not self._connected:
                time.sleep(1.0)
                # Try to reconnect
                self.connect()
                continue

            try:
                with self._ws_lock:
                    self._ws.settimeout(0.1)
                    try:
                        data = self._ws.recv()
                        msg = json.loads(data)

                        if msg.get("type") == "kinetic":
                            self.latest_joint_commands = msg.get("joints", [0.0] * 19)
                            self.latest_speech = msg.get("speech", "")
                            if self._on_kinetic_callback:
                                self._on_kinetic_callback(self.latest_joint_commands)
                            if self._on_speech_callback and self.latest_speech:
                                self._on_speech_callback(self.latest_speech)
                    except Exception:
                        pass  # Timeout — no data, that's fine

            except Exception:
                time.sleep(0.5)

    def on_kinetic(self, callback):
        """Register callback for when server sends kinetic commands."""
        self._on_kinetic_callback = callback

    def on_speech(self, callback):
        """Register callback for when server sends speech."""
        self._on_speech_callback = callback
