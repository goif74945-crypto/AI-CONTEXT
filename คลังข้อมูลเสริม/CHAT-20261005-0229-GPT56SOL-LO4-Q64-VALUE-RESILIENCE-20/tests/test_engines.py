import random
import unittest

from lo4q64 import Q64, SPECS, canonical_evaluation, canonical_input, evaluate, sha256_hex
from lo4q64.contracts import Decision


def value(seed: int, key: str) -> Q64:
    # Stable deterministic pseudo-random unit value independent of Python hash randomization.
    acc = seed
    for ch in key.encode("utf-8"):
        acc = (acc * 131 + ch) % 10_001
    return Q64.from_basis_points(acc)


def case_for(concept_id: str, seed: int = 7):
    spec = SPECS[concept_id]
    return {k: value(seed, f"{concept_id}:{k}") for k in spec.required_inputs}


class EngineTests(unittest.TestCase):
    def test_registry_has_exactly_20_unique_concepts(self):
        self.assertEqual(len(SPECS), 20)
        self.assertEqual(len(set(SPECS)), 20)
        self.assertEqual(len({s.title for s in SPECS.values()}), 20)

    def test_all_concepts_execute_and_remain_unit_bounded(self):
        for cid in SPECS:
            with self.subTest(cid=cid):
                result = evaluate(cid, case_for(cid))
                self.assertGreaterEqual(result.readiness.raw, 0)
                self.assertLessEqual(result.readiness.raw, 1 << 64)
                self.assertGreaterEqual(result.confidence.raw, 0)
                self.assertLessEqual(result.confidence.raw, 1 << 64)
                self.assertIn(result.decision, set(Decision))

    def test_exact_replay_determinism(self):
        for cid in SPECS:
            values = case_for(cid, 91)
            first = canonical_evaluation(evaluate(cid, values))
            for _ in range(20):
                self.assertEqual(first, canonical_evaluation(evaluate(cid, dict(reversed(list(values.items()))))))

    def test_canonical_input_key_order_independent(self):
        for cid in SPECS:
            values = case_for(cid, 33)
            forward = canonical_input(cid, values)
            reverse = canonical_input(cid, dict(reversed(list(values.items()))))
            self.assertEqual(forward, reverse)
            self.assertEqual(sha256_hex(forward), sha256_hex(reverse))

    def test_missing_and_extra_inputs_fail_closed(self):
        for cid, spec in SPECS.items():
            values = case_for(cid)
            missing = dict(values)
            missing.pop(spec.required_inputs[0])
            with self.assertRaises(ValueError):
                evaluate(cid, missing)
            extra = dict(values)
            extra["__unexpected__"] = Q64.zero()
            with self.assertRaises(ValueError):
                evaluate(cid, extra)

    def test_out_of_domain_fails_closed(self):
        cid = "L4Q64-01"
        values = case_for(cid)
        values["expected_value"] = Q64.from_int(2)
        with self.assertRaises(Exception):
            evaluate(cid, values)

    def test_low_confidence_freezes(self):
        cid = "L4Q64-01"
        values = {k: Q64.one() for k in SPECS[cid].required_inputs}
        values["evidence_strength"] = Q64.zero()
        values["estimate_stability"] = Q64.zero()
        self.assertEqual(evaluate(cid, values).decision, Decision.FREEZE)

    def test_adversarial_boundaries_no_crash(self):
        boundaries = [Q64.zero(), Q64.from_ratio(1, 10_000), Q64.from_ratio(1, 2), Q64.from_ratio(9_999, 10_000), Q64.one()]
        rng = random.Random(20261005)
        for cid, spec in SPECS.items():
            for _ in range(200):
                values = {k: rng.choice(boundaries) for k in spec.required_inputs}
                result = evaluate(cid, values)
                self.assertGreaterEqual(result.readiness.raw, 0)
                self.assertLessEqual(result.readiness.raw, 1 << 64)


if __name__ == "__main__":
    unittest.main()
