from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, asdict
from numbers import Real
from math import isfinite
from typing import Any, Iterable, Mapping

from core.canonical import fingerprint


OBSERVED_ONLY = "OBSERVED_PATTERN_NOT_REQUIREMENT"


@dataclass(frozen=True)
class Pattern:
    kind: str
    field: str
    detail: Mapping[str, Any]
    support: int
    total: int
    authority: str = OBSERVED_ONLY

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MiningReport:
    status: str
    event_count: int
    patterns: tuple[Pattern, ...]
    report_fingerprint: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "event_count": self.event_count,
            "patterns": [p.as_dict() for p in self.patterns],
            "report_fingerprint": self.report_fingerprint,
        }


def _is_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (str, bool, int, float))


def _stable_scalar(value: Any) -> tuple[str, str]:
    # Type tag prevents True from colliding with 1 and 1 from colliding with 1.0.
    return (type(value).__name__, repr(value))


def mine_contracts(
    events: Iterable[Mapping[str, Any]],
    *,
    max_enum_cardinality: int = 6,
    min_implication_support: int = 2,
) -> MiningReport:
    """Mine deterministic observational patterns without promoting them to authority.

    The miner intentionally emits only patterns that are exactly true for the supplied
    finite trace set. It does not infer causality, necessity, or normative requirements.
    """
    raw_events = list(events)
    if any(not isinstance(e, Mapping) for e in raw_events):
        raise TypeError("every event must be a mapping")
    rows = [dict(e) for e in raw_events]
    if max_enum_cardinality < 1:
        raise ValueError("max_enum_cardinality must be >= 1")
    if min_implication_support < 1:
        raise ValueError("min_implication_support must be >= 1")
    for row in rows:
        for key, value in row.items():
            if not isinstance(key, str):
                raise TypeError("event field names must be strings")
            if isinstance(value, float) and not isfinite(value):
                raise ValueError("non-finite float values are not supported")

    total = len(rows)
    if total == 0:
        payload = {"status": "NO_DATA", "event_count": 0, "patterns": []}
        return MiningReport("NO_DATA", 0, (), fingerprint(payload))

    all_fields = sorted({k for row in rows for k in row if isinstance(k, str)})
    patterns: list[Pattern] = []

    required = [field for field in all_fields if all(field in row for row in rows)]
    for field in required:
        patterns.append(Pattern("REQUIRED_FIELD", field, {"present_in_all": True}, total, total))

    categorical_values: dict[str, list[Any]] = {}
    for field in required:
        values = [row[field] for row in rows]
        if all(_is_scalar(v) for v in values):
            tagged = {_stable_scalar(v) for v in values}
            if len(tagged) == 1:
                patterns.append(Pattern("CONSTANT", field, {"value": values[0]}, total, total))
            if len(tagged) <= max_enum_cardinality:
                counts = Counter(_stable_scalar(v) for v in values)
                render = [
                    {"type": t, "repr": r, "count": counts[(t, r)]}
                    for t, r in sorted(counts)
                ]
                patterns.append(Pattern("FINITE_ENUM_OBSERVED", field, {"values": render}, total, total))
                categorical_values[field] = values

        numeric = [v for v in values if isinstance(v, Real) and not isinstance(v, bool)]
        if len(numeric) == total:
            patterns.append(
                Pattern(
                    "OBSERVED_NUMERIC_RANGE",
                    field,
                    {"min": min(numeric), "max": max(numeric)},
                    total,
                    total,
                )
            )

    # Exact implication mining for categorical fields. We only emit A=>B when every
    # observed row satisfying A also satisfies B and A has adequate support.
    atoms: list[tuple[str, Any]] = []
    for field, values in sorted(categorical_values.items()):
        unique: dict[tuple[str, str], Any] = {}
        for value in values:
            unique.setdefault(_stable_scalar(value), value)
        for key in sorted(unique):
            atoms.append((field, unique[key]))

    for left_field, left_value in atoms:
        left_tag = _stable_scalar(left_value)
        left_idx = [i for i, row in enumerate(rows) if _stable_scalar(row[left_field]) == left_tag]
        if len(left_idx) < min_implication_support:
            continue
        for right_field, right_value in atoms:
            if right_field == left_field:
                continue
            right_tag = _stable_scalar(right_value)
            if all(_stable_scalar(rows[i][right_field]) == right_tag for i in left_idx):
                patterns.append(
                    Pattern(
                        "OBSERVED_IMPLICATION",
                        left_field,
                        {
                            "if_equals": left_value,
                            "then_field": right_field,
                            "then_equals": right_value,
                        },
                        len(left_idx),
                        total,
                    )
                )

    patterns.sort(key=lambda p: (p.kind, p.field, repr(dict(p.detail)), p.support, p.total))
    payload = {
        "status": "READY",
        "event_count": total,
        "patterns": [p.as_dict() for p in patterns],
    }
    return MiningReport("READY", total, tuple(patterns), fingerprint(payload))
