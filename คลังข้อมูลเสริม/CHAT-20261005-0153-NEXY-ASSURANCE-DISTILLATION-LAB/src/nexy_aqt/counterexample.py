from __future__ import annotations

import copy
from typing import Any

from .common import ContractError, count_nodes, fingerprint, pointer_tokens, resolve_pointer
from .predicates import evaluate_rules


def _protected_top_keys(paths: list[str]) -> set[str]:
    out: set[str] = set()
    for path in paths:
        tokens = pointer_tokens(path)
        if tokens:
            out.add(tokens[0])
    return out


def _interesting(document: Any, rules: list[dict[str, Any]], mode: str) -> bool:
    verdict, _ = evaluate_rules(document, rules, mode)
    return verdict


def _reduce_list(items: list[Any], keep: callable) -> list[Any]:
    current = list(items)
    changed = True
    while changed:
        changed = False
        for i in range(len(current)):
            candidate = current[:i] + current[i + 1 :]
            if keep(candidate):
                current = candidate
                changed = True
                break
    return current


def _recursive_minimize(value: Any, keep_root: callable, root: Any, path: list[Any]) -> Any:
    if isinstance(value, dict):
        current = copy.deepcopy(value)
        for key in sorted(list(current)):
            candidate_root = copy.deepcopy(root)
            target = candidate_root
            for part in path:
                target = target[part]
            candidate = dict(target)
            candidate.pop(key, None)
            if path:
                parent = candidate_root
                for part in path[:-1]:
                    parent = parent[part]
                parent[path[-1]] = candidate
            else:
                candidate_root = candidate
            if keep_root(candidate_root):
                root = candidate_root
                current = candidate
        for key in sorted(list(current)):
            new_root = copy.deepcopy(root)
            target = new_root
            for part in path:
                target = target[part]
            child_path = path + [key]
            minimized = _recursive_minimize(target[key], keep_root, new_root, child_path)
            target = new_root
            for part in path:
                target = target[part]
            target[key] = minimized
            if keep_root(new_root):
                root = new_root
                current[key] = minimized
        return current
    if isinstance(value, list):
        indices = list(range(len(value)))
        current = copy.deepcopy(value)
        changed = True
        while changed:
            changed = False
            for i in range(len(current)):
                candidate_root = copy.deepcopy(root)
                target = candidate_root
                for part in path:
                    target = target[part]
                candidate = current[:i] + current[i + 1 :]
                if path:
                    parent = candidate_root
                    for part in path[:-1]:
                        parent = parent[part]
                    parent[path[-1]] = candidate
                else:
                    candidate_root = candidate
                if keep_root(candidate_root):
                    root = candidate_root
                    current = candidate
                    changed = True
                    break
        return current
    return value


def distill(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ContractError("payload must be an object")
    case = payload.get("case")
    rules = payload.get("interesting_when")
    mode = payload.get("mode", "all")
    protected = payload.get("protected_paths", [])
    if not isinstance(case, (dict, list)):
        raise ContractError("case must be object or list")
    max_nodes = payload.get("max_nodes", 2000)
    if not isinstance(max_nodes, int) or not 1 <= max_nodes <= 100000:
        raise ContractError("max_nodes must be an integer in [1, 100000]")
    if count_nodes(case, limit=max_nodes) > max_nodes:
        raise ContractError("case exceeds max_nodes")
    if not isinstance(rules, list) or len(rules) > 128:
        raise ContractError("interesting_when must contain at most 128 rules")
    if not isinstance(protected, list) or len(protected) > 128 or not all(isinstance(p, str) for p in protected):
        raise ContractError("protected_paths must be a list of JSON pointers")
    if not _interesting(case, rules, mode):
        return {"status": "FREEZE", "reason_codes": ["BASELINE_NOT_INTERESTING"], "input_hash": fingerprint(payload)}

    missing = object()
    protected_snapshot = {}
    for path in protected:
        value = resolve_pointer(case, path, missing=missing)
        if value is missing:
            raise ContractError("protected path does not exist in baseline case")
        protected_snapshot[path] = copy.deepcopy(value)

    def preserves_protected(candidate: Any) -> bool:
        for path, expected in protected_snapshot.items():
            actual = resolve_pointer(candidate, path, missing=missing)
            if actual is missing or actual != expected:
                return False
        return True

    current = copy.deepcopy(case)
    if isinstance(current, dict):
        protected_keys = _protected_top_keys(protected)
        changed = True
        while changed:
            changed = False
            for key in sorted(list(current)):
                if key in protected_keys:
                    continue
                candidate = copy.deepcopy(current)
                candidate.pop(key)
                if preserves_protected(candidate) and _interesting(candidate, rules, mode):
                    current = candidate
                    changed = True
                    break
    # recursively shrink non-protected content while preserving the interesting predicate.
    keep = lambda candidate: preserves_protected(candidate) and _interesting(candidate, rules, mode)
    current = _recursive_minimize(current, keep, current, [])
    _, failed = evaluate_rules(current, rules, mode)
    return {
        "status": "PASS",
        "reason_codes": [],
        "input_hash": fingerprint(payload),
        "reduced_hash": fingerprint(current),
        "reduced_case": current,
        "remaining_failed_rule_ids": failed,
    }
