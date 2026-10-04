from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from .errors import ContractError


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"
    BLOCKED = "BLOCKED"
    NOT_VERIFIED = "NOT_VERIFIED"
    UNKNOWN = "UNKNOWN"
    CONFLICT = "CONFLICT"


_ALLOWED_INVARIANTS = {
    "exists",
    "equals",
    "type",
    "range",
    "one_of",
    "min_evidence",
    "no_sensitive_keys",
}


@dataclass(frozen=True, slots=True)
class ProviderManifest:
    provider_id: str
    model_id: str
    adapter_version: str
    capabilities: frozenset[str]
    manifest_version: str = "1"

    @property
    def ref(self) -> str:
        return f"{self.provider_id}/{self.model_id}@{self.adapter_version}"

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> "ProviderManifest":
        required = ("provider_id", "model_id", "adapter_version", "capabilities")
        _require_fields(raw, required, "provider manifest")
        caps = raw["capabilities"]
        if not isinstance(caps, list) or not caps or not all(isinstance(x, str) and x for x in caps):
            raise ContractError("capabilities must be a non-empty string list")
        return cls(
            provider_id=_nonempty(raw["provider_id"], "provider_id"),
            model_id=_nonempty(raw["model_id"], "model_id"),
            adapter_version=_nonempty(raw["adapter_version"], "adapter_version"),
            capabilities=frozenset(caps),
            manifest_version=_nonempty(raw.get("manifest_version", "1"), "manifest_version"),
        )


@dataclass(frozen=True, slots=True)
class Invariant:
    kind: str
    path: str = ""
    value: Any = None
    values: tuple[Any, ...] = ()
    minimum: float | int | None = None
    maximum: float | int | None = None

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> "Invariant":
        kind = _nonempty(raw.get("kind"), "invariant.kind")
        if kind not in _ALLOWED_INVARIANTS:
            raise ContractError(f"unsupported invariant kind: {kind}")
        path = raw.get("path", "")
        if not isinstance(path, str):
            raise ContractError("invariant.path must be a string")
        values = raw.get("values", [])
        if not isinstance(values, list):
            raise ContractError("invariant.values must be a list")
        return cls(
            kind=kind,
            path=path,
            value=raw.get("value"),
            values=tuple(values),
            minimum=raw.get("minimum"),
            maximum=raw.get("maximum"),
        )


@dataclass(frozen=True, slots=True)
class CaseContract:
    case_id: str
    request: Any
    required_capabilities: frozenset[str]
    invariants: tuple[Invariant, ...]
    deterministic_paths: tuple[str, ...] = ()
    cross_provider_paths: tuple[str, ...] = ()
    min_observations: int = 1
    contract_version: str = "1"

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> "CaseContract":
        _require_fields(raw, ("case_id", "request", "required_capabilities", "invariants"), "case")
        caps = raw["required_capabilities"]
        invs = raw["invariants"]
        if not isinstance(caps, list) or not all(isinstance(x, str) and x for x in caps):
            raise ContractError("required_capabilities must be a string list")
        if not isinstance(invs, list):
            raise ContractError("invariants must be a list")
        deterministic_paths = _string_list(raw.get("deterministic_paths", []), "deterministic_paths")
        cross_provider_paths = _string_list(raw.get("cross_provider_paths", []), "cross_provider_paths")
        min_observations = raw.get("min_observations", 1)
        if not isinstance(min_observations, int) or isinstance(min_observations, bool) or min_observations < 1:
            raise ContractError("min_observations must be a positive integer")
        return cls(
            case_id=_nonempty(raw["case_id"], "case_id"),
            request=raw["request"],
            required_capabilities=frozenset(caps),
            invariants=tuple(Invariant.from_dict(x) for x in invs),
            deterministic_paths=deterministic_paths,
            cross_provider_paths=cross_provider_paths,
            min_observations=min_observations,
            contract_version=_nonempty(raw.get("contract_version", "1"), "contract_version"),
        )


@dataclass(frozen=True, slots=True)
class Observation:
    observation_id: str
    case_id: str
    provider_ref: str
    request_hash: str
    output: Any
    evidence: tuple[Mapping[str, Any], ...]
    trace_id: str
    error_code: str | None = None
    adapter_meta: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> "Observation":
        required = (
            "observation_id",
            "case_id",
            "provider_ref",
            "request_hash",
            "output",
            "evidence",
            "trace_id",
        )
        _require_fields(raw, required, "observation")
        evidence = raw["evidence"]
        if not isinstance(evidence, list) or not all(isinstance(x, dict) for x in evidence):
            raise ContractError("evidence must be a list of objects")
        adapter_meta = raw.get("adapter_meta", {})
        if not isinstance(adapter_meta, dict):
            raise ContractError("adapter_meta must be an object")
        error_code = raw.get("error_code")
        if error_code is not None and not isinstance(error_code, str):
            raise ContractError("error_code must be null or string")
        return cls(
            observation_id=_nonempty(raw["observation_id"], "observation_id"),
            case_id=_nonempty(raw["case_id"], "case_id"),
            provider_ref=_nonempty(raw["provider_ref"], "provider_ref"),
            request_hash=_nonempty(raw["request_hash"], "request_hash"),
            output=raw["output"],
            evidence=tuple(evidence),
            trace_id=_nonempty(raw["trace_id"], "trace_id"),
            error_code=error_code,
            adapter_meta=adapter_meta,
        )


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    status: Status
    message: str
    observation_id: str | None = None
    path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "status": self.status.value,
            "message": self.message,
            "observation_id": self.observation_id,
            "path": self.path,
        }


@dataclass(frozen=True, slots=True)
class Report:
    case_id: str
    provider_ref: str
    status: Status
    findings: tuple[Finding, ...]
    evidence_fingerprint: str
    observation_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "provider_ref": self.provider_ref,
            "status": self.status.value,
            "findings": [f.to_dict() for f in self.findings],
            "evidence_fingerprint": self.evidence_fingerprint,
            "observation_count": self.observation_count,
        }


def _nonempty(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{name} must be a non-empty string")
    return value


def _string_list(value: Any, name: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(x, str) and x for x in value):
        raise ContractError(f"{name} must be a string list")
    return tuple(value)


def _require_fields(raw: Mapping[str, Any], fields: tuple[str, ...], name: str) -> None:
    missing = [field for field in fields if field not in raw]
    if missing:
        raise ContractError(f"{name} missing required fields: {', '.join(missing)}")
