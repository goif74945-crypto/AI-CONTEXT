"""Counterexample Minimization Engine (CME).

Implements deterministic delta-debugging (ddmin) for sequence-shaped failing
cases. The failure predicate must return True when the candidate still
reproduces the target failure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class MinimizationStep:
    candidate_size: int
    reproduced: bool


@dataclass(frozen=True, slots=True)
class MinimizationResult:
    minimized: tuple[T, ...]
    evaluations: int
    history: tuple[MinimizationStep, ...]


def minimize_sequence(
    failing_input: Sequence[T],
    reproduces_failure: Callable[[Sequence[T]], bool],
    *,
    max_evaluations: int = 10_000,
) -> MinimizationResult:
    if max_evaluations < 1:
        raise ValueError("max_evaluations must be >= 1")

    current = list(failing_input)
    history: list[MinimizationStep] = []
    evaluations = 0

    def check(candidate: Sequence[T]) -> bool:
        nonlocal evaluations
        if evaluations >= max_evaluations:
            raise RuntimeError("evaluation budget exhausted")
        evaluations += 1
        result = bool(reproduces_failure(candidate))
        history.append(MinimizationStep(candidate_size=len(candidate), reproduced=result))
        return result

    if not check(current):
        raise ValueError("failing_input does not reproduce the target failure")
    if not current:
        return MinimizationResult((), evaluations, tuple(history))

    n = 2
    while len(current) >= 2:
        subset_size = (len(current) + n - 1) // n
        reduced = False

        # First try each subset directly.
        for start in range(0, len(current), subset_size):
            subset = current[start : start + subset_size]
            if check(subset):
                current = subset
                n = max(n - 1, 2)
                reduced = True
                break
        if reduced:
            continue

        # Then try complements. This catches failures requiring elements that
        # happen to straddle subset boundaries.
        for start in range(0, len(current), subset_size):
            complement = current[:start] + current[start + subset_size :]
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

    # Final 1-minimal pass: no single element may be removed while preserving
    # the failure. This strengthens the result beyond chunk-level ddmin.
    index = 0
    while index < len(current):
        candidate = current[:index] + current[index + 1 :]
        if check(candidate):
            current = candidate
        else:
            index += 1

    return MinimizationResult(tuple(current), evaluations, tuple(history))
