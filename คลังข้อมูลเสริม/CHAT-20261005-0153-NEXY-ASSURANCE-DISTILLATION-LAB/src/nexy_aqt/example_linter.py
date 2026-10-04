from __future__ import annotations

from typing import Any

from .common import ContractError, fingerprint
from .predicates import evaluate_rules


def lint_examples(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ContractError("payload must be object")
    rules = payload.get("rules")
    mode = payload.get("mode", "all")
    examples = payload.get("examples")
    if not isinstance(examples, list) or not examples:
        raise ContractError("examples must be non-empty list")
    if len(examples) > 5000:
        raise ContractError("example count exceeds 5000")
    if not isinstance(rules, list) or not rules or len(rules) > 512:
        raise ContractError("rules must be a non-empty list with at most 512 entries")
    seen: set[str] = set()
    findings = []
    for index, example in enumerate(examples):
        if not isinstance(example, dict):
            raise ContractError("example must be object")
        eid = example.get("id", f"example-{index:04d}")
        if not isinstance(eid, str) or not eid:
            raise ContractError("example id must be non-empty string")
        if eid in seen:
            raise ContractError(f"duplicate example id: {eid}")
        seen.add(eid)
        expected = example.get("expected")
        if expected not in {"PASS", "FREEZE"}:
            raise ContractError("example.expected must be PASS or FREEZE")
        actual_bool, failed = evaluate_rules(example.get("data"), rules, mode)
        actual = "PASS" if actual_bool else "FREEZE"
        if actual != expected:
            findings.append({
                "example_id": eid,
                "expected": expected,
                "actual": actual,
                "failed_rule_ids": failed,
            })
    return {
        "status": "PASS" if not findings else "FAIL",
        "reason_codes": [] if not findings else ["SPEC_EXAMPLE_CONTRADICTION"],
        "input_hash": fingerprint(payload),
        "findings": findings,
        "checked_examples": len(examples),
    }
