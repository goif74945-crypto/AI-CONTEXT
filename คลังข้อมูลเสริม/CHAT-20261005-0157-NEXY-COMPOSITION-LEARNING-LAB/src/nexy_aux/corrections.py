from __future__ import annotations

from typing import Any

from .canonical import dumps, sha256

_ALLOWED_OPS = {"eq", "neq", "contains", "not_contains", "exists", "not_exists"}
_ALLOWED_SCOPE_MODES = {"BOUNDED", "GLOBAL_EXPLICIT"}


def _finish(result: dict[str, Any]) -> dict[str, Any]:
    result["fingerprint"] = sha256(result)
    return result


def compile_correction(correction: dict[str, Any]) -> dict[str, Any]:
    """Compile an explicit correction into a deterministic regression contract.

    The compiler intentionally does not interpret free-form language. Upstream AI
    may propose structured fields, but promotion requires explicit authority/scope.
    """
    if not isinstance(correction, dict):
        raise ValueError("correction must be an object")
    cid = correction.get("id")
    authority = correction.get("authority")
    scope_mode = correction.get("scope_mode")
    selector = correction.get("selector")
    assertions = correction.get("assertions")

    if not isinstance(cid, str) or not cid:
        raise ValueError("correction.id is required")
    if not isinstance(authority, str) or not authority:
        raise ValueError("correction.authority is required")
    if scope_mode not in _ALLOWED_SCOPE_MODES:
        raise ValueError("scope_mode must be BOUNDED or GLOBAL_EXPLICIT")
    if not isinstance(selector, dict):
        raise ValueError("selector must be an object")
    if not isinstance(assertions, list) or not assertions:
        raise ValueError("assertions must be a non-empty list")

    if scope_mode == "BOUNDED":
        if len(selector) < 2:
            raise ValueError("BOUNDED corrections require at least two selector dimensions")
        if any(not isinstance(k, str) or not k for k in selector):
            raise ValueError("BOUNDED selector keys must be non-empty strings")
        if any(v == "*" or v is None for v in selector.values()):
            raise ValueError("BOUNDED selector cannot contain wildcard or null values")
    else:
        if authority != "USER_LAW":
            raise ValueError("GLOBAL_EXPLICIT corrections require USER_LAW authority")
        if selector != {"global": True}:
            raise ValueError("GLOBAL_EXPLICIT selector must be exactly {'global': True}")

    normalized_assertions: list[dict[str, Any]] = []
    for idx, raw in enumerate(assertions):
        if not isinstance(raw, dict):
            raise ValueError(f"assertion[{idx}] must be an object")
        field = raw.get("field")
        op = raw.get("op")
        if not isinstance(field, str) or not field:
            raise ValueError(f"assertion[{idx}].field is required")
        if op not in _ALLOWED_OPS:
            raise ValueError(f"assertion[{idx}].op is invalid")
        if op not in {"exists", "not_exists"} and "value" not in raw:
            raise ValueError(f"assertion[{idx}].value is required for op={op}")
        item = {"field": field, "op": op}
        if "value" in raw:
            item["value"] = raw["value"]
        normalized_assertions.append(item)

    supersedes_raw = correction.get("supersedes", [])
    if not isinstance(supersedes_raw, list) or any(not isinstance(x, str) or not x for x in supersedes_raw):
        raise ValueError("supersedes must be a list of non-empty correction ids")
    if cid in supersedes_raw:
        raise ValueError("a correction cannot supersede itself")

    contract = {
        "schema_version": "nexy.correction-contract.v1",
        "correction_id": cid,
        "authority": authority,
        "scope_mode": scope_mode,
        "selector": {k: selector[k] for k in sorted(selector)},
        "assertions": sorted(normalized_assertions, key=lambda x: (x["field"], x["op"], repr(x.get("value")))),
        "supersedes": sorted(set(supersedes_raw)),
    }
    contract["fingerprint"] = sha256(contract)
    return contract


