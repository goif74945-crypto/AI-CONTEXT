from __future__ import annotations

import json
import math
import unicodedata
from dataclasses import dataclass
from typing import Any


class BoundaryPayloadError(ValueError):
    pass


@dataclass(frozen=True)
class Limits:
    max_depth: int = 32
    max_nodes: int = 10_000
    max_abs_number: float = 1e18


def _strict_object(pairs):
    result = {}
    raw_seen = set()
    normalized_seen = {}
    for key, value in pairs:
        if not isinstance(key, str):
            raise BoundaryPayloadError("object key is not a string")
        if key in raw_seen:
            raise BoundaryPayloadError(f"duplicate object key: {key!r}")
        raw_seen.add(key)
        normalized = unicodedata.normalize("NFC", key)
        prior = normalized_seen.get(normalized)
        if prior is not None and prior != key:
            raise BoundaryPayloadError(
                f"Unicode-normalization key collision: {prior!r} vs {key!r}"
            )
        normalized_seen[normalized] = key
        result[key] = value
    return result


def _reject_constant(value: str):
    raise BoundaryPayloadError(f"non-finite JSON number is forbidden: {value}")


def _validate(value: Any, limits: Limits) -> None:
    nodes = 0

    def walk(node: Any, depth: int) -> None:
        nonlocal nodes
        nodes += 1
        if nodes > limits.max_nodes:
            raise BoundaryPayloadError(f"payload exceeds max_nodes={limits.max_nodes}")
        if depth > limits.max_depth:
            raise BoundaryPayloadError(f"payload exceeds max_depth={limits.max_depth}")
        if isinstance(node, dict):
            for key, child in node.items():
                if not isinstance(key, str):
                    raise BoundaryPayloadError("object key is not a string")
                walk(child, depth + 1)
        elif isinstance(node, list):
            for child in node:
                walk(child, depth + 1)
        elif isinstance(node, bool) or node is None or isinstance(node, str):
            return
        elif isinstance(node, int):
            if abs(node) > limits.max_abs_number:
                raise BoundaryPayloadError("numeric magnitude exceeds configured limit")
        elif isinstance(node, float):
            if not math.isfinite(node):
                raise BoundaryPayloadError("non-finite number is forbidden")
            if abs(node) > limits.max_abs_number:
                raise BoundaryPayloadError("numeric magnitude exceeds configured limit")
        else:
            raise BoundaryPayloadError(f"unsupported JSON value type: {type(node).__name__}")

    walk(value, 0)


def strict_loads(text: str, *, limits: Limits = Limits()) -> Any:
    if not isinstance(text, str):
        raise TypeError("text must be str")
    try:
        value = json.loads(text, object_pairs_hook=_strict_object, parse_constant=_reject_constant)
    except BoundaryPayloadError:
        raise
    except (json.JSONDecodeError, RecursionError) as exc:
        raise BoundaryPayloadError(f"invalid JSON payload: {exc}") from exc
    _validate(value, limits)
    return value


def _normalize_keys(value: Any) -> Any:
    if isinstance(value, dict):
        output = {}
        for key in sorted(value, key=lambda s: unicodedata.normalize("NFC", s)):
            normalized = unicodedata.normalize("NFC", key)
            if normalized in output:
                raise BoundaryPayloadError(f"key collision during canonicalization: {normalized!r}")
            output[normalized] = _normalize_keys(value[key])
        return output
    if isinstance(value, list):
        return [_normalize_keys(v) for v in value]
    return value


def canonical_json(value: Any, *, limits: Limits = Limits()) -> str:
    _validate(value, limits)
    normalized = _normalize_keys(value)
    return json.dumps(
        normalized,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )
