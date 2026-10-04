import unittest
from lo4_frontier.dependency_dominator_analyzer.engine import compute_dominators, critical_dominators

class DominatorTests(unittest.TestCase):
    def setUp(self):
        self.graph = {"root":["a","b"],"a":["c"],"b":["c"],"c":["x","y"],"x":[],"y":[]}

    def test_computes_dominators(self):
        dom = compute_dominators(self.graph, "root")
        self.assertEqual(dom["c"], frozenset({"root","c"}))
        self.assertEqual(dom["x"], frozenset({"root","c","x"}))

    def test_finds_shared_chokepoint(self):
        self.assertEqual(critical_dominators(self.graph, "root", ["x","y"]), ("c",))

    def test_ignores_unreachable_nodes(self):
        graph = dict(self.graph)
        graph["z"] = []
        self.assertNotIn("z", compute_dominators(graph, "root"))
