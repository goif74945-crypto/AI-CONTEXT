"""Behavioral Canary Compiler/Runner (BCC).

A canary captures compact, deterministic behavioral fingerprints at integration
boundaries. It is intentionally not deployment proof; it is a fast drift signal
that can gate more expensive verification.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Callable, Iterable, Mapping


def _canonicalize(
    value: Any,
    ignored_top_level_fields: frozenset[str],
    *,
    depth: int = 0,
) -> Any:
    if isinstance(value, Mapping):
        return {
            str(key): _canonicalize(inner, ignored_top_level_fields, depth=depth + 1)
            for key, inner in sorted(value.items(), key=lambda pair: str(pair[0]))
            if not (depth == 0 and str(key) in ignored_top_level_fields)
        }
    if isinstance(value, (list, tuple)):
        return [
            _canonicalize(item, ignored_top_level_fields, depth=depth + 1)
            for item in value
        ]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"unsupported output type for canonical canary encoding: {type(value).__name__}")


def _digest(value: Any, ignored_top_level_fields: frozenset[str]) -> str:
    payload = json.dumps(
        _canonicalize(value, ignored_top_level_fields),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True, slots=True)
class CanaryCase:
    case_id: str
    request: Any

    def __post_init__(self) -> None:
        if not self.case_id.strip():
            raise ValueError("case_id must be non-empty")


@dataclass(frozen=True, slots=True)
class CanaryBaseline:
    signatures: Mapping[str, str]
    ignored_top_level_fields: frozenset[str] = frozenset()


@dataclass(frozen=True, slots=True)
class CanaryWitness:
    case_id: str
    expected_signature: str
    observed_signature: str
    status: str


@dataclass(frozen=True, slots=True)
class CanaryResult:
    status: str
    witnesses: tuple[CanaryWitness, ...]


def _validate_cases(cases: Iterable[CanaryCase]) -> tuple[CanaryCase, ...]:
    ordered = tuple(sorted(cases, key=lambda case: case.case_id))
    if not ordered:
        raise ValueError("at least one canary case is required")
    if len({case.case_id for case in ordered}) != len(ordered):
        raise ValueError("case_id values must be unique")
    return ordered


def record_baseline(
    cases: Iterable[CanaryCase],
    adapter: Callable[[Any], Any],
    *,
    ignored_top_level_fields: frozenset[str] = frozenset(),
) -> CanaryBaseline:
    ordered = _validate_cases(cases)
    signatures = {
        case.case_id: _digest(adapter(case.request), ignored_top_level_fields)
        for case in ordered
    }
    return CanaryBaseline(
        signatures=signatures,
        ignored_top_level_fields=ignored_top_level_fields,
    )


def verify_canaries(
    cases: Iterable[CanaryCase],
    adapter: Callable[[Any], Any],
    baseline: CanaryBaseline,
) -> CanaryResult:
    ordered = _validate_cases(cases)
    witnesses: list[CanaryWitness] = []

    expected_ids = set(baseline.signatures)
    actual_ids = {case.case_id for case in ordered}
    if expected_ids != actual_ids:
        missing = sorted(expected_ids - actual_ids)
        extra = sorted(actual_ids - expected_ids)
        raise ValueError(f"baseline/case ID mismatch; missing={missing}, extra={extra}")

    for case in ordered:
        observed = _digest(adapter(case.request), baseline.ignored_top_level_fields)
        expected = baseline.signatures[case.case_id]
        witnesses.append(
            CanaryWitness(
                case_id=case.case_id,
                expected_signature=expected,
                observed_signature=observed,
                status="PASS" if observed == expected else "DRIFT",
            )
        )

    return CanaryResult(
        status="PASS" if all(w.status == "PASS" for w in witnesses) else "DRIFT",
        witnesses=tuple(witnesses),
    )
