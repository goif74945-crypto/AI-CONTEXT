import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]/"src"))
from model_drift_sentinel import Probe, Observation, evaluate

class TestMDS(unittest.TestCase):
    def setUp(self):
        self.probes=[Probe("structured", True), Probe("refusal", False)]
        self.base=[Observation("structured","ok",{"answer":"x","citations":["a"]}), Observation("refusal","blocked",{"reason":"x"})]

    def test_pass_when_structure_matches(self):
        cand=[Observation("structured","ok",{"answer":"different","citations":["b","c"]}), Observation("refusal","blocked",{"reason":"y"})]
        self.assertEqual(evaluate(self.probes,self.base,cand)["status"],"PASS")

    def test_critical_shape_drift_freezes(self):
        cand=[Observation("structured","ok",{"answer":42,"citations":["b"]}), Observation("refusal","blocked",{"reason":"y"})]
        self.assertEqual(evaluate(self.probes,self.base,cand)["status"],"FREEZE")

    def test_noncritical_missing_is_drift(self):
        cand=[Observation("structured","ok",{"answer":"a","citations":["z"]})]
        self.assertEqual(evaluate(self.probes,self.base,cand)["status"],"DRIFT")

    def test_missing_critical_candidate_freezes(self):
        cand=[Observation("refusal","blocked",{"reason":"y"})]
        self.assertEqual(evaluate(self.probes,self.base,cand)["status"],"FREEZE")

    def test_extra_probe_reports_drift(self):
        cand=[Observation("structured","ok",{"answer":"a","citations":["z"]}), Observation("refusal","blocked",{"reason":"y"}), Observation("new","ok",{})]
        self.assertEqual(evaluate(self.probes,self.base,cand)["status"],"DRIFT")

    def test_duplicate_observation_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(self.probes,self.base,self.base+self.base[:1])

if __name__ == '__main__': unittest.main()
