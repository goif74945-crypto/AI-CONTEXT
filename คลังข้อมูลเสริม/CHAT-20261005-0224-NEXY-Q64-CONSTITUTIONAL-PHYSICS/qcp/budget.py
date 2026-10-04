from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .fixed import Q64


def _validated_vector(values: Mapping[str, Q64], *, allow_empty: bool = False) -> dict[str, Q64]:
    result: dict[str, Q64] = {}
    if not values and not allow_empty:
        raise ValueError("budget vector must not be empty")
    for key, value in values.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("budget dimension must be a non-empty string")
        if not isinstance(value, Q64):
            raise TypeError("budget values must be Q64")
        if value < Q64.zero():
            raise ValueError("budget values cannot be negative")
        result[key] = value
    return dict(sorted(result.items()))


@dataclass(frozen=True, slots=True)
class Reservation:
    reservation_id: str
    vector: Mapping[str, Q64]

    @classmethod
    def create(cls, reservation_id: str, vector: Mapping[str, Q64]) -> "Reservation":
        if not reservation_id.strip():
            raise ValueError("reservation_id must be non-empty")
        return cls(reservation_id, _validated_vector(vector))


@dataclass(frozen=True, slots=True)
class BudgetState:
    caps: Mapping[str, Q64]
    used: Mapping[str, Q64]
    reservations: Mapping[str, Mapping[str, Q64]]

    @classmethod
    def create(cls, caps: Mapping[str, Q64]) -> "BudgetState":
        clean = _validated_vector(caps)
        return cls(clean, {k: Q64.zero() for k in clean}, {})


@dataclass(frozen=True, slots=True)
class BudgetDecision:
    status: str
    reason: str
    bottleneck: str | None = None
    headroom: Q64 | None = None


class VectorBudgetReactor:
    """Reserve and commit non-fungible budget dimensions without scalar averaging."""

    @staticmethod
    def _reserved_totals(state: BudgetState) -> dict[str, Q64]:
        totals = {k: Q64.zero() for k in state.caps}
        for vector in state.reservations.values():
            for dim, value in vector.items():
                totals[dim] = totals[dim] + value
        return totals

    def reserve(self, state: BudgetState, reservation: Reservation) -> tuple[BudgetState, BudgetDecision]:
        if reservation.reservation_id in state.reservations:
            return state, BudgetDecision("FREEZE", "DUPLICATE_RESERVATION")
        unknown = sorted(set(reservation.vector) - set(state.caps))
        if unknown:
            return state, BudgetDecision("FREEZE", "UNKNOWN_DIMENSION", unknown[0], None)

        reserved = self._reserved_totals(state)
        for dim in sorted(reservation.vector):
            projected = state.used[dim] + reserved[dim] + reservation.vector[dim]
            if projected > state.caps[dim]:
                headroom = state.caps[dim] - state.used[dim] - reserved[dim]
                return state, BudgetDecision("FREEZE", "DIMENSION_CAP_EXCEEDED", dim, headroom)

        new_reservations = {k: dict(v) for k, v in state.reservations.items()}
        new_reservations[reservation.reservation_id] = dict(reservation.vector)
        return (
            BudgetState(dict(state.caps), dict(state.used), new_reservations),
            BudgetDecision("PASS", "RESERVED"),
        )

    def commit(self, state: BudgetState, reservation_id: str) -> tuple[BudgetState, BudgetDecision]:
        if reservation_id not in state.reservations:
            return state, BudgetDecision("FREEZE", "UNKNOWN_RESERVATION")
        vector = state.reservations[reservation_id]
        used = dict(state.used)
        for dim, value in vector.items():
            used[dim] = used[dim] + value
            if used[dim] > state.caps[dim]:
                return state, BudgetDecision("FREEZE", "INTERNAL_CAP_VIOLATION", dim, Q64.zero())
        reservations = {k: dict(v) for k, v in state.reservations.items() if k != reservation_id}
        return BudgetState(dict(state.caps), used, reservations), BudgetDecision("PASS", "COMMITTED")

    def release(self, state: BudgetState, reservation_id: str) -> tuple[BudgetState, BudgetDecision]:
        if reservation_id not in state.reservations:
            return state, BudgetDecision("FREEZE", "UNKNOWN_RESERVATION")
        reservations = {k: dict(v) for k, v in state.reservations.items() if k != reservation_id}
        return BudgetState(dict(state.caps), dict(state.used), reservations), BudgetDecision("PASS", "RELEASED")
