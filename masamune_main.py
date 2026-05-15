"""
===============================================================================
              MASAMUNE MAIN — HPP SOVEREIGN KINETIC ORCHESTRATOR
===============================================================================
Phase 16: The entry point for the fully embodied Masamune samurai chassis.

ARCHITECTURE:
    BRAIN:  Runs on the shop server (workbench PC with GPU)
    BODY:   Runs on Jetson Orin NX (this script) on Masamune's chassis
    LINK:   WebSocket over Wi-Fi (with repeaters for outdoor coverage)

THREADS:
    BODY THREAD  (50 Hz)  — Local servo control, interpolation, safety
    NET THREAD   (5 Hz)   — Sends proprioception, receives brain commands
    MAIN THREAD           — User I/O, telemetry, shutdown handling

AUTONOMOUS FALLBACK:
    When disconnected from the shop server (e.g., outside the building),
    Masamune enters AUTONOMOUS mode:
    - Maintains last commanded stance
    - Safety governor remains fully active
    - Soft-touch protocol stays armed
    - Keeps trying to reconnect every 3 seconds
    - Can perform basic pre-programmed stances locally

Usage:
    python masamune_main.py                                 # Simulated, no server
    python masamune_main.py --server ws://192.168.1.100:8000/ws/masamune
    python masamune_main.py --server ws://192.168.1.100:8000/ws/masamune --live
===============================================================================
"""
import os
import sys
import time
import torch
import threading
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.hal.dynamixel_bridge import DynamixelBridge
from core.hal.safety_governor import SafetyGovernor
from core.hal.servo_interpolator import ServoInterpolator
from core.hal.network_bridge import MasamuneNetworkBridge


# ================================================================
# PRE-PROGRAMMED STANCES (Available offline / autonomous mode)
# ================================================================
STANCES = {
    "home": [0.0] * 19,
    "guard": [
        # Left arm: shield position
        0.3, 0.5, 0.0, 0.7, 0.0, 0.2, 0.0,
        # Right arm: blade ready
        -0.2, -0.3, 0.0, 0.5, 0.0, -0.1, 0.0,
        # Stance: rooted, slightly forward
        0.0, 0.1, 0.0, 0.0,
        # Grip: firm
        0.7
    ],
    "rest": [
        # Arms relaxed at sides
        0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.3, 0.0, 0.0, 0.0,
        # Stance: neutral, slightly lowered
        0.0, 0.0, 0.0, -0.2,
        # Grip: released
        0.0
    ],
    "bow": [
        # Arms at sides, formal
        0.0, 0.1, 0.0, 0.1, 0.0, 0.0, 0.0,
        0.0, -0.1, 0.0, 0.1, 0.0, 0.0, 0.0,
        # Stance: forward lean (bow)
        0.0, 0.4, 0.0, -0.1,
        # Grip: released
        0.0
    ],
}


