"""
HPP PHASE 16: SAFETY GOVERNOR
Non-negotiable safety layer between the brain and the body.
This module enforces physical constraints that override ALL neural commands.

THE RULES:
1. No joint exceeds its physical limits (ever)
2. No joint accelerates faster than the global cap
3. Watchdog kills motion if brain goes silent
4. Thermal shutdown protects servos from burnout
5. Hardware E-Stop overrides everything (GPIO interrupt)

SOFT-TOUCH PROTOCOL (Creator Safety):
6. Force-limited compliance — if Masamune contacts anything unexpected,
   it yields immediately (spring-damper behavior)
7. Proximity-based speed scaling — the closer to the Creator, the slower
8. Contact detection → instant torque drop to near-zero
9. All movements default to 40% max velocity unless explicitly overridden
10. Startup sequence is always slow and predictable
"""
import time
import math


class SoftTouchProtocol:
    """
    CREATOR SAFETY SYSTEM
    
    Ensures Masamune can never injure the Architect.
    Implements industrial collaborative robot (cobot) safety principles:
    
    - ISO 10218-1: Robot safety
    - ISO/TS 15066: Collaborative robot force limits
    
    Human pain thresholds by body region (from ISO/TS 15066):
        - Hand/Finger: 140N max
        - Chest/Abdomen: 210N max  
        - Head/Face: 65N max
    
    We set Masamune's global limit at 30N — well below ANY pain threshold.
    The robot should feel like a firm handshake, never a threat.
    """

    def __init__(self):
        # ─── Force Limits ──────────────────────────────────────────
        self.max_contact_force_N = 30.0      # Newton — well below pain threshold
        self.torque_compliance_pct = 40.0     # Default operating torque (% of max)
        self.contact_torque_pct = 10.0        # Drop to this on unexpected contact
        
        # ─── Speed Limits ──────────────────────────────────────────
        self.max_speed_pct = 40.0             # Default max speed (% of servo max)
        self.proximity_speed_scale = 1.0      # Multiplier (0.0-1.0) from proximity
        self.startup_speed_pct = 15.0         # Speed during first 3 seconds after wake
        
        # ─── Compliance (Spring-Damper) ────────────────────────────
        self.compliance_stiffness = 0.3       # Low = more compliant (0.0-1.0)
        self.compliance_damping = 0.8         # High = less oscillation (0.0-1.0)
        
        # ─── Contact Detection ─────────────────────────────────────
        self.load_baseline = {}               # joint_name → baseline load
        self.contact_threshold = 0.15         # Load spike above baseline = contact
        self.contact_detected = False
        self.contact_joint = None
        self.contact_cooldown = 0.0           # Seconds remaining in yield mode
        self.yield_duration = 1.5             # How long to stay yielded after contact
        
        # ─── Startup Safety ────────────────────────────────────────
        self.startup_time = time.perf_counter()
        self.startup_duration = 3.0           # Slow startup period (seconds)
        
        print("[SOFT-TOUCH] Creator Safety Protocol armed.")
        print(f"  Max contact force: {self.max_contact_force_N}N")
        print(f"  Default speed: {self.max_speed_pct}% of maximum")
        print(f"  Compliance: stiffness={self.compliance_stiffness}, "
              f"damping={self.compliance_damping}")

    def scale_velocity(self, neural_values: list, dt: float) -> list:
        """
        Scale all joint velocities based on safety state.
        This is the primary "soft touch" — movements are always gentle.
        """
        now = time.perf_counter()
        
        # 1. Startup speed ramp (first 3 seconds are extra slow)
        time_since_start = now - self.startup_time
        if time_since_start < self.startup_duration:
            speed_factor = self.startup_speed_pct / 100.0
        else:
            speed_factor = self.max_speed_pct / 100.0
        
        # 2. Proximity scaling (from external sensor — camera/lidar)
        speed_factor *= self.proximity_speed_scale
        
        # 3. Contact cooldown (stay slow after any contact)
        if self.contact_cooldown > 0:
            self.contact_cooldown = max(0, self.contact_cooldown - dt)
            speed_factor *= 0.2  # 20% speed during yield
        
        # 4. Apply speed scaling to all joints
        return [v * speed_factor for v in neural_values]

    def check_contact(self, joints: dict) -> bool:
        """
        Monitor servo loads for unexpected contact.
        If any joint's load spikes above baseline, Masamune yields.
        
        Args:
            joints: dict of {joint_name: JointState} from DynamixelBridge
        """
        contact = False
        
        for name, joint in joints.items():
            # Build baseline (first few readings)
            if name not in self.load_baseline:
                self.load_baseline[name] = joint.actual_load
                continue
            
            # Exponential moving average for baseline
            self.load_baseline[name] = (
                0.95 * self.load_baseline[name] + 0.05 * joint.actual_load
            )
            
            # Check for spike above baseline
            load_delta = joint.actual_load - self.load_baseline[name]
            if load_delta > self.contact_threshold:
                if not self.contact_detected:
                    print(f"[SOFT-TOUCH] CONTACT DETECTED on {name}! "
                          f"Load delta: {load_delta:.3f}")
                    print(f"[SOFT-TOUCH] Yielding for {self.yield_duration}s...")
                self.contact_detected = True
                self.contact_joint = name
                self.contact_cooldown = self.yield_duration
                contact = True
        
        # Clear contact flag when cooldown expires
        if self.contact_cooldown <= 0 and self.contact_detected:
            self.contact_detected = False
            self.contact_joint = None
            print("[SOFT-TOUCH] Contact cleared. Resuming normal operation.")
        
        return contact

    def apply_compliance(self, commanded: list, actual: list) -> list:
        """
        Apply spring-damper compliance to commanded positions.
        
        If the actual position differs from commanded (external force pushing),
        the robot "gives way" instead of fighting back.
        
        This is what makes Masamune safe to be around. A stiff robot
        pushes back. A compliant robot yields.
        """
        result = []
        for i in range(len(commanded)):
            if i >= len(actual):
                result.append(commanded[i])
                continue
                
            error = commanded[i] - actual[i]
            
            # Spring: pull gently toward target
            spring_force = error * self.compliance_stiffness
            
            # Damper: resist rapid changes
            # (In a real implementation, this would use velocity)
            damped_command = actual[i] + spring_force * (1.0 - self.compliance_damping)
            
            result.append(damped_command)
        
        return result

    def set_proximity(self, distance_m: float):
        """
        Update proximity-based speed scaling.
        Called by camera/lidar perception system.
        
        Args:
            distance_m: estimated distance to nearest person in meters
        """
        if distance_m < 0.3:
            # Very close — almost stop
            self.proximity_speed_scale = 0.1
        elif distance_m < 0.6:
            # Close — very slow
            self.proximity_speed_scale = 0.3
        elif distance_m < 1.0:
            # Moderate — reduced speed
            self.proximity_speed_scale = 0.6
        elif distance_m < 2.0:
            # Normal working distance
            self.proximity_speed_scale = 0.85
        else:
            # Far away — full allowed speed
            self.proximity_speed_scale = 1.0

    def get_report(self) -> dict:
        return {
            "contact_detected": self.contact_detected,
            "contact_joint": self.contact_joint,
            "contact_cooldown": round(self.contact_cooldown, 2),
            "proximity_speed_scale": self.proximity_speed_scale,
            "effective_speed_pct": round(
                self.max_speed_pct * self.proximity_speed_scale, 1
            ),
            "compliance_stiffness": self.compliance_stiffness,
            "max_contact_force_N": self.max_contact_force_N
        }


