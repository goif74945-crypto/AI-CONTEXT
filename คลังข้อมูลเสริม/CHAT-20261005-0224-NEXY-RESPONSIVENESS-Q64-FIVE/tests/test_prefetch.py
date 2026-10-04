import unittest
from nexy_responsiveness import PrefetchCandidate,Q64,plan_prefetch,q
class PrefetchTests(unittest.TestCase):
    def c(self,i,p,s,c,r,ro=True,ready=True): return PrefetchCandidate(i,q(p),q(s),q(c),q(r),ro,ready)
    def test_reject_write(self): self.assertFalse(plan_prefetch([self.c("w","1","10","1","0",False)],q("10"),q("1")).selected)
    def test_budget(self):
        d=plan_prefetch([self.c("a","0.9","10","2","0.1"),self.c("b","0.5","20","4","0.1")],q("4"),q("2"));self.assertEqual(d.selected,("a",))
    def test_tie(self): self.assertEqual(plan_prefetch([self.c("b","1","2","1","0"),self.c("a","1","2","1","0")],q("1"),Q64.zero()).selected,("a",))
