"""AI-PROPOSED: deterministic trace divergence localization."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable, Mapping

DEFAULT_VOLATILE_KEYS = frozenset({"timestamp", "trace_id", "span_id", "duration_ms"})


def _strip_volatile(value: Any, volatile_keys: frozenset[str]) -> Any:
    if isinstance(value, Mapping):
        return {
            str(k): _strip_volatile(v, volatile_keys)
            for k, v in sorted(value.items(), key=lambda item: str(item[0]))
            if str(k) not in volatile_keys
        }
    if isinstance(value, list):
        return [_strip_volatile(v, volatile_keys) for v in value]
    if isinstance(value, tuple):
        return [_strip_volatile(v, volatile_keys) for v in value]
    return value


def canonical_step_hash(step: Mapping[str, Any], volatile_keys: Iterable[str] = DEFAULT_VOLATILE_KEYS) -> str:
    cleaned = _strip_volatile(step, frozenset(volatile_keys))
    payload = json.dumps(cleaned, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _prefix_chain(trace: list[Mapping[str, Any]]) -> list[str]:
    prev = "0" * 64
    chain: list[str] = []
    for step in trace:
        step_hash = canonical_step_hash(step)
        prev = hashlib.sha256(f"{prev}:{step_hash}".encode("utf-8")).hexdigest()
        chain.append(prev)
    return chain


def bisect_divergence(
    left_trace: Iterable[Mapping[str, Any]],
    right_trace: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    """Locate the first deterministic divergence in ordered execution traces.

    Chained prefix hashes make prefix equality monotonic, allowing binary search.
    """
    left = list(left_trace)
    right = list(right_trace)
    common = min(len(left), len(right))
    left_chain = _prefix_chain(left[:common])
    right_chain = _prefix_chain(right[:common])

    if common and left_chain[-1] != right_chain[-1]:
        lo, hi = 0, common - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if left_chain[mid] == right_chain[mid]:
                lo = mid + 1
            else:
                hi = mid
        index = lo
        left_step = left[index]
        right_step = right[index]
        step_id = left_step.get("id") if left_step.get("id") == right_step.get("id") else None
        deps = left_step.get("deps", []) if isinstance(left_step.get("deps", []), list) else []
        return {
            "status": "DIVERGED",
            "first_index": index,
            "step_id": step_id,
            "reason": "STEP_CONTENT" if step_id is not None else "STEP_ID",
            "left_hash": canonical_step_hash(left_step),
            "right_hash": canonical_step_hash(right_step),
            "dependency_frontier": sorted({str(dep) for dep in deps}),
        }

    if len(left) != len(right):
        return {
            "status": "DIVERGED",
            "first_index": common,
            "step_id": None,
            "reason": "TRACE_LENGTH",
            "left_length": len(left),
            "right_length": len(right),
            "dependency_frontier": [],
        }

    return {
        "status": "EQUIVALENT",
        "first_index": None,
        "step_id": None,
        "reason": None,
        "dependency_frontier": [],
    }
