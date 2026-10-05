"""Bounded deterministic audit for recipient route substitution defenses."""
from __future__ import annotations

from datetime import datetime, timezone
from itertools import product
import json
import sys

from src.privacy_firewall import (
    Action,
    DataItem,
    EgressRequest,
    PrivacyFirewall,
    RecipientClass,
    RecipientRouteProof,
    Sensitivity,
)


NOW = datetime(2026, 10, 6, 1, 0, tzinfo=timezone.utc)
RECIPIENT = "model-a"
MARKER = "RECIPIENT-ROUTE-AUDIT-MARKER"


def run() -> dict[str, int]:
    firewall = PrivacyFirewall()
    cases = deterministic_replays = expected_outcomes = value_non_echo_checks = 0
    chains = ((), ("relay-x",), tuple(f"hop-{n}" for n in range(9)))

    for recipient_class, requested_match, resolved_match, chain in product(
        tuple(RecipientClass), (False, True), (False, True), chains
    ):
        recipient = "local-core" if recipient_class is RecipientClass.LOCAL_TRUSTED else RECIPIENT
        proof = RecipientRouteProof(
            requested_recipient=recipient if requested_match else "requested-alias-marker",
            resolved_recipient=recipient if resolved_match else "resolved-alias-marker",
            redirect_chain=chain,
            resolver_version="audit-registry-v1",
        )
        item = DataItem(
            item_id="public-item",
            value={"private": MARKER},
            sensitivity=Sensitivity.PUBLIC,
            allowed_purposes=frozenset({"answer"}),
            allowed_recipients=frozenset({recipient}),
            required=True,
        )
        request = EgressRequest(
            request_id=f"route-{cases:03d}",
            purpose="answer",
            recipient=recipient,
            recipient_class=recipient_class,
            now=NOW,
            items=(item,),
            recipient_route_proof=proof,
        )
        cases += 1
        first = firewall.evaluate(request)
        second = firewall.evaluate(request)
        deterministic_replays += 1
        assert first == second
        expected = Action.ALLOW if requested_match and resolved_match and not chain else Action.FREEZE
        assert first.action is expected
        expected_outcomes += 1
        if first.action is Action.FREEZE:
            assert first.payload == {}
        receipt_json = json.dumps(first.receipt.to_dict(), sort_keys=True)
        assert MARKER not in receipt_json
        assert "requested-alias-marker" not in receipt_json
        assert "resolved-alias-marker" not in receipt_json
        value_non_echo_checks += 1

    for recipient_class in tuple(RecipientClass):
        recipient = "local-core" if recipient_class is RecipientClass.LOCAL_TRUSTED else RECIPIENT
        request = EgressRequest(
            request_id=f"missing-proof-{recipient_class.value}",
            purpose="answer",
            recipient=recipient,
            recipient_class=recipient_class,
            now=NOW,
            items=(DataItem(
                item_id="public-item",
                value=MARKER,
                sensitivity=Sensitivity.PUBLIC,
                allowed_purposes=frozenset({"answer"}),
                allowed_recipients=frozenset({recipient}),
                required=True,
            ),),
        )
        cases += 1
        first = firewall.evaluate(request)
        second = firewall.evaluate(request)
        deterministic_replays += 1
        assert first == second
        expected = Action.ALLOW if recipient_class is RecipientClass.LOCAL_TRUSTED else Action.FREEZE
        assert first.action is expected
        expected_outcomes += 1
        assert MARKER not in json.dumps(first.receipt.to_dict(), sort_keys=True)
        value_non_echo_checks += 1

    return {
        "bounded_cases": cases,
        "deterministic_replays": deterministic_replays,
        "expected_outcomes": expected_outcomes,
        "value_non_echo_checks": value_non_echo_checks,
        "failures": 0,
    }


if __name__ == "__main__":
    try:
        print(json.dumps(run(), sort_keys=True, indent=2))
    except AssertionError as exc:
        print(json.dumps({"failures": 1, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        raise SystemExit(1)
