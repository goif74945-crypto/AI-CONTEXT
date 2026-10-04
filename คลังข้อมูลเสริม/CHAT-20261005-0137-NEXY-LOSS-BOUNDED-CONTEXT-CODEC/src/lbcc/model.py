from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping

SCHEMA_VERSION = "lbcc/0.1"
PPM = 1_000_000


def _freeze_json(value: Any, path: str = "metadata") -> Any:
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        raise ValueError(f"{path} must not contain floats; use integer/fixed-point values")
    if isinstance(value, Mapping):
        frozen: dict[str, Any] = {}
        for key, child in value.items():
            if not isinstance(key, str):
                raise ValueError(f"{path} keys must be strings")
            frozen[key] = _freeze_json(child, f"{path}.{key}")
        return MappingProxyType(frozen)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(child, f"{path}[]") for child in value)
    raise ValueError(f"{path} contains unsupported type: {type(value).__name__}")


class TruthClass(str, Enum):
    SOURCE_FACT = "SOURCE_FACT"
    REPO_FACT = "REPO_FACT"
    RUNTIME_FACT = "RUNTIME_FACT"
    EXTERNAL_FACT = "EXTERNAL_FACT"
    INFERENCE = "INFERENCE"
    ASSUMPTION = "ASSUMPTION"
    UNKNOWN = "UNKNOWN"
    CONFLICT = "CONFLICT"
    NOT_VERIFIED = "NOT_VERIFIED"


class CodecStatus(str, Enum):
    PASS = "PASS"
    FREEZE = "FREEZE"


@dataclass(frozen=True, slots=True)
class ContextAtom:
    atom_id: str
    text: str
    truth_class: TruthClass
    authority_rank: int = 0
    provenance: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    immutable: bool = False
    tags: tuple[str, ...] = ()
    valid_from: str | None = None
    valid_to: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.atom_id or not self.atom_id.strip():
            raise ValueError("atom_id must be non-empty")
        if not self.text or not self.text.strip():
            raise ValueError(f"atom {self.atom_id!r} text must be non-empty")
        if not 0 <= self.authority_rank <= 100:
            raise ValueError(f"atom {self.atom_id!r} authority_rank must be 0..100")
        for field_name, values in (
            ("provenance", self.provenance),
            ("evidence", self.evidence),
            ("tags", self.tags),
        ):
            normalized = tuple(values)
            if any(not isinstance(v, str) or not v for v in normalized):
                raise ValueError(f"atom {self.atom_id!r} {field_name} must contain non-empty strings")
            object.__setattr__(self, field_name, normalized)
        object.__setattr__(self, "metadata", _freeze_json(self.metadata))


@dataclass(frozen=True, slots=True)
class ContextBundle:
    bundle_id: str
    atoms: tuple[ContextAtom, ...]

    def __post_init__(self) -> None:
        if not self.bundle_id or not self.bundle_id.strip():
            raise ValueError("bundle_id must be non-empty")
        ids = [a.atom_id for a in self.atoms]
        if len(ids) != len(set(ids)):
            duplicates = sorted({x for x in ids if ids.count(x) > 1})
            raise ValueError(f"duplicate atom_id(s): {', '.join(duplicates)}")


@dataclass(frozen=True, slots=True)
class CodecPolicy:
    max_capsule_bytes: int
    max_loss_ppm: int = 0
    protect_unknown_conflict: bool = True
    protected_authority_rank: int = 95
    allow_sensitive: bool = False

    def __post_init__(self) -> None:
        if self.max_capsule_bytes <= 0:
            raise ValueError("max_capsule_bytes must be > 0")
        if not 0 <= self.max_loss_ppm <= PPM:
            raise ValueError("max_loss_ppm must be 0..1_000_000")
        if not 0 <= self.protected_authority_rank <= 100:
            raise ValueError("protected_authority_rank must be 0..100")


@dataclass(frozen=True, slots=True)
class DroppedRef:
    atom_id: str
    atom_sha256: str
    importance: int


@dataclass(frozen=True, slots=True)
class ContextCapsule:
    schema_version: str
    bundle_id: str
    source_commitment_sha256: str
    retained_atoms: tuple[ContextAtom, ...]
    dropped_count: int
    dropped_commitment_sha256: str
    total_importance: int
    dropped_importance: int
    loss_ppm: int


@dataclass(frozen=True, slots=True)
class CodecMetrics:
    source_atoms: int
    retained_atoms: int
    dropped_atoms: int
    capsule_bytes: int
    total_importance: int
    dropped_importance: int
    loss_ppm: int


@dataclass(frozen=True, slots=True)
class CodecResult:
    schema_version: str
    status: CodecStatus
    reason: str | None
    capsule: ContextCapsule | None
    loss_ledger: tuple[DroppedRef, ...]
    metrics: CodecMetrics
