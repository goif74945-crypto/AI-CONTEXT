#!/usr/bin/env python3
"""Bounded exhaustive invariant checker for the MPAL example policy."""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

from mpal_engine import approval_for, evaluate

ROOT = Path(__file__).resolve().parent


def load(name: str):
    return json.loads((ROOT / "fixtures" / name).read_text(encoding="utf-8"))


def build_choice(policy, request, pid: str, group: str | None, choice: str):
    if choice == "NONE":
        return None
    if choice == "APPROVE":
        return approval_for(policy, request, pid, "APPROVE", group, valid_from_tick=0, valid_until_tick=100)
    if choice == "DENY":
        return approval_for(policy, request, pid, "DENY", None, valid_from_tick=0, valid_until_tick=100)
    if choice == "EXPIRED_APPROVE":
        return approval_for(policy, request, pid, "APPROVE", group, valid_from_tick=0, valid_until_tick=10)
    raise AssertionError(choice)


def run() -> dict:
    policy = load("policy.example.json")
    request = load("request.example.json")
    principals = [
        ("bob", "security"),
        ("alice", "operations"),
        ("dave", "operations"),
        ("carol", "operations"),
    ]
    choices = ("NONE", "APPROVE", "DENY", "EXPIRED_APPROVE")
    counts: Counter[str] = Counter()
    evaluated = 0

    for vector in itertools.product(choices, repeat=len(principals)):
        approvals = []
        for (pid, group), choice in zip(principals, vector, strict=True):
            item = build_choice(policy, request, pid, group, choice)
            if item is not None:
                approvals.append(item)

        decision = evaluate(policy, request, approvals, evaluation_tick=50)
        reverse = evaluate(policy, request, list(reversed(approvals)), evaluation_tick=50)
        assert decision.to_dict() == reverse.to_dict(), (vector, decision, reverse)

        mapping = dict(zip([p[0] for p in principals], vector, strict=True))
        owner_veto = mapping["alice"] == "DENY"
        security_veto = mapping["bob"] == "DENY"
        if owner_veto or security_veto:
            assert decision.state == "DENY", (vector, decision)
        if decision.state == "ALLOW":
            assert mapping["bob"] == "APPROVE", (vector, decision)
            assert mapping["alice"] == "APPROVE", (vector, decision)
            assert mapping["dave"] == "APPROVE", (vector, decision)
            counted = {gid: set(ids) for gid, ids in decision.counted_approvals}
            assert "carol" not in set().union(*counted.values()), (vector, decision)

        counts[decision.state] += 1
        evaluated += 1

    return {
        "model": "MPAL-example-policy-bounded-check/v1",
        "vectors_evaluated": evaluated,
        "approval_order_invariance": "PASS",
        "veto_dominance": "PASS",
        "allow_requires_all_quorums": "PASS",
        "requester_self_approval_excluded": "PASS",
        "state_counts": dict(sorted(counts.items())),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
