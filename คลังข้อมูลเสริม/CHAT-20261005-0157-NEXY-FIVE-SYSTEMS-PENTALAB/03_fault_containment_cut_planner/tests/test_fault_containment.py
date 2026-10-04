import itertools
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from fault_containment import Component, ContainmentInputError, Dependency, plan_containment


class FaultContainmentTests(unittest.TestCase):
    def base_components(self):
        return [
            Component("db"),
            Component("search"),
            Component("api", mandatory=True),
            Component("analytics"),
            Component("ui", mandatory=True),
        ]

    def test_hard_failure_propagates_minimal_closure(self):
        deps = [
            Dependency("db", "api", "HARD"),
            Dependency("api", "ui", "HARD"),
            Dependency("db", "analytics", "SOFT"),
            Dependency("search", "ui", "SOFT"),
        ]
        r = plan_containment(self.base_components(), deps, ["db"])
        self.assertEqual(r.status, "FREEZE")
        self.assertEqual(r.quarantined, ("api", "db", "ui"))
        self.assertEqual(r.degraded, ("analytics",))
        self.assertEqual(r.reason_path("ui"), ("db", "api", "ui"))
        self.assertEqual(dict(r.reason_parents)["ui"], "api")

    def test_soft_failure_degrades_but_does_not_quarantine_consumer(self):
        comps = [Component("telemetry"), Component("core", mandatory=True)]
        r = plan_containment(comps, [Dependency("telemetry", "core", "SOFT")], ["telemetry"])
        self.assertEqual(r.status, "DEGRADED")
        self.assertEqual(r.quarantined, ("telemetry",))
        self.assertEqual(r.degraded, ("core",))

    def test_isolated_edge_does_not_propagate(self):
        comps = [Component("sandbox"), Component("core", mandatory=True)]
        r = plan_containment(comps, [Dependency("sandbox", "core", "ISOLATED")], ["sandbox"])
        self.assertEqual(r.status, "DEGRADED")
        self.assertEqual(r.healthy, ("core",))

    def test_hard_cycle_closes_without_infinite_loop(self):
        comps = [Component("a"), Component("b"), Component("c")]
        deps = [Dependency("a", "b", "HARD"), Dependency("b", "a", "HARD"), Dependency("b", "c", "HARD")]
        self.assertEqual(plan_containment(comps, deps, ["a"]).quarantined, ("a", "b", "c"))

    def test_unknown_reference_is_rejected(self):
        with self.assertRaises(ContainmentInputError):
            plan_containment([Component("a")], [Dependency("missing", "a", "HARD")], ["a"])

    def test_input_order_is_deterministic(self):
        comps = [Component("a"), Component("b"), Component("c")]
        deps = [Dependency("a", "b", "SOFT"), Dependency("a", "c", "HARD")]
        fps = set()
        for cp in itertools.permutations(comps):
            for dp in itertools.permutations(deps):
                fps.add(plan_containment(cp, dp, ["a"]).fingerprint)
        self.assertEqual(len(fps), 1)

    def test_no_failure_is_full(self):
        r = plan_containment([Component("a", mandatory=True)], [], [])
        self.assertEqual(r.status, "FULL")
        self.assertEqual(r.healthy, ("a",))


if __name__ == "__main__":
    unittest.main()
