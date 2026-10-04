import unittest

from authority_provenance import (
    AuthorityRef,
    AuthorityVerdict,
    PolicyEnvelope,
    assess_authority,
    evaluate_governed,
)
from human_agency_lab import AgencyPolicy, Decision, RequestProfile


class AuthorityRefTests(unittest.TestCase):
    def test_digest_is_order_invariant_for_duplicate_prefix_set(self):
        a = AuthorityRef("a1", "user", ("repo:", "file:", "repo:"))
        b = AuthorityRef("a1", "user", ("file:", "repo:"))
        self.assertEqual(a.digest(), b.digest())

    def test_invalid_revision_window_rejected(self):
        with self.assertRaises(ValueError):
            AuthorityRef(
                "a1",
                "user",
                ("x",),
                valid_from_revision=5,
                valid_through_revision=4,
            )

    def test_empty_prefixes_rejected(self):
        with self.assertRaises(ValueError):
            AuthorityRef("a1", "user", tuple())


class AuthorityAssessmentTests(unittest.TestCase):
    def setUp(self):
        self.request = RequestProfile(
            action_id="repo:edit:file",
            scope_breadth=0.4,
        )

    def test_missing(self):
        result = assess_authority(None, self.request, revision=2)
        self.assertEqual(result.verdict, AuthorityVerdict.MISSING)

    def test_revoked(self):
        ref = AuthorityRef("a1", "user", ("repo:",), revoked=True)
        result = assess_authority(ref, self.request, revision=2)
        self.assertEqual(result.verdict, AuthorityVerdict.REVOKED)

    def test_not_yet_valid(self):
        ref = AuthorityRef("a1", "user", ("repo:",), valid_from_revision=3)
        result = assess_authority(ref, self.request, revision=2)
        self.assertEqual(result.verdict, AuthorityVerdict.NOT_YET_VALID)

    def test_stale(self):
        ref = AuthorityRef(
            "a1", "user", ("repo:",), valid_from_revision=1, valid_through_revision=2
        )
        result = assess_authority(ref, self.request, revision=3)
        self.assertEqual(result.verdict, AuthorityVerdict.STALE)

    def test_action_out_of_scope(self):
        ref = AuthorityRef("a1", "user", ("drive:",))
        result = assess_authority(ref, self.request, revision=2)
        self.assertEqual(result.verdict, AuthorityVerdict.ACTION_OUT_OF_SCOPE)

    def test_scope_limit_exceeded(self):
        ref = AuthorityRef("a1", "user", ("repo:",), max_scope_breadth=0.3)
        result = assess_authority(ref, self.request, revision=2)
        self.assertEqual(result.verdict, AuthorityVerdict.SCOPE_LIMIT_EXCEEDED)

    def test_destructive_permission_required(self):
        req = RequestProfile(action_id="repo:delete", destructive=True)
        ref = AuthorityRef("a1", "user", ("repo:",), allow_destructive=False)
        result = assess_authority(ref, req, revision=2)
        self.assertEqual(result.verdict, AuthorityVerdict.DESTRUCTIVE_NOT_ALLOWED)

    def test_external_permission_required(self):
        req = RequestProfile(action_id="repo:send", external_side_effect=True)
        ref = AuthorityRef("a1", "user", ("repo:",), allow_external_effect=False)
        result = assess_authority(ref, req, revision=2)
        self.assertEqual(result.verdict, AuthorityVerdict.EXTERNAL_EFFECT_NOT_ALLOWED)

    def test_auth_boundary_permission_required(self):
        req = RequestProfile(action_id="repo:grant", crosses_auth_boundary=True)
        ref = AuthorityRef("a1", "user", ("repo:",), allow_auth_boundary=False)
        result = assess_authority(ref, req, revision=2)
        self.assertEqual(result.verdict, AuthorityVerdict.AUTH_BOUNDARY_NOT_ALLOWED)

    def test_valid(self):
        ref = AuthorityRef("a1", "user", ("repo:",), max_scope_breadth=0.5)
        result = assess_authority(ref, self.request, revision=2)
        self.assertEqual(result.verdict, AuthorityVerdict.VALID)
        self.assertTrue(result.valid)


class PolicyEnvelopeTests(unittest.TestCase):
    def test_digest_repeatability(self):
        envelope = PolicyEnvelope("agency", "1", "1", AgencyPolicy())
        self.assertEqual(envelope.digest(), envelope.digest())

    def test_version_changes_digest(self):
        a = PolicyEnvelope("agency", "1", "1", AgencyPolicy())
        b = PolicyEnvelope("agency", "2", "1", AgencyPolicy())
        self.assertNotEqual(a.digest(), b.digest())

    def test_policy_change_changes_digest(self):
        a = PolicyEnvelope("agency", "1", "1", AgencyPolicy())
        b = PolicyEnvelope(
            "agency", "1", "1", AgencyPolicy(material_cost=0.8)
        )
        self.assertNotEqual(a.digest(), b.digest())


class GovernedDecisionTests(unittest.TestCase):
    def setUp(self):
        self.policy = PolicyEnvelope("agency", "1", "1", AgencyPolicy())

    def test_valid_authority_prevents_missing_authority_freeze(self):
        request = RequestProfile(action_id="repo:wide", scope_breadth=0.9)
        authority = AuthorityRef(
            "a1", "user", ("repo:",), max_scope_breadth=1.0
        )
        result = evaluate_governed(
            request, authority=authority, revision=3, policy=self.policy
        )
        self.assertEqual(result.authority.verdict, AuthorityVerdict.VALID)
        self.assertEqual(result.decision.decision, Decision.PREVIEW)

    def test_stale_authority_freezes_high_impact(self):
        request = RequestProfile(action_id="repo:wide", scope_breadth=0.9)
        authority = AuthorityRef(
            "a1",
            "user",
            ("repo:",),
            max_scope_breadth=1.0,
            valid_through_revision=2,
        )
        result = evaluate_governed(
            request, authority=authority, revision=3, policy=self.policy
        )
        self.assertEqual(result.authority.verdict, AuthorityVerdict.STALE)
        self.assertEqual(result.decision.decision, Decision.FREEZE)

    def test_valid_destructive_authority_does_not_bypass_rollback_freeze(self):
        request = RequestProfile(
            action_id="repo:delete",
            destructive=True,
            rollback_available=False,
            reversibility=0.0,
        )
        authority = AuthorityRef(
            "a1", "user", ("repo:",), allow_destructive=True
        )
        result = evaluate_governed(
            request, authority=authority, revision=1, policy=self.policy
        )
        self.assertEqual(result.authority.verdict, AuthorityVerdict.VALID)
        self.assertEqual(result.decision.decision, Decision.FREEZE)

    def test_governed_digest_repeatability(self):
        request = RequestProfile(action_id="repo:read")
        authority = AuthorityRef("a1", "user", ("repo:",))
        digests = {
            evaluate_governed(
                request, authority=authority, revision=1, policy=self.policy
            ).digest()
            for _ in range(500)
        }
        self.assertEqual(len(digests), 1)


if __name__ == "__main__":
    unittest.main()
