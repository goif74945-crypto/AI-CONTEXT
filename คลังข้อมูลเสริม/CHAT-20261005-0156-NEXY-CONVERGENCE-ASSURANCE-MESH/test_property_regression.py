from __future__ import annotations

import itertools
import random
import unittest

from c1_interpretation_convergence.implementation import DecisionSignature, Interpretation, evaluate_convergence
from c2_context_noninterference.implementation import MutationSet, verify_noninterference
from c3_evidence_acquisition.implementation import ClaimNeed, Probe, plan_evidence_acquisition
from c4_resume_equivalence.implementation import ResumeState, compile_capsule
from c5_independent_evidence_quorum.implementation import EvidenceRecord, QuorumNeed, evaluate_independent_quorum


class PropertyRegressionTests(unittest.TestCase):
    def test_interpretation_permutation_invariance(self) -> None:
        base = [Interpretation(str(i), {"target": "vault"}) for i in range(5)]
        evaluator = lambda item: DecisionSignature("read", item.variables["target"], ("x",), ("none",), "law")
        expected = evaluate_convergence(base, evaluator).details
        for permutation in itertools.islice(itertools.permutations(base), 120):
            self.assertEqual(evaluate_convergence(permutation, evaluator).details, expected)

    def test_evidence_planner_matches_bruteforce_small_random_instances(self) -> None:
        rng = random.Random(74945)
        for case_index in range(160):
            needs = [ClaimNeed(f"c{i}", "E2") for i in range(rng.randint(1, 4))]
            probes = []
            for j in range(rng.randint(1, 7)):
                produces = {
                    need.claim_id: rng.choice(("E1", "E2", "E3"))
                    for need in needs
                    if rng.random() < 0.55
                }
                probes.append(Probe(f"p{j}", rng.randint(0, 7), produces))

            result = plan_evidence_acquisition(needs, probes)
            target = {need.claim_id for need in needs}
            candidates = []
            for size in range(len(probes) + 1):
                for combo in itertools.combinations(probes, size):
                    covered = {
                        claim
                        for probe in combo
                        for claim, klass in probe.produces.items()
                        if claim in target and int(klass[1:]) >= 2
                    }
                    if covered == target:
                        ids = tuple(sorted(p.probe_id for p in combo))
                        candidates.append((sum(p.cost for p in combo), len(combo), ids))
            if not candidates:
                self.assertEqual(result.status, "FREEZE", msg=f"case={case_index}")
            else:
                expected = min(candidates)
                self.assertEqual(result.status, "PLANNED", msg=f"case={case_index}")
                self.assertEqual(result.details["total_cost"], expected[0], msg=f"case={case_index}")
                self.assertEqual(tuple(result.details["selected_probes"]), expected[2], msg=f"case={case_index}")

    def test_noninterference_stable_function_survives_random_mutations(self) -> None:
        rng = random.Random(17)
        values = tuple(rng.randint(-10_000, 10_000) for _ in range(20))
        result = verify_noninterference(
            {"authority": "allow", "noise": 0},
            [MutationSet("noise", values)],
            lambda ctx: {"decision": ctx["authority"]},
            include_joint_case=False,
        )
        self.assertEqual(result.status, "PASS")

    def test_resume_capsule_ignores_mapping_insertion_order(self) -> None:
        rng = random.Random(99)
        items = [(f"k{i}", i) for i in range(10)]
        reference = None
        for _ in range(100):
            rng.shuffle(items)
            state = ResumeState("t", "law", "target", dict(items))
            capsule = compile_capsule(state, lambda critical: critical["resume_critical"]["k0"])
            if reference is None:
                reference = capsule
            self.assertEqual(capsule, reference)

    def test_quorum_simple_random_case_matches_pairwise_rule(self) -> None:
        rng = random.Random(2026)
        for case_index in range(150):
            records = []
            for i in range(rng.randint(0, 6)):
                records.append(
                    EvidenceRecord(
                        f"e{i}",
                        "claim",
                        "E3",
                        f"producer-{rng.randint(0, 3)}",
                        frozenset({f"domain-{rng.randint(0, 3)}"}),
                    )
                )
            expected = any(
                a.producer != b.producer and a.failure_domains.isdisjoint(b.failure_domains)
                for a, b in itertools.combinations(records, 2)
            )
            result = evaluate_independent_quorum(QuorumNeed("claim", "E3", 2), records)
            self.assertEqual(result.status == "PASS", expected, msg=f"case={case_index}")


if __name__ == "__main__":
    unittest.main()