def is_applicable(contract: dict[str, Any], context: dict[str, Any]) -> bool:
    if contract["scope_mode"] == "GLOBAL_EXPLICIT":
        return True
    return all(context.get(k) == v for k, v in contract["selector"].items())


def _get_path(obj: dict[str, Any], path: str) -> tuple[bool, Any]:
    cur: Any = obj
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False, None
        cur = cur[part]
    return True, cur


def evaluate(contract: dict[str, Any], context: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    if not is_applicable(contract, context):
        return _finish({"status": "NOT_APPLICABLE", "correction_id": contract["correction_id"], "violations": []})

    violations: list[dict[str, Any]] = []
    for rule in contract["assertions"]:
        exists, actual = _get_path(output, rule["field"])
        op = rule["op"]
        expected = rule.get("value")
        passed = False
        if op == "exists":
            passed = exists
        elif op == "not_exists":
            passed = not exists
        elif op == "eq":
            passed = exists and actual == expected
        elif op == "neq":
            passed = exists and actual != expected
        elif op == "contains":
            passed = exists and isinstance(actual, (str, list, tuple, set, dict)) and expected in actual
        elif op == "not_contains":
            passed = (not exists) or (isinstance(actual, (str, list, tuple, set, dict)) and expected not in actual)
        if not passed:
            violations.append({"field": rule["field"], "op": op, "expected": expected, "actual": actual if exists else None})

    return _finish({
        "status": "PASS" if not violations else "FAIL",
        "correction_id": contract["correction_id"],
        "violations": violations,
    })


def _rules_conflict(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if left["field"] != right["field"]:
        return False
    lop, rop = left["op"], right["op"]
    lv, rv = left.get("value"), right.get("value")

    if {lop, rop} == {"exists", "not_exists"}:
        return True

    requires_existence = {"eq", "neq", "contains", "exists"}
    if lop == "not_exists" and rop in requires_existence:
        return True
    if rop == "not_exists" and lop in requires_existence:
        return True

    if lop == rop == "eq" and lv != rv:
        return True
    if {lop, rop} == {"eq", "neq"} and lv == rv:
        return True
    if {lop, rop} == {"contains", "not_contains"} and lv == rv:
        return True
    return False


def compile_corrections(corrections: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(corrections, list):
        raise ValueError("corrections must be a list")
    contracts = [compile_correction(c) for c in corrections]
    by_id: dict[str, dict[str, Any]] = {}
    for c in contracts:
        if c["correction_id"] in by_id:
            raise ValueError(f"duplicate correction id: {c['correction_id']}")
        by_id[c["correction_id"]] = c

    conflicts: list[dict[str, Any]] = []
    ids = sorted(by_id)

    # Compare only corrections that can actually overlap. Grouping avoids the
    # O(n^2) all-pairs scan when a large correction registry contains many
    # independent bounded scopes.
    scope_groups: dict[tuple[str, str], list[str]] = {}
    for correction_id in ids:
        contract = by_id[correction_id]
        key = (contract["scope_mode"], dumps(contract["selector"]))
        scope_groups.setdefault(key, []).append(correction_id)

    for group_ids in scope_groups.values():
        group_ids = sorted(group_ids)
        for i, left_id in enumerate(group_ids):
            left = by_id[left_id]
            for right_id in group_ids[i + 1:]:
                right = by_id[right_id]
                for left_rule in left["assertions"]:
                    for right_rule in right["assertions"]:
                        if _rules_conflict(left_rule, right_rule):
                            conflicts.append({
                                "left": left_id,
                                "right": right_id,
                                "field": left_rule["field"],
                                "left_rule": left_rule,
                                "right_rule": right_rule,
                            })

    conflicts = sorted(conflicts, key=lambda x: (x["left"], x["right"], x["field"], repr(x["left_rule"]), repr(x["right_rule"])))
    return _finish({
        "status": "FREEZE" if conflicts else "PASS",
        "reason": "CONFLICTING_CORRECTIONS" if conflicts else "CORRECTIONS_COMPILED",
        "contracts": [by_id[i] for i in ids],
        "conflicts": conflicts,
    })
