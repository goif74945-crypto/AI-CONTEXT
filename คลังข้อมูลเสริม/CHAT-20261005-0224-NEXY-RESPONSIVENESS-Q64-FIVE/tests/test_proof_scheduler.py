import unittest
from nexy_responsiveness import ProofScheduleFreeze,ProofTask,schedule_proofs,q
class ProofTests(unittest.TestCase):
    def test_deps(self):
        p=schedule_proofs([ProofTask("s",q("2"),q("1"),authority_critical=True),ProofTask("u",q("5"),q("8"),("s",))],2);b={x.task_id:x for x in p.tasks};self.assertGreaterEqual(b["u"].start,b["s"].end)
    def test_cycle(self):
        with self.assertRaises(ProofScheduleFreeze): schedule_proofs([ProofTask("a",q("1"),q("1"),("b",)),ProofTask("b",q("1"),q("1"),("a",))],2)
