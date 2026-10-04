import unittest

from frontierfive.correlation_quorum import Witness, verify_independent_quorum


class CorrelationQuorumTests(unittest.TestCase):
    def w(self, wid, domains, verdict="PASS", artifact="h"):
        return Witness(wid, "claim", artifact, verdict, tuple(domains))

    def test_independent_quorum_allows(self):
        v = verify_independent_quorum(
            [self.w("a", ["model:gpt", "runtime:r1"]), self.w("b", ["model:gemini", "runtime:r2"])],
            claim_id="claim", artifact_hash="h", k=2,
        )
        self.assertEqual(v.status, "ALLOW")
        self.assertEqual(v.payload["quorum"], ["a", "b"])

    def test_shared_failure_domain_blocks_false_consensus(self):
        v = verify_independent_quorum(
            [self.w("a", ["retrieval:same"]), self.w("b", ["retrieval:same"])],
            claim_id="claim", artifact_hash="h", k=2,
        )
        self.assertIn("INSUFFICIENT_INDEPENDENT_QUORUM", v.reasons)
        self.assertIn("retrieval:same", v.payload["repeated_failure_domains"])

    def test_selects_independent_subset(self):
        v = verify_independent_quorum(
            [self.w("a", ["m:1"]), self.w("b", ["m:1"]), self.w("c", ["m:2"])],
            claim_id="claim", artifact_hash="h", k=2,
        )
        self.assertEqual(v.status, "ALLOW")
        self.assertEqual(v.payload["quorum"], ["a", "c"])

    def test_target_mismatch_freezes(self):
        v = verify_independent_quorum([self.w("a", ["x"], artifact="other")], claim_id="claim", artifact_hash="h", k=1)
        self.assertIn("WITNESS_TARGET_MISMATCH", v.reasons)

    def test_fail_verdict_does_not_count(self):
        v = verify_independent_quorum([self.w("a", ["x"], verdict="FAIL")], claim_id="claim", artifact_hash="h", k=1)
        self.assertIn("INSUFFICIENT_INDEPENDENT_QUORUM", v.reasons)
