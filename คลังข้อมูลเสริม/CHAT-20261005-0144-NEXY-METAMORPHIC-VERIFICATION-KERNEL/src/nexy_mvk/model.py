from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
from types import MappingProxyType
from typing import Any, Callable, Mapping, Protocol, Sequence

JsonScalar = None | bool | int | float | str
JsonValue = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]


class RelationStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"
    NOT_VERIFIED = "NOT_VERIFIED"


@dataclass(frozen=True, slots=True)
class Case:
    """Immutable verification input presented to a target adapter."""

    prompt: str
    context: Mapping[str, Any] = field(default_factory=dict)
    authority: tuple[str, ...] = ()
    permissions: frozenset[str] = frozenset()
    evidence: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.prompt, str) or not self.prompt.strip():
            raise ValueError("prompt must be a non-empty string")
        object.__setattr__(self, "context", MappingProxyType(dict(self.context)))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
        object.__setattr__(self, "authority", tuple(self.authority))
        object.__setattr__(self, "permissions", frozenset(self.permissions))
        object.__setattr__(self, "evidence", tuple(self.evidence))

    def evolve(self, **changes: Any) -> "Case":
        return replace(self, **changes)


@dataclass(frozen=True, slots=True)
class Observation:
    """Normalized externally observable result from the target system."""

    status: str
    released: bool
    payload: Any = None
    side_effects: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.status, str) or not self.status.strip():
            raise ValueError("status must be a non-empty string")
        object.__setattr__(self, "side_effects", tuple(self.side_effects))
        object.__setattr__(self, "evidence", tuple(self.evidence))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class OracleResult:
    passed: bool
    reason: str
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.reason:
            raise ValueError("oracle result reason must not be empty")
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))


class SystemAdapter(Protocol):
    def __call__(self, case: Case) -> Observation: ...


Mutator = Callable[[Case], Case]
Oracle = Callable[[Observation, Observation, Case, Case], OracleResult]
Projection = Callable[[Observation], Any]


@dataclass(frozen=True, slots=True)
class MetamorphicRelation:
    relation_id: str
    description: str
    mutator: Mutator
    oracle: Oracle
    risk: str = "medium"
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.relation_id.strip():
            raise ValueError("relation_id must not be empty")
        if not self.description.strip():
            raise ValueError("description must not be empty")
        if self.risk not in {"low", "medium", "high", "critical"}:
            raise ValueError("risk must be low|medium|high|critical")


@dataclass(frozen=True, slots=True)
class RelationResult:
    relation_id: str
    status: RelationStatus
    reason: str
    seed_case_hash: str
    derived_case_hash: str | None
    baseline_observation_hash: str | None
    derived_observation_hash: str | None
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))


@dataclass(frozen=True, slots=True)
class VerificationReport:
    run_id: str
    results: tuple[RelationResult, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "results", tuple(self.results))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    @property
    def passed(self) -> bool:
        return bool(self.results) and all(r.status is RelationStatus.PASS for r in self.results)

    @property
    def counts(self) -> Mapping[str, int]:
        counts = {s.value: 0 for s in RelationStatus}
        for result in self.results:
            counts[result.status.value] += 1
        return MappingProxyType(counts)
