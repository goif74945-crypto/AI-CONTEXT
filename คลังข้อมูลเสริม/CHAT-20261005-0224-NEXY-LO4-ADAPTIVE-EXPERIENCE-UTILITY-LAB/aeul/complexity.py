from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .common import ContractError, fingerprint, require_text, require_unit
from .q64 import Q64


@dataclass(frozen=True, slots=True)
class ComplexityWeights:
    persistence: Q64
    migration: Q64
    public_contract: Q64
    rollback: Q64

    def __post_init__(self) -> None:
        total = Q64.zero()
        for field in ("persistence", "migration", "public_contract", "rollback"):
            value = getattr(self, field)
            require_unit(value, field)
            total = total + value
        if total != Q64.one():
            raise ContractError("complexity weights must sum exactly to 1.0")


@dataclass(frozen=True, slots=True)
class ChangeSurface:
    surface_id: str
    touch_weight: Q64
    persistence: Q64
    migration: Q64
    public_contract: Q64
    rollback: Q64

    def __post_init__(self) -> None:
        require_text(self.surface_id, "surface_id")
        for field in ("touch_weight", "persistence", "migration", "public_contract", "rollback"):
            require_unit(getattr(self, field), field)
        if self.touch_weight.raw == 0:
            raise ContractError("touch_weight must be > 0")


@dataclass(frozen=True, slots=True)
class ComplexityDecision:
    status: str
    total_tax: Q64
    normalized_tax: Q64
    surface_count: int
    max_surface_tax: Q64
    reason: str
    fingerprint: str


def assess_complexity(
    surfaces: Iterable[ChangeSurface],
    *,
    weights: ComplexityWeights,
    max_total_tax: Q64,
    max_surface_tax: Q64,
) -> ComplexityDecision:
    if not isinstance(max_total_tax, Q64) or max_total_tax.raw < 0:
        raise ContractError("max_total_tax must be non-negative Q64.64")
    if not isinstance(max_surface_tax, Q64) or max_surface_tax.raw < 0:
        raise ContractError("max_surface_tax must be non-negative Q64.64")
    items = list(surfaces)
    ids = [s.surface_id for s in items]
    if len(ids) != len(set(ids)):
        return _result("FREEZE", Q64.zero(), Q64.zero(), len(items), Q64.zero(), "DUPLICATE_SURFACE_ID")
    if not items:
        return _result("PASS", Q64.zero(), Q64.zero(), 0, Q64.zero(), "NO_CHANGE_SURFACE")

    total_tax = Q64.zero()
    total_touch = Q64.zero()
    max_single = Q64.zero()
    for surface in items:
        intrinsic = (
            weights.persistence * surface.persistence
            + weights.migration * surface.migration
            + weights.public_contract * surface.public_contract
            + weights.rollback * surface.rollback
        )
        tax = surface.touch_weight * intrinsic
        total_tax = total_tax + tax
        total_touch = total_touch + surface.touch_weight
        if tax.raw > max_single.raw:
            max_single = tax
    normalized = total_tax / total_touch
    if max_single.raw > max_surface_tax.raw:
        return _result("REJECT", total_tax, normalized, len(items), max_single, "SINGLE_SURFACE_TAX_EXCEEDS_LIMIT")
    if total_tax.raw > max_total_tax.raw:
        return _result("REJECT", total_tax, normalized, len(items), max_single, "TOTAL_COMPLEXITY_TAX_EXCEEDS_LIMIT")
    return _result("PASS", total_tax, normalized, len(items), max_single, "COMPLEXITY_WITHIN_BUDGET")


def _result(status: str, total: Q64, normalized: Q64, count: int, max_single: Q64, reason: str) -> ComplexityDecision:
    core = {
        "status": status,
        "total_tax": total,
        "normalized_tax": normalized,
        "surface_count": count,
        "max_surface_tax": max_single,
        "reason": reason,
    }
    return ComplexityDecision(status, total, normalized, count, max_single, reason, fingerprint(core))
