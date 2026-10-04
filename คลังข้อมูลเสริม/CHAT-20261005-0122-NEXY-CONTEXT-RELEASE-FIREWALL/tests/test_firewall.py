from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nexy_crf import (  # noqa: E402
    ContextField,
    ContextReleaseFirewall,
    ContextSet,
    DeclassificationGrant,
    ReleasePolicy,
    ReleaseRequest,
    ReleaseStatus,
    Sensitivity,
)
from nexy_crf.engine import ContextValidationError, PolicyValidationError  # noqa: E402

NOW = "2026-10-05T01:30:00+07:00"


def field(
    key: str,
    value,
    sensitivity: Sensitivity = Sensitivity.PUBLIC,
    *,
    compartments=(),
    purposes=(),
    derived_from=(),
    expires_at=None,
):
    return ContextField(
        key=key,
        value=value,
        sensitivity=sensitivity,
        provenance=f"fixture:{key}",
        compartments=frozenset(compartments),
        allowed_purposes=frozenset(purposes),
        derived_from=tuple(derived_from),
        expires_at=expires_at,
    )


def request(required=("task",), optional=(), compartments=(), purpose="code_review", consumer="agent:gpt"):
    return ReleaseRequest(
        request_id="req-001",
        consumer_id=consumer,
        purpose=purpose,
        required_keys=tuple(required),
        optional_keys=tuple(optional),
        allowed_compartments=frozenset(compartments),
    )


def policy(
    max_sensitivity=Sensitivity.CONFIDENTIAL,
    compartments=(),
    purposes=("code_review",),
    consumer="agent:gpt",
    declass=False,
):
    return ReleasePolicy(
        policy_id="policy-001",
        consumer_id=consumer,
        allowed_purposes=frozenset(purposes),
        max_sensitivity=max_sensitivity,
        allowed_compartments=frozenset(compartments),
        allow_declassification=declass,
    )


