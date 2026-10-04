import json
import unittest
from datetime import datetime, timedelta, timezone
from itertools import permutations

from src.privacy_firewall import (
    Action,
    ConsentGrant,
    ConsentMode,
    DataItem,
    EgressRequest,
    PrivacyFirewall,
    RecipientClass,
    Sensitivity,
)

UTC = timezone.utc
NOW = datetime(2026, 10, 5, 1, 22, tzinfo=UTC)


def item(
    item_id="i1",
    value=None,
    sensitivity=Sensitivity.PUBLIC,
    purposes=frozenset({"answer"}),
    recipients=frozenset({"model-a"}),
    expires_at=None,
    consent_mode=ConsentMode.NONE,
    required=False,
    field_purposes=None,
):
    return DataItem(
        item_id=item_id,
        value={"text": "hello"} if value is None else value,
        sensitivity=sensitivity,
        allowed_purposes=purposes,
        allowed_recipients=recipients,
        expires_at=expires_at,
        consent_mode=consent_mode,
        required=required,
        field_purposes={} if field_purposes is None else field_purposes,
    )


def request(items, purpose="answer", recipient="model-a", recipient_class=RecipientClass.EXTERNAL_MODEL, grants=()):
    return EgressRequest(
        request_id="req-1",
        purpose=purpose,
        recipient=recipient,
        recipient_class=recipient_class,
        now=NOW,
        items=tuple(items),
        consent_grants=tuple(grants),
    )


