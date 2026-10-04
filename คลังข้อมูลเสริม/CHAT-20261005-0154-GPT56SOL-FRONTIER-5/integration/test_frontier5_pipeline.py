import sys, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
for d in [
 "01_MODEL_DRIFT_SENTINEL/src","02_SEMANTIC_CAPABILITY_ABI/src","03_CONTEXT_TAINT_FIREWALL/src","04_EFFECT_TRANSACTION_COORDINATOR/src","05_SCOPED_AUTHORITY_LEASE/src"]:
    sys.path.insert(0,str(ROOT/d))
from model_drift_sentinel import Probe, Observation, evaluate
from semantic_abi import CapabilityContract,ProviderCapability,compile_bindings,schema_hash
from context_taint_firewall import Graph,Node,UNTRUSTED_EXTERNAL,VERIFIED_EVIDENCE
from effect_transaction_coordinator import Action,execute_plan
from scoped_authority_lease import Lease,authorize

class TestFrontierPipeline(unittest.TestCase):
    def test_admission_authority_and_effect_pipeline(self):
        g=Graph(); g.add(Node("web",frozenset({UNTRUSTED_EXTERNAL}))); g.add(Node("checked",frozenset({VERIFIED_EVIDENCE}),("web",),("ev:1",)))
        self.assertEqual(g.decide("checked","AUTHORITY_INPUT")["status"],"PASS")
        ih=schema_hash({"q":"str"}); oh=schema_hash({"items":["str"]})
        c=CapabilityContract("search",1,ih,oh,"structural","E2"); p=ProviderCapability("search","p.search",1,ih,oh,"strict","E3")
        self.assertEqual(compile_bindings([c],[p])["status"],"PASS")
        probes=[Probe("contract",True)]; b=[Observation("contract","ok",{"x":"y"})]; cand=[Observation("contract","ok",{"x":"z"})]
        self.assertEqual(evaluate(probes,b,cand)["status"],"PASS")
        lease=Lease("user","agent","tool.write",("project/*",),("update",),0,1000,1)
        self.assertEqual(authorize(lease,now=1,subject="agent",capability="tool.write",resource="project/a",action="update",uses=0)["status"],"PASS")
        self.assertEqual(execute_plan([Action("write","idem",True,{}, {})],lambda a:True,lambda a:True)["status"],"PASS")

if __name__=="__main__": unittest.main()
