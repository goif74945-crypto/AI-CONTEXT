from __future__ import annotations

from typing import Any

from .common import ContractError, resolve_pointer

_MISSING = object()
_ALLOWED = {"exists", "eq", "ne", "in", "not_in", "gt", "gte", "lt", "lte", "type", "contains", "not_contains"}
_TYPES = {"null": type(None), "bool": bool, "int": int, "float": float, "str": str, "list": list, "dict": dict}


def evaluate_rule(document: Any, rule: dict[str, Any]) -> bool:
    if not isinstance(rule, dict):
        raise ContractError("rule must be an object")
    op = rule.get("op")
    path = rule.get("path", "")
    if op not in _ALLOWED:
        raise ContractError(f"unsupported rule op: {op!r}")
    actual = resolve_pointer(document, path, missing=_MISSING)

    if op == "exists":
        expected = rule.get("value", True)
        if not isinstance(expected, bool):
            raise ContractError("exists.value must be boolean")
        return (actual is not _MISSING) is expected
    if actual is _MISSING:
        return False

    expected = rule.get("value")
    if op == "eq":
        return actual == expected
    if op == "ne":
        return actual != expected
    if op == "in":
        if not isinstance(expected, list):
            raise ContractError("in.value must be a list")
        return actual in expected
    if op == "not_in":
        if not isinstance(expected, list):
            raise ContractError("not_in.value must be a list")
        return actual not in expected
    if op == "gt":
        return actual > expected
    if op == "gte":
        return actual >= expected
    if op == "lt":
        return actual < expected
    if op == "lte":
        return actual <= expected
    if op == "type":
        if expected not in _TYPES:
            raise ContractError(f"unsupported type: {expected!r}")
        if expected == "int":
            return isinstance(actual, int) and not isinstance(actual, bool)
        if expected == "float":
            return isinstance(actual, float)
        return isinstance(actual, _TYPES[expected])
    if op == "contains":
        if isinstance(actual, (str, list, dict)):
            return expected in actual
        raise ContractError(f"contains not supported for {type(actual).__name__}")
    if op == "not_contains":
        if isinstance(actual, (str, list, dict)):
            return expected not in actual
        raise ContractError(f"not_contains not supported for {type(actual).__name__}")
    raise AssertionError("unreachable")


def evaluate_rules(document: Any, rules: list[dict[str, Any]], mode: str = "all") -> tuple[bool, list[str]]:
    if mode not in {"all", "any"}:
        raise ContractError("mode must be 'all' or 'any'")
    if not isinstance(rules, list) or not rules:
        raise ContractError("rules must be a non-empty list")
    results: list[bool] = []
    failed: list[str] = []
    seen: set[str] = set()
    for index, rule in enumerate(rules):
        rid = rule.get("id", f"rule-{index:04d}")
        if not isinstance(rid, str) or not rid:
            raise ContractError("rule id must be non-empty string")
        if rid in seen:
            raise ContractError(f"duplicate rule id: {rid}")
        seen.add(rid)
        ok = evaluate_rule(document, rule)
        results.append(ok)
        if not ok:
            failed.append(rid)
    verdict = all(results) if mode == "all" else any(results)
    return verdict, sorted(failed)
