from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping


class Outcome(str, Enum):
    RELEASE = "RELEASE"
    FREEZE = "FREEZE"
    STOP = "STOP"


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    BLOCKING = "BLOCKING"


@dataclass(frozen=True)
class EvidenceRef:
    evidence_class: str
    ref: str
    revision: str

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "EvidenceRef":
        evidence_class = str(raw.get("class", "")).upper()
        if evidence_class not in {f"E{i}" for i in range(8)}:
            raise ValueError(f"invalid evidence class: {evidence_class!r}")
        ref = str(raw.get("ref", "")).strip()
        revision = str(raw.get("revision", "")).strip()
        if not ref:
            raise ValueError("evidence ref must be non-empty")
        if not revision:
            raise ValueError("evidence revision must be non-empty")
        return cls(evidence_class=evidence_class, ref=ref, revision=revision)


@dataclass(frozen=True)
class DecisionRecord:
    case_id: str
    input_fingerprint: str
    revision: str
    policy_fingerprint: str
    authority_chain: tuple[str, ...]
    outcome: Outcome
    action: str | None
    required_evidence_classes: tuple[str, ...]
    evidence: tuple[EvidenceRef, ...]
    safety_labels: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "DecisionRecord":
        case_id = _required_text(raw, "case_id")
        input_fingerprint = _required_text(raw, "input_fingerprint")
        revision = _required_text(raw, "revision")
        policy_fingerprint = _required_text(raw, "policy_fingerprint")

        authority_chain = _string_tuple(raw.get("authority_chain", ()), "authority_chain")
        if not authority_chain:
            raise ValueError("authority_chain must contain at least one authority")

        try:
            outcome = Outcome(str(raw.get("outcome", "")).upper())
        except ValueError as exc:
            raise ValueError(f"invalid outcome: {raw.get('outcome')!r}") from exc

        action_raw = raw.get("action")
        action = None if action_raw is None else str(action_raw)
        if outcome is Outcome.RELEASE and (action is None or not action.strip()):
            raise ValueError("RELEASE records require a non-empty action")
        if outcome in {Outcome.FREEZE, Outcome.STOP} and action not in {None, ""}:
            raise ValueError(f"{outcome.value} records must not carry an executable action")

        required = tuple(x.upper() for x in _string_tuple(raw.get("required_evidence_classes", ()), "required_evidence_classes"))
        invalid_required = [x for x in required if x not in {f"E{i}" for i in range(8)}]
        if invalid_required:
            raise ValueError(f"invalid required evidence classes: {invalid_required}")

        evidence_raw = raw.get("evidence", ())
        if not isinstance(evidence_raw, list):
            raise ValueError("evidence must be a list")
        evidence = tuple(EvidenceRef.from_mapping(x) for x in evidence_raw)

        safety_labels = _string_tuple(raw.get("safety_labels", ()), "safety_labels")
        return cls(
            case_id=case_id,
            input_fingerprint=input_fingerprint,
            revision=revision,
            policy_fingerprint=policy_fingerprint,
            authority_chain=authority_chain,
            outcome=outcome,
            action=action,
            required_evidence_classes=required,
            evidence=evidence,
            safety_labels=safety_labels,
        )

    def evidence_classes(self) -> frozenset[str]:
        return frozenset(e.evidence_class for e in self.evidence)

    def stale_evidence(self) -> tuple[EvidenceRef, ...]:
        return tuple(e for e in self.evidence if e.revision != self.revision)


def _required_text(raw: Mapping[str, Any], key: str) -> str:
    value = str(raw.get(key, "")).strip()
    if not value:
        raise ValueError(f"{key} must be non-empty")
    return value


def _string_tuple(value: Any, name: str) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{name} must be an array")
    result = tuple(str(x).strip() for x in value)
    if any(not x for x in result):
        raise ValueError(f"{name} cannot contain blank values")
    return result


@dataclass(frozen=True)
class Finding:
    code: str
    severity: Severity
    case_id: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "severity": self.severity.value,
            "case_id": self.case_id,
            "message": self.message,
        }


@dataclass(frozen=True)
class GateReport:
    status: str
    stable_cases: int
    candidate_cases: int
    compared_cases: int
    findings: tuple[Finding, ...]

    def as_dict(self) -> dict[str, Any]:
        counts: dict[str, int] = {}
        for finding in self.findings:
            counts[finding.code] = counts.get(finding.code, 0) + 1
        return {
            "status": self.status,
            "stable_cases": self.stable_cases,
            "candidate_cases": self.candidate_cases,
            "compared_cases": self.compared_cases,
            "finding_counts": dict(sorted(counts.items())),
            "findings": [finding.as_dict() for finding in self.findings],
        }
