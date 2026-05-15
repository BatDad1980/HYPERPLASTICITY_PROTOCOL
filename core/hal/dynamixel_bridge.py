"""
HPP PHASE 16: DYNAMIXEL BRIDGE
The neural-to-physical bridge. Converts SamuraiBodyController joint vectors
into Dynamixel servo commands over RS-485 (or simulated for development).

When `simulated: true` in the YAML config, all servo I/O is mocked in-memory
so the full pipeline can be tested without hardware.
"""
import os
import time
import yaml
import math


class JointState:
    """Current state of a single physical joint."""
    __slots__ = ['name', 'servo_id', 'neural_index', 'min_deg', 'max_deg',
                 'home_deg', 'max_vel', 'commanded_deg', 'actual_deg',
                 'actual_velocity', 'actual_load', 'temperature', 'mode']

    def __init__(self, cfg: dict):
        self.name = cfg['joint']
        self.servo_id = cfg['servo_id']
        self.neural_index = cfg.get('neural_index', 0)
        self.min_deg = cfg.get('min_deg', -180)
        self.max_deg = cfg.get('max_deg', 180)
        self.home_deg = cfg.get('home_deg', 0)
        self.max_vel = cfg.get('max_vel', 60)
        self.mode = cfg.get('mode', 'position_control')
        self.commanded_deg = self.home_deg
        self.actual_deg = self.home_deg
        self.actual_velocity = 0.0
        self.actual_load = 0.0
        self.temperature = 25.0

    def neural_to_degrees(self, neural_value: float) -> float:
        """Convert normalized [-1, 1] neural output to degree value within limits."""
        center = (self.max_deg + self.min_deg) / 2.0
        half_range = (self.max_deg - self.min_deg) / 2.0
        return center + (neural_value * half_range)

    def degrees_to_neural(self) -> float:
        """Convert current actual position back to [-1, 1] for proprioception."""
        center = (self.max_deg + self.min_deg) / 2.0
        half_range = (self.max_deg - self.min_deg) / 2.0
        if half_range == 0:
            return 0.0
        return (self.actual_deg - center) / half_range


class SimulatedServo:
    """Software mock of a Dynamixel servo for development without hardware."""

    def __init__(self, joint: JointState):
        self.joint = joint
        self._target_deg = joint.home_deg

    def write_position(self, target_deg: float):
        self._target_deg = max(self.joint.min_deg, min(self.joint.max_deg, target_deg))

    def step(self, dt: float):
        """Simulate servo movement over a timestep."""
        error = self._target_deg - self.joint.actual_deg
        max_step = self.joint.max_vel * dt
        if abs(error) > max_step:
            self.joint.actual_deg += max_step * (1.0 if error > 0 else -1.0)
        else:
            self.joint.actual_deg = self._target_deg
        self.joint.actual_velocity = error / max(dt, 1e-6)
        self.joint.actual_load = abs(error) * 0.01  # Simulated load
        self.joint.commanded_deg = self._target_deg

    def read_state(self) -> dict:
        return {
            'position': self.joint.actual_deg,
            'velocity': self.joint.actual_velocity,
            'load': self.joint.actual_load,
            'temperature': self.joint.temperature
        }


