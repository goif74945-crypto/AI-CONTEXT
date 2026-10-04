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
            target=str(raw.get("target",