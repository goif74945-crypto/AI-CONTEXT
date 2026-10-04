from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any, TypeVar

from .canonical import sha256

T = TypeVar("T")


class _OracleNondeterministic(RuntimeError):
    pass


def _finish(result: dict[str, Any]) -> dict[str, Any]:
    result["fingerprint"] = sha256(result)
    return result


def _chunks(items: list[T], n: int) -> list[tuple[int, int]]:
    length = len(items)
    base, extra = divmod(length, n)
    chunks: list[tuple[int, int]] = []
    start = 0
    for idx in range(n):
        size = base + (1 if idx < extra else 0)
        end = start + size
        if start < end:
            chunks.append((start, end))
        start = end
    return chunks


def distill(items: Sequence[T], oracle: Callable[[list[T]], str | None], target_signature: str) -> dict[str, Any]:
    """Return a deterministic 1-minimal failure-inducing subsequence using ddmin.

    Each candidate is evaluated twice. If the oracle gives different signatures for
    the same candidate, minimization freezes rather than turning flaky behavior into
    a false minimal counterexample. The result is 1-minimal, not guaranteed to have
    globally minimum cardinality.
    """
    if not isinstance(target_signature, str) or not target_signature:
        raise ValueError("target_signature must be a non-empty string")

    current = list(items)
    evaluations = 0

    def check(candidate: list[T]) -> bool:
        nonlocal evaluations
        first = oracle(list(candidate))
        second = oracle(list(candidate))
        evaluations += 2
        if first != second:
            raise _OracleNondeterministic
        return first == target_signature

    try:
        if not check(current):
            return _finish({
                "status": "FREEZE",
                "reason": "TARGET_SIGNATURE_NOT_REPRODUCED",
                "target_signature": target_signature,
                "evaluations": evaluations,
            })

        n = 2
        while len(current) >= 2:
            n = min(n, len(current))
            reduced = False
            for start, end in _chunks(current, n):
                complement = current[:start] + current[end:]
                if check(complement):
                    current = complement
                    n = max(2, n - 1)
                    reduced = True
                    break
            if reduced:
                continue
            if n >= len(current):
                break
            n = min(len(current), n * 2)

        changed = True
        while changed and current:
            changed = False
            for idx in range(len(current)):
                candidate = current[:idx] + current[idx + 1:]
                if check(candidate):
                    current = candidate
                    changed = True
                    break

        one_minimal = True
        for idx in range(len(current)):
            candidate = current[:idx] + current[idx + 1:]
            if check(candidate):
                one_minimal = False
                break

        return _finish({
            "status": "PASS",
            "reason": "ONE_MINIMAL_COUNTEREXAMPLE",
            "target_signature": target_signature,
            "minimal_items": current,
            "original_size": len(items),
            "minimal_size": len(current),
            "evaluations": evaluations,
            "oracle_confirmations_per_candidate": 2,
            "one_minimal": one_minimal,
        })
    except _OracleNondeterministic:
        return _finish({
            "status": "FREEZE",
            "reason": "ORACLE_NONDETERMINISTIC",
            "target_signature": target_signature,
            "evaluations": evaluations,
        })
