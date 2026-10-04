from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import digest, normalize
from .q64 import Q64


@dataclass(frozen=True)
class ObservableContract:
    included_fields: tuple[str, ...]
    ignored_fields: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.included_fields:
            raise ValueError("at least one observable field is required")
        if len(set(self.included_fields)) != len(self.included_fields):
            raise ValueError("included_fields must be unique")
        if set(self.included_fields) & set(self.ignored_fields):
            raise ValueError("field cannot be both included and ignored")


@dataclass(frozen=True)
class TraceMismatch:
    event_index: int
    field: str
    left: Any
    right: Any


@dataclass(frozen=True)
class EquivalenceWitness:
    equivalent: bool
    left_digest: str
    right_digest: str
    event_count_left: int
    event_count_right: int
    compared_cells: int
    matched_cells: int
    match_ratio: Q64
    mismatches: tuple[TraceMismatch, ...]


def _project(trace: tuple[dict[str, Any], ...], contract: ObservableContract) -> tuple[dict[str, Any], ...]:
    projected: list[dict[str, Any]] = []
    for event in trace:
        if not isinstance(event, dict):
            raise TypeError("trace events must be dictionaries")
        row: dict[str, Any] = {}
        for field in contract.included_fields:
            if field not in event:
                raise ValueError(f"missing observable field: {field}")
            row[field] = normalize(event[field])
        projected.append(row)
    return tuple(projected)


def compile_equivalence_witness(
    left: tuple[dict[str, Any], ...],
    right: tuple[dict[str, Any], ...],
    contract: ObservableContract,
) -> EquivalenceWitness:
    left_projected = _project(left, contract)
    right_projected = _project(right, contract)
    left_digest = digest(left_projected)
    right_digest = digest(right_projected)
    mismatches: list[TraceMismatch] = []
    compared = 0
    matched = 0
    overlap = min(len(left_projected), len(right_projected))
    for index in range(overlap):
        for field in contract.included_fields:
            compared += 1
            left_value = left_projected[index][field]
            right_value = right_projected[index][field]
            if left_value == right_value:
                matched += 1
            else:
                mismatches.append(TraceMismatch(index, field, left_value, right_value))
    extra_events = abs(len(left_projected) - len(right_projected))
    if extra_events:
        compared += extra_events * len(contract.included_fields)
    ratio = Q64.one() if compared == 0 else Q64.from_ratio(matched, compared)
    equivalent = len(left_projected) == len(right_projected) and not mismatches
    return EquivalenceWitness(
        equivalent=equivalent,
        left_digest=left_digest,
        right_digest=right_digest,
        event_count_left=len(left_projected),
        event_count_right=len(right_projected),
        compared_cells=compared,
        matched_cells=matched,
        match_ratio=ratio,
        mismatches=tuple(mismatches),
    )
