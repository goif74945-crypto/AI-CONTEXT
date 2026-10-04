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


def overlaps_scope(left: str, ri