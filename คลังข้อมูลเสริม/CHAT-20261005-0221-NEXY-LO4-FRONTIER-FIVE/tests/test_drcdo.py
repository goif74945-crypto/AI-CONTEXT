import unittest

from nexy_lo4_frontier import FrontierInputError, ReplayCapsule, differential_oracle


class DeterministicReplayOracleTests(unittest.TestCase):
    def capsule(self):
        return ReplayCapsule(
            "cap-1",
            {"op": "sum", "values": [1, 2, 3]},
            {"mode": "strict"},
            "a" * 64,
            (("calculator", "1.0"),),
            7,
        )

    def test_equivalent_executors_pass_despite_mapping_order(self):
        def a(c):
            return {"result": sum(c.request["values"]), "status": "PASS"}

        def b(c):
            return {"status": "PASS", "result": 6}

        report = differential_oracle(self.capsule(), {"b": b, "a": a})
        self.assertEqual(report.status, "PASS")
        self.assertEqual(report.divergent_executors, ())
        self.assertEqual(report.reference_executor, "a")

    def test_output_divergence_freezes(self):
        report = differential_oracle(self.capsule(), {"a": lambda c: {"result": 6}, "b": lambda c: {"result": 7}})
        self.assertEqual(report.status, "FREEZE")
        self.assertEqual(report.divergent_executors, ("b",))

    def test_executor_exception_becomes_freeze_evidence(self):
        def bad(_):
            raise RuntimeError("boom")

        report = differential_oracle(self.capsule(), {"a": lambda c: {"result": 6}, "bad": bad})
        self.assertEqual(report.status, "FREEZE")
        fault = [r for r in report.results if r.executor_id == "bad"][0]
        self.assertEqual(fault.error_code, "EXECUTOR_EXCEPTION:RuntimeError")

    def test_executor_mutation_cannot_poison_later_replays(self):
        capsule = self.capsule()

        def mutator(c):
            c.request["values"].append(999)
            return {"result": sum(c.request["values"])}

        def observer(c):
            return {"result": sum(c.request["values"])}

        report = differential_oracle(capsule, {"mutator": mutator, "observer": observer})
        self.assertEqual(report.status, "FREEZE")
        observed = {r.executor_id: r.output for r in report.results}
        self.assertEqual(observed["observer"], {"result": 6})
        self.assertEqual(capsule.request["values"], [1, 2, 3])

    def test_invalid_policy_hash_rejected(self):
        c = ReplayCapsule("x", {}, {}, "not-a-hash", (), 0)
        with self.assertRaisesRegex(FrontierInputError, "POLICY_HASH"):
            differential_oracle(c, {"a": lambda x: {}})


if __name__ == "__main__":
    unittest.main()
