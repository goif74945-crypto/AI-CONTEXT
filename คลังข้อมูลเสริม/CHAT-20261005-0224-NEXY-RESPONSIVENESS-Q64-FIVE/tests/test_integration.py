import unittest
from nexy_responsiveness import *
class IntegrationTests(unittest.TestCase):
    def test_pipeline(self):
        l=compile_latency_budget(q("120"),[StageRequirement("authority",q("20"),q("3")),StageRequirement("verification",q("40"),q("5"))]);self.assertEqual(sum(x.allocated.raw for x in l.allocations),q("120").raw)
        w=plan_warmset([ContextChunk("canon",30,1,q("1"),q("1"),q("0")),ContextChunk("counter",20,9,q("1"),q("0.5"),q("0"),True)],55);self.assertIn("counter",w.resident)
        p=plan_prefetch([PrefetchCandidate("read",q("0.8"),q("30"),q("2"),q("0.1"),True),PrefetchCandidate("write",q("1"),q("100"),q("1"),q("0"),False)],q("3"),q("5"));self.assertNotIn("write",p.selected)
        s=schedule_proofs([ProofTask("a",q("5"),q("1"),authority_critical=True),ProofTask("u",q("20"),q("10"),("a",))],2);self.assertTrue(s.tasks)
        a=plan_attention([Notice("conflict",q("1"),q("1"),q("1"),q("1"),authority_conflict=True)],q("0"),0);self.assertIn("conflict",a.surface_now)
