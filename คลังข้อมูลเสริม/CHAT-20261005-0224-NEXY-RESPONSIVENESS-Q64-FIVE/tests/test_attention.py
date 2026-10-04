import unittest
from nexy_responsiveness import Notice,plan_attention,q
class AttentionTests(unittest.TestCase):
    def n(self,i,**f): return Notice(i,q("1"),q("1"),q("1"),q("1"),**f)
    def test_mandatory(self):
        p=plan_attention([self.n("b",blocker=True),self.n("s",security=True),self.n("c",authority_conflict=True)],q("0"),0);self.assertEqual(set(p.mandatory),{"b","s","c"})
