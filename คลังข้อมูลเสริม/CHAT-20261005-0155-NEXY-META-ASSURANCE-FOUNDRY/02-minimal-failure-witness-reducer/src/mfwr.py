from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Callable, Generic, Sequence, TypeVar, Any

T = TypeVar("T")


class ReductionError(RuntimeError):
    pass


class InitialCaseDoesNotFail(ReductionError):
    pass


class OracleUnstableError(ReductionError):
    pass


class EvaluationLimitExceeded(ReductionError):
    pass


def _canonical_bytes(items: Sequence[Any]) -> bytes:
    try:
        return json.dumps(list(items), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ReductionError("items must be JSON-compatible") from exc


def _digest(items: Sequence[Any]) -> str:
    return sha256(_canonical_bytes(items)).hexdigest()


@dataclass(frozen=True)
class ReductionResult(Generic[T]):
    status: str
    original_count: int
    reduced_count: int
    evaluations: int
    original_fingerprint: str
    witness_fingerprint: str
    witness: tuple[T, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "original_count": self.original_count,
            "reduced_count": self.reduced_count,
            "evaluations": self.evaluations,
            "original_fingerprint": self.original_fingerprint,
            "witness_fingerprint": self.witness_fingerprint,
            "witness": list(self.witness),
        }


class _StableOracle(Generic[T]):
    def __init__(self, oracle: Callable[[Sequence[T]], bool], max_evaluations: int) -> None:
        if not callable(oracle):
            raise ReductionError("oracle must be callable")
        if not isinstance(max_evaluations, int) or max_evaluations < 2:
            raise ReductionError("max_evaluations must be an integer >= 2")
        self._oracle = oracle
        self._max = max_evaluations
        self.evaluations = 0
        self._cache: dict[str, bool] = {}

    def fails(self, items: Sequence[T]) -> bool:
        key = _digest(items)
        if key in self._cache:
            return self._cache[key]
        if self.evaluations + 2 > self._max:
            raise EvaluationLimitExceeded("oracle evaluation budget exhausted")
        first = self._oracle(tuple(items))
        second = self._oracle(tuple(items))
        self.evaluations += 2
        if not isinstance(first, bool) or not isinstance(second, bool):
            raise ReductionError("oracle must return bool")
        if first != second:
            raise OracleUnstableError(f"oracle disagreed for candidate {key}")
        self._cache[key] = first
        return first


def _partitions(length: int, n: int) -> list[tuple[int, int]]:
    base, extra = divmod(length, n)
    ranges: list[tuple[int, int]] = []
    start = 0
    for i in range(n):
        size = base + (1 if i < extra else 0)
        end = start + size
        if start != end:
            ranges.append((start, end))
        start = end
    return ranges


def reduce_failure(
    items: Sequence[T],
    oracle: Callable[[Sequence[T]], bool],
    *,
    max_evaluations: int = 10_000,
) -> ReductionResult[T]:
    current = list(items)
    original = tuple(current)
    _canonical_bytes(original)
    stable = _StableOracle(oracle, max_evaluations)

    if not stable.fails(current):
        raise InitialCaseDoesNotFail("full input does not reproduce the failure")

    if current:
        n = 2
        while len(current) >= 2:
            n = min(n, len(current))
            removed_any = False
            for start, end in _partitions(len(current), n):
                complement = current[:start] + current[end:]
                if stable.fails(complement):
                    current = complement
                    n = max(2, n - 1)
                    removed_any = True
                    break
            if removed_any:
                continue
            if n >= len(current):
                break
            n = min(len(current), n * 2)

    changed = True
    while changed and current:
        changed = False
        for index in range(len(current)):
            candidate = current[:index] + current[index + 1 :]
            if stable.fails(candidate):
                current = candidate
                changed = True
                break

    for index in range(len(current)):
        candidate = current[:index] + current[index + 1 :]
        if stable.fails(candidate):
            raise ReductionError("internal error: result is not 1-minimal")

    witness = tuple(current)
    return ReductionResult(
        status="ONE_MINIMAL",
        original_count=len(original),
        reduced_count=len(witness),
        evaluations=stable.evaluations,
        original_fingerprint=_digest(original),
        witness_fingerprint=_digest(witness),
        witness=witness,
    )
