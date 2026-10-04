import unittest
from nexy_responsiveness import ContextChunk,WarmsetFreeze,plan_warmset,q
class WarmTests(unittest.TestCase):
    def c(self,i,t,r,c=False): return ContextChunk(i,t,r,q("1"),q("1"),q("0"),c)
    def test_pins(self):
        p=plan_warmset([self.c("spec",10,1),self.c("counter",10,9,True),self.c("doc",10,9)],20);self.assertIn("spec",p.resident);self.assertIn("counter",p.resident)
    def test_freeze(self):
        with self.assertRaises(WarmsetFreeze): plan_warmset([self.c("spec",11,1)],10)
