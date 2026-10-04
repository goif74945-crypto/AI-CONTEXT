from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class Severity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass(frozen=True, slots=True, order=True)
class Finding:
    severity: Severity
    rule_id: str
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "severity": self.severity.value,
            "rule_id": self.rule_id,
            "path": self.path,
            "message": self.message,
        }


@dataclass(frozen=True, slots=True)
class ValidationReport:
    profile: str
    surface_id: str
    findings: tuple[Finding, ...]

    @property
    def passed(self) -> bool:
        return not any(item.severity is Severity.ERROR for item in self.findings)

    @property
    def errors(self) -> tuple[Finding, ...]:
        return tuple(item for item in self.findings if item.severity is Severity.ERROR)

    @property
    def warnings(self) -> tuple[Finding, ...]:
        return tuple(item for item in self.findings if item.severity is Severity.WARNING)

    def to_dict(self) -> dict[str, Any]:
        ordered = tuple(sorted(self.findings))
        return {
            "profile": self.profile,
            "surface_id": self.surface_id,
            "status": "PASS" if self.passed else "FAIL",
            "counts": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "total": len(self.findings),
            },
            "findings": [item.to_dict() for item in ordered],
        }


JSONMapping = Mapping[str, Any]