class ContextReleaseFirewallTests(unittest.TestCase):
    def test_public_required_field_releases(self):
        ctx = ContextSet({"task": field("task", "review this diff")})
        result = ContextReleaseFirewall().release(ctx, request(), policy(), evaluated_at=NOW)
        self.assertEqual(result.status, ReleaseStatus.RELEASED)
        self.assertEqual(dict(result.payload), {"task": "review this diff"})

    def test_unrequested_secret_is_never_released(self):
        secret = "TOP-SECRET-VALUE-DO-NOT-LEAK"
        ctx = ContextSet({
            "task": field("task", "review"),
            "secret": field("secret", secret, Sensitivity.SECRET),
        })
        result = ContextReleaseFirewall().release(ctx, request(), policy(), evaluated_at=NOW)
        self.assertNotIn("secret", result.payload)
        self.assertNotIn(secret, json.dumps(result.receipt.public_dict(), sort_keys=True))

    def test_unrequested_fields_do_not_change_context_metadata_hash(self):
        base = ContextSet({"task": field("task", "review")})
        with_unrelated = ContextSet({
            "task": field("task", "review"),
            "secret": field("secret", "unrelated", Sensitivity.SECRET),
        })
        fw = ContextReleaseFirewall()
        r1 = fw.release(base, request(), policy(), evaluated_at=NOW)
        r2 = fw.release(with_unrelated, request(), policy(), evaluated_at=NOW)
        self.assertEqual(r1.receipt.context_metadata_hash, r2.receipt.context_metadata_hash)
        self.assertEqual(r1.receipt.receipt_hash, r2.receipt.receipt_hash)

    def test_required_secret_blocks_atomically(self):
        ctx = ContextSet({
            "task": field("task", "review"),
            "secret": field("secret", "dont-leak", Sensitivity.SECRET),
        })
        result = ContextReleaseFirewall().release(
            ctx,
            request(required=("task", "secret")),
            policy(max_sensitivity=Sensitivity.CONFIDENTIAL),
            evaluated_at=NOW,
        )
        self.assertEqual(result.status, ReleaseStatus.FROZEN)
        self.assertEqual(dict(result.payload), {})
        self.assertIsNone(result.receipt.payload_hash)

    def test_optional_secret_is_omitted_without_freeze(self):
        ctx = ContextSet({
            "task": field("task", "review"),
            "secret": field("secret", "dont-leak", Sensitivity.SECRET),
        })
        result = ContextReleaseFirewall().release(
            ctx,
            request(optional=("secret",)),
            policy(max_sensitivity=Sensitivity.CONFIDENTIAL),
            evaluated_at=NOW,
        )
        self.assertEqual(result.status, ReleaseStatus.RELEASED)
        self.assertEqual(dict(result.payload), {"task": "review"})

    def test_missing_required_freezes(self):
        result = ContextReleaseFirewall().release(
            ContextSet({}), request(required=("missing",)), policy(), evaluated_at=NOW
        )
        self.assertEqual(result.status, ReleaseStatus.FROZEN)
        self.assertEqual(result.receipt.decisions[0].reason_code, "MISSING_REQUIRED")

    def test_missing_optional_does_not_freeze(self):
        ctx = ContextSet({"task": field("task", "review")})
        result = ContextReleaseFirewall().release(ctx, request(optional=("missing",)), policy(), evaluated_at=NOW)
        self.assertEqual(result.status, ReleaseStatus.RELEASED)
        reasons = {d.key: d.reason_code for d in result.receipt.decisions}
        self.assertEqual(reasons["missing"], "MISSING_OPTIONAL")

    def test_field_purpose_mismatch_blocks_required(self):
        ctx = ContextSet({"task": field("task", "review", purposes=("summarize",))})
        result = ContextReleaseFirewall().release(ctx, request(), policy(), evaluated_at=NOW)
        self.assertEqual(result.status, ReleaseStatus.FROZEN)
        self.assertEqual(result.receipt.decisions[0].reason_code, "PURPOSE_MISMATCH")

    def test_field_purpose_match_releases(self):
        ctx = ContextSet({"task": field("task", "review", purposes=("code_review",))})
        result = ContextReleaseFirewall().release(ctx, request(), policy(), evaluated_at=NOW)
        self.assertEqual(result.status, ReleaseStatus.RELEASED)

    def test_compartment_mismatch_blocks(self):
        ctx = ContextSet({"task": field("task", "review", compartments=("project-alpha",))})
        result = ContextReleaseFirewall().release(ctx, request(compartments=()), policy(compartments=("project-alpha",)), evaluated_at=NOW)
        self.assertEqual(result.status, ReleaseStatus.FROZEN)
        self.assertEqual(result.receipt.decisions[0].reason_code, "COMPARTMENT_MISMATCH")

    def test_compartment_match_releases(self):
        ctx = ContextSet({"task": field("task", "review", compartments=("project-alpha",))})
        result = ContextReleaseFirewall().release(
            ctx,
            request(compartments=("project-alpha",)),
            policy(compartments=("project-alpha", "project-beta")),
            evaluated_at=NOW,
        )
        self.assertEqual(result.status, ReleaseStatus.RELEASED)

    def test_request_cannot_expand_policy_compartments(self):
        ctx = ContextSet({"task": field("task", "review")})
        with self.assertRaises(PolicyValidationError):
            ContextReleaseFirewall().release(
                ctx,
                request(compartments=("project-beta",)),
                policy(compartments=("project-alpha",)),
                evaluated_at=NOW,
            )

    def test_request_purpose_must_be_explicitly_allowed(self):
        ctx = ContextSet({"task": field("task", "review")})
        with self.assertRaises(PolicyValidationError):
            ContextReleaseFirewall().release(ctx, request(purpose="summarize"), policy(), evaluated_at=NOW)

    def test_consumer_mismatch_is_rejected(self):
        ctx = ContextSet({"task": field("task", "review")})
        with self.assertRaises(PolicyValidationError):
            ContextReleaseFirewall().release(ctx, request(consumer="agent:gemini"), policy(), evaluated_at=NOW)

    def test_expired_required_field_freezes(self):
        ctx = ContextSet({"task": field("task", "review", expires_at="2026-10-04T00:00:00Z")})
        result = ContextReleaseFirewall().release(ctx, request(), policy(), evaluated_at=NOW)
        self.assertEqual(result.status, ReleaseStatus.FROZEN)
        self.assertEqual(result.receipt.decisions[0].reason_code, "EXPIRED")

    def test_future_expiry_releases(self):
        ctx = ContextSet({"task": field("task", "review", expires_at="2026-10-06T00:00:00Z")})
        result = ContextReleaseFirewall().release(ctx, request(), policy(), evaluated_at=NOW)
        self.assertEqual(result.status, ReleaseStatus.RELEASED)

    def test_derived_sensitivity_downgrade_is_rejected(self):
        ctx = ContextSet({
            "secret": field("secret", "s", Sensitivity.SECRET),
            "derived": field("derived", "summary", Sensitivity.PUBLIC, derived_from=("secret",)),
        })
        with self.assertRaises(ContextValidationError):
            ContextReleaseFirewall().validate_context(ctx)

    def test_derived_compartment_narrowing_is_rejected(self):
        ctx = ContextSet({
            "source": field("source", "s", Sensitivity.INTERNAL, compartments=("alpha",)),
            "derived": field("derived", "d", Sensitivity.INTERNAL, derived_from=("source",)),
        })
        with self.assertRaises(ContextValidationError):
            ContextReleaseFirewall().validate_context(ctx)

    def test_derived_purpose_broadening_is_rejected(self):
        ctx = ContextSet({
            "source": field("source", "s", purposes=("code_review",)),
            "derived": field("derived", "d", purposes=("code_review", "summarize"), derived_from=("source",)),
        })
        with self.assertRaises(ContextValidationError):
            ContextReleaseFirewall().validate_context(ctx)

    def test_derived_purpose_can_narrow(self):
        ctx = ContextSet({
            "a": field("a", "a", purposes=("code_review", "summarize")),
            "b": field("b", "b", purposes=("code_review",)),
            "derived": field("derived", "d", purposes=("code_review",), derived_from=("a", "b")),
        })
        ContextReleaseFirewall().validate_context(ctx)

    def test_unknown_derived_dependency_is_rejected(self):
        ctx = ContextSet({"derived": field("derived", "d", derived_from=("missing",))})
        with self.assertRaises(ContextValidationError):
            ContextReleaseFirewall().validate_context(ctx)

    def test_derived_cycle_is_rejected(self):
        ctx = ContextSet({
            "a": field("a", "a", derived_from=("b",)),
            "b": field("b", "b", derived_from=("a",)),
        })
        with self.assertRaises(ContextValidationError):
            ContextReleaseFirewall().validate_context(ctx)

    def test_receipt_does_not_echo_blocked_value(self):
        secret = "SUPER-SENSITIVE-CANARY-928374"
        ctx = ContextSet({"secret": field("secret", secret, Sensitivity.SECRET)})
        result = ContextReleaseFirewall().release(
            ctx,
            request(required=("secret",)),
            policy(max_sensitivity=Sensitivity.PUBLIC),
            evaluated_at=NOW,
        )
        encoded = json.dumps(result.receipt.public_dict(), sort_keys=True)
        self.assertNotIn(secret, encoded)

    def test_receipt_is_deterministic_across_context_map_order(self):
        ctx1 = ContextSet({
            "task": field("task", "review"),
            "notes": field("notes", ["a", "b"], Sensitivity.INTERNAL),
        })
        ctx2 = ContextSet({
            "notes": field("notes", ["a", "b"], Sensitivity.INTERNAL),
            "task": field("task", "review"),
        })
        req = request(optional=("notes",))
        p = policy()
        fw = ContextReleaseFirewall()
        r1 = fw.release(ctx1, req, p, evaluated_at=NOW)
        r2 = fw.release(ctx2, req, p, evaluated_at=NOW)
        self.assertEqual(r1.receipt.receipt_hash, r2.receipt.receipt_hash)
        self.assertEqual(r1.receipt.context_metadata_hash, r2.receipt.context_metadata_hash)

    def test_float_values_are_rejected_for_cross_runtime_canonicality(self):
        ctx = ContextSet({"task": field("task", 0.1)})
        with self.assertRaises(ContextValidationError):
            ContextReleaseFirewall().validate_context(ctx)

    def test_declassification_requires_trusted_digest(self):
        grant = DeclassificationGrant(
            grant_id="grant-1",
            field_key="secret",
            from_sensitivity=Sensitivity.SECRET,
            to_sensitivity=Sensitivity.CONFIDENTIAL,
            authority_id="core:law",
            consumer_id="agent:gpt",
            purpose="code_review",
            not_before="2026-10-05T00:00:00Z",
            not_after="2026-10-06T00:00:00Z",
            reason_code="USER_EXPLICIT_RELEASE",
        )
        ctx = ContextSet({"secret": field("secret", "authorized", Sensitivity.SECRET)})
        result = ContextReleaseFirewall().release(
            ctx,
            request(required=("secret",)),
            policy(max_sensitivity=Sensitivity.CONFIDENTIAL, declass=True),
            evaluated_at=NOW,
            declassification_grants=(grant,),
        )
        self.assertEqual(result.status, ReleaseStatus.FROZEN)

    def test_trusted_declassification_can_release(self):
        grant = DeclassificationGrant(
            grant_id="grant-1",
            field_key="secret",
            from_sensitivity=Sensitivity.SECRET,
            to_sensitivity=Sensitivity.CONFIDENTIAL,
            authority_id="core:law",
            consumer_id="agent:gpt",
            purpose="code_review",
            not_before="2026-10-04T00:00:00Z",
            not_after="2026-10-06T00:00:00Z",
            reason_code="USER_EXPLICIT_RELEASE",
        )
        fw = ContextReleaseFirewall({grant.grant_id: grant.digest()})
        ctx = ContextSet({"secret": field("secret", "authorized", Sensitivity.SECRET)})
        result = fw.release(
            ctx,
            request(required=("secret",)),
            policy(max_sensitivity=Sensitivity.CONFIDENTIAL, declass=True),
            evaluated_at=NOW,
            declassification_grants=(grant,),
        )
        self.assertEqual(result.status, ReleaseStatus.RELEASED)
        self.assertEqual(dict(result.payload), {"secret": "authorized"})
        self.assertEqual(result.receipt.decisions[0].reason_code, "DECLASSIFIED")

    def test_tampered_trusted_grant_is_rejected(self):
        original = DeclassificationGrant(
            grant_id="grant-1",
            field_key="secret",
            from_sensitivity=Sensitivity.SECRET,
            to_sensitivity=Sensitivity.CONFIDENTIAL,
            authority_id="core:law",
            consumer_id="agent:gpt",
            purpose="code_review",
            not_before="2026-10-05T00:00:00Z",
            not_after="2026-10-06T00:00:00Z",
            reason_code="USER_EXPLICIT_RELEASE",
        )
        tampered = DeclassificationGrant(
            grant_id="grant-1",
            field_key="secret",
            from_sensitivity=Sensitivity.SECRET,
            to_sensitivity=Sensitivity.CONFIDENTIAL,
            authority_id="core:law",
            consumer_id="agent:gpt",
            purpose="summarize",
            not_before="2026-10-05T00:00:00Z",
            not_after="2026-10-06T00:00:00Z",
            reason_code="USER_EXPLICIT_RELEASE",
        )
        fw = ContextReleaseFirewall({original.grant_id: original.digest()})
        ctx = ContextSet({"secret": field("secret", "authorized", Sensitivity.SECRET)})
        result = fw.release(
            ctx,
            request(required=("secret",)),
            policy(max_sensitivity=Sensitivity.CONFIDENTIAL, declass=True),
            evaluated_at=NOW,
            declassification_grants=(tampered,),
        )
        self.assertEqual(result.status, ReleaseStatus.FROZEN)

    def test_expired_trusted_grant_is_rejected(self):
        grant = DeclassificationGrant(
            grant_id="grant-expired",
            field_key="secret",
            from_sensitivity=Sensitivity.SECRET,
            to_sensitivity=Sensitivity.CONFIDENTIAL,
            authority_id="core:law",
            consumer_id="agent:gpt",
            purpose="code_review",
            not_before="2026-10-01T00:00:00Z",
            not_after="2026-10-02T00:00:00Z",
            reason_code="USER_EXPLICIT_RELEASE",
        )
        fw = ContextReleaseFirewall({grant.grant_id: grant.digest()})
        ctx = ContextSet({"secret": field("secret", "authorized", Sensitivity.SECRET)})
        result = fw.release(
            ctx,
            request(required=("secret",)),
            policy(max_sensitivity=Sensitivity.CONFIDENTIAL, declass=True),
            evaluated_at=NOW,
            declassification_grants=(grant,),
        )
        self.assertEqual(result.status, ReleaseStatus.FROZEN)

    def test_request_keys_must_be_unique(self):
        with self.assertRaises(ValueError):
            request(required=("task",), optional=("task",))

    def test_sensitivity_lattice_is_exhaustive(self):
        for field_level in Sensitivity:
            for ceiling in Sensitivity:
                with self.subTest(field=field_level.name, ceiling=ceiling.name):
                    ctx = ContextSet({"task": field("task", "x", field_level)})
                    result = ContextReleaseFirewall().release(
                        ctx, request(), policy(max_sensitivity=ceiling), evaluated_at=NOW
                    )
                    expected = ReleaseStatus.RELEASED if field_level <= ceiling else ReleaseStatus.FROZEN
                    self.assertEqual(result.status, expected)

    def test_identity_fields_reject_surrounding_whitespace(self):
        with self.assertRaises(ValueError):
            ReleaseRequest(
                request_id=" req ",
                consumer_id="agent:gpt",
                purpose="code_review",
                required_keys=("task",),
            )

    def test_identity_fields_reject_non_nfkc_form(self):
        # U+212A KELVIN SIGN normalizes to ASCII K under NFKC.
        with self.assertRaises(ValueError):
            ContextField(
                key="Key",
                value="x",
                sensitivity=Sensitivity.PUBLIC,
                provenance="fixture",
            )

    def test_identity_fields_reject_format_characters(self):
        with self.assertRaises(ValueError):
            ReleasePolicy(
                policy_id="policy",
                consumer_id="agent:\u200bgpt",
                allowed_purposes=frozenset({"code_review"}),
                max_sensitivity=Sensitivity.PUBLIC,
                allowed_compartments=frozenset(),
            )

    def test_declassification_cannot_raise_or_equal_sensitivity(self):
        with self.assertRaises(ValueError):
            DeclassificationGrant(
                grant_id="bad",
                field_key="x",
                from_sensitivity=Sensitivity.CONFIDENTIAL,
                to_sensitivity=Sensitivity.CONFIDENTIAL,
                authority_id="core",
                consumer_id="agent:gpt",
                purpose="code_review",
                not_before="2026-10-05T00:00:00Z",
                not_after="2026-10-06T00:00:00Z",
                reason_code="BAD",
            )


class AdversarialFixtureTests(unittest.TestCase):
    def test_fixture_manifest_is_well_formed(self):
        data = json.loads((ROOT / "fixtures" / "adversarial_cases.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data["cases"]), 12)
        ids = [case["id"] for case in data["cases"]]
        self.assertEqual(len(ids), len(set(ids)))
        for case in data["cases"]:
            self.assertIn(case["expected_status"], {"RELEASED", "FROZEN", "VALIDATION_ERROR"})
            self.assertTrue(case["attack_or_failure"])
            self.assertTrue(case["expected_invariant"])


if __name__ == "__main__":
    unittest.main()
