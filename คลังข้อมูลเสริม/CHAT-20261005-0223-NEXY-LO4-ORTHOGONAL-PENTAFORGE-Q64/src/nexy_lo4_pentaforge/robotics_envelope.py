from __future__ import annotations

from dataclasses import dataclass

from .q64 import Q64


@dataclass(frozen=True)
class MotionEnvelopeInput:
    speed: Q64
    max_speed: Q64
    reaction_time: Q64
    max_deceleration: Q64
    obstacle_distance: Q64
    safety_margin: Q64


@dataclass(frozen=True)
class MotionEnvelopeReport:
    safe: bool
    stopping_distance: Q64
    available_distance: Q64
    clearance: Q64
    clearance_ratio: Q64
    reasons: tuple[str, ...]


def evaluate_motion_envelope(value: MotionEnvelopeInput) -> MotionEnvelopeReport:
    zero = Q64.zero()
    two = Q64.from_int(2)
    fields = (
        value.speed,
        value.max_speed,
        value.reaction_time,
        value.max_deceleration,
        value.obstacle_distance,
        value.safety_margin,
    )
    if any(field < zero for field in fields):
        raise ValueError("motion envelope quantities must be nonnegative")
    if value.max_deceleration <= zero:
        raise ValueError("max_deceleration must be positive")
    reaction_distance = value.speed * value.reaction_time
    braking_distance = (value.speed * value.speed) / (two * value.max_deceleration)
    stopping = reaction_distance + braking_distance
    available = value.obstacle_distance - value.safety_margin
    clearance = available - stopping
    reasons: list[str] = []
    if value.speed > value.max_speed:
        reasons.append("SPEED_LIMIT_EXCEEDED")
    if available < zero:
        reasons.append("MARGIN_EXCEEDS_OBSTACLE_DISTANCE")
    if clearance < zero:
        reasons.append("INSUFFICIENT_STOPPING_DISTANCE")
    if stopping > zero:
        ratio = available / stopping
    else:
        ratio = Q64.one() if available >= zero else Q64.zero()
    return MotionEnvelopeReport(
        safe=not reasons,
        stopping_distance=stopping,
        available_distance=available,
        clearance=clearance,
        clearance_ratio=ratio,
        reasons=tuple(reasons),
    )
