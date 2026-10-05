import importlib
import math
import random
import unittest

from frontier_assurance_lab import FreezeError, ParetoPruner, Plan


def api(testcase):
    try:
        return importlib.import_module("parex_metric_integrity")
    except ModuleNotFoundError:
        testcase.fail("parex_metric_integrity implementation is missing")


def profile(testcase, **overrides):
    module = api(testcase)
    axes = (
        module.MetricAxis("benefit", "MAX", "benefit_point", 0, 100),
        module.MetricAxis("evidence", "MAX", "evidence_point", 0, 100),
        module.MetricAxis("cost", "MIN", "cost_point", 0, 100),
        module.MetricAxis("latency", "MIN", "millisecond", 0, 10000),
        module.MetricAxis("risk", "MIN", "risk_point", 0, 100),
    )
    values = {
        "contract_id": "parex-profile-v1",
        "transformation_digest": "a" * 64,
        "axes": axes,
    }
    values.update(overrides)
    return module.ParexMetricContract(**values)


def plan(testcase, contract, pid="a", values=(10, 9, 3, 4, 2), **overrides):
    module = api(testcase)
    kwargs = {
        "pid": pid,
        "profile_hash": contract.profile_hash(),
        "benefit": values[0],
        "evidence": values[1],
        "cost": values[2],
        "latency": values[3],
        "risk": values[4],
        "metric_evidence": tuple(
            (name, f"evidence://{pid}/{name}")
            for name in ("benefit", "evidence", "cost", "latency", "risk")
        ),
    }
    kwargs.update(overrides)
    return module.AttestedPlan(**kwargs)


class MetricIntegrityPositiveTests(unittest.TestCase):
    def test_valid_plans_delegate_to_original_dominance(self):
        module = api(self)
        contract = profile(self)
        result = module.MetricIntegrityPruner().prune(
            contract,
            [plan(self, contract, "worse", (8, 8, 5, 4, 3)), plan(self, contract)],
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["frontier"], ["a"])
        self.assertEqual(result["pruned"]["worse"]["reason"], "PARETO_DOMINATED")

    def test_tradeoff_frontier_is_preserved(self):
        module = api(self)
        contract = profile(self)
        result = module.MetricIntegrityPruner().prune(
            contract,
            [
                plan(self, contract, "cheap", (6, 6, 1, 3, 2)),
                plan(self, contract, "strong", (10, 10, 5, 5, 1)),
            ],
        )
        self.assertEqual(result["frontier"], ["cheap", "strong"])

    def test_result_binds_profile_and_admitted_candidate_digest(self):
        module = api(self)
        contract = profile(self)
        result = module.MetricIntegrityPruner().prune(contract, [plan(self, contract)])
        self.assertEqual(result["metric_profile_hash"], contract.profile_hash())
        self.assertRegex(result["admitted_candidates_hash"], r"^[0-9a-f]{64}$")
        self.assertRegex(result["result_hash"], r"^[0-9a-f]{64}$")


