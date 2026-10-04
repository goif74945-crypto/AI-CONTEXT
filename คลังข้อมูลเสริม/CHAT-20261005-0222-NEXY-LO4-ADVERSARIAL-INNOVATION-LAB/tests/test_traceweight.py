import unittest

from lo4lab.traceweight import InfluenceGraph, InfluenceNode


class TraceweightTests(unittest.TestCase):
    def test_balanced_verified_sources_pass(self):
        graph = InfluenceGraph([
            InfluenceNode("a", {}, True, True),
            InfluenceNode("b", {}, True, True),
            InfluenceNode("merge", {"a": 1, "b": 1}),
            InfluenceNode("final", {"merge": 1}),
        ])
        report = graph.analyze("final")
        self.assertEqual(report.status, "PASS")
        self.assertAlmostEqual(report.dominance_ratio, 0.5)
        self.assertAlmostEqual(report.effective_source_count, 2.0)

    def test_single_source_dominance_freezes(self):
        graph = InfluenceGraph([
            InfluenceNode("a", {}, True, True),
            InfluenceNode("b", {}, True, True),
            InfluenceNode("final", {"a": 9, "b": 1}),
        ])
        report = graph.analyze("final")
        self.assertEqual(report.status, "FREEZE")
        self.assertIn("single_source_dominance", report.reasons)

    def test_unverified_influence_freezes(self):
        graph = InfluenceGraph([
            InfluenceNode("a", {}, True, True),
            InfluenceNode("b", {}, True, False),
            InfluenceNode("final", {"a": 1, "b": 1}),
        ])
        report = graph.analyze("final", max_dominance_ratio=0.7, max_unverified_influence=0.1)
        self.assertEqual(report.status, "FREEZE")
        self.assertIn("unverified_influence_exceeded", report.reasons)

    def test_cycle_detected(self):
        graph = InfluenceGraph([
            InfluenceNode("a", {"b": 1}),
            InfluenceNode("b", {"a": 1}),
            InfluenceNode("source", {}, True, True),
        ])
        with self.assertRaises(ValueError):
            graph.analyze("a")

    def test_missing_parent_rejected(self):
        with self.assertRaises(ValueError):
            InfluenceGraph([InfluenceNode("x", {"missing": 1})])


if __name__ == "__main__":
    unittest.main()
