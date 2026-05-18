"""Deterministic robotics safety boundary for HPP V2.

This adapter keeps neural intent on the safe side of the robotics boundary.
It recommends actions from telemetry; it does not command hardware.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RobotTelemetry:
    """Input schema for simulation-first robotics safety checks."""

    source: str
    robot_model: str
    mode: str
    battery_percent: float
    imu_instability: float
    joint_error: float
    operator_override: bool
    unknown_state: bool


@dataclass(frozen=True)
class RobotRecommendation:
    """Deterministic recommendation emitted by the safety boundary."""

    hpp_mode: str
    action: str
    sentinel_required: bool
    reason: str
    evidence_tag: str


class SafetyBoundaryAdapter:
    """Route HPP intent through hard safety rules before robotics use."""

    def __init__(self) -> None:
        self.evidence_log: list[RobotRecommendation] = []

    def evaluate_state(self, telemetry: RobotTelemetry, hpp_intent: str) -> RobotRecommendation:
        if telemetry.operator_override:
            return self._record(
                RobotRecommendation(
                    "operator_manual",
                    "operator_control",
                    False,
                    "Operator override detected.",
                    "EV_OP_OVERRIDE",
                )
            )

        if telemetry.unknown_state:
            return self._record(
                RobotRecommendation(
                    "inspection",
                    "request_inspection",
                    True,
                    "Telemetry incomplete or contradictory.",
                    "EV_UNKNOWN_STATE",
                )
            )

        if telemetry.battery_percent < 15.0:
            return self._record(
                RobotRecommendation(
                    "conservation",
                    "low_power_pause",
                    False,
                    f"Critical battery at {telemetry.battery_percent}%.",
                    "EV_LOW_BATTERY",
                )
            )

        if telemetry.imu_instability > 0.8 or telemetry.joint_error > 0.8:
            return self._record(
                RobotRecommendation(
                    "sentinel_lock",
                    "sentinel_stop",
                    True,
                    f"Critical instability: imu={telemetry.imu_instability}, joint={telemetry.joint_error}.",
                    "EV_CRIT_INSTABILITY",
                )
            )

        if telemetry.imu_instability > 0.4 or telemetry.joint_error > 0.4:
            return self._record(
                RobotRecommendation(
                    "observation",
                    "observe",
                    False,
                    "Moderate instability detected. Holding action for observation.",
                    "EV_MOD_INSTABILITY",
                )
            )

        if hpp_intent == "MASAMUNE_MOVE":
            return self._record(
                RobotRecommendation(
                    "active_simulation",
                    "continue_simulation",
                    False,
                    "Nominal telemetry. Movement intent is simulation-authorized only.",
                    "EV_NOMINAL_SIM",
                )
            )

        return self._record(
            RobotRecommendation("standby", "observe", False, "No active intent. Standing by.", "EV_STANDBY")
        )

    def _record(self, recommendation: RobotRecommendation) -> RobotRecommendation:
        self.evidence_log.append(recommendation)
        return recommendation
