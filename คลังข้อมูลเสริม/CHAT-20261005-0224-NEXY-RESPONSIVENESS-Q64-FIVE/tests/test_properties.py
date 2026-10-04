import random,unittest
from fractions import Fraction
from nexy_responsiveness import *
from nexy_responsiveness.q64 import Q64,SCALE
class PropertyTests(unittest.TestCase):
    def test_q64_500(self):
        r=random.Random(74945)
        for _ in range(500):
            a=Q64.from_ratio(r.randint(-10000,10000),r.randint(1,1000));b=Q64.from_ratio(r.randint(-10000,10000),r.randint(1,1000))
            self.assertLessEqual(abs((a*b).to_fraction()-a.to_fraction()*b.to_fraction()),Fraction(1,2*SCALE))
    def test_latency_200(self):
        r=random.Random(1001)
        for _ in range(200):
            n=r.randint(1,8);mins=[r.randint(0,20) for _ in range(n)];total=sum(mins)+r.randint(0,100);p=compile_latency_budget(q(total),[StageRequirement(f"s{i}",q(mins[i]),q(r.randint(1,10))) for i in range(n)]);self.assertEqual(sum(x.allocated.raw for x in p.allocations),q(total).raw)
    def test_prefetch_200(self):
        r=random.Random(2002)
        for _ in range(200):
            cs=[];mut=set()
            for i in range(20):
                ro=bool(r.getrandbits(1));mut.add(f"c{i}") if not ro else None;cs.append(PrefetchCandidate(f"c{i}",Q64.from_ratio(r.randint(0,100),100),q(r.randint(0,20)),q(r.randint(0,5)),Q64.from_ratio(r.randint(0,100),100),ro,bool(r.getrandbits(1))))
            b=q(r.randint(0,25));p=plan_prefetch(cs,b,q(5));self.assertLessEqual(p.total_cost,b);self.assertTrue(mut.isdisjoint(p.selected))
    def test_dag_100(self):
        r=random.Random(3003)
        for _ in range(100):
            ts=[]
            for i in range(20):
                prev=list(range(i));r.shuffle(prev);deps=tuple(f"t{j}" for j in sorted(prev[:r.randint(0,min(3,len(prev)))]));ts.append(ProofTask(f"t{i}",q(r.randint(1,10)),q(r.randint(0,20)),deps,i==0))
            a=schedule_proofs(ts,4);b=schedule_proofs(reversed(ts),4);self.assertEqual(tuple((x.task_id,x.lane,x.start.raw,x.end.raw) for x in a.tasks),tuple((x.task_id,x.lane,x.start.raw,x.end.raw) for x in b.tasks))
    def test_warm_200(self):
        for _ in range(200):
            p=plan_warmset([ContextChunk("a",5,1,q("1"),q("1"),q("0")),ContextChunk("c",5,9,q("1"),q("0.1"),q("5"),True)],10);self.assertIn("a",p.resident);self.assertIn("c",p.resident)
    def test_attention_200(self):
        for _ in range(200):
            p=plan_attention([Notice("b",q("1"),q("1"),q("1"),q("10"),blocker=True)],q("0"),0);self.assertIn("b",p.surface_now)
