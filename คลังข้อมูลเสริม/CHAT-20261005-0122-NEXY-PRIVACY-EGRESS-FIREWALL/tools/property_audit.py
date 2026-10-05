"""Deterministic invariant audit for the NPCEF reference prototype.

This is not a benchmark and makes no performance claim. It enumerates a bounded
state space to pressure core privacy/safety invariants without third-party deps.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from itertools import product, permutations
import json
import sys

from src.privacy_firewall import (
    Action,
    ConsentGrant,
    ConsentMode,
    DataItem,
    EgressRequest,
    PrivacyFirewall,
    RecipientClass,
    RecipientRouteProof,
    Sensitivity,
)

NOW = datetime(2026, 10, 5, 1, 22, tzinfo=timezone.utc)
PURPOSE = "answer"
RECIPIENT = "model-a"
MARKER_PREFIX = "PRIVATE_MARKER_"


def run() -> dict[str, int]:
    fw = PrivacyFirewall()
    cases = 0
    deterministic_replays = 0
    secret_egress_checks = 0
    terminal_payload_checks = 0
    receipt_non_echo_checks = 0

    for (
        sensitivity,
        recipient_class,
        required,
        explicit_consent,
        purpose_match,
        recipient_match,
        expired,
        valid_grant,
    ) in product(
        tuple(Sensitivity),
        tuple(RecipientClass),
        (False, True),
        (False, True),
        (False, True),
        (False, True),
        (False, True),
        (False, True),
    ):
        cases += 1
        item_id = f"i-{cases:04d}"
        marker = MARKER_PREFIX + item_id
        recipient = "local-core" if recipient_class is RecipientClass.LOCAL_TRUSTED else RECIPIENT
        allowed_recipient = recipient if recipient_match else "other-recipient"
        allowed_purpose = PURPOSE if purpose_match else "other-purpose"
        expires_at = NOW - timedelta(seconds=1) if expired else NOW + timedelta(hours=1)
        consent_mode = ConsentMode.EXPLICIT if explicit_consent else ConsentMode.NONE

        data_item = DataItem(
            item_id=item_id,
            value={"needed": marker, "extra": marker + "_EXTRA"},
            sensitivity=sensitivity,
            allowed_purposes=frozenset({allowed_purpose}),
            allowed_recipients=frozenset({allowed_recipient}),
            expires_at=expires_at,
            consent_mode=consent_mode,
            required=required,
            field_purposes={
                "needed": frozenset({PURPOSE}),
                "extra": frozenset({"other-purpose"}),
            },
        )
        grant = ConsentGrant(
            grant_id="grant-1",
            item_id=item_id,
            purpose=PURPOSE,
            recipient=recipient,
            expires_at=NOW + timedelta(minutes=5),
            revoked=not valid_grant,
        )
        req = EgressRequest(
            request_id=f"req-{cases:04d}",
            purpose=PURPOSE,
            recipient=recipient,
            recipient_class=recipient_class,
            now=NOW,
            items=(data_item,),
            consent_grants=(grant,),
            recipient_route_proof=(
                None
                if recipient_class is RecipientClass.LOCAL_TRUSTED
                else RecipientRouteProof(recipient, recipient, (), "audit-registry-v1")
            ),
        )

        first = fw.evaluate(req)
        second = fw.evaluate(req)
        deterministic_replays += 1
        assert first.action == second.action
        assert first.payload == second.payload
        assert first.receipt.digest == second.receipt.digest

        receipt_json = json.dumps(first.receipt.to_dict(), sort_keys=True)
        receipt_non_echo_checks += 1
        assert marker not in receipt_json

        if first.action in {Action.ASK, Action.BLOCK, Action.FREEZE}:
            terminal_payload_checks += 1
            assert first.payload == {}

        if sensitivity is Sensitivity.SECRET and recipient_class is not RecipientClass.LOCAL_TRUSTED:
            secret_egress_checks += 1
            assert item_id not in first.payload

        if item_id in first.payload:
            value = first.payload[item_id]
            assert isinstance(value, dict)
            assert set(value) <= {"needed"}
            assert purpose_match
            assert recipient_match
            assert not expired

    order_items = tuple(
        DataItem(
            item_id=f"order-{n}",
            value={"k": n},
            sensitivity=Sensitivity.PUBLIC,
            allowed_purposes=frozenset({PURPOSE}),
            allowed_recipients=frozenset({RECIPIENT}),
        )
        for n in range(4)
    )
    order_digests = set()
    order_payloads = []
    for ordering in permutations(order_items):
        req = EgressRequest(
            request_id="order-invariance",
            purpose=PURPOSE,
            recipient=RECIPIENT,
            recipient_class=RecipientClass.EXTERNAL_MODEL,
            now=NOW,
            items=ordering,
            recipient_route_proof=RecipientRouteProof(RECIPIENT, RECIPIENT, (), "audit-registry-v1"),
        )
        result = fw.evaluate(req)
        order_digests.add(result.receipt.digest)
        order_payloads.append(result.payload)
    assert len(order_digests) == 1
    assert all(payload == order_payloads[0] for payload in order_payloads)

    return {
        "bounded_cases": cases,
        "deterministic_replays": deterministic_replays,
        "receipt_non_echo_checks": receipt_non_echo_checks,
        "terminal_payload_checks": terminal_payload_checks,
        "secret_external_egress_checks": secret_egress_checks,
        "order_permutations": 24,
        "failures": 0,
    }


if __name__ == "__main__":
    try:
        print(json.dumps(run(), sort_keys=True, indent=2))
    except AssertionError:
        print("PROPERTY_AUDIT_FAILED", file=sys.stderr)
        raise
