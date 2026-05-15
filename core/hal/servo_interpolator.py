"""
HPP PHASE 16: SERVO INTERPOLATOR
Smooth trajectory planning between brain ticks.

The brain thinks at ~15 Hz. Servos update at 50 Hz.
This module generates smooth intermediate positions so Masamune
moves fluidly instead of jerking between brain commands.

Uses cubic Hermite interpolation for natural, organic motion.
"""
import time
import math


class ServoInterpolator:
    """
    Generates smooth trajectories between brain-issued joint commands.
    Runs at body-loop frequency (50 Hz), interpolating between the
    slower brain-loop commands (~15 Hz).
    """

    def __init__(self, num_joints: int = 19, smoothing: float = 0.85):
        """
        Args:
            num_joints: Total joint count (14 arms + 4 stance + 1 grip = 19)
            smoothing: Exponential smoothing factor (0 = no smoothing, 1 = frozen)
        """
        self.num_joints = num_joints
        self.smoothing = smoothing

        # Command buffers
        self._current_target = [0.0] * num_joints
        self._previous_target = [0.0] * num_joints
        self._smoothed_output = [0.0] * num_joints

        # Timing
        self._target_received_at = time.perf_counter()
        self._target_interval = 1.0 / 15.0  # Expected brain rate

        self._initialized = False

    def set_target(self, joint_values: list):
        """
        Called by the brain thread when a new command arrives.
        
        Args:
            joint_values: list of floats — full 19-element command vector
                         [left_arm(7), right_arm(7), stance(4), grip(1)]
        """
        if len(joint_values) != self.num_joints:
            raise ValueError(
                f"Expected {self.num_joints} joints, got {len(joint_values)}"
            )

        now = time.perf_counter()
        self._target_interval = max(now - self._target_received_at, 0.01)
        self._target_received_at = now

        self._previous_target = list(self._smoothed_output)
        self._current_target = list(joint_values)

        if not self._initialized:
            self._smoothed_output = list(joint_values)
            self._initialized = True

    def get_interpolated(self) -> list:
        """
        Called by the body thread at 50 Hz.
        Returns smoothly interpolated joint positions.
        """
        if not self._initialized:
            return list(self._smoothed_output)

        # Calculate interpolation parameter (0.0 = just received, 1.0 = next expected)
        elapsed = time.perf_counter() - self._target_received_at
        t = min(elapsed / self._target_interval, 1.0)

        # Cubic ease-in-out for natural motion
        t_smooth = self._ease_in_out_cubic(t)

        for i in range(self.num_joints):
            # Interpolate between previous and current target
            interp = self._previous_target[i] + (
                self._current_target[i] - self._previous_target[i]
            ) * t_smooth

            # Exponential smoothing on top for extra fluidity
            self._smoothed_output[i] = (
                self.smoothing * self._smoothed_output[i]
                + (1.0 - self.smoothing) * interp
            )

        return list(self._smoothed_output)

    def get_split_commands(self) -> tuple:
        """
        Returns interpolated values split into the groups expected by DynamixelBridge.
        
        Returns:
            (left_arm[7], right_arm[7], stance[4], grip_force)
        """
        values = self.get_interpolated()
        left_arm = values[0:7]
        right_arm = values[7:14]
        stance = values[14:18]
        grip = values[18] if len(values) > 18 else 0.0
        return left_arm, right_arm, stance, grip

    @staticmethod
    def _ease_in_out_cubic(t: float) -> float:
        """Cubic ease-in-out curve for natural servo motion."""
        if t < 0.5:
            return 4.0 * t * t * t
        else:
            p = 2.0 * t - 2.0
            return 0.5 * p * p * p + 1.0

    def reset(self):
        """Reset interpolator to zero state."""
        self._current_target = [0.0] * self.num_joints
        self._previous_target = [0.0] * self.num_joints
        self._smoothed_output = [0.0] * self.num_joints
        self._initialized = False
