import json
import unittest
from datetime import datetime, timedelta, timezone

from src.privacy_firewall import (
    Action,
    ConsentGrant,
    DataItem,
    EgressRequest,
    PrivacyFirewall,
    RecipientClass,
    RecipientRouteProof,
    Sensitivity,
)


NOW = datetime(2026, 10, 6, 1, 0, tzinfo=timezone.utc)
RECIPIENT = "model-a"


def proof(**changes) -> RecipientRouteProof:
    values = {
        "requested_recipient": RECIPIENT,
        "resolved_recipient": RECIPIENT,
        "redirect_chain": (),
        "resolver_version": "registry-v1",
    }
    values.update(changes)
    return RecipientRouteProof(**values)


def item(*, sensitivity=Sensitivity.PUBLIC, required=True) -> DataItem:
    return DataItem(
        item_id="profile",
        value={"private": "ROUTE_PAYLOAD_MARKER"},
        sensitivity=sensitivity,
        allowed_purposes=frozenset({"answer"}),
        allowed_recipients=frozenset({RECIPIENT}),
        required=required,
    )


def request(*, route=proof(), recipient_class=RecipientClass.EXTERNAL_MODEL, grants=()) -> EgressRequest:
    recipient = "local-core" if recipient_class is RecipientClass.LOCAL_TRUSTED else RECIPIENT
    data_item = item()
    if recipient_class is RecipientClass.LOCAL_TRUSTED:
        data_item = DataItem(
            item_id=data_item.item_id,
            value=data_item.value,
            sensitivity=data_item.sensitivity,
            allowed_purposes=data_item.allowed_purposes,
            allowed_recipients=frozenset({recipient}),
            required=data_item.required,
        )
    return EgressRequest(
        request_id="route-request",
        purpose="answer",
        recipient=recipient,
        recipient_class=recipient_class,
        now=NOW,
        items=(data_item,),
        consent_grants=tuple(grants),
        recipient_route_proof=route,
    )


class RecipientRouteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.firewall = PrivacyFirewall()

    def test_exact_direct_route_allows_bound_public_item(self):
        result = self.firewall.evaluate(request())
        self.assertEqual(Action.ALLOW, result.action)

    def test_external_route_proof_is_required(self):
        result = self.firewall.evaluate(request(route=None))
        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("RECIPIENT_ROUTE_PROOF_REQUIRED", result.receipt.reason_codes)

    def test_alias_resolution_cannot_claim_equivalence(self):
        result = self.firewall.evaluate(
            request(route=proof(resolved_recipient="model-a-friendly-alias"))
        )
        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("RECIPIENT_ROUTE_SUBSTITUTION", result.receipt.reason_codes)

    def test_redirect_chain_freezes_even_when_it_returns_to_approved_identity(self):
        result = self.firewall.evaluate(
            request(route=proof(redirect_chain=("relay-x", RECIPIENT)))
        )
        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("RECIPIENT_REDIRECT_NOT_AUTHORIZED", result.receipt.reason_codes)

    def test_requested_recipient_must_match_request_binding(self):
        result = self.firewall.evaluate(
            request(route=proof(requested_recipient="model-b"))
        )
        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("RECIPIENT_ROUTE_BINDING_MISMATCH", result.receipt.reason_codes)

    def test_blank_resolver_version_is_invalid_metadata(self):
        result = self.firewall.evaluate(request(route=proof(resolver_version=" ")))
        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("INVALID_RECIPIENT_ROUTE_PROOF", result.receipt.reason_codes)

    def test_non_tuple_redirect_chain_is_invalid_metadata(self):
        result = self.firewall.evaluate(
            request(route=proof(redirect_chain=["relay-x"]))  # type: ignore[arg-type]
        )
        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("INVALID_RECIPIENT_ROUTE_PROOF", result.receipt.reason_codes)

    def test_blank_redirect_hop_is_invalid_metadata(self):
        result = self.firewall.evaluate(request(route=proof(redirect_chain=("",))))
        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("INVALID_RECIPIENT_ROUTE_PROOF", result.receipt.reason_codes)

    def test_unbounded_redirect_chain_is_invalid_metadata(self):
        result = self.firewall.evaluate(
            request(route=proof(redirect_chain=tuple(f"hop-{n}" for n in range(9))))
        )
        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("RECIPIENT_ROUTE_TOO_LONG", result.receipt.reason_codes)

    def test_local_trusted_request_may_omit_route_proof(self):
        result = self.firewall.evaluate(
            request(route=None, recipient_class=RecipientClass.LOCAL_TRUSTED)
        )
        self.assertEqual(Action.ALLOW, result.action)

    def test_original_recipient_grant_cannot_override_route_substitution(self):
        grant = ConsentGrant(
            grant_id="grant-1",
            item_id="profile",
            purpose="answer",
            recipient=RECIPIENT,
            expires_at=NOW + timedelta(minutes=5),
        )
        sensitive_item = item(sensitivity=Sensitivity.SENSITIVE)
        req = request(route=proof(resolved_recipient="model-b"), grants=(grant,))
        req = EgressRequest(
            request_id=req.request_id,
            purpose=req.purpose,
            recipient=req.recipient,
            recipient_class=req.recipient_class,
            now=req.now,
            items=(sensitive_item,),
            consent_grants=req.consent_grants,
            recipient_route_proof=req.recipient_route_proof,
        )
        result = self.firewall.evaluate(req)
        self.assertEqual(Action.FREEZE, result.action)
        self.assertEqual({}, result.payload)

    def test_route_alias_and_payload_values_are_not_echoed_in_receipt(self):
        marker = "ROUTE_ALIAS_DO_NOT_ECHO"
        result = self.firewall.evaluate(
            request(route=proof(resolved_recipient=marker))
        )
        receipt_json = json.dumps(result.receipt.to_dict(), sort_keys=True)
        self.assertNotIn(marker, receipt_json)
        self.assertNotIn("ROUTE_PAYLOAD_MARKER", receipt_json)


if __name__ == "__main__":
    unittest.main()
