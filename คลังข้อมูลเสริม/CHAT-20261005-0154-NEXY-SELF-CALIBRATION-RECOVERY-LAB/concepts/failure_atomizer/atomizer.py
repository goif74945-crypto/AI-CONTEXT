from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Callable, Generic, Iterable, TypeVar

from core.canonical import fingerprint

T = TypeVar("T")


@dataclass(frozen=True)
class Evaluation(Generic[T]):
    candidate: tuple[T, ...]
    fails: bool

    def as_dict(self) -> dict[str, object]:
        return {"candidate": list(self.candidate), "fails": self.fails}


@dataclass(frozen=True)
class AtomizationResult(Generic[T]):
    status: str
    original: tuple[T, ...]
    minimal: tuple[T, ...]
    evaluations: int
    trace: tuple[Evaluation[T], ...]
    result_fingerprint: str

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "original": list(self.original),
            "minimal": list(self.minimal),
            "evaluations": self.evaluations,
            "trace": [x.as_dict() for x in self.trace],
            "result_fingerprint": self.result_fingerprint,
        }


def ddmin(
    items: Iterable[T],
    fails: Callable[[tuple[T, ...]], bool],
    *,
    max_evaluations: int = 10_000,
) -> AtomizationResult[T]:
    """Deterministic delta debugging minimizer.

    Returns a 1-minimal failing subsequence under the supplied predicate. The algorithm
    never claims global cardinality minimality; that distinction is deliberate.
    """
    original = tuple(items)
    current = original
    if max_evaluations < 1:
        raise ValueError("max_evaluations must be >= 1")
    trace: list[Evaluation[T]] = []

    def check(candidate: tuple[T, ...]) -> bool:
        if len(trace) >= max_evaluations:
            raise RuntimeError("evaluation budget exhausted")
        outcome = bool(fails(candidate))
        trace.append(Evaluation(candidate, outcome))
        return outcome

    if not check(current):
        payload = {
            "status": "BASELINE_NOT_FAILING",
            "original": list(original),
            "minimal": list(original),
            "evaluations": len(trace),
            "trace": [x.as_dict() for x in trace],
        }
        return AtomizationResult("BASELINE_NOT_FAILING", original, original, len(trace), tuple(trace), fingerprint(payload))

    if current and check(()) or not current:
        payload = {
            "status": "EMPTY_CAUSES_FAILURE",
            "original": list(original),
            "minimal": [],
            "evaluations": len(trace),
            "trace": [x.as_dict() for x in trace],
        }
        return AtomizationResult("EMPTY_CAUSES_FAILURE", original, (), len(trace), tuple(trace), fingerprint(payload))

    n = 2
    while len(current) >= 2:
        subset_size = (len(current) + n - 1) // n
        ranges = [(i, min(i + subset_size, len(current))) for i in range(0, len(current), subset_size)]
        reduced = False

        for start, end in ranges:
            chunk = current[start:end]
            if check(chunk):
                current = chunk
                n = max(n - 1, 2)
                reduced = True
                break
        if reduced:
            continue

        for start, end in ranges:
            complement = current[:start] + current[end:]
            if check(complement):
                current = complement
                n = max(n - 1, 2)
                reduced = True
                break
        if reduced:
            continue

        if n >= len(current):
            break
        n = min(len(current), n * 2)

    # Explicit post-proof: enforce actual 1-minimality for arbitrary predicates.
    changed = True
    while changed and current:
        changed = False
        for i in range(len(current)):
            candidate = current[:i] + current[i + 1 :]
            if check(candidate):
                current = candidate
                changed = True
                break

    payload = {
        "status": "MINIMIZED_1_MINIMAL",
        "original": list(original),
        "minimal": list(current),
        "evaluations": len(trace),
        "trace": [x.as_dict() for x in trace],
    }
    return AtomizationResult("MINIMIZED_1_MINIMAL", original, current, len(trace), tuple(trace), fingerprint(payload))