class DynamixelBridge:
    """
    HPP PHASE 16: THE BRIDGE BETWEEN THOUGHT AND MOTION
    
    Manages all Dynamixel servos on Masamune's chassis.
    Supports both real hardware (via dynamixel_sdk) and simulated mode.
    """

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__), 'config', 'masamune_servo_map.yaml'
            )

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.simulated = self.config['bus'].get('simulated', True)
        self.joints = {}       # name -> JointState
        self.servo_map = {}    # servo_id -> JointState
        self._sim_servos = {}  # servo_id -> SimulatedServo (only in sim mode)
        self._port_handler = None
        self._packet_handler = None
        self._last_step_time = time.perf_counter()

        # Build joint registry from all groups
        for group_name in ['left_arm', 'right_arm', 'stance', 'grip']:
            group = self.config.get(group_name, [])
            for joint_cfg in group:
                joint = JointState(joint_cfg)
                self.joints[joint.name] = joint
                self.servo_map[joint.servo_id] = joint
                if self.simulated:
                    self._sim_servos[joint.servo_id] = SimulatedServo(joint)

        # Safety parameters
        safety = self.config.get('safety', {})
        self.watchdog_timeout = safety.get('watchdog_timeout_ms', 500) / 1000.0
        self.max_acceleration = safety.get('max_acceleration', 100)
        self.torque_limit_pct = safety.get('torque_limit_pct', 80)
        self.temp_shutdown = safety.get('temperature_shutdown', 70)
        self._last_command_time = time.perf_counter()
        self._e_stopped = False

        if self.simulated:
            print("[HAL] SIMULATED MODE — No physical servos connected")
        else:
            self._init_hardware()

        total = len(self.joints)
        print(f"[HAL] Masamune Bridge initialized: {total} joints registered")

    def _init_hardware(self):
        """Initialize real Dynamixel SDK connection."""
        try:
            from dynamixel_sdk import PortHandler, PacketHandler
            bus = self.config['bus']
            self._port_handler = PortHandler(bus['port'])
            self._packet_handler = PacketHandler(bus['protocol'])

            if not self._port_handler.openPort():
                raise IOError(f"Failed to open port: {bus['port']}")
            if not self._port_handler.setBaudRate(bus['baudrate']):
                raise IOError(f"Failed to set baudrate: {bus['baudrate']}")

            print(f"[HAL] Hardware connected: {bus['port']} @ {bus['baudrate']} baud")

            # Enable torque on all servos
            for sid in self.servo_map:
                self._write_register(sid, 64, 1, 1)  # ADDR_TORQUE_ENABLE

        except ImportError:
            print("[HAL] WARNING: dynamixel_sdk not installed — falling back to simulation")
            self.simulated = True
            for sid, joint in self.servo_map.items():
                self._sim_servos[sid] = SimulatedServo(joint)

    def _write_register(self, servo_id, addr, length, value):
        """Write to a Dynamixel register (real hardware only)."""
        if self.simulated or not self._packet_handler:
            return
        if length == 1:
            self._packet_handler.write1ByteTxRx(self._port_handler, servo_id, addr, value)
        elif length == 2:
            self._packet_handler.write2ByteTxRx(self._port_handler, servo_id, addr, value)
        elif length == 4:
            self._packet_handler.write4ByteTxRx(self._port_handler, servo_id, addr, value)

    def _read_register(self, servo_id, addr, length):
        """Read from a Dynamixel register (real hardware only)."""
        if self.simulated or not self._packet_handler:
            return 0
        if length == 1:
            val, _, _ = self._packet_handler.read1ByteTxRx(self._port_handler, servo_id, addr)
        elif length == 2:
            val, _, _ = self._packet_handler.read2ByteTxRx(self._port_handler, servo_id, addr)
        elif length == 4:
            val, _, _ = self._packet_handler.read4ByteTxRx(self._port_handler, servo_id, addr)
        else:
            val = 0
        return val

    # ================================================================
    # PUBLIC API: Called by SamuraiBodyController / MasamuneMain
    # ================================================================

    def command_arms(self, left_arm_neural, right_arm_neural):
        """
        Command both arms from SamuraiBodyController neural output.
        left_arm_neural: list of 7 floats in [-1, 1]
        right_arm_neural: list of 7 floats in [-1, 1]
        """
        if self._e_stopped:
            return

        arm_configs = self.config.get('left_arm', [])
        for i, cfg in enumerate(arm_configs):
            if i < len(left_arm_neural):
                joint = self.joints[cfg['joint']]
                target = joint.neural_to_degrees(left_arm_neural[i])
                self._command_joint(joint, target)

        arm_configs = self.config.get('right_arm', [])
        for i, cfg in enumerate(arm_configs):
            if i < len(right_arm_neural):
                joint = self.joints[cfg['joint']]
                target = joint.neural_to_degrees(right_arm_neural[i])
                self._command_joint(joint, target)

        self._last_command_time = time.perf_counter()

    def command_stance(self, stance_neural):
        """
        Command stance from SamuraiBodyController neural output.
        stance_neural: list of 4 floats in [-1, 1]
        """
        if self._e_stopped:
            return

        stance_configs = self.config.get('stance', [])
        for i, cfg in enumerate(stance_configs):
            if i < len(stance_neural):
                joint = self.joints[cfg['joint']]
                target = joint.neural_to_degrees(stance_neural[i])
                self._command_joint(joint, target)

        self._last_command_time = time.perf_counter()

    def command_grip(self, grip_force: float):
        """
        Command grip from SamuraiBodyController neural output.
        grip_force: float in [0, 1] (sigmoid output)
        """
        if self._e_stopped:
            return

        grip_configs = self.config.get('grip', [])
        if grip_configs:
            cfg = grip_configs[0]
            joint = self.joints[cfg['joint']]
            max_t = cfg.get('max_torque', 1.5)
            joint.commanded_deg = grip_force * max_t
            if self.simulated:
                joint.actual_load = grip_force * max_t

        self._last_command_time = time.perf_counter()

    def step(self, dt: float = None):
        """
        Advance the simulation by one timestep.
        In hardware mode, reads actual servo positions.
        """
        now = time.perf_counter()
        if dt is None:
            dt = now - self._last_step_time
        self._last_step_time = now

        # Watchdog: if brain hasn't commanded in too long, safe park
        if (now - self._last_command_time) > self.watchdog_timeout:
            if not self._e_stopped:
                print("[HAL] WATCHDOG TIMEOUT — Brain unresponsive. Safe parking...")
                self.safe_park()

        if self.simulated:
            for sim in self._sim_servos.values():
                sim.step(dt)
        else:
            self._read_all_hardware()

    def read_proprioception(self) -> list:
        """
        Read the full 19-element proprioceptive state vector.
        Returns: [14 limb positions, 4 stance positions, 1 grip force]
        All normalized to [-1, 1] (or [0, 1] for grip).
        This feeds directly into KineticProprioception.forward().
        """
        state = []

        # Left arm (7)
        for cfg in self.config.get('left_arm', []):
            joint = self.joints[cfg['joint']]
            state.append(joint.degrees_to_neural())

        # Right arm (7)
        for cfg in self.config.get('right_arm', []):
            joint = self.joints[cfg['joint']]
            state.append(joint.degrees_to_neural())

        # Stance (4)
        for cfg in self.config.get('stance', []):
            joint = self.joints[cfg['joint']]
            state.append(joint.degrees_to_neural())

        # Grip (1)
        grip_configs = self.config.get('grip', [])
        if grip_configs:
            joint = self.joints[grip_configs[0]['joint']]
            max_t = grip_configs[0].get('max_torque', 1.5)
            state.append(joint.actual_load / max(max_t, 1e-6))
        else:
            state.append(0.0)

        return state

    def safe_park(self):
        """Emergency: move all joints to home position."""
        print("[HAL] !!! SAFE PARK ENGAGED — ALL JOINTS TO HOME !!!")
        for name, joint in self.joints.items():
            if joint.mode != 'current_control':
                self._command_joint(joint, joint.home_deg)
            else:
                joint.commanded_deg = 0.0
        self._e_stopped = True

    def reset_e_stop(self):
        """Clear the e-stop flag after manual verification."""
        print("[HAL] E-Stop cleared. Masamune re-armed.")
        self._e_stopped = False
        self._last_command_time = time.perf_counter()

    def get_status_report(self) -> dict:
        """Full diagnostic report for telemetry display."""
        joint_report = {}
        for name, joint in self.joints.items():
            joint_report[name] = {
                'commanded': round(joint.commanded_deg, 2),
                'actual': round(joint.actual_deg, 2),
                'load': round(joint.actual_load, 3),
                'temp': round(joint.temperature, 1)
            }
        return {
            'e_stopped': self._e_stopped,
            'simulated': self.simulated,
            'total_joints': len(self.joints),
            'joints': joint_report
        }

    # ================================================================
    # INTERNAL
    # ================================================================

    def _command_joint(self, joint: JointState, target_deg: float):
        """Send a position command to a single joint with safety clamping."""
        # Clamp to joint limits
        target_deg = max(joint.min_deg, min(joint.max_deg, target_deg))
        joint.commanded_deg = target_deg

        if self.simulated:
            self._sim_servos[joint.servo_id].write_position(target_deg)
        else:
            # Dynamixel XM series: Goal Position register
            # Convert degrees to raw position (0-4095 for 0-360°)
            raw_pos = int((target_deg + 180.0) / 360.0 * 4095)
            raw_pos = max(0, min(4095, raw_pos))
            self._write_register(joint.servo_id, 116, 4, raw_pos)

    def _read_all_hardware(self):
        """Read actual positions from all Dynamixel servos."""
        for sid, joint in self.servo_map.items():
            raw_pos = self._read_register(sid, 132, 4)  # Present Position
            joint.actual_deg = (raw_pos / 4095.0 * 360.0) - 180.0
            raw_vel = self._read_register(sid, 128, 4)  # Present Velocity
            joint.actual_velocity = raw_vel * 0.229  # RPM to deg/s approx
            raw_load = self._read_register(sid, 126, 2)  # Present Load
            joint.actual_load = raw_load / 1000.0
            raw_temp = self._read_register(sid, 146, 1)  # Present Temperature
            joint.temperature = float(raw_temp)

            # Thermal protection
            if joint.temperature > self.temp_shutdown:
                print(f"[HAL] THERMAL SHUTDOWN on {joint.name}: {joint.temperature}°C")
                self.safe_park()

    def shutdown(self):
        """Graceful shutdown: park all servos and close port."""
        print("[HAL] Shutting down Masamune bridge...")
        self.safe_park()
        # Let servos reach home
        for _ in range(50):
            self.step(0.02)
            time.sleep(0.02)
        if self._port_handler:
            # Disable torque
            for sid in self.servo_map:
                self._write_register(sid, 64, 1, 0)
            self._port_handler.closePort()
        print("[HAL] Masamune bridge shutdown complete.")
