import unittest
from datetime import datetime, timedelta, timezone

from src.privacy_firewall import (
    Action,
    ConsentBundleGrant,
    ConsentGrant,
    ConsentMode,
    DataItem,
    EgressRequest,
    PrivacyFirewall,
    RecipientClass,
    RecipientRouteProof,
    Sensitivity,
)


NOW = datetime(2026, 10, 5, 20, 4, tzinfo=timezone.utc)


def sensitive(item_id: str) -> DataItem:
    return DataItem(
        item_id=item_id,
        value={"private": f"marker-{item_id}"},
        sensitivity=Sensitivity.SENSITIVE,
        allowed_purposes=frozenset({"answer"}),
        allowed_recipients=frozenset({"model-a"}),
        consent_mode=ConsentMode.EXPLICIT,
        required=True,
    )


def bundle(**changes) -> ConsentBundleGrant:
    values = {
        "grant_id": "bundle-1",
        "request_id": "request-1",
        "item_ids": frozenset({"profile", "history"}),
        "purpose": "answer",
        "recipient": "model-a",
        "expires_at": NOW + timedelta(minutes=5),
    }
    values.update(changes)
    return ConsentBundleGrant(**values)


def request(items, grants=(), *, request_id: str = "request-1") -> EgressRequest:
    return EgressRequest(
        request_id=request_id,
        purpose="answer",
        recipient="model-a",
        recipient_class=RecipientClass.EXTERNAL_MODEL,
        now=NOW,
        items=tuple(items),
        consent_grants=tuple(grants),
        recipient_route_proof=RecipientRouteProof("model-a", "model-a", (), "test-registry-v1"),
    )


class BatchConsentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.firewall = PrivacyFirewall()
        self.items = (sensitive("profile"), sensitive("history"))

    def test_exact_batch_grant_allows_the_bound_items(self):
        result = self.firewall.evaluate(request(self.items, [bundle()]))

        self.assertEqual(Action.ALLOW, result.action)
        self.assertEqual({"history", "profile"}, set(result.payload))

    def test_bundle_missing_one_consent_item_freezes_exact_scope(self):
        result = self.firewall.evaluate(
            request(self.items, [bundle(item_ids=frozenset({"profile", "unused"}))])
        )

        self.assertEqual(Action.FREEZE, result.action)
        self.assertEqual({}, result.payload)
        self.assertIn("BUNDLE_SCOPE_NOT_EXACT", result.receipt.reason_codes)

    def test_bundle_with_extra_item_freezes_exact_scope(self):
        result = self.firewall.evaluate(
            request(
                self.items,
                [bundle(item_ids=frozenset({"profile", "history", "future-item"}))],
            )
        )

        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("BUNDLE_SCOPE_NOT_EXACT", result.receipt.reason_codes)

    def test_bundle_is_bound_to_exact_request_id(self):
        result = self.firewall.evaluate(
            request(self.items, [bundle(request_id="different-request")])
        )

        self.assertEqual(Action.ASK, result.action)
        self.assertEqual({}, result.payload)

    def test_expired_or_revoked_bundle_is_inert(self):
        cases = (
            bundle(expires_at=NOW),
            bundle(revoked=True),
        )
        for grant in cases:
            with self.subTest(grant=grant):
                result = self.firewall.evaluate(request(self.items, [grant]))
                self.assertEqual(Action.ASK, result.action)
                self.assertEqual({}, result.payload)

    def test_bundle_is_bound_to_exact_purpose_and_recipient(self):
        cases = (
            bundle(purpose="summarize"),
            bundle(recipient="model-b"),
        )
        for grant in cases:
            with self.subTest(grant=grant):
                result = self.firewall.evaluate(request(self.items, [grant]))
                self.assertEqual(Action.ASK, result.action)

    def test_single_item_bundle_is_invalid_metadata(self):
        result = self.firewall.evaluate(
            request(self.items, [bundle(item_ids=frozenset({"profile"}))])
        )

        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("BUNDLE_REQUIRES_MULTIPLE_ITEMS", result.receipt.reason_codes)

    def test_duplicate_grant_ids_freeze(self):
        result = self.firewall.evaluate(
            request(self.items, [bundle(), bundle()])
        )

        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("DUPLICATE_GRANT_ID", result.receipt.reason_codes)

    def test_multiple_distinct_active_bundles_freeze_ambiguous_authority(self):
        result = self.firewall.evaluate(
            request(self.items, [bundle(), bundle(grant_id="bundle-2")])
        )

        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("AMBIGUOUS_GRANT_COVERAGE", result.receipt.reason_codes)

    def test_non_frozenset_bundle_scope_is_invalid_metadata(self):
        result = self.firewall.evaluate(
            request(self.items, [bundle(item_ids=("profile", "history"))])  # type: ignore[arg-type]
        )

        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("INVALID_BUNDLE_ITEM_SCOPE", result.receipt.reason_codes)

    def test_valid_single_grant_overlapping_bundle_freezes_ambiguous_authority(self):
        single = ConsentGrant(
            grant_id="single-1",
            item_id="profile",
            purpose="answer",
            recipient="model-a",
            expires_at=NOW + timedelta(minutes=5),
        )
        result = self.firewall.evaluate(request(self.items, [bundle(), single]))

        self.assertEqual(Action.FREEZE, result.action)
        self.assertIn("AMBIGUOUS_GRANT_COVERAGE", result.receipt.reason_codes)

    def test_item_order_does_not_change_batch_decision_or_receipt(self):
        forward = self.firewall.evaluate(request(self.items, [bundle()]))
        reverse = self.firewall.evaluate(request(tuple(reversed(self.items)), [bundle()]))

        self.assertEqual(forward.action, reverse.action)
        self.assertEqual(forward.payload, reverse.payload)
        self.assertEqual(forward.receipt.digest, reverse.receipt.digest)


if __name__ == "__main__":
    unittest.main()
