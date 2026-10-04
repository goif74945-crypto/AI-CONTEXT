import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from semantic_abi import *

class TestSCAC(unittest.TestCase):
    def contract(self):
        i=schema_hash({"q":"str"}); o=schema_hash({"items":["str"]})
        return CapabilityContract("search",1,i,o,"structural","E2"), i, o
    def test_compile_success(self):
        c,i,o=self.contract(); p=ProviderCapability("search","provider.search",1,i,o,"strict","E3")
        r=compile_bindings([c],[p]); self.assertEqual(r["status"],"PASS"); self.assertEqual(len(r["bindings"]),1)
    def test_schema_mismatch_freezes(self):
        c,i,o=self.contract(); p=ProviderCapability("search","x",1,i,"bad","strict","E3")
        self.assertEqual(compile_bindings([c],[p])["status"],"FREEZE")
    def test_weak_evidence_freezes(self):
        c,i,o=self.contract(); p=ProviderCapability("search","x",1,i,o,"strict","E1")
        self.assertEqual(compile_bindings([c],[p])["status"],"FREEZE")

    def test_missing_capability_freezes(self):
        c,_,_=self.contract(); self.assertEqual(compile_bindings([c],[])["status"],"FREEZE")

    def test_weak_determinism_freezes(self):
        c,i,o=self.contract(); p=ProviderCapability("search","x",1,i,o,"best_effort","E3")
        self.assertEqual(compile_bindings([c],[p])["status"],"FREEZE")

    def test_duplicate_offer_rejected(self):
        c,i,o=self.contract(); p=ProviderCapability("search","x",1,i,o,"strict","E3")
        with self.assertRaises(ValueError): compile_bindings([c],[p,p])

if __name__=='__main__': unittest.main()
