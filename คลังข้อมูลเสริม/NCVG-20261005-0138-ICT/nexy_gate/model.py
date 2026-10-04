from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping

VALID_STATUSES = {
    "PASS",
    "FAIL",
    "PARTIAL",
    "BLOCKED",
    "NOT_VERIFIED",
    "UNKNOWN",
    "CONFLICT",
    "MISSING",
    "SCOPE",
}

EVIDENCE_CLASSES = {
    "E0_PRESENCE",
    "E1_STATIC",
    "E2_UNIT",
    "E3_INTEGRATION",
    "E4_E2E",
    "E5_RUNTIME",
    "E6_DEPLOYMENT",
    "E7_PHYSICAL",
}


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    path: str
    message: str
    severity: str = "ERROR"

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class GateDecision:
    decision: str
    status: str
    bundle_sha256: str
    findings: tuple[Finding, ...]
    verified_requirements: tuple[str, ...]
    total_mandatory_requirements: int

    @property
    def allowed(self) -> bool:
        return self.decision == "ALLOW"

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "status": self.status,
            "bundle_sha256": self.bundle_sha256,
            "verified_requirements": list(self.verified_requirements),
            "total_mandatory_requirements": self.total_mandatory_requirements,
            "findings": [f.to_dict() for f in self.findings],
        }


def expect_mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None
