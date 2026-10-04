from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .fixed import Q64


@dataclass(frozen=True, slots=True)
class UncertaintyStage:
    stage_id: str
    incoming: Q64
    introduced: Q64
    resolved: Q64
    outgoing: Q64
    evidence_receipts: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.stage_id.strip():
            raise ValueError("stage_id must be non-empty")
        for name in ("incoming", "introduced", "resolved", "outgoing"):
            value = getattr(self, name)
            if not isinstance(value, Q64):
                raise TypeError(f"{name} must be Q64")
            if value < Q64.zero():
                raise ValueError(f"{name} cannot be negative")
        if any(not receipt.strip() for receipt in self.evidence_receipts):
            raise ValueError("evidence receipt IDs must be non-empty")


@dataclass(frozen=True, slots=True)
class UncertaintyDecision:
    status: str
    reason: str
    final_mass: Q64
    failing_stage: str | None = None


class UncertaintyMassCompiler:
    """Prevent uncertainty from disappearing without an explicit evidence-backed resolution."""

    def compile(self, stages: Iterable[UncertaintyStage]) -> UncertaintyDecision:
        ordered = tuple(stages)
        if not ordered:
            return UncertaintyDecision("FREEZE", "NO_STAGES", Q64.zero(), None)
        if len({s.stage_id for s in ordered}) != len(ordered):
            return UncertaintyDecision("FREEZE", "DUPLICATE_STAGE", Q64.zero(), None)

        previous: Q64 | None = None
        for stage in ordered:
            if previous is not None and stage.incoming != previous:
                return UncertaintyDecision("FREEZE", "CHAIN_MISMATCH", previous, stage.stage_id)
            if stage.resolved > Q64.zero() and not stage.evidence_receipts:
                return UncertaintyDecision("FREEZE", "UNSUPPORTED_RESOLUTION", stage.incoming, stage.stage_id)
            left = stage.incoming + stage.introduced
            right = stage.outgoing + stage.resolved
            # Independent decimal-to-Q64 quantization can create at most a one-ULP
            # boundary residual in otherwise equivalent conservation equations.
            # This is an exact raw-unit rule, not a floating epsilon.
            if abs(left.raw - right.raw) > 1:
                return UncertaintyDecision("FREEZE", "MASS_NOT_CONSERVED", stage.incoming, stage.stage_id)
            previous = stage.outgoing

        assert previous is not None
        return UncertaintyDecision("PASS", "CONSERVED", previous, None)
