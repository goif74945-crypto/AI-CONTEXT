from __future__ import annotations

from dataclasses import dataclass
from numbers import Real
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class CandidateInvariant:
    kind: str
    field: str
    parameters: tuple[Any, ...]
    training_support: int
    holdout_checked: int
    holdout_violations: int
    status: str


class TraceInvariantCandidateMiner:
    """Mines deterministic *candidate* invariants from traces.

    Output is never canonical authority. Holdout support can strengthen a candidate but cannot promote it to law.
    """

    @staticmethod
    def _common_fields(records: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
        if not records:
            return ()
        fields = set(records[0])
        for record in records[1:]:
            fields &= set(record)
        return tuple(sorted(fields))

    @staticmethod
    def _holds(kind: str, params: tuple[Any, ...], values: Sequence[Any]) -> int:
        violations = 0
        if kind == "constant":
            expected = params[0]
            violations += sum(v != expected for v in values)
        elif kind == "numeric_range":
            low, high = params
            violations += sum(not isinstance(v, Real) or not (low <= v <= high) for v in values)
        elif kind == "nondecreasing":
            violations += sum(b < a for a, b in zip(values, values[1:]))
        elif kind == "allowed_values":
            allowed = set(params)
            violations += sum(v not in allowed for v in values)
        else:
            raise ValueError(f"unsupported invariant kind: {kind}")
        return violations

    @classmethod
    def mine(
        cls,
        training: Iterable[Mapping[str, Any]],
        holdout: Iterable[Mapping[str, Any]] = (),
        max_enum_values: int = 8,
    ) -> tuple[CandidateInvariant, ...]:
        train = tuple(training)
        test = tuple(holdout)
        if len(train) < 2:
            raise ValueError("at least two training records are required")
        if max_enum_values < 1:
            raise ValueError("max_enum_values must be positive")

        candidates: list[tuple[str, str, tuple[Any, ...]]] = []
        for field in cls._common_fields(train):
            values = [r[field] for r in train]
            first = values[0]
            if all(v == first for v in values):
                candidates.append(("constant", field, (first,)))
            if all(isinstance(v, Real) and not isinstance(v, bool) for v in values):
                candidates.append(("numeric_range", field, (min(values), max(values))))
                if all(b >= a for a, b in zip(values, values[1:])):
                    candidates.append(("nondecreasing", field, ()))
            else:
                unique = tuple(dict.fromkeys(values))
                if len(unique) <= max_enum_values:
                    candidates.append(("allowed_values", field, unique))

        results: list[CandidateInvariant] = []
        holdout_fields = set(cls._common_fields(test)) if test else set()
        for kind, field, params in candidates:
            if test and field in holdout_fields:
                values = [r[field] for r in test]
                violations = cls._holds(kind, params, values)
                status = "SUPPORTED_BY_HOLDOUT" if violations == 0 else "REFUTED_BY_HOLDOUT"
                checked = len(values)
            else:
                violations = 0
                checked = 0
                status = "CANDIDATE_NOT_VERIFIED"
            results.append(CandidateInvariant(kind, field, params, len(train), checked, violations, status))

        return tuple(sorted(results, key=lambda c: (c.field, c.kind)))