class MasamuneOrchestrator:
    """
    The sovereign conductor. Runs on Masamune's Jetson.
    Coordinates the local body (servos, sensors, safety) with the
    remote brain (shop server) over the network.
    """

    def __init__(self, server_url: str = None, simulated: bool = True,
                 body_hz: float = 50.0, net_hz: float = 5.0):
        self.body_hz = body_hz
        self.net_hz = net_hz
        self._running = False
        self._mode = "DISCONNECTED"  # CONNECTED, DISCONNECTED, AUTONOMOUS

        # ─── Display ───────────────────────────────────────────────
        print("\n" + "=" * 70)
        print("           ⚔️  MASAMUNE KINETIC ORCHESTRATOR  ⚔️")
        print("=" * 70)
        print(f"[INIT] Hardware: {'SIMULATED' if simulated else 'LIVE'}")
        print(f"[INIT] Body loop: {body_hz} Hz")
        print(f"[INIT] Network: {server_url or 'STANDALONE (no server)'}")
        print("=" * 70)

        # ─── HAL Layer (runs locally on Jetson) ────────────────────
        config_path = os.path.join(
            os.path.dirname(__file__), 'core', 'hal', 'config',
            'masamune_servo_map.yaml'
        )
        self.bridge = DynamixelBridge(config_path)
        if not simulated:
            self.bridge.simulated = False

        self.governor = SafetyGovernor(self.bridge)
        self.interpolator = ServoInterpolator(num_joints=19, smoothing=0.85)

        # ─── Network Bridge (connects to shop server) ─────────────
        self.network = None
        if server_url:
            http_url = server_url.replace("ws://", "http://").replace("/ws/masamune", "")
            self.network = MasamuneNetworkBridge(
                server_url=server_url,
                http_url=http_url
            )

        # ─── State ────────────────────────────────────────────────
        self._current_command = ""
        self._latest_speech = ""
        self._command_lock = threading.Lock()
        self._body_cycle_count = 0
        self._net_cycle_count = 0
        self._reconnect_interval = 3.0
        self._last_reconnect_attempt = 0

        print("\n[INIT] Masamune is ready. Soft-Touch Protocol armed.")
        print("=" * 70)

    # ================================================================
    # BODY THREAD — Fast local servo control (50 Hz)
    # ================================================================
    def _body_loop(self):
        """Runs locally on the Jetson. Never depends on network."""
        interval = 1.0 / self.body_hz

        while self._running:
            start = time.perf_counter()

            try:
                # 1. Get interpolated commands
                left, right, stance, grip = self.interpolator.get_split_commands()

                # 2. Safety filter (soft-touch, acceleration, thermal)
                safe_left, safe_right, safe_stance, safe_grip = (
                    self.governor.filter_command(left, right, stance, grip)
                )

                # 3. Command servos
                self.bridge.command_arms(safe_left, safe_right)
                self.bridge.command_stance(safe_stance)
                self.bridge.command_grip(safe_grip)

                # 4. Step simulation / read hardware
                self.bridge.step()

                self._body_cycle_count += 1

            except Exception as e:
                print(f"[BODY] Error: {e}")

            elapsed = time.perf_counter() - start
            sleep_time = interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    # ================================================================
    # NETWORK THREAD — Server communication (5 Hz)
    # ================================================================
    def _net_loop(self):
        """
        Handles communication with the shop server.
        If disconnected, keeps trying to reconnect while Masamune
        operates autonomously with local safety.
        """
        interval = 1.0 / self.net_hz

        while self._running:
            start = time.perf_counter()

            if self.network is None:
                time.sleep(interval)
                continue

            try:
                if not self.network.is_connected:
                    # ─── AUTONOMOUS MODE ───────────────────────────
                    self._mode = "AUTONOMOUS"
                    now = time.perf_counter()

                    if now - self._last_reconnect_attempt > self._reconnect_interval:
                        self._last_reconnect_attempt = now
                        if self.network.connect():
                            self._mode = "CONNECTED"
                            print("[NET] Reconnected to shop server!")
                        # Don't spam — exponential backoff up to 30s
                        self._reconnect_interval = min(
                            self._reconnect_interval * 1.5, 30.0
                        )
                else:
                    # ─── CONNECTED MODE ────────────────────────────
                    self._mode = "CONNECTED"
                    self._reconnect_interval = 3.0  # Reset backoff

                    # Send proprioception to server
                    proprio = self.bridge.read_proprioception()
                    self.network.send_proprioception(proprio)

                    # If there's a pending command, send it to server brain
                    with self._command_lock:
                        cmd = self._current_command
                        self._current_command = ""

                    if cmd:
                        result = self.network.request_kinetic(cmd)
                        if result:
                            joints = result.get("joints", [0.0] * 19)
                            self.interpolator.set_target(joints)
                            self._latest_speech = result.get("speech", "")

                self._net_cycle_count += 1

            except Exception as e:
                print(f"[NET] Error: {e}")
                self._mode = "AUTONOMOUS"

            elapsed = time.perf_counter() - start
            sleep_time = interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    # ================================================================
    # PUBLIC API
    # ================================================================

    def start(self):
        """Start body and network threads."""
        self._running = True

        # Try initial connection
        if self.network:
            if self.network.connect():
                self._mode = "CONNECTED"
            else:
                self._mode = "AUTONOMOUS"
                print("[MASAMUNE] No server connection — starting in AUTONOMOUS mode")

        self._body_thread = threading.Thread(
            target=self._body_loop, daemon=True, name="MasamuneBody"
        )
        self._net_thread = threading.Thread(
            target=self._net_loop, daemon=True, name="MasamuneNet"
        )

        self._body_thread.start()
        self._net_thread.start()
        print(f"[MASAMUNE] Threads active. Mode: {self._mode}")

    def stop(self):
        """Graceful shutdown."""
        print("\n[MASAMUNE] Initiating shutdown sequence...")
        self._running = False
        time.sleep(0.2)
        if self.network:
            self.network.disconnect()
        self.bridge.shutdown()
        print("[MASAMUNE] Shutdown complete. Masamune at rest.")

    def command(self, prompt: str):
        """Send a command (routed to server if connected, local if not)."""
        if self._mode == "CONNECTED":
            with self._command_lock:
                self._current_command = prompt
        else:
            # Autonomous: check for local stance commands
            lower = prompt.strip().lower()
            if lower in STANCES:
                self.interpolator.set_target(STANCES[lower])
                self._latest_speech = f"[LOCAL] Executing stance: {lower}"
            else:
                self._latest_speech = (
                    "[AUTONOMOUS] Server unreachable. "
                    "Local stances available: " + ", ".join(STANCES.keys())
                )

    def set_stance(self, stance_name: str):
        """Directly set a pre-programmed stance (works offline)."""
        if stance_name in STANCES:
            self.interpolator.set_target(STANCES[stance_name])
            return True
        return False

    def get_telemetry(self) -> dict:
        body_status = self.bridge.get_status_report()
        safety_status = self.governor.get_report()

        return {
            "mode": self._mode,
            "body_cycles": self._body_cycle_count,
            "net_cycles": self._net_cycle_count,
            "latest_speech": self._latest_speech,
            "body": body_status,
            "safety": safety_status
        }