class MetricIntegrityNegativeTests(unittest.TestCase):
    def assert_rejected(self, candidate):
        module = api(self)
        contract = profile(self)
        with self.assertRaises(FreezeError):
            module.MetricIntegrityPruner().prune(contract, [candidate(contract)])

    def test_nan_metric_rejected(self):
        self.assert_rejected(lambda c: plan(self, c, benefit=math.nan))

    def test_infinity_metric_rejected(self):
        self.assert_rejected(lambda c: plan(self, c, benefit=math.inf))

    def test_boolean_metric_rejected(self):
        self.assert_rejected(lambda c: plan(self, c, benefit=True))

    def test_integral_float_metric_rejected(self):
        self.assert_rejected(lambda c: plan(self, c, benefit=10.0))

    def test_out_of_bounds_metric_rejected(self):
        self.assert_rejected(lambda c: plan(self, c, latency=10001))

    def test_wrong_profile_hash_rejected(self):
        self.assert_rejected(lambda c: plan(self, c, profile_hash="0" * 64))

    def test_missing_axis_evidence_rejected(self):
        self.assert_rejected(
            lambda c: plan(
                self,
                c,
                metric_evidence=(("benefit", "evidence://a/benefit"),),
            )
        )

    def test_duplicate_axis_evidence_rejected(self):
        self.assert_rejected(
            lambda c: plan(
                self,
                c,
                metric_evidence=(
                    ("benefit", "evidence://1"),
                    ("benefit", "evidence://2"),
                    ("evidence", "evidence://3"),
                    ("cost", "evidence://4"),
                    ("latency", "evidence://5"),
                    ("risk", "evidence://6"),
                ),
            )
        )

    def test_duplicate_plan_id_rejected(self):
        module = api(self)
        contract = profile(self)
        with self.assertRaises(FreezeError):
            module.MetricIntegrityPruner().prune(
                contract, [plan(self, contract), plan(self, contract)]
            )

    def test_empty_plan_set_rejected(self):
        module = api(self)
        with self.assertRaises(FreezeError):
            module.MetricIntegrityPruner().prune(profile(self), [])

    def test_foreign_candidate_fails_closed(self):
        module = api(self)
        with self.assertRaises(FreezeError):
            module.MetricIntegrityPruner().prune(profile(self), [object()])

    def test_unhashable_evidence_axis_fails_closed(self):
        self.assert_rejected(
            lambda c: plan(
                self,
                c,
                metric_evidence=(
                    (["benefit"], "evidence://1"),
                    ("evidence", "evidence://2"),
                    ("cost", "evidence://3"),
                    ("latency", "evidence://4"),
                    ("risk", "evidence://5"),
                ),
            )
        )


class MetricIntegrityAdversarialTests(unittest.TestCase):
    def test_axis_direction_tampering_rejected(self):
        module = api(self)
        axes = list(profile(self).axes)
        axes[0] = module.MetricAxis("benefit", "MIN", "benefit_point", 0, 100)
        with self.assertRaises(FreezeError):
            module.MetricIntegrityPruner().prune(profile(self, axes=tuple(axes)), [])

    def test_unit_change_changes_profile_and_blocks_mixed_candidate(self):
        module = api(self)
        original = profile(self)
        axes = list(original.axes)
        axes[3] = module.MetricAxis("latency", "MIN", "second", 0, 10000)
        changed = profile(self, axes=tuple(axes))
        self.assertNotEqual(original.profile_hash(), changed.profile_hash())
        with self.assertRaises(FreezeError):
            module.MetricIntegrityPruner().prune(changed, [plan(self, original)])

    def test_100_input_permutations_are_deterministic(self):
        module = api(self)
        contract = profile(self)
        candidates = [
            plan(self, contract, "a", (10, 8, 3, 5, 1)),
            plan(self, contract, "b", (8, 8, 4, 5, 2)),
            plan(self, contract, "c", (7, 10, 2, 8, 1)),
            plan(self, contract, "d", (1, 1, 9, 9, 9), hard_eligible=False),
        ]
        pruner = module.MetricIntegrityPruner()
        expected = pruner.prune(contract, candidates)
        rng = random.Random(74945)
        for _ in range(100):
            sample = candidates[:]
            rng.shuffle(sample)
            self.assertEqual(pruner.prune(contract, sample), expected)


class MetricIntegrityIntegrationTests(unittest.TestCase):
    def test_valid_adapter_result_matches_original_pareto_fields(self):
        module = api(self)
        contract = profile(self)
        candidates = [
            plan(self, contract, "a", (10, 9, 3, 4, 2)),
            plan(self, contract, "b", (8, 8, 5, 4, 3)),
        ]
        original = ParetoPruner().prune(
            [Plan(p.pid, p.benefit, p.evidence, p.cost, p.latency, p.risk) for p in candidates]
        )
        admitted = module.MetricIntegrityPruner().prune(contract, candidates)
        for key in ("status", "frontier", "pruned"):
            self.assertEqual(admitted[key], original[key])

    def test_original_nan_pass_is_blocked_by_integrity_adapter(self):
        module = api(self)
        self.assertEqual(ParetoPruner().prune([Plan("x", math.nan, 1, 1, 1, 1)])["status"], "PASS")
        contract = profile(self)
        with self.assertRaises(FreezeError):
            module.MetricIntegrityPruner().prune(
                contract, [plan(self, contract, "x", benefit=math.nan)]
            )


if __name__ == "__main__":
    unittest.main()
