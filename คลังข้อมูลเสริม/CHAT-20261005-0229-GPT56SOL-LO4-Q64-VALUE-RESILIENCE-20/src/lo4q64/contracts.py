from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from .q64 import Q64, ensure_unit


class Decision(str, Enum):
    ACT = "ACT"
    HOLD = "HOLD"
    ESCALATE = "ESCALATE"
    FREEZE = "FREEZE"


@dataclass(frozen=True, slots=True)
class Evaluation:
    concept_id: str
    readiness: Q64
    confidence: Q64
    decision: Decision
    rationale_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        ensure_unit(self.readiness)
        ensure_unit(self.confidence)
        if not self.rationale_codes:
            raise ValueError("rationale_codes must not be empty")

    def as_dict(self) -> dict[str, object]:
        return {
            "concept_id": self.concept_id,
            "readiness_raw_q64": self.readiness.raw,
            "readiness": self.readiness.to_decimal_string(),
            "confidence_raw_q64": self.confidence.raw,
            "confidence": self.confidence.to_decimal_string(),
            "decision": self.decision.value,
            "rationale_codes": list(self.rationale_codes),
        }


@dataclass(frozen=True, slots=True)
class ConceptSpec:
    concept_id: str
    title: str
    required_inputs: tuple[str, ...]
    summary: str


def validate_inputs(spec: ConceptSpec, values: Mapping[str, Q64]) -> None:
    keys = set(values)
    required = set(spec.required_inputs)
    missing = required - keys
    extra = keys - required
    if missing:
        raise ValueError(f"{spec.concept_id}: missing inputs: {sorted(missing)}")
    if extra:
        raise ValueError(f"{spec.concept_id}: unexpected inputs: {sorted(extra)}")
    for key in spec.required_inputs:
        ensure_unit(values[key])


def band(readiness: Q64, confidence: Q64) -> Decision:
    ensure_unit(readiness)
    ensure_unit(confidence)
    # Confidence is a release gate, not a cosmetic annotation.
    if confidence.raw < Q64.from_ratio(1, 2).raw:
        return Decision.FREEZE
    if readiness.raw >= Q64.from_ratio(3, 4).raw:
        return Decision.ACT
    if readiness.raw >= Q64.from_ratio(1, 2).raw:
        return Decision.HOLD
    if readiness.raw >= Q64.from_ratio(1, 4).raw:
        return Decision.ESCALATE
    return Decision.FREEZE