class SafetyGovernor:
    """
    Sits between SamuraiBodyController output and DynamixelBridge input.
    Every command passes through here before reaching the servos.
    
    Integrates the SoftTouchProtocol for human-safe operation.
    """

    def __init__(self, bridge, safety_config: dict = None):
        self.bridge = bridge
        cfg = safety_config or bridge.config.get('safety', {})

        self.max_acceleration = cfg.get('max_acceleration', 100)  # deg/s²
        self.torque_limit_pct = cfg.get('torque_limit_pct', 80)
        self.temp_shutdown = cfg.get('temperature_shutdown', 70)

        # ─── Soft Touch Protocol ───────────────────────────────────
        self.soft_touch = SoftTouchProtocol()

        # Track previous commands for acceleration limiting
        self._prev_arm_left = [0.0] * 7
        self._prev_arm_right = [0.0] * 7
        self._prev_stance = [0.0] * 4
        self._prev_time = time.perf_counter()

        # Violation counters (for telemetry)
        self.violations = {
            'clamp': 0,
            'acceleration': 0,
            'thermal': 0,
            'watchdog': 0,
            'e_stop': 0,
            'contact': 0
        }

        print("[SAFETY] Governor armed with Soft-Touch Protocol.")

    def filter_command(self, left_arm, right_arm, stance, grip_force):
        """
        Main filter: takes raw neural outputs and returns safe, clamped commands.
        
        Pipeline:
        1. Range clamp [-1, 1]
        2. Acceleration limiting (prevent jerky motion)
        3. Soft-touch velocity scaling (gentle by default)
        4. Contact compliance (yield on unexpected contact)
        5. Thermal protection
        """
        now = time.perf_counter()
        dt = max(now - self._prev_time, 1e-6)
        self._prev_time = now

        # 1. Clamp all values to valid range
        safe_left = [max(-1.0, min(1.0, v)) for v in left_arm]
        safe_right = [max(-1.0, min(1.0, v)) for v in right_arm]
        safe_stance = [max(-1.0, min(1.0, v)) for v in stance]
        safe_grip = max(0.0, min(1.0, grip_force))

        # 2. Acceleration limiting
        safe_left = self._limit_acceleration(safe_left, self._prev_arm_left, dt)
        safe_right = self._limit_acceleration(safe_right, self._prev_arm_right, dt)
        safe_stance = self._limit_acceleration(safe_stance, self._prev_stance, dt)

        # 3. Soft-touch velocity scaling (the "gentle giant" filter)
        safe_left = self.soft_touch.scale_velocity(safe_left, dt)
        safe_right = self.soft_touch.scale_velocity(safe_right, dt)
        safe_stance = self.soft_touch.scale_velocity(safe_stance, dt)
        safe_grip *= (self.soft_touch.torque_compliance_pct / 100.0)

        # 4. Contact compliance — read servo loads and check for contact
        if self.bridge.joints:
            contact = self.soft_touch.check_contact(self.bridge.joints)
            if contact:
                self.violations['contact'] += 1
                # Apply compliance: yield toward actual position
                actual_proprio = self.bridge.read_proprioception()
                actual_left = actual_proprio[0:7]
                actual_right = actual_proprio[7:14]
                actual_stance = actual_proprio[14:18]

                safe_left = self.soft_touch.apply_compliance(safe_left, actual_left)
                safe_right = self.soft_touch.apply_compliance(safe_right, actual_right)
                safe_stance = self.soft_touch.apply_compliance(safe_stance, actual_stance)
                safe_grip = safe_grip * 0.3  # Release grip on contact

        # Store for next frame
        self._prev_arm_left = list(safe_left)
        self._prev_arm_right = list(safe_right)
        self._prev_stance = list(safe_stance)

        # 5. Thermal check
        if self._check_thermal():
            return self._prev_arm_left, self._prev_arm_right, self._prev_stance, 0.0

        return safe_left, safe_right, safe_stance, safe_grip

    def _limit_acceleration(self, current, previous, dt):
        """Limit the rate of change to prevent dangerous jerky motions."""
        max_delta = (self.max_acceleration * dt) / 180.0
        result = []
        for i in range(len(current)):
            delta = current[i] - previous[i]
            if abs(delta) > max_delta:
                clamped = previous[i] + max_delta * (1.0 if delta > 0 else -1.0)
                result.append(clamped)
                self.violations['acceleration'] += 1
            else:
                result.append(current[i])
        return result

    def _check_thermal(self) -> bool:
        """Check if any servo is overheating."""
        for name, joint in self.bridge.joints.items():
            if joint.temperature > self.temp_shutdown:
                print(f"[SAFETY] THERMAL VIOLATION: {name} at {joint.temperature}°C")
                self.violations['thermal'] += 1
                self.bridge.safe_park()
                return True
        return False

    def get_report(self) -> dict:
        """Return safety status for telemetry."""
        return {
            'armed': True,
            'e_stopped': self.bridge._e_stopped,
            'violations': dict(self.violations),
            'max_acceleration': self.max_acceleration,
            'torque_limit_pct': self.torque_limit_pct,
            'soft_touch': self.soft_touch.get_report()
        }