class PrivacyFirewallTests(unittest.TestCase):
    def setUp(self):
        self.fw = PrivacyFirewall()

    def test_public_item_allowed_for_bound_purpose_and_recipient(self):
        result = self.fw.evaluate(request([item()]))
        self.assertEqual(Action.ALLOW, result.action)
        self.assertEqual({"i1": {"text": "hello"}}, result.payload)

    def test_optional_purpose_mismatch_is_redacted(self):
        result = self.fw.evaluate(request([item(purposes=frozenset({"summarize"}))]))
        self.assertEqual(Action.REDACT, result.action)
        self.assertEqual({}, result.payload)
        self.assertIn("PURPOSE_MISMATCH", result.receipt.reason_codes)

    def test_required_purpose_mismatch_blocks(self):
        result = self.fw.evaluate(request([item(purposes=frozenset({"summarize"}), required=True)]))
        self.assertEqual(Action.BLOCK, result.action)
        self.assertEqual({}, result.payload)

    def test_sensitive_external_item_requires_consent(self):
        result = self.fw.evaluate(request([item(sensitivity=Sensitivity.SENSITIVE, required=True)]))
        self.assertEqual(Action.ASK, result.action)
        self.assertEqual(("i1",), result.receipt.consent_required_item_ids)

    def test_valid_consent_allows_sensitive_external_item(self):
        grant = ConsentGrant(
            grant_id="g1",
            item_id="i1",
            purpose="answer",
            recipient="model-a",
            expires_at=NOW + timedelta(minutes=5),
        )
        result = self.fw.evaluate(request([item(sensitivity=Sensitivity.SENSITIVE, required=True)], grants=[grant]))
        self.assertEqual(Action.ALLOW, result.action)
        self.assertIn("i1", result.payload)

    def test_expired_consent_is_not_valid(self):
        grant = ConsentGrant(
            grant_id="g1",
            item_id="i1",
            purpose="answer",
            recipient="model-a",
            expires_at=NOW - timedelta(seconds=1),
        )
        result = self.fw.evaluate(request([item(sensitivity=Sensitivity.SENSITIVE, required=True)], grants=[grant]))
        self.assertEqual(Action.ASK, result.action)

    def test_revoked_consent_is_not_valid(self):
        grant = ConsentGrant(
            grant_id="g1",
            item_id="i1",
            purpose="answer",
            recipient="model-a",
            expires_at=NOW + timedelta(minutes=5),
            revoked=True,
        )
        result = self.fw.evaluate(request([item(sensitivity=Sensitivity.SENSITIVE, required=True)], grants=[grant]))
        self.assertEqual(Action.ASK, result.action)

    def test_consent_is_bound_to_purpose(self):
        grant = ConsentGrant(
            grant_id="g1",
            item_id="i1",
            purpose="summarize",
            recipient="model-a",
            expires_at=NOW + timedelta(minutes=5),
        )
        result = self.fw.evaluate(request([item(sensitivity=Sensitivity.SENSITIVE, required=True)], grants=[grant]))
        self.assertEqual(Action.ASK, result.action)

    def test_consent_is_bound_to_recipient(self):
        grant = ConsentGrant(
            grant_id="g1",
            item_id="i1",
            purpose="answer",
            recipient="model-b",
            expires_at=NOW + timedelta(minutes=5),
        )
        result = self.fw.evaluate(request([item(sensitivity=Sensitivity.SENSITIVE, required=True)], grants=[grant]))
        self.assertEqual(Action.ASK, result.action)

    def test_secret_external_item_is_blocked_even_with_consent(self):
        grant = ConsentGrant(
            grant_id="g1",
            item_id="i1",
            purpose="answer",
            recipient="model-a",
            expires_at=NOW + timedelta(minutes=5),
        )
        result = self.fw.evaluate(request([item(sensitivity=Sensitivity.SECRET, required=True)], grants=[grant]))
        self.assertEqual(Action.BLOCK, result.action)
        self.assertIn("SECRET_EXTERNAL_EGRESS_FORBIDDEN", result.receipt.reason_codes)

    def test_explicit_consent_mode_applies_even_to_internal_data(self):
        result = self.fw.evaluate(request([item(sensitivity=Sensitivity.INTERNAL, consent_mode=ConsentMode.EXPLICIT, required=True)]))
        self.assertEqual(Action.ASK, result.action)

    def test_field_level_purpose_minimization(self):
        value = {"name": "Ada", "email": "ada@example.test", "internal_note": "do-not-send"}
        field_purposes = {
            "name": frozenset({"answer", "summarize"}),
            "email": frozenset({"contact"}),
            "internal_note": frozenset(),
        }
        result = self.fw.evaluate(request([item(value=value, field_purposes=field_purposes)]))
        self.assertEqual(Action.REDACT, result.action)
        self.assertEqual({"i1": {"name": "Ada"}}, result.payload)
        self.assertEqual(("email", "internal_note"), result.receipt.field_redactions["i1"])

    def test_required_expired_item_blocks(self):
        result = self.fw.evaluate(request([item(expires_at=NOW - timedelta(seconds=1), required=True)]))
        self.assertEqual(Action.BLOCK, result.action)
        self.assertIn("ITEM_EXPIRED", result.receipt.reason_codes)

    def test_optional_expired_item_redacts(self):
        result = self.fw.evaluate(request([item(expires_at=NOW - timedelta(seconds=1), required=False)]))
        self.assertEqual(Action.REDACT, result.action)
        self.assertEqual({}, result.payload)

    def test_required_recipient_mismatch_blocks(self):
        result = self.fw.evaluate(request([item(recipients=frozenset({"model-b"}), required=True)]))
        self.assertEqual(Action.BLOCK, result.action)

    def test_duplicate_item_ids_freeze(self):
        result = self.fw.evaluate(request([item(item_id="dup"), item(item_id="dup")]))
        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("DUPLICATE_ITEM_ID", result.receipt.reason_codes)

    def test_empty_purpose_metadata_freezes(self):
        result = self.fw.evaluate(request([item(purposes=frozenset())]))
        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("INVALID_ITEM_METADATA", result.receipt.reason_codes)

    def test_empty_recipient_metadata_freezes_sensitive_item(self):
        result = self.fw.evaluate(request([item(sensitivity=Sensitivity.SENSITIVE, recipients=frozenset())]))
        self.assertEqual(Action.FREEZE, result.action)

    def test_sensitive_wildcard_recipient_binding_freezes(self):
        result = self.fw.evaluate(request([item(sensitivity=Sensitivity.SENSITIVE, recipients=frozenset({"*"}))]))
        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("INVALID_ITEM_METADATA", result.receipt.reason_codes)

    def test_receipt_does_not_echo_payload_values(self):
        secret_marker = "ULTRA_PRIVATE_6f73a4"
        result = self.fw.evaluate(request([item(value={"secret": secret_marker}, sensitivity=Sensitivity.SECRET)]))
        serialized = json.dumps(result.receipt.to_dict(), sort_keys=True)
        self.assertNotIn(secret_marker, serialized)

    def test_deterministic_receipt_for_same_input(self):
        req = request([item(item_id="b"), item(item_id="a")])
        one = self.fw.evaluate(req)
        two = self.fw.evaluate(req)
        self.assertEqual(one.receipt.digest, two.receipt.digest)
        self.assertEqual(one.payload, two.payload)

    def test_item_order_does_not_change_result(self):
        items = [item(item_id="a"), item(item_id="b"), item(item_id="c")]
        digests = set()
        payloads = []
        for ordering in permutations(items):
            result = self.fw.evaluate(request(ordering))
            digests.add(result.receipt.digest)
            payloads.append(result.payload)
        self.assertEqual(1, len(digests))
        self.assertTrue(all(p == payloads[0] for p in payloads))

    def test_local_trusted_sensitive_does_not_auto_require_consent(self):
        result = self.fw.evaluate(
            request(
                [item(sensitivity=Sensitivity.SENSITIVE, required=True, recipients=frozenset({"local-core"}))],
                recipient="local-core",
                recipient_class=RecipientClass.LOCAL_TRUSTED,
            )
        )
        self.assertEqual(Action.ALLOW, result.action)

    def test_optional_sensitive_without_consent_is_redacted_not_ask(self):
        result = self.fw.evaluate(request([item(sensitivity=Sensitivity.SENSITIVE, required=False)]))
        self.assertEqual(Action.REDACT, result.action)
        self.assertEqual({}, result.payload)

    def test_required_item_field_minimization_with_no_remaining_fields_blocks(self):
        value = {"email": "ada@example.test"}
        field_purposes = {"email": frozenset({"contact"})}
        result = self.fw.evaluate(request([item(value=value, field_purposes=field_purposes, required=True)]))
        self.assertEqual(Action.BLOCK, result.action)
        self.assertIn("NO_PURPOSE_NECESSARY_FIELDS", result.receipt.reason_codes)


if __name__ == "__main__":
    unittest.main()
