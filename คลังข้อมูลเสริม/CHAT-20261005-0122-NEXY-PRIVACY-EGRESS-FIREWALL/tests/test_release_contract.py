import json
import unittest
from datetime import datetime, timedelta, timezone

from src.privacy_firewall import (
    Action, ConsentGrant, DataItem, EgressRequest, PrivacyFirewall,
    RecipientClass, RecipientRouteProof, Sensitivity,
)

NOW = datetime(2026, 10, 5, 1, 22, tzinfo=timezone.utc)


def make_item(**changes):
    values = dict(
        item_id="x",
        value={"needed": "ok", "extra": "PRIVATE_MARKER_RELEASE"},
        sensitivity=Sensitivity.PUBLIC,
        allowed_purposes=frozenset({"answer"}),
        allowed_recipients=frozenset({"model-a"}),
        required=False,
        field_purposes={},
    )
    values.update(changes)
    return DataItem(**values)


def make_request(items, **changes):
    values = dict(
        request_id="release-check",
        purpose="answer",
        recipient="model-a",
        recipient_class=RecipientClass.EXTERNAL_MODEL,
        now=NOW,
        items=tuple(items),
        consent_grants=(),
        recipient_route_proof=RecipientRouteProof("model-a", "model-a", (), "test-registry-v1"),
    )
    values.update(changes)
    return EgressRequest(**values)


class ReleaseContractTests(unittest.TestCase):
    def setUp(self):
        self.fw = PrivacyFirewall()

    def test_public_bound_item_allows(self):
        result = self.fw.evaluate(make_request([make_item()]))
        self.assertEqual(Action.ALLOW, result.action)
        self.assertIn("x", result.payload)

    def test_required_purpose_mismatch_blocks_and_releases_nothing(self):
        result = self.fw.evaluate(make_request([make_item(required=True, allowed_purposes=frozenset({"other"}))]))
        self.assertEqual(Action.BLOCK, result.action)
        self.assertEqual({}, result.payload)

    def test_optional_purpose_mismatch_redacts(self):
        result = self.fw.evaluate(make_request([make_item(allowed_purposes=frozenset({"other"}))]))
        self.assertEqual(Action.REDACT, result.action)
        self.assertEqual({}, result.payload)

    def test_sensitive_external_required_item_asks_without_grant(self):
        result = self.fw.evaluate(make_request([make_item(sensitivity=Sensitivity.SENSITIVE, required=True)]))
        self.assertEqual(Action.ASK, result.action)
        self.assertEqual({}, result.payload)

    def test_exact_active_grant_allows_sensitive_item(self):
        grant = ConsentGrant("g", "x", "answer", "model-a", NOW + timedelta(minutes=5))
        result = self.fw.evaluate(make_request(
            [make_item(sensitivity=Sensitivity.SENSITIVE, required=True)],
            consent_grants=(grant,),
        ))
        self.assertEqual(Action.ALLOW, result.action)

    def test_secret_external_is_hard_blocked_even_with_grant(self):
        grant = ConsentGrant("g", "x", "answer", "model-a", NOW + timedelta(minutes=5))
        result = self.fw.evaluate(make_request(
            [make_item(sensitivity=Sensitivity.SECRET, required=True)],
            consent_grants=(grant,),
        ))
        self.assertEqual(Action.BLOCK, result.action)
        self.assertEqual({}, result.payload)

    def test_sensitive_wildcard_binding_freezes(self):
        result = self.fw.evaluate(make_request([
            make_item(sensitivity=Sensitivity.SENSITIVE, allowed_recipients=frozenset({"*"}))
        ]))
        self.assertEqual(Action.FREEZE, result.action)
        self.assertEqual({}, result.payload)

    def test_field_minimization_removes_unneeded_field(self):
        result = self.fw.evaluate(make_request([make_item(
            field_purposes={"needed": frozenset({"answer"}), "extra": frozenset({"other"})}
        )]))
        self.assertEqual(Action.REDACT, result.action)
        self.assertEqual({"x": {"needed": "ok"}}, result.payload)

    def test_receipt_never_echoes_raw_marker(self):
        result = self.fw.evaluate(make_request([make_item(sensitivity=Sensitivity.SECRET)]))
        self.assertNotIn("PRIVATE_MARKER_RELEASE", json.dumps(result.receipt.to_dict(), sort_keys=True))

    def test_deterministic_replay_has_same_digest(self):
        req = make_request([make_item()])
        one = self.fw.evaluate(req)
        two = self.fw.evaluate(req)
        self.assertEqual(one.receipt.digest, two.receipt.digest)
        self.assertEqual(one.payload, two.payload)

    def test_invalid_recipient_class_freezes_without_receipt_crash(self):
        class BadRecipient:
            value = object()
        result = self.fw.evaluate(make_request([make_item()], recipient_class=BadRecipient()))
        self.assertEqual(Action.FREEZE, result.action)
        self.assertEqual("INVALID", result.receipt.recipient_class)

    def test_fake_grant_object_freezes_without_attribute_crash(self):
        class FakeGrant:
            grant_id = "fake"
        result = self.fw.evaluate(make_request(
            [make_item(sensitivity=Sensitivity.SENSITIVE, required=True)],
            consent_grants=(FakeGrant(),),
        ))
        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("INVALID_GRANT_METADATA", result.receipt.reason_codes)


if __name__ == "__main__":
    unittest.main()
