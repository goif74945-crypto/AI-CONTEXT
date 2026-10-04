from __future__ import annotations
import json, random, unittest
from proof_capsule import Claim,Evidence,Policy,ContractError,compile_capsule
A="2026-10-05T01:30:00+07:00"; V="sha256:v1"; D="sha256:"+"a"*64
def c(i,cls=("E2",),required=True,material=True): return Claim(i,f"claim {i}","demo",V,cls,required,material)
def e(i,s,status="PASS",cls="E2",rank=1,cost=1,obs="2026-10-05T01:00:00+07:00",until="2026-10-06T01:00:00+07:00",version=V,digest=D): return Evidence(i,f"ev/{i}",status,cls,"demo",version,s,rank,obs,until,cost,digest)
class T(unittest.TestCase):
 def test_pass(self): self.assertEqual(compile_capsule([c("C")],[e("E",("C",))],as_of=A).status,"PASS")
 def test_missing(self): self.assertEqual(compile_capsule([c("C")],[],as_of=A).status,"FREEZE")
 def test_class_exact(self): self.assertEqual(compile_capsule([c("C")],[e("E",("C",),cls="E6")],as_of=A).status,"FREEZE")
 def test_equal_conflict(self): self.assertIn("CONFLICT:C",compile_capsule([c("C")],[e("P",("C",)),e("F",("C",),status="FAIL")],as_of=A).reasons)
 def test_stronger_fail(self): self.assertIn("FAIL:C",compile_capsule([c("C")],[e("F",("C",),status="FAIL",rank=1),e("P",("C",),rank=2)],as_of=A).reasons)
 def test_dissent(self): self.assertEqual(compile_capsule([c("C")],[e("P",("C",),rank=1),e("F",("C",),status="FAIL",rank=2)],as_of=A).dissent["C"],("F",))
 def test_stale_future_version(self):
  self.assertEqual(compile_capsule([c("C")],[e("S",("C",),until="2026-10-05T01:10:00+07:00")],as_of=A).status,"FREEZE")
  self.assertEqual(compile_capsule([c("C")],[e("F",("C",),obs="2026-10-05T02:00:00+07:00")],as_of=A).status,"FREEZE")
  self.assertEqual(compile_capsule([c("C")],[e("V",("C",),version="old")],as_of=A).status,"FREEZE")
 def test_budgets(self):
  r=compile_capsule([c("A"),c("B")],[e("1",("A",)),e("2",("B",))],as_of=A,policy=Policy(max_items=1,max_cost=99)); self.assertEqual((r.status,r.evidence),("FREEZE",()))
  self.assertEqual(compile_capsule([c("C")],[e("E",("C",),cost=9)],as_of=A,policy=Policy(max_cost=2)).status,"FREEZE")
 def test_refs(self):
  self.assertEqual(compile_capsule([c("C")],[e("E",("C","X"))],as_of=A).status,"FREEZE")
  self.assertEqual(compile_capsule([c("C")],[e("E",("C","X"))],as_of=A,policy=Policy(strict_refs=False)).status,"PASS")
 def test_digest(self):
  with self.assertRaises(ContractError): compile_capsule([c("C")],[e("E",("C",),digest=None)],as_of=A)
  self.assertEqual(compile_capsule([c("C")],[e("E",("C",),digest=None)],as_of=A,policy=Policy(require_digest=False)).status,"PASS")
 def test_invalid_contracts(self):
  with self.assertRaises(ContractError): compile_capsule([c("C",required=False)],[],as_of=A)
  with self.assertRaises(ContractError): compile_capsule([c("C")],[e("E",("C","C"))],as_of=A)
  with self.assertRaises(ContractError): compile_capsule([c("C")],[e("E",("C",),obs="2026-10-05T02:00:00+07:00",until="2026-10-05T01:00:00+07:00")],as_of=A)
 def test_identity_binds_semantics(self):
  x=compile_capsule([c("C")],[e("E",("C",))],as_of=A)
  y=compile_capsule([Claim("C","changed","demo",V,("E2",))],[e("E",("C",))],as_of=A)
  self.assertNotEqual(x.capsule_id,y.capsule_id)
 def test_determinism_randomized(self):
  rng=random.Random(74945)
  for case in range(100):
   n=rng.randint(1,8); cs=[c(f"C{i}") for i in range(n)]; es=[e(f"B{i}",(f"C{i}",)) for i in range(n)]
   for j in range(rng.randint(0,8)):
    ss=tuple(sorted({f"C{rng.randrange(n)}" for _ in range(rng.randint(1,min(n,3)))})); es.append(e(f"M{case}-{j}",ss,cost=rng.randint(1,4)))
   p=Policy(max_items=100,max_cost=1000); a=compile_capsule(cs,es,as_of=A,policy=p); self.assertEqual(a.status,"PASS"); self.assertTrue(all(a.coverage[x.id] for x in cs))
   cc=list(cs); ee=list(es); rng.shuffle(cc); rng.shuffle(ee); self.assertEqual(a.to_dict(),compile_capsule(cc,ee,as_of=A,policy=p).to_dict())
 def test_json(self): json.dumps(compile_capsule([c("C")],[e("E",("C",))],as_of=A).to_dict(),sort_keys=True)
if __name__=="__main__": unittest.main(verbosity=2)
