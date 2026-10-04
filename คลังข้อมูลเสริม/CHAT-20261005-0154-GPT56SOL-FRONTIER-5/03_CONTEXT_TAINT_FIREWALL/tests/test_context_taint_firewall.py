import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from context_taint_firewall import *

class TestCTF(unittest.TestCase):
    def test_prompt_injection_cannot_become_authority(self):
        g=Graph(); g.add(Node("web",frozenset({UNTRUSTED_EXTERNAL})))
        g.add(Node("summary",frozenset({MODEL_GENERATED}),("web",)))
        self.assertEqual(g.decide("summary","AUTHORITY_INPUT")["status"],"FREEZE")
    def test_verified_transform_can_feed_authority(self):
        g=Graph(); g.add(Node("web",frozenset({UNTRUSTED_EXTERNAL})))
        g.add(Node("verified",frozenset({VERIFIED_EVIDENCE}),("web",),("evidence:123",)))
        self.assertEqual(g.decide("verified","AUTHORITY_INPUT")["status"],"PASS")
    def test_secret_never_egresses_even_if_verified(self):
        g=Graph(); g.add(Node("secret",frozenset({SECRET,AUTHORITY_SOURCE})))
        g.add(Node("checked",frozenset({VERIFIED_EVIDENCE}),("secret",),("e:1",)))
        self.assertEqual(g.decide("checked","EXTERNAL_EGRESS")["status"],"FREEZE")

    def test_missing_parent_rejected(self):
        g=Graph()
        with self.assertRaises(ValueError): g.add(Node("x",parent_ids=("missing",)))

    def test_transitive_secret_propagates(self):
        g=Graph(); g.add(Node("s",frozenset({SECRET}))); g.add(Node("a",parent_ids=("s",))); g.add(Node("b",parent_ids=("a",)))
        self.assertIn(SECRET,g.effective_taints("b"))
        self.assertEqual(g.decide("b","EXTERNAL_EGRESS")["status"],"FREEZE")

    def test_untrusted_non_authority_sink_passes(self):
        g=Graph(); g.add(Node("web",frozenset({UNTRUSTED_EXTERNAL})))
        self.assertEqual(g.decide("web","WORKING_CONTEXT")["status"],"PASS")

if __name__=='__main__': unittest.main()
