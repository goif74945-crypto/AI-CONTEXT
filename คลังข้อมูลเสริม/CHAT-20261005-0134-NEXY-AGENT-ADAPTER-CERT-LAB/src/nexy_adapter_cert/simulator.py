from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from .canonical import sha256_hex
from .validator import validate_manifest


class SimulationEvent(StrEnum):
    RESULT_VALID = "result_valid"
    RESULT_SCHEMA_INVALID = "result_schema_invalid"
    TIMEOUT = "timeout"
    PROVIDER_FAILURE = "provider_failure"


@dataclass(frozen=True, slots=True)
class SimulationReport:
    status: str
    action: str
    reason_code: str
    manifest_digest: str
    event: str
    report_digest: str
    limitation: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "action": self.action,
            "reason_code": self.reason_code,
            "manifest_digest": self.manifest_digest,
            "event": self.event,
            "report_digest": self.report_digest,
            "limitation": self.limitation,
        }


def simulate(
    manifest: Any,
    event: SimulationEvent | str,
    *,
    quorum_possible_after_exclusion: bool | None = None,
) -> SimulationReport:
    """Replay source-grounded adapter failure semantics without touching NEXY runtime."""
    validation = validate_manifest(manifest)
    event_value = SimulationEvent(event)

    if validation.status != "PASS":
        return _report(
            "FAIL",
            "FREEZE_PRE_EXEC",
            "ADAPTER_CONTRACT_INVALID",
            validation.manifest_digest,
            event_value,
        )

    critical = manifest["adapter"]["critical"]

    if event_value is SimulationEvent.RESULT_VALID:
        return _report(
            "PASS",
            "CONTINUE_TO_CROSS_VERIFY",
            "CANDIDATE_RESULT_VALID",
            validation.manifest_digest,
            event_value,
        )

    if event_value is SimulationEvent.RESULT_SCHEMA_INVALID:
        return _report(
            "PASS",
            "FREEZE",
            "AGENT_SCHEMA_INVALID",
            validation.manifest_digest,
            event_value,
        )

    if event_value is SimulationEvent.PROVIDER_FAILURE:
        return _report(
            "PASS",
            "FREEZE",
            "DEPENDENCY_FAILURE",
            validation.manifest_digest,
            event_value,
        )

    if event_value is SimulationEvent.TIMEOUT:
        if critical:
            return _report(
                "PASS",
                "FREEZE",
                "AGENT_TIMEOUT_CRITICAL",
                validation.manifest_digest,
                event_value,
            )
        if quorum_possible_after_exclusion is True:
            return _report(
                "PASS",
                "EXCLUDE_AGENT_AND_CONTINUE",
                "AGENT_TIMEOUT_NONCRITICAL_QUORUM_REMAINS",
                validation.manifest_digest,
                event_value,
            )
        if quorum_possible_after_exclusion is False:
            return _report(
                "PASS",
                "FREEZE",
                "CONSENSUS_QUORUM_WOULD_FAIL",
                validation.manifest_digest,
                event_value,
            )
        return _report(
            "PASS",
            "FREEZE",
            "QUORUM_STATUS_UNKNOWN_ZERO_GUESS",
            validation.manifest_digest,
            event_value,
        )

    raise AssertionError("unreachable")


def _report(status: str, action: str, reason_code: str, manifest_digest: str, event: SimulationEvent) -> SimulationReport:
    limitation = (
        "Deterministic lab simulation only; this is not E3/E5 evidence from the real NEXY.AI runtime."
    )
    digest_payload = {
        "status": status,
        "action": action,
        "reason_code": reason_code,
        "manifest_digest": manifest_digest,
        "event": event.value,
        "limitation": limitation,
    }
    return SimulationReport(
        status=status,
        action=action,
        reason_code=reason_code,
        manifest_digest=manifest_digest,
        event=event.value,
        report_digest=sha256_hex(digest_payload),
        limitation=limitation,
    )
