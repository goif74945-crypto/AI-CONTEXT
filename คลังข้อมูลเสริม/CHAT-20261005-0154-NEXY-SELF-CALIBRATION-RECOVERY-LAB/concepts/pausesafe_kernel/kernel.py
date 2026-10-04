from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Iterable

from core.canonical import fingerprint


class StepStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PASS = "PASS"
    FAIL = "FAIL"


@dataclass(frozen=True)
class StepState:
    step_id: str
    status: StepStatus
    idempotent: bool
    checkpointed: bool = False
    compensation_registered: bool = False

    def __post_init__(self) -> None:
        if not self.step_id.strip():
            raise ValueError("step_id must be non-empty")

    def as_dict(self) -> dict[str, object]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


@dataclass(frozen=True)
class ResumeToken:
    mission_id: str
    checkpoint_id: str
    completed_steps: tuple[str, ...]
    state_fingerprint: str
    token_fingerprint: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _state_payload(mission_id: str, checkpoint_id: str, steps: Iterable[StepState]) -> dict[str, object]:
    ordered = sorted((s.as_dict() for s in steps), key=lambda x: str(x["step_id"]))
    return {"mission_id": mission_id, "checkpoint_id": checkpoint_id, "steps": ordered}


def _validate_steps(rows: list[StepState]) -> None:
    ids = [s.step_id for s in rows]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate step_id")


def preemption_assessment(steps: Iterable[StepState]) -> dict[str, object]:
    rows = list(steps)
    _validate_steps(rows)
    running = [s for s in rows if s.status is StepStatus.RUNNING]
    unsafe = [
        s.step_id
        for s in running
        if not s.idempotent and not s.checkpointed and not s.compensation_registered
    ]
    drain = [
        s.step_id
        for s in running
        if not s.checkpointed and (s.idempotent or s.compensation_registered)
    ]
    if unsafe:
        status = "BLOCKED_UNSAFE_INFLIGHT"
    elif drain:
        status = "DRAIN_REQUIRED"
    else:
        status = "PREEMPT_SAFE"
    return {
        "status": status,
        "unsafe_steps": sorted(unsafe),
        "drain_steps": sorted(drain),
        "running_steps": sorted(s.step_id for s in running),
    }


def create_resume_token(mission_id: str, checkpoint_id: str, steps: Iterable[StepState]) -> ResumeToken:
    mission_id = mission_id.strip()
    checkpoint_id = checkpoint_id.strip()
    if not mission_id or not checkpoint_id:
        raise ValueError("mission_id and checkpoint_id must be non-empty")
    rows = list(steps)
    _validate_steps(rows)
    assessment = preemption_assessment(rows)
    if assessment["status"] != "PREEMPT_SAFE":
        raise RuntimeError(f"cannot checkpoint: {assessment['status']}")
    state_fp = fingerprint(_state_payload(mission_id, checkpoint_id, rows))
    completed = tuple(sorted(s.step_id for s in rows if s.status is StepStatus.PASS))
    token_payload = {
        "mission_id": mission_id,
        "checkpoint_id": checkpoint_id,
        "completed_steps": completed,
        "state_fingerprint": state_fp,
    }
    return ResumeToken(mission_id, checkpoint_id, completed, state_fp, fingerprint(token_payload))


def validate_resume(token: ResumeToken, steps: Iterable[StepState]) -> dict[str, object]:
    rows = list(steps)
    _validate_steps(rows)
    current_fp = fingerprint(_state_payload(token.mission_id, token.checkpoint_id, rows))
    if current_fp != token.state_fingerprint:
        return {
            "status": "STATE_DRIFT",
            "expected_state_fingerprint": token.state_fingerprint,
            "current_state_fingerprint": current_fp,
            "next_steps": [],
        }
    completed = tuple(sorted(s.step_id for s in rows if s.status is StepStatus.PASS))
    if completed != token.completed_steps:
        return {"status": "COMPLETION_DRIFT", "next_steps": []}
    next_steps = sorted(s.step_id for s in rows if s.status is StepStatus.PENDING)
    return {"status": "RESUME_SAFE", "next_steps": next_steps}
