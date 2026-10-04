import random
import unittest

from nexy_lo4_lab.authority import AuthorityClaim, AuthorityError, AuthorityLevel, AuthorityProvenanceSeal
from nexy_lo4_lab.output_compiler import ClaimArtifact, EvidenceRecord, ProofCarryingOutputCompiler
from nexy_lo4_lab.planner import ClaimRequirement, MinimumProofPlanner, Probe
from nexy_lo4_lab.uncertainty import ClaimNode, EpistemicStatus, UncertaintyContainmentLattice
from nexy_lo4_lab.witness import RequirementBoundaryWitnessEngine, RequirementSpec


class AdversarialPropertyTests(unittest.TestCase):
    def test_planner_is_permutation_deterministic_over_seeded_cases(self):
        rng = random.Random(74945)
        planner = MinimumProofPlanner(max_exact_claims=8)
        reqs = [ClaimRequirement(f"c{i}", 2) for i in range(5)]
        probes = [Probe("all", 10, 2, frozenset(r.claim_id for r in reqs))]
        for i, req in enumerate(reqs):
            probes.append(Probe(f"single-{i}", 2, 2, frozenset({req.claim_id})))
        baseline = planner.plan(reqs, probes)
        for _ in range(50):
            req_copy = reqs[:]
            probe_copy = probes[:]
            rng.shuffle(req_copy)
            rng.shuffle(probe_copy)
            self.assertEqual(planner.plan(req_copy, probe_copy), baseline)

    def test_lattice_never_contaminates_disconnected_claim(self):
        lattice = UncertaintyContainmentLattice()
        for status in (EpistemicStatus.UNKNOWN, EpistemicStatus.NOT_VERIFIED, EpistemicStatus.CONFLICT, EpistemicStatus.FAIL):
            result = lattice.evaluate([
                ClaimNode("bad", status),
                ClaimNode("dependent", EpistemicStatus.PASS, ("bad",)),
                ClaimNode("isolated", EpistemicStatus.PASS),
            ])
            self.assertEqual(result["dependent"].effective_status, status)
            self.assertEqual(result["isolated"].effective_status, EpistemicStatus.PASS)

    def test_witnesses_self_execute_for_operator_matrix(self):
        engine = RequirementBoundaryWitnessEngine()
        specs = [
            RequirementSpec("eq", "x", "eq", "safe"),
            RequirementSpec("neq", "x", "neq", "blocked"),
            RequirementSpec("min", "x", "min", 2),
            RequirementSpec("max", "x", "max", 5),
            RequirementSpec("in", "x", "in", ("a", "b")),
        ]
        for spec in specs:
            for witness in engine.generate(spec):
                self.assertEqual(engine.evaluate(spec, witness.payload), witness.should_pass)

    def test_compiler_rejects_cross_version_replay(self):
        digest = "d" * 64
        result = ProofCarryingOutputCompiler().compile(
            [ClaimArtifact("c", "claim", digest, EpistemicStatus.PASS, "v2", 2, ("e",))],
            trusted_authority_digests=frozenset({digest}),
            evidence_catalog=(EvidenceRecord("e", "c", 7, True, "v1"),),
        )
        self.assertEqual(result.status, "FREEZE")
        self.assertIn("c:EVIDENCE_TARGET_MISMATCH:e", result.blockers)

    def test_self_asserted_canon_never_seals(self):
        sealer = AuthorityProvenanceSeal({"model": AuthorityLevel.MODEL_PROPOSAL})
        for source in ("fake-canon", "user-ish", "copied-doc"):
            with self.assertRaises(AuthorityError):
                sealer.seal([AuthorityClaim("x", "claim", AuthorityLevel.CANON, source)], "x")


if __name__ == "__main__":
    unittest.main()