# ================================================================
# INTERACTIVE TERMINAL
# ================================================================
def run_interactive(server_url: str = None, simulated: bool = True):
    """Run Masamune in interactive terminal mode."""
    masamune = MasamuneOrchestrator(
        server_url=server_url, simulated=simulated
    )
    masamune.start()

    print("\n" + "-" * 70)
    print("  MASAMUNE SOVEREIGN TERMINAL")
    print("  Commands:")
    print("    <text>     — Send to brain (server) for kinetic response")
    print("    guard      — Local pre-programmed guard stance")
    print("    rest       — Local rest position")
    print("    bow        — Formal bow stance")
    print("    home       — Return all joints to home")
    print("    status     — System telemetry")
    print("    park       — Emergency safe park")
    print("    reset      — Clear E-stop")
    print("    exit       — Shutdown")
    print("-" * 70)

    try:
        while True:
            try:
                mode_tag = masamune._mode[:4]
                prompt = input(f"\n[{mode_tag}] ARCHITECT: ")
            except EOFError:
                break

            if not prompt.strip():
                continue

            cmd = prompt.strip().lower()

            if cmd in ('exit', 'quit', 'shutdown'):
                break
            elif cmd == 'status':
                tel = masamune.get_telemetry()
                print(f"\n[TELEMETRY]")
                print(f"  Mode:          {tel['mode']}")
                print(f"  Body cycles:   {tel['body_cycles']}")
                print(f"  Net cycles:    {tel['net_cycles']}")
                print(f"  E-Stopped:     {tel['body']['e_stopped']}")
                print(f"  Simulated:     {tel['body']['simulated']}")
                st = tel['safety'].get('soft_touch', {})
                print(f"  Contact:       {st.get('contact_detected', False)}")
                print(f"  Speed:         {st.get('effective_speed_pct', 0)}%")
                print(f"  Violations:    {tel['safety']['violations']}")
            elif cmd == 'park':
                masamune.bridge.safe_park()
            elif cmd == 'reset':
                masamune.bridge.reset_e_stop()
            elif cmd in STANCES:
                masamune.set_stance(cmd)
                print(f"[MASAMUNE] Stance: {cmd}")
            else:
                masamune.command(prompt)
                print("[Thinking...]")
                time.sleep(2.5)
                print(f"\n[HEPP]: {masamune._latest_speech}")

    except KeyboardInterrupt:
        pass

    masamune.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Masamune Kinetic Orchestrator")
    parser.add_argument('--server', type=str, default=None,
                        help='Shop server WebSocket URL '
                             '(e.g., ws://192.168.1.100:8000/ws/masamune)')
    parser.add_argument('--live', action='store_true',
                        help='Run with real Dynamixel hardware')
    args = parser.parse_args()

    run_interactive(server_url=args.server, simulated=not args.live)
