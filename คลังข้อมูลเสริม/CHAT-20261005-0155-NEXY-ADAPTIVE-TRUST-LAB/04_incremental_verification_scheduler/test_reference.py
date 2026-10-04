import unittest
from reference import TestSpec, impacted_nodes, schedule


class TestIVS(unittest.TestCase):
    def test_transitive_impact(self):
        deps = {"api": {"core"}, "ui": {"api"}, "core": {"schema"}}
        self.assertEqual(impacted_nodes(deps, ["schema"]), {"schema", "core", "api", "ui"})

    def test_cost_aware_cover_plan(self):
        deps = {"api": {"core"}, "ui": {"api"}}
        tests = [
            TestSpec("all", frozenset({"core", "api", "ui"}), 4.0),
            TestSpec("core_api", frozenset({"core", "api"}), 1.0),
            TestSpec("ui", frozenset({"ui"}), 1.0),
        ]
        d = schedule(deps, ["core"], tests)
        self.assertEqual(d.status, "PLAN")
        self.assertEqual(d.selected_tests, ("core_api", "ui"))

    def test_uncovered_impact_freezes(self):
        deps = {"api": {"core"}}
        d = schedule(deps, ["core"], [TestSpec("core", frozenset({"core"}), 1.0)])
        self.assertEqual(d.status, "FREEZE")
        self.assertEqual(d.uncovered_nodes, ("api",))

    def test_invalid_cost_freezes(self):
        d = schedule({}, ["x"], [TestSpec("bad", frozenset({"x"}), 0)])
        self.assertEqual(d.status, "FREEZE")

    def test_deterministic_tie_break(self):
        tests = [TestSpec("b", frozenset({"x"}), 1), TestSpec("a", frozenset({"x"}), 1)]
        self.assertEqual(schedule({}, ["x"], tests).selected_tests, ("a",))


if __name__ == "__main__":
    unittest.main()
