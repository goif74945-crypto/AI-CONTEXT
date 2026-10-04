from __future__ import annotations
import unittest

from nexy_lo4_q64.q64 import Q64, Q64Error, Q64Overflow
from nexy_lo4_q64 import systems as s

q = Q64.from_decimal

class TestQ64(unittest.TestCase):
    def test_exact_basic_arithmetic(self):
        self.assertEqual((q("1.5")+q("2.25")).canonical(), "15/4")
        self.assertEqual((q("1.5")*q("2")).canonical(), "3/1")
        self.assertEqual((q("3")/q("2")).canonical(), "3/2")
    def test_float_forbidden(self):
        with self.assertRaises(TypeError): Q64.coerce(0.5)
    def test_overflow(self):
        with self.assertRaises(Q64Overflow): Q64((1<<127))
    def test_div_zero(self):
        with self.assertRaises(ZeroDivisionError): q("1")/Q64.zero()
    def test_decimal_nonfinite_rejected(self):
        with self.assertRaises(Q64Error): q("NaN")

class TestSystems(unittest.TestCase):
    def test_01_dab(self): self.assertTrue(Q64.zero() <= s.attention_budget(q("1"),q("1"),q("0"),q("1")) <= Q64.one())
    def test_02_ceg(self): self.assertEqual(s.context_entropy([q("1"),q("0")]), Q64.zero())
    def test_02_ceg_bad_sum(self):
        with self.assertRaises(Q64Error): s.context_entropy([q("0.4"),q("0.4")])
    def test_03_sdi(self): self.assertEqual(s.semantic_drift([q("0.2"),q("0.8")],[q("0.2"),q("0.8")]), Q64.zero())
    def test_04_icp(self): self.assertEqual(s.compression_priority(q("1"),q("1"),q("1")), Q64.zero())
    def test_05_uff(self): self.assertTrue(s.friction_score(10,2,q("0.5"),q("0.5")).raw > 0)
    def test_06_dvs_delay(self): self.assertTrue(s.deferred_value(q("1"),q("0.1"),10,q("0")).raw < q("1").raw)
    def test_07_igr_cost_zero(self):
        with self.assertRaises(Q64Error): s.information_gain(q("1"),q("1"),q("0"))
    def test_08_tics(self): self.assertTrue(s.tool_efficiency(q("1"),q("1"),q("0"),q("0")).raw > q("0.99").raw)
    def test_09_edc(self): self.assertTrue(s.explanation_density(10,100,q("0")).raw > 0)
    def test_10_rpo(self): self.assertTrue(s.recovery_priority(q("1"),q("0"),q("1"),q("0")).raw > q("0.9").raw)
    def test_11_mhui_penalty(self): self.assertEqual(s.horizon_utility(q("1"),q("1"),q("1"),q("1")), Q64.zero())
    def test_12_csm(self): self.assertEqual(s.capability_saturation(q("100"),q("1"),q("1")), Q64.one())
    def test_13_irr(self): self.assertTrue(s.rhythm_pressure(q("1"),q("1"),q("0")).raw > q("0.99").raw)
    def test_14_drm(self): self.assertEqual(s.reversibility_score(q("1"),q("1"),q("0")), Q64.one())
    def test_15_sfde(self): self.assertTrue(s.freshness(q("1"),100,q("0.01")).raw < q("1").raw)
    def test_16_besa(self): self.assertTrue(s.evidence_sampling_priority(q("1"),q("1"),q("1"),q("0")).raw > q("0.99").raw)
    def test_17_ccm(self): self.assertEqual(s.calibration_mix([(q("0"),q("1")),(q("1"),q("1"))]).canonical(), "1/2")
    def test_17_ccm_zero_weight(self):
        with self.assertRaises(Q64Error): s.calibration_mix([(q("0.5"),q("0"))])
    def test_18_sciw(self): self.assertTrue(s.change_wavefront(q("1"),100,q("1"),q("1")).raw > q("0.9").raw)
    def test_19_dhce(self): self.assertEqual(s.handoff_continuity(q("1"),q("1"),q("1"),q("1")), Q64.one())
    def test_20_uvfe_correctness_dominant(self):
        a=s.user_value_frontier(q("1"),q("0"),q("0"),q("0"),q("0"))
        b=s.user_value_frontier(q("0"),q("1"),q("0"),q("0"),q("0"))
        self.assertTrue(b.raw > a.raw)
    def test_unit_interval_rejection(self):
        with self.assertRaises(Q64Error): s.attention_budget(q("1.1"),q("1"),q("0"),q("0"))
    def test_deterministic_rank_tie_break(self):
        r=s.rank({"β":q("1"),"a":q("1"),"b":q("2")})
        self.assertEqual([x.key for x in r],["b","a","β"])
    def test_registry_has_exactly_20(self): self.assertEqual(len(s.SYSTEMS),20)

if __name__ == "__main__": unittest.main()
