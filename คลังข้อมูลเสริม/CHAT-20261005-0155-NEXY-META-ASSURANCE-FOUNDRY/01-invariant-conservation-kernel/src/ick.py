from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Iterable, Mapping, Any


class ContractError(ValueError):
    """Raised when an ICK input violates the structural contract."""


def _clean_set(name: str, values: Iterable[str]) -> frozenset[str]:
    result: set[str] = set()
    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise ContractError(f"{name} must contain non-empty strings")
        result.add(value.strip())
    return frozenset(result)


@dataclass(frozen=True)
class Snapshot:
    authority_level: int
    evidence_level: int
    unknowns: frozenset[str]
    constraints: frozenset[str]
    capabilities: frozenset[str]
    side_effects: frozenset[str]

    @classmethod
    def build(
        cls,
        *,
        authority_level: int,
        evidence_level: int,
        unknowns: Iterable[str] = (),
        constraints: Iterable[str] = (),
        capabilities: Iterable[str] = (),
        side_effects: Iterable[str] = (),
    ) -> "Snapshot":
        if not isinstance(authority_level, int) or authority_level < 0:
            raise ContractError("authority_level must be a non-negative integer")
        if not isinstance(evidence_level, int) or evidence_level < 0:
            raise ContractError("evidence_level must be a non-negative integer")
        snapshot = cls(
            authority_level=authority_level,
            evidence_level=evidence_level,
            unknowns=_clean_set("unknowns", unknowns),
            constraints=_clean_set("constraints", constraints),
            capabilities=_clean_set("capabilities", capabilities),
            side_effects=_clean_set("side_effects", side_effects),
        )
        return snapshot


@dataclass(frozen=True)
class TransitionReceipt:
    authority_grant_id: str | None = None
    evidence_refs: frozenset[str] = frozenset()
    resolved_unknowns: frozenset[str] = frozenset()
    waived_constraints: frozenset[str] = frozenset()
    granted_capabilities: frozenset[str] = frozenset()

    @classmethod
    def build(
        cls,
        *,
        authority_grant_id: str | None = None,
        evidence_refs: Iterable[str] = (),
        resolved_unknowns: Iterable[str] = (),
        waived_constraints: Iterable[str] = (),
        granted_capabilities: Iterable[str] = (),
    ) -> "TransitionReceipt":
        if authority_grant_id is not None:
            if not isinstance(authority_grant_id, str) or not authority_grant_id.strip():
                raise ContractError("authority_grant_id must be a non-empty string or None")
            authority_grant_id = authority_grant_id.strip()
        return cls(
            authority_grant_id=authority_grant_id,
            evidence_refs=_clean_set("evidence_refs", evidence_refs),
            resolved_unknowns=_clean_set("resolved_unknowns", resolved_unknowns),
            waived_constraints=_clean_set("waived_constraints", waived_constraints),
            granted_capabilities=_clean_set("granted_capabilities", granted_capabilities),
        )


@dataclass(frozen=True)
class ConservationReport:
    status: str
    action: str
    reason_codes: tuple[str, ...]
    fingerprint: str
    details: Mapping[str, tuple[str, ...]]

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "action": self.action,
            "reason_codes": list(self.reason_codes),
            "fingerprint": self.fingerprint,
            "details": {key: list(value) for key, value in sorted(self.details.items())},
        }


def _snapshot_dict(value: Snapshot) -> dict[str, Any]:
    return {
        "authority_level": value.authority_level,
        "evidence_level": value.evidence_level,
        "unknowns": sorted(value.unknowns),
        "constraints": sorted(value.constraints),
        "capabilities": sorted(value.capabilities),
        "side_effects": sorted(value.side_effects),
    }


def _receipt_dict(value: TransitionReceipt) -> dict[str, Any]:
    return {
        "authority_grant_id": value.authority_grant_id,
        "evidence_refs": sorted(value.evidence_refs),
        "resolved_unknowns": sorted(value.resolved_unknowns),
        "waived_constraints": sorted(value.waived_constraints),
        "granted_capabilities": sorted(value.granted_capabilities),
    }


def _fingerprint(before: Snapshot, after: Snapshot, receipt: TransitionReceipt) -> str:
    payload = {
        "before": _snapshot_dict(before),
        "after": _snapshot_dict(after),
        "receipt": _receipt_dict(receipt),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256(encoded).hexdigest()


def evaluate_transition(
    before: Snapshot,
    after: Snapshot,
    receipt: TransitionReceipt | None = None,
) -> ConservationReport:
    if not isinstance(before, Snapshot) or not isinstance(after, Snapshot):
        raise ContractError("before and after must be Snapshot instances")
    receipt = receipt or TransitionReceipt()
    if not isinstance(receipt, TransitionReceipt):
        raise ContractError("receipt must be a TransitionReceipt")

    reasons: set[str] = set()
    details: dict[str, tuple[str, ...]] = {}

    unauthorized_effects = after.side_effects - after.capabilities
    if unauthorized_effects:
        reasons.add("SIDE_EFFECT_WITHOUT_CAPABILITY")
        details["unauthorized_side_effects"] = tuple(sorted(unauthorized_effects))

    if after.authority_level > before.authority_level and receipt.authority_grant_id is None:
        reasons.add("AUTHORITY_INFLATION")

    if after.evidence_level > before.evidence_level and not receipt.evidence_refs:
        reasons.add("EVIDENCE_INFLATION")

    removed_unknowns = before.unknowns - after.unknowns
    unresolved_disappearances = removed_unknowns - receipt.resolved_unknowns
    if unresolved_disappearances:
        reasons.add("UNCERTAINTY_ERASURE")
        details["unresolved_removed_unknowns"] = tuple(sorted(unresolved_disappearances))

    removed_constraints = before.constraints - after.constraints
    unwaived = removed_constraints - receipt.waived_constraints
    if unwaived:
        reasons.add("CONSTRAINT_WEAKENING")
        details["unwaived_removed_constraints"] = tuple(sorted(unwaived))

    added_capabilities = after.capabilities - before.capabilities
    ungranted = added_capabilities - receipt.granted_capabilities
    if ungranted:
        reasons.add("CAPABILITY_ESCALATION")
        details["ungranted_capabilities"] = tuple(sorted(ungranted))

    status = "FREEZE" if reasons else "PASS"
    return ConservationReport(
        status=status,
        action="FREEZE" if reasons else "RELEASE",
        reason_codes=tuple(sorted(reasons)) or ("CONSERVATION_OK",),
        fingerprint=_fingerprint(before, after, receipt),
        details=details,
    )
