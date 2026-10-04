import unittest
from dataclasses import replace

from frontierfive.approval_escrow import issue_seal, verify_seal


class ApprovalEscrowTests(unittest.TestCase):
    def setUp(self):
        self.key = b"unit-test-key-not-a-production-secret"
        self.plan = {"actions": ["write:a", "write:b"], "scope": ["a", "b"]}
        self.seal = issue_seal(
            self.plan,
            authority_id="user:1",
            allowed_scope=["a", "b"],
            expires_at=200,
            directive_epoch=7,
            max_mutations=2,
            key=self.key,
        )

    def verify(self, plan=None, seal=None, **kw):
        return verify_seal(
            plan or self.plan,
            seal or self.seal,
            requested_scope=kw.get("requested_scope", ["a"]),
            mutation_count=kw.get("mutation_count", 1),
            now=kw.get("now", 100),
            current_directive_epoch=kw.get("epoch", 7),
            key=kw.get("key", self.key),
        )

    def test_valid_seal_allows(self):
        self.assertEqual(self.verify().status, "ALLOW")

    def test_tampered_plan_freezes(self):
        v = self.verify(plan={"actions": ["write:x"]})
        self.assertIn("PLAN_HASH_MISMATCH", v.reasons)

    def test_expired_epoch_scope_budget_and_signature_each_freeze(self):
        self.assertIn("APPROVAL_EXPIRED", self.verify(now=201).reasons)
        self.assertIn("DIRECTIVE_EPOCH_MISMATCH", self.verify(epoch=8).reasons)
        self.assertIn("SCOPE_ESCALATION", self.verify(requested_scope=["a", "c"]).reasons)
        self.assertIn("MUTATION_BUDGET_EXCEEDED", self.verify(mutation_count=3).reasons)
        self.assertIn("SEAL_SIGNATURE_INVALID", self.verify(key=b"wrong").reasons)

    def test_seal_payload_tamper_invalidates_signature(self):
        bad = replace(self.seal, max_mutations=99)
        self.assertIn("SEAL_SIGNATURE_INVALID", self.verify(seal=bad).reasons)
