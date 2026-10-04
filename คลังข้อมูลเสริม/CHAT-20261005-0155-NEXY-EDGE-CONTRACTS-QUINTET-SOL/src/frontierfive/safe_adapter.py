from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .common import Verdict, allow, freeze, digest

_MISSING = object()


@dataclass(frozen=True)
class FieldSpec:
    name: str
    kind: str
    required: bool = True
    aliases: tuple[str, ...] = ()
    default: Any = _MISSING
    critical: bool = False


_SAFE_KINDS = {
    ("integer", "integer"),
    ("integer", "number"),
    ("number", "number"),
    ("string", "string"),
    ("boolean", "boolean"),
    ("object", "object"),
    ("array", "array"),
    ("null", "null"),
}


def _default_valid(kind: str, value: Any) -> bool:
    if kind == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "number":
        return (isinstance(value, (int, float)) and not isinstance(value, bool))
    if kind == "string":
        return isinstance(value, str)
    if kind == "boolean":
        return isinstance(value, bool)
    if kind == "object":
        return isinstance(value, dict)
    if kind == "array":
        return isinstance(value, list)
    if kind == "null":
        return value is None
    return False


def compile_adapter(source: Mapping[str, FieldSpec], target: Mapping[str, FieldSpec]) -> Verdict:
    reasons: list[str] = []
    mappings: dict[str, str] = {}
    defaults: dict[str, Any] = {}

    for target_name in sorted(target):
        dst = target[target_name]
        if target_name != dst.name:
            return freeze("INVALID_TARGET_INDEX")
        candidates = []
        if target_name in source:
            candidates.append(target_name)
        for alias in dst.aliases:
            if alias in source:
                candidates.append(alias)
        candidates = sorted(set(candidates))
        if len(candidates) > 1:
            reasons.append(f"AMBIGUOUS_MAPPING:{target_name}")
            continue
        if candidates:
            src_name = candidates[0]
            src = source[src_name]
            if (src.kind, dst.kind) not in _SAFE_KINDS:
                reasons.append(f"UNSAFE_TYPE:{src_name}->{target_name}")
                continue
            if dst.critical and (src_name != target_name or src.kind != dst.kind):
                reasons.append(f"CRITICAL_FIELD_DRIFT:{target_name}")
                continue
            mappings[target_name] = src_name
            continue
        if dst.default is not _MISSING:
            if dst.critical:
                reasons.append(f"CRITICAL_DEFAULT_FORBIDDEN:{target_name}")
            elif not _default_valid(dst.kind, dst.default):
                reasons.append(f"INVALID_DEFAULT:{target_name}")
            else:
                defaults[target_name] = dst.default
            continue
        if dst.required:
            reasons.append(f"MISSING_REQUIRED:{target_name}")

    if reasons:
        return freeze(*reasons)
    plan = {
        "defaults": defaults,
        "mappings": mappings,
        "target_fields": sorted(target),
    }
    return allow({"adapter": plan, "adapter_hash": digest(plan)})


def apply_adapter(record: Mapping[str, Any], adapter: Mapping[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for target_name in adapter["target_fields"]:
        if target_name in adapter["mappings"]:
            source_name = adapter["mappings"][target_name]
            if source_name not in record:
                raise KeyError(f"missing source value: {source_name}")
            out[target_name] = record[source_name]
        elif target_name in adapter["defaults"]:
            out[target_name] = adapter["defaults"][target_name]
    return out
