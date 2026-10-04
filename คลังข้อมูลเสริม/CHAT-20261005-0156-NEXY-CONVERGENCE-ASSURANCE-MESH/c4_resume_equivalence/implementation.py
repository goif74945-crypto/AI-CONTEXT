from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

from shared import GateResult, sha256_hex


NextActionFn = Callable[[Mapping[str, Any]], Any]


@dataclass(frozen=True)
class ResumeState:
    task_id: str
    authority_epoch: str
    target_identity: str
    resume_critical: Mapping[str, Any]
    ephemeral: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.task_id.strip() or not self.authority_epoch.strip() or not self.target_identity.strip():
            raise ValueError("task_id, authority_epoch, and target_identity must be non-empty")

    def critical_payload(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "authority_epoch": self.authority_epoch,
            "target_identity": self.target_identity,
            "resume_critical": self.resume_critical,
        }


def compile_capsule(state: ResumeState, next_action_fn: NextActionFn) -> dict[str, Any]:
    critical = state.critical_payload()
    next_action = next_action_fn(critical)
    payload = {
        "schema": "nexy.resume-equivalence.v1",
        "critical_state": critical,
        "critical_state_hash": sha256_hex(critical),
        "next_action": next_action,
        "next_action_hash": sha256_hex(next_action),
    }
    return {**payload, "capsule_hash": sha256_hex(payload)}


def verify_resume_equivalence(
    capsule: Mapping[str, Any],
    reconstructed: ResumeState,
    next_action_fn: NextActionFn,
) -> GateResult:
    required = {
        "schema",
        "critical_state",
        "critical_state_hash",
        "next_action",
        "next_action_hash",
        "capsule_hash",
    }
    missing = sorted(required - set(capsule))
    if missing:
        return GateResult("FAIL", "CAPSULE_FIELDS_MISSING", {"missing": missing})

    unsigned = {key: capsule[key] for key in required if key != "capsule_hash"}
    if sha256_hex(unsigned) != capsule["capsule_hash"]:
        return GateResult("FAIL", "CAPSULE_INTEGRITY_MISMATCH", {})
    if capsule["schema"] != "nexy.resume-equivalence.v1":
        return GateResult("FAIL", "UNSUPPORTED_CAPSULE_SCHEMA", {"schema": capsule["schema"]})

    critical = reconstructed.critical_payload()
    critical_hash = sha256_hex(critical)
    if critical_hash != capsule["critical_state_hash"]:
        return GateResult(
            "FREEZE",
            "RESUME_CRITICAL_STATE_DRIFT",
            {
                "expected_hash": capsule["critical_state_hash"],
                "observed_hash": critical_hash,
            },
        )

    try:
        next_action = next_action_fn(critical)
    except Exception as exc:
        return GateResult(
            "FREEZE",
            "NEXT_ACTION_RECONSTRUCTION_FAILED",
            {"error_type": type(exc).__name__, "error": str(exc)},
        )

    action_hash = sha256_hex(next_action)
    if action_hash != capsule["next_action_hash"]:
        return GateResult(
            "FREEZE",
            "NEXT_ACTION_DRIFT",
            {"expected_hash": capsule["next_action_hash"], "observed_hash": action_hash},
        )

    return GateResult(
        "VERIFIED",
        "RESUMPTION_EQUIVALENT",
        {
            "critical_state_hash": critical_hash,
            "next_action_hash": action_hash,
            "ephemeral_fields_ignored": sorted(reconstructed.ephemeral),
        },
    )
