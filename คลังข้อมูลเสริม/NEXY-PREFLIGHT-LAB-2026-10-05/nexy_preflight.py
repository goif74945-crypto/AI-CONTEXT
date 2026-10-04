from __future__ import annotations



# ===== models.py =====

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping


class Decision(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_VERIFIED = "NOT_VERIFIED"
    CONFLICT = "CONFLICT"


class EvidenceClass(str, Enum):
    E0 = "E0"
    E1 = "E1"
    E2 = "E2"
    E3 = "E3"
    E4 = "E4"
    E5 = "E5"
    E6 = "E6"
    E7 = "E7"

    @property
    def rank(self) -> int:
        return int(self.value[1:])


class OperationKind(str, Enum):
    READ = "read"
    SEARCH = "search"
    ANALYZE = "analyze"
    WRITE = "write"
    UPDATE = "update"
    DELETE = "delete"
    DEPLOY = "deploy"
    MERGE = "merge"
    PERMISSION = "permission"
    EXECUTE = "execute"

    @property
    def is_mutation(self) -> bool:
        return self in {
            OperationKind.WRITE,
            OperationKind.UPDATE,
            OperationKind.DELETE,
            OperationKind.DEPLOY,
            OperationKind.MERGE,
            OperationKind.PERMISSION,
        }


@dataclass(frozen=True, slots=True)
class Operation:
    kind: OperationKind
    resource: str
    irreversible: bool = False
    approval: str | None = None


@dataclass(frozen=True, slots=True)
class Claim:
    id: str
    kind: str
    text: str


@dataclass(frozen=True, slots=True)
class Evidence:
    claim_id: str
    evidence_class: EvidenceClass
    result: str
    artifact: str | None = None


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    message: str
    decision: Decision
    resource: str | None = None
    claim_id: str | None = None


@dataclass(frozen=True, slots=True)
class TaskContract:
    task_id: str
    objective: str
    target: str
    authorized_scope: tuple[str, ...]
    protected_scope: tuple[str, ...]
    authority_sources: tuple[str, ...]
    preconditions: tuple[str, ...]
    operations: tuple[Operation, ...]
    claims: tuple[Claim, ...]
    evidence: tuple[Evidence, ...]
    approvals: tuple[str, ...]

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "TaskContract":
        def strings(key: str) -> tuple[str, ...]:
            value = raw.get(key, ())
            if not isinstance(value, (list, tuple)):
                raise ValueError(f"{key} must be a list")
            return tuple(_require_nonblank(str(v), key) for v in value)

        operations = tuple(
            Operation(
                kind=OperationKind(str(item["kind"]).strip().lower()),
                resource=_require_nonblank(str(item["resource"]), "operations.resource"),
                irreversible=bool(item.get("irreversible", False)),
                approval=(str(item["approval"]).strip() if item.get("approval") else None),
            )
            for item in _mapping_list(raw.get("operations", ()), "operations")
        )
        claims = tuple(
            Claim(
                id=_require_nonblank(str(item["id"]), "claims.id"),
                kind=_require_nonblank(str(item["kind"]), "claims.kind").lower(),
                text=_require_nonblank(str(item["text"]), "claims.text"),
            )
            for item in _mapping_list(raw.get("claims", ()), "claims")
        )
        evidence = tuple(
            Evidence(
                claim_id=_require_nonblank(str(item["claim_id"]), "evidence.claim_id"),
                evidence_class=EvidenceClass(str(item.get("class", item.get("evidence_class")))),
                result=_require_nonblank(str(item["result"]), "evidence.result").upper(),
                artifact=(str(item["artifact"]).strip() if item.get("artifact") else None),
            )
            for item in _mapping_list(raw.get("evidence", ()), "evidence")
        )
        return cls(
            task_id=_require_nonblank(str(raw.get("task_id", "")), "task_id"),
            objective=_require_nonblank(str(raw.get("objective", "")), "objective"),
            target=str(raw.get("target", "")).strip(),
            authorized_scope=strings("authorized_scope"),
            protected_scope=strings("protected_scope"),
            authority_sources=strings("authority_sources"),
            preconditions=strings("preconditions"),
            operations=operations,
            claims=claims,
            evidence=evidence,
            approvals=strings("approvals"),
        )

    def to_primitive(self) -> dict[str, Any]:
        data = asdict(self)
        for op in data["operations"]:
            op["kind"] = op["kind"].value if isinstance(op["kind"], Enum) else op["kind"]
        for ev in data["evidence"]:
            key = "evidence_class"
            ev[key] = ev[key].value if isinstance(ev[key], Enum) else ev[key]
        return data


@dataclass(frozen=True, slots=True)
class AdmissionEnvelope:
    contract_hash: str
    decision: Decision
    findings: tuple[Finding, ...] = field(default_factory=tuple)
    required_evidence: Mapping[str, EvidenceClass] = field(default_factory=dict)
    required_capabilities: tuple[str, ...] = field(default_factory=tuple)

    def to_primitive(self) -> dict[str, Any]:
        return {
            "contract_hash": self.contract_hash,
            "decision": self.decision.value,
            "findings": [
                {
                    "code": f.code,
                    "message": f.message,
                    "decision": f.decision.value,
                    "resource": f.resource,
                    "claim_id": f.claim_id,
                }
                for f in self.findings
            ],
            "required_evidence": {k: v.value for k, v in sorted(self.required_evidence.items())},
            "required_capabilities": list(self.required_capabilities),
        }


def _mapping_list(value: Any, name: str) -> Iterable[Mapping[str, Any]]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{name} must be a list")
    for item in value:
        if not isinstance(item, Mapping):
            raise ValueError(f"{name} items must be objects")
        yield item


def _require_nonblank(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be blank")
    return normalized

# ===== canonical.py =====

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    """Serialize JSON-compatible data with a stable byte representation."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_identity(value: Any) -> str:
    payload = canonical_json(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

# ===== pathing.py =====


def normalize_scope(value: str) -> str:
    """Lexically normalize a logical repository/resource scope.

    The first two segments are treated as repository owner/name and case-folded,
    while the remaining logical path remains case-sensitive. This mirrors GitHub
    repository identity without pretending every downstream filesystem is
    case-insensitive.
    """
    raw = value.replace("\\", "/").strip()
    while "//" in raw:
        raw = raw.replace("//", "/")

    parts: list[str] = []
    for part in raw.split("/"):
        if not part or part == ".":
            continue
        if part == "..":
            if parts and parts[-1] != "..":
                parts.pop()
            else:
                parts.append(part)
            continue
        parts.append(part)

    if len(parts) >= 1:
        parts[0] = parts[0].casefold()
    if len(parts) >= 2:
        parts[1] = parts[1].casefold()
    return "/".join(parts)


def contains_scope(parent: str, child: str) -> bool:
    """Boundary-aware logical scope containment, not a filesystem sandbox."""
    p = normalize_scope(parent)
    c = normalize_scope(child)
    if p == c:
        return True
    if not p:
        return False
    return c.startswith(p + "/")


def overlaps_scope(left: str, right: str) -> bool:
    return contains_scope(left, right) or contains_scope(right, left)

# ===== verification.py =====

from collections import Counter, defaultdict
from typing import Iterable



_MINIMUM: dict[str, EvidenceClass] = {
    "presence": EvidenceClass.E0,
    "static": EvidenceClass.E1,
    "type": EvidenceClass.E1,
    "schema": EvidenceClass.E1,
    "unit": EvidenceClass.E2,
    "behavior": EvidenceClass.E2,
    "integration": EvidenceClass.E3,
    "e2e": EvidenceClass.E4,
    "user-flow": EvidenceClass.E4,
    "runtime": EvidenceClass.E5,
    "recovery": EvidenceClass.E5,
    "performance": EvidenceClass.E5,
    "deployment": EvidenceClass.E6,
    "physical": EvidenceClass.E7,
    "hardware": EvidenceClass.E7,
}


def minimum_for_claim(kind: str) -> EvidenceClass | None:
    return _MINIMUM.get(kind.strip().lower())


def evidence_obligations(
    claims: Iterable[Claim], evidence: Iterable[Evidence]
) -> tuple[dict[str, EvidenceClass], list[Finding]]:
    claims = tuple(claims)
    evidence = tuple(evidence)
    required: dict[str, EvidenceClass] = {}
    findings: list[Finding] = []

    claim_counts = Counter(claim.id for claim in claims)
    duplicate_ids = {claim_id for claim_id, count in claim_counts.items() if count > 1}
    for claim_id in sorted(duplicate_ids):
        findings.append(
            Finding(
                code="PFL-CLAIM-DUPLICATE",
                message=f"Claim id '{claim_id}' is duplicated and cannot be addressed uniquely.",
                decision=Decision.CONFLICT,
                claim_id=claim_id,
            )
        )

    claim_ids = set(claim_counts)
    for item in evidence:
        if item.claim_id not in claim_ids:
            findings.append(
                Finding(
                    code="PFL-EVIDENCE-ORPHAN",
                    message=f"Evidence references unknown claim '{item.claim_id}'.",
                    decision=Decision.CONFLICT,
                    claim_id=item.claim_id,
                )
            )

    by_claim: dict[str, list[Evidence]] = defaultdict(list)
    for item in evidence:
        by_claim[item.claim_id].append(item)

    for claim in claims:
        if claim.id in duplicate_ids:
            continue
        minimum = minimum_for_claim(claim.kind)
        if minimum is None:
            findings.append(
                Finding(
                    code="PFL-EVIDENCE-POLICY-UNKNOWN",
                    message=f"No minimum evidence policy is defined for claim kind '{claim.kind}'.",
                    decision=Decision.BLOCKED,
                    claim_id=claim.id,
                )
            )
            continue
        required[claim.id] = minimum
        candidates = by_claim.get(claim.id, [])
        if not candidates:
            findings.append(
                Finding(
                    code="PFL-EVIDENCE-MISSING",
                    message=f"Claim '{claim.id}' requires {minimum.value} or stronger evidence.",
                    decision=Decision.NOT_VERIFIED,
                    claim_id=claim.id,
                )
            )
            continue

        passing = [e for e in candidates if e.result == "PASS"]
        failing = [e for e in candidates if e.result == "FAIL"]
        if failing and not passing:
            findings.append(
                Finding(
                    code="PFL-EVIDENCE-FAILED",
                    message=f"Claim '{claim.id}' has explicit failing evidence.",
                    decision=Decision.FAIL,
                    claim_id=claim.id,
                )
            )
            continue

        if not any(e.evidence_class.rank >= minimum.rank for e in passing):
            strongest = max((e.evidence_class.rank for e in passing), default=-1)
            observed = f"E{strongest}" if strongest >= 0 else "none"
            findings.append(
                Finding(
                    code="PFL-EVIDENCE-INSUFFICIENT",
                    message=(
                        f"Claim '{claim.id}' requires {minimum.value} or stronger PASS evidence; "
                        f"strongest passing class is {observed}."
                    ),
                    decision=Decision.NOT_VERIFIED,
                    claim_id=claim.id,
                )
            )
    return required, findings

# ===== engine.py =====

from collections import Counter



_PRIORITY = {
    Decision.PASS: 0,
    Decision.NOT_VERIFIED: 1,
    Decision.BLOCKED: 2,
    Decision.FAIL: 3,
    Decision.CONFLICT: 4,
}


def evaluate_contract(contract: TaskContract) -> AdmissionEnvelope:
    findings: list[Finding] = []

    if not contract.target:
        findings.append(
            Finding(
                code="PFL-TARGET-MISSING",
                message="Target identity is missing.",
                decision=Decision.BLOCKED,
            )
        )

    if not contract.authorized_scope:
        findings.append(
            Finding(
                code="PFL-SCOPE-MISSING",
                message="No authorized scope was declared.",
                decision=Decision.BLOCKED,
            )
        )

    if not contract.authority_sources:
        findings.append(
            Finding(
                code="PFL-AUTHORITY-MISSING",
                message="No authority source was declared.",
                decision=Decision.BLOCKED,
            )
        )

    findings.extend(_operation_findings(contract))

    required, evidence_findings = evidence_obligations(contract.claims, contract.evidence)
    findings.extend(evidence_findings)

    ordered = tuple(sorted(findings, key=_finding_key))
    decision = max((f.decision for f in ordered), key=lambda d: _PRIORITY[d], default=Decision.PASS)
    capabilities = tuple(sorted({op.kind.value for op in contract.operations}))
    return AdmissionEnvelope(
        contract_hash=sha256_identity(contract.to_primitive()),
        decision=decision,
        findings=ordered,
        required_evidence=required,
        required_capabilities=capabilities,
    )


def _operation_findings(contract: TaskContract) -> list[Finding]:
    findings: list[Finding] = []
    approval_counts = Counter(contract.approvals)

    for op in contract.operations:
        if not any(contains_scope(scope, op.resource) for scope in contract.authorized_scope):
            findings.append(
                Finding(
                    code="PFL-SCOPE-OUTSIDE",
                    message=f"Operation target '{op.resource}' is outside declared authorized scope.",
                    decision=Decision.BLOCKED,
                    resource=op.resource,
                )
            )

        if op.kind.is_mutation and any(
            contains_scope(scope, op.resource) for scope in contract.protected_scope
        ):
            findings.append(
                Finding(
                    code="PFL-PROTECTED-WRITE",
                    message=f"Mutation '{op.kind.value}' targets protected scope '{op.resource}'.",
                    decision=Decision.CONFLICT,
                    resource=op.resource,
                )
            )

        if op.irreversible:
            required_approval = op.approval or f"approve:{op.kind.value}:{op.resource}"
            if approval_counts[required_approval] <= 0:
                findings.append(
                    Finding(
                        code="PFL-APPROVAL-MISSING",
                        message=(
                            f"Irreversible operation '{op.kind.value}' on '{op.resource}' requires "
                            f"explicit approval token '{required_approval}'."
                        ),
                        decision=Decision.BLOCKED,
                        resource=op.resource,
                    )
                )
    return findings


def _finding_key(finding: Finding) -> tuple[int, str, str, str]:
    return (
        -_PRIORITY[finding.decision],
        finding.code,
        finding.resource or "",
        finding.claim_id or "",
    )

# ===== drift.py =====

from dataclasses import dataclass



@dataclass(frozen=True, slots=True)
class DriftReport:
    findings: tuple[Finding, ...]

    @property
    def safe(self) -> bool:
        return not self.findings

    def to_primitive(self) -> dict[str, object]:
        return {
            "safe": self.safe,
            "findings": [
                {
                    "code": f.code,
                    "message": f.message,
                    "decision": f.decision.value,
                    "resource": f.resource,
                }
                for f in self.findings
            ],
        }


def compare_contracts(baseline: TaskContract, candidate: TaskContract) -> DriftReport:
    findings: list[Finding] = []
    findings.extend(_write_expansion(baseline, candidate))
    findings.extend(_protection_relaxation(baseline, candidate))
    findings.extend(_new_irreversible(baseline, candidate))
    findings.extend(_authority_removed(baseline, candidate))
    findings.extend(_approvals_removed(baseline, candidate))
    return DriftReport(tuple(sorted(findings, key=lambda f: (f.code, f.resource or ""))))


def _write_expansion(baseline: TaskContract, candidate: TaskContract) -> list[Finding]:
    old_write_resources = {
        op.resource for op in baseline.operations if op.kind.is_mutation
    }
    result: list[Finding] = []
    for op in candidate.operations:
        if not op.kind.is_mutation or op.resource in old_write_resources:
            continue
        if not any(contains_scope(scope, op.resource) for scope in baseline.authorized_scope):
            result.append(
                Finding(
                    code="PFL-DRIFT-WRITE-EXPANDED",
                    message=f"Candidate adds mutation outside baseline authorized scope: '{op.resource}'.",
                    decision=Decision.BLOCKED,
                    resource=op.resource,
                )
            )
    return result


def _protection_relaxation(baseline: TaskContract, candidate: TaskContract) -> list[Finding]:
    result: list[Finding] = []
    for protected in baseline.protected_scope:
        if not any(contains_scope(new, protected) for new in candidate.protected_scope):
            result.append(
                Finding(
                    code="PFL-DRIFT-PROTECTION-RELAXED",
                    message=f"Candidate no longer protects baseline scope '{protected}'.",
                    decision=Decision.CONFLICT,
                    resource=protected,
                )
            )
    return result


def _new_irreversible(baseline: TaskContract, candidate: TaskContract) -> list[Finding]:
    old = {(op.kind.value, op.resource) for op in baseline.operations if op.irreversible}
    result: list[Finding] = []
    for op in candidate.operations:
        identity = (op.kind.value, op.resource)
        if op.irreversible and identity not in old:
            result.append(
                Finding(
                    code="PFL-DRIFT-IRREVERSIBLE-ADDED",
                    message=f"Candidate adds irreversible operation '{op.kind.value}' on '{op.resource}'.",
                    decision=Decision.BLOCKED,
                    resource=op.resource,
                )
            )
    return result


def _authority_removed(baseline: TaskContract, candidate: TaskContract) -> list[Finding]:
    removed = sorted(set(baseline.authority_sources) - set(candidate.authority_sources))
    return [
        Finding(
            code="PFL-DRIFT-AUTHORITY-REMOVED",
            message=f"Candidate removes authority source '{source}'.",
            decision=Decision.CONFLICT,
            resource=source,
        )
        for source in removed
    ]


def _approvals_removed(baseline: TaskContract, candidate: TaskContract) -> list[Finding]:
    removed = sorted(set(baseline.approvals) - set(candidate.approvals))
    return [
        Finding(
            code="PFL-DRIFT-APPROVAL-REMOVED",
            message=f"Candidate removes previously explicit approval '{approval