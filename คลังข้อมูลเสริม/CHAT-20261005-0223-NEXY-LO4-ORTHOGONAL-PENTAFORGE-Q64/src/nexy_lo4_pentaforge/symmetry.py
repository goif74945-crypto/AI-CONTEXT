from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Iterable

from .canonical import canonical_json, digest
from .q64 import Q64


@dataclass(frozen=True)
class SymmetricEntity:
    group: str
    attributes: dict[str, Any]


@dataclass(frozen=True)
class SymmetryState:
    global_state: dict[str, Any]
    entities: tuple[SymmetricEntity, ...]


@dataclass(frozen=True)
class QuotientRepresentative:
    key: str
    digest: str
    original_indices: tuple[int, ...]
    orbit_upper_bound: int


@dataclass(frozen=True)
class SymmetryQuotientReport:
    input_count: int
    representative_count: int
    eliminated_count: int
    reduction_ratio: Q64
    representatives: tuple[QuotientRepresentative, ...]


def _canonical_state(state: SymmetryState) -> tuple[str, int]:
    groups: dict[str, list[str]] = {}
    for entity in state.entities:
        if not entity.group:
            raise ValueError("symmetry group must be non-empty")
        groups.setdefault(entity.group, []).append(canonical_json(entity.attributes))
    orbit = 1
    group_payload: dict[str, list[str]] = {}
    for group in sorted(groups):
        members = sorted(groups[group])
        group_payload[group] = members
        orbit *= math.factorial(len(members))
    payload = {"global": state.global_state, "groups": group_payload}
    return canonical_json(payload), orbit


def quotient_states(states: Iterable[SymmetryState]) -> SymmetryQuotientReport:
    materialized = tuple(states)
    if not materialized:
        raise ValueError("at least one state is required")
    buckets: dict[str, list[int]] = {}
    orbits: dict[str, int] = {}
    for index, state in enumerate(materialized):
        key, orbit = _canonical_state(state)
        buckets.setdefault(key, []).append(index)
        orbits[key] = orbit
    representatives = tuple(
        QuotientRepresentative(
            key=key,
            digest=digest(key),
            original_indices=tuple(buckets[key]),
            orbit_upper_bound=orbits[key],
        )
        for key in sorted(buckets)
    )
    input_count = len(materialized)
    representative_count = len(representatives)
    eliminated = input_count - representative_count
    ratio = Q64.from_ratio(eliminated, input_count)
    return SymmetryQuotientReport(
        input_count=input_count,
        representative_count=representative_count,
        eliminated_count=eliminated,
        reduction_ratio=ratio,
        representatives=representatives,
    )
