import itertools
import unittest

from nexy_meta_assurance.conservation import ConservationRule, verify_transition
from nexy_meta_assurance.fingerprint import ScenarioRecord, build_fingerprint
from nexy_meta_assurance.metamorphic import MetamorphicRelation, verify_relation
from nexy_meta_assurance.spec_mutation import Constraint, ConstraintOp, generate_illegal_mutations, validate_spec
from nexy_meta_assurance.witness import EvidenceItem, extract_minimal_witness


class DeterministicStressTests(unittest.TestCase):
    def test_metamorphic_affine_shift_grid(self):
        subject = lambda x: 7 * x - 11
        checked = 0
        for x in range(-20, 21):
            for shift in range(-5, 6):
                result = verify_relation(
                    subject,
                    x,
                    MetamorphicRelation(
                        f"affine-shift-{shift}",
                        "shift_int",
                        "delta_int",
                        transform_arg=shift,
                        expectation_arg=7 * shift,
                    ),
                )
                self.assertTrue(result.passed)
                checked += 1
        self.assertEqual(checked, 451)

    def test_conservation_transfer_grid(self):
        rule = ConservationRule("three-account balance", ("a", "b", "c"))
        checked = 0
        for a in range(0, 11):
            for b in range(0, 11 - a):
                c = 10 - a - b
                for transfer in range(0, min(a, 3) + 1):
                    result = verify_transition(
                        {"a": a, "b": b, "c": c},
                        {"a": a - transfer, "b": b + transfer, "c": c},
                        rule,
                    )
                    self.assertTrue(result.passed)
                    checked += 1
        self.assertGreater(checked, 100)

    def test_witness_dp_matches_bruteforce_objective(self):
        requirements = ("R1", "R2", "R3", "R4")
        items = (
            EvidenceItem("E1", frozenset({"R1", "R2"}), 3),
            EvidenceItem("E2", frozenset({"R2", "R3"}), 2),
            EvidenceItem("E3", frozenset({"R3", "R4"}), 2),
            EvidenceItem("E4", frozenset({"R1"}), 1),
            EvidenceItem("E5", frozenset({"R4"}), 1),
            EvidenceItem("E6", frozenset({"R1", "R2", "R3", "R4"}), 7),
        )
        result = extract_minimal_witness(requirements, items)

        best = None
        for size in range(len(items) + 1):
            for combo in itertools.combinations(items, size):
                covered = set().union(*(item.covers for item in combo)) if combo else set()
                if covered != set(requirements):
                    continue
                ids = tuple(sorted(item.evidence_id for item in combo))
                score = (sum(item.cost for item in combo), len(combo), ids)
                if best is None or score < best:
                    best = score
        self.assertIsNotNone(best)
        self.assertEqual((result.total_cost, len(result.selected_ids), result.selected_ids), best)

    def test_fingerprint_is_stable_across_all_scenario_permutations(self):
        records = (
            ScenarioRecord("S1", {"x": 1}, "PASS", {"y": 2}),
            ScenarioRecord("S2", {"x": 2}, "FREEZE", {"reason": "missing-evidence"}),
            ScenarioRecord("S3", {"x": 3}, "PASS", {"y": 6}),
            ScenarioRecord("S4", {"x": 4}, "FAIL", {"reason": "constraint"}),
        )
        expected = build_fingerprint(records).digest
        digests = {build_fingerprint(permutation).digest for permutation in itertools.permutations(records)}
        self.assertEqual(digests, {expected})

    def test_each_generated_spec_mutation_breaks_its_target_constraint(self):
        spec = {
            "mode": "verify_only",
            "minimum": 3,
            "maximum": 9,
            "tier": "safe",
            "owners": ("human",),
        }
        constraints = (
            Constraint("EQ", "mode", ConstraintOp.EQ, "verify_only"),
            Constraint("MIN", "minimum", ConstraintOp.MIN_INT, 3),
            Constraint("MAX", "maximum", ConstraintOp.MAX_INT, 9),
            Constraint("MEMBER", "tier", ConstraintOp.MEMBER_OF, ("safe", "strict")),
            Constraint("NONEMPTY", "owners", ConstraintOp.NONEMPTY),
        )
        mutations = generate_illegal_mutations(spec, constraints)
        self.assertEqual(len(mutations), len(constraints))
        for mutation in mutations:
            mutated = dict(spec)
            mutated[mutation.field] = mutation.mutated_value
            violations = validate_spec(mutated, constraints)
            self.assertIn(mutation.constraint_id, violations)


if __name__ == "__main__":
    unittest.main()
