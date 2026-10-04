import unittest

from nexy_lo4_lab.output_compiler import (
    ClaimArtifact,
    EvidenceRecord,
    ProofCarryingOutputCompiler,
)
from nexy_lo4_lab.uncertainty import EpistemicStatus


TRUSTED = "a" * 64


def claim(**overrides):
    data = dict(
        claim_id="c1",
        text="Verified claim.",
        authority_digest=TRUSTED,
        uncertainty_status=EpistemicStatus.PASS,
        target_version="v1",
        evidence_class_required=2,
        evidence_refs=("test-1",),
    )
    data.update(overrides)
    return ClaimArtifact(**data)


def evidence(**overrides):
    data = dict(
        evidence_ref="test-1",
        claim_id="c1",
        evidence_class=2,
        passed=True,
        target_version="v1",
    )
    data.update(overrides)
    return EvidenceRecord(**data)


class ProofCarryingOutputCompilerTests(unittest.TestCase):
    def setUp(self):
        self.compiler = ProofCarryingOutputCompiler()

    def compile(self, claims, records=(evidence(),), trusted=frozenset({TRUSTED})):
        return self.compiler.compile(
            claims,
            trusted_authority_digests=trusted,
            evidence_catalog=records,
        )

    def test_valid_claim_compiles(self):
        out = self.compile([claim()])
        self.assertEqual(out.status, "PASS")
        self.assertEqual(out.output, "Verified claim.")
        self.assertIsNone(out.freeze_code)

    def test_untrusted_authority_digest_freezes(self):
        out = self.compile([claim(authority_digest="b" * 64)])
        self.assertEqual(out.status, "FREEZE")
        self.assertIn("c1:AUTHORITY_DIGEST_UNTRUSTED", out.blockers)

    def test_uncertainty_freezes(self):
        out = self.compile([claim(uncertainty_status=EpistemicStatus.NOT_VERIFIED)])
        self.assertEqual(out.status, "FREEZE")
        self.assertIn("c1:EPISTEMIC_NOT_VERIFIED", out.blockers)

    def test_insufficient_evidence_freezes(self):
        out = self.compile([claim()], records=(evidence(evidence_class=1),))
        self.assertEqual(out.status, "FREEZE")
        self.assertIn("c1:EVIDENCE_E1_LT_E2", out.blockers)

    def test_unknown_evidence_reference_freezes(self):
        out = self.compile([claim(evidence_refs=("ghost",))])
        self.assertEqual(out.status, "FREEZE")
        self.assertIn("c1:EVIDENCE_REF_UNKNOWN:ghost", out.blockers)

    def test_stale_evidence_target_freezes(self):
        out = self.compile([claim(target_version="v2")], records=(evidence(target_version="v1"),))
        self.assertEqual(out.status, "FREEZE")
        self.assertIn("c1:EVIDENCE_TARGET_MISMATCH:test-1", out.blockers)

    def test_failed_evidence_freezes(self):
        out = self.compile([claim()], records=(evidence(passed=False),))
        self.assertEqual(out.status, "FREEZE")
        self.assertIn("c1:EVIDENCE_FAILED:test-1", out.blockers)

    def test_cross_claim_evidence_binding_is_rejected(self):
        out = self.compile([claim()], records=(evidence(claim_id="other"),))
        self.assertEqual(out.status, "FREEZE")
        self.assertIn("c1:EVIDENCE_BINDING_MISMATCH:test-1", out.blockers)

    def test_required_evidence_without_reference_freezes(self):
        out = self.compile([claim(evidence_refs=())], records=())
        self.assertEqual(out.status, "FREEZE")
        self.assertIn("c1:EVIDENCE_REF_MISSING", out.blockers)

    def test_digest_changes_if_evidence_result_changes(self):
        passing = self.compile([claim()], records=(evidence(passed=True),)).digest
        failing = self.compile([claim()], records=(evidence(passed=False),)).digest
        self.assertNotEqual(passing, failing)

    def test_digest_does_not_depend_on_claim_input_order(self):
        a = claim(claim_id="a", text="A", evidence_refs=("ea",))
        b = claim(claim_id="b", text="B", evidence_refs=("eb",))
        records = (
            EvidenceRecord("ea", "a", 2, True, "v1"),
            EvidenceRecord("eb", "b", 2, True, "v1"),
        )
        self.assertEqual(
            self.compile([a, b], records=records).digest,
            self.compile([b, a], records=reversed(records)).digest,
        )


if __name__ == "__main__":
    unittest.main()
