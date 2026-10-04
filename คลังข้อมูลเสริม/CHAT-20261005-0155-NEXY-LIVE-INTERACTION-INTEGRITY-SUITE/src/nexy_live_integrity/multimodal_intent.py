from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .common import GateStatus, canonical_digest, normalized_string_tuple, normalized_text, require_nonempty


@dataclass(frozen=True, slots=True)
class IntentContract:
    modality: str
    objective: str
    operation: str
    targets: tuple[str, ...]
    mode: str
    allow_external: bool
    deterministic_required: bool
    authority_scope: str
    constraints: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "modality", require_nonempty("modality", self.modality).lower())
        object.__setattr__(self, "objective", normalized_text(self.objective))
        object.__setattr__(self, "operation", require_nonempty("operation", self.operation).upper())
        object.__setattr__(self, "targets", normalized_string_tuple(self.targets, name="target"))
        object.__setattr__(self, "mode", require_nonempty("mode", self.mode).lower())
        object.__setattr__(self, "authority_scope", require_nonempty("authority_scope", self.authority_scope))
        if type(self.allow_external) is not bool:
            raise TypeError("allow_external must be boolean")
        if type(self.deterministic_required) is not bool:
            raise TypeError("deterministic_required must be boolean")
        normalized_constraints: list[tuple[str, str]] = []
        for key, value in self.constraints:
            normalized_constraints.append((require_nonempty("constraint key", key), normalized_text(value)))
        if len({k for k, _ in normalized_constraints}) != len(normalized_constraints):
            raise ValueError("constraints contain duplicate keys")
        object.__setattr__(self, "constraints", tuple(sorted(normalized_constraints)))

    @property
    def semantic_payload(self) -> Mapping[str, object]:
        return {
            "objective": self.objective,
            "operation": self.operation,
            "targets": self.targets,
            "mode": self.mode,
            "allow_external": self.allow_external,
            "deterministic_required": self.deterministic_required,
            "authority_scope": self.authority_scope,
            "constraints": self.constraints,
        }

    @property
    def semantic_fingerprint(self) -> str:
        return canonical_digest(self.semantic_payload)


@dataclass(frozen=True, slots=True)
class IntentEquivalenceResult:
    status: GateStatus
    code: str
    fingerprint: str
    reference_modality: str | None
    mismatches: tuple[str, ...]

    @property
    def allowed(self) -> bool:
        return self.status is GateStatus.PASS


class IntentEquivalenceGate:
    """Checks adapter-produced intent contracts across text/voice/image/etc.

    The gate does not infer semantic equivalence from raw media. Each modality
    adapter must first produce the explicit contract. Any critical-field mismatch
    freezes instead of being auto-reconciled.
    """

    @staticmethod
    def compare(contracts: Sequence[IntentContract], *, required_modalities: Sequence[str] = ()) -> IntentEquivalenceResult:
        if not contracts:
            return IntentEquivalenceResult(GateStatus.REJECT, "INTENT_NO_CONTRACTS", canonical_digest([]), None, ("no_contracts",))
        modalities = [c.modality for c in contracts]
        if len(set(modalities)) != len(modalities):
            return IntentEquivalenceResult(GateStatus.FREEZE, "INTENT_DUPLICATE_MODALITY", canonical_digest(contracts), None, ("duplicate_modality",))
        required = {require_nonempty("required modality", m).lower() for m in required_modalities}
        missing = tuple(sorted(required - set(modalities)))
        if missing:
            return IntentEquivalenceResult(GateStatus.FREEZE, "INTENT_REQUIRED_MODALITY_MISSING", canonical_digest(contracts), contracts[0].modality, tuple(f"missing:{m}" for m in missing))

        reference = contracts[0]
        mismatches: list[str] = []
        fields = (
            "objective",
            "operation",
            "targets",
            "mode",
            "allow_external",
            "deterministic_required",
            "authority_scope",
            "constraints",
        )
        for other in contracts[1:]:
            for field in fields:
                if getattr(other, field) != getattr(reference, field):
                    mismatches.append(f"{other.modality}:{field}")
        fingerprint = canonical_digest([c.semantic_payload for c in sorted(contracts, key=lambda c: c.modality)])
        if mismatches:
            return IntentEquivalenceResult(GateStatus.FREEZE, "INTENT_SEMANTIC_DIVERGENCE", fingerprint, reference.modality, tuple(sorted(mismatches)))
        return IntentEquivalenceResult(GateStatus.PASS, "INTENT_EQUIVALENT", fingerprint, reference.modality, ())
