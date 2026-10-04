import unittest
from nexy_responsiveness import LatencyBudgetFreeze,StageRequirement,compile_latency_budget,q
class LatencyTests(unittest.TestCase):
    def test_total(self):
        p=compile_latency_budget(q("100"),[StageRequirement("a",q("20"),q("3")),StageRequirement("v",q("30"),q("2"))]);self.assertEqual(sum(x.allocated.raw for x in p.allocations),q("100").raw)
    def test_freeze(self):
        with self.assertRaises(LatencyBudgetFreeze): compile_latency_budget(q("10"),[StageRequirement("a",q("6"),q("1")),StageRequirement("b",q("6"),q("1"))])
