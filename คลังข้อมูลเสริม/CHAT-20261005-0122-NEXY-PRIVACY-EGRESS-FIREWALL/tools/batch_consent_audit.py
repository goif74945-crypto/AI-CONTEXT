"""Bounded deterministic audit for exact-scope batch consent grants."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from itertools import permutations
import json
import sys

from src.privacy_firewall import (
    Action,
    ConsentBundleGrant,
    ConsentMode,
    DataItem,
    EgressRequest,
    PrivacyFirewall,
    RecipientClass,
    RecipientRouteProof,
    Sensitivity,
)


NOW = datetime(2026, 10, 5, 20, 4, tzinfo=timezone.utc)
MARKER = "PRIVATE-BATCH-CONSENT-MARKER"


def _items() -> tuple[DataItem, ...]:
    return tuple(
        DataItem(
            item_id=item_id,
            value={"private": f"{MARKER}-{item_id}"},
            sensitivity=Sensitivity.SENSITIVE,
            allowed_purposes=frozenset({"answer"}),
            allowed_recipients=frozenset({"model-a"}),
            consent_mode=ConsentMode.EXPLICIT,
            required=True,
        )
        for item_id in ("profile", "history")
    )


def _grant(**changes: object) -> ConsentBundleGrant:
    values: dict[str, object] = {
        "grant_id": "bundle-1",
        "request_id": "request-1",
        "item_ids": frozenset({"profile", "history"}),
        "purpose": "answer",
        "recipient": "model-a",
        "expires_at": NOW + timedelta(minutes=5),
        "revoked": False,
    }
    values.update(changes)
    return ConsentBundleGrant(**values)  # type: ignore[arg-type]


def run() -> dict[str, int]:
    scenarios = (
        ("exact", (_grant(),), Action.ALLOW),
        ("expired", (_grant(expires_at=NOW),), Action.ASK),
        ("revoked", (_grant(revoked=True),), Action.ASK),
        ("wrong_request", (_grant(request_id="other"),), Action.ASK),
        ("wrong_purpose", (_grant(purpose="other"),), Action.ASK),
        ("wrong_recipient", (_grant(recipient="other"),), Action.ASK),
        ("under_scope", (_grant(item_ids=frozenset({"profile", "unused"})),), Action.FREEZE),
        ("over_scope", (_grant(item_ids=frozenset({"profile", "history", "future"})),), Action.FREEZE),
        ("ambiguous", (_grant(), _grant(grant_id="bundle-2")), Action.FREEZE),
    )
    firewall = PrivacyFirewall()
    cases = deterministic_replays = value_non_echo_checks = 0
    expected_outcomes = 0

    for _, grants, expected in scenarios:
        order_results = []
        for ordering in permutations(_items()):
            request = EgressRequest(
                request_id="request-1",
                purpose="answer",
                recipient="model-a",
                recipient_class=RecipientClass.EXTERNAL_MODEL,
                now=NOW,
                items=ordering,
                consent_grants=grants,
                recipient_route_proof=RecipientRouteProof("model-a", "model-a", (), "audit-registry-v1"),
            )
            cases += 1
            first = firewall.evaluate(request)
            second = firewall.evaluate(request)
            deterministic_replays += 1
            assert first == second
            assert first.action is expected
            expected_outcomes += 1
            value_non_echo_checks += 1
            assert MARKER not in json.dumps(first.receipt.to_dict(), sort_keys=True)
            if first.action in {Action.ASK, Action.BLOCK, Action.FREEZE}:
                assert first.payload == {}
            order_results.append(first)
        assert order_results[0] == order_results[1]

    return {
        "bounded_cases": cases,
        "deterministic_replays": deterministic_replays,
        "expected_outcomes": expected_outcomes,
        "value_non_echo_checks": value_non_echo_checks,
        "order_invariance_pairs": len(scenarios),
        "failures": 0,
    }


if __name__ == "__main__":
    try:
        print(json.dumps(run(), sort_keys=True, indent=2))
    except AssertionError:
        print("BATCH_CONSENT_AUDIT_FAILED", file=sys.stderr)
        raise
