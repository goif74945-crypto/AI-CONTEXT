from __future__ import annotations
import unittest

from nexy_lo4_q64.q64 import Q64
from nexy_lo4_q64 import systems as s

q=Q64.from_decimal

class TestFabricIntegration(unittest.TestCase):
    def test_twenty_system_pipeline_composes_deterministically(self):
        # Representative adapter-neutral state. Every real-valued decision input is Q64.64.
        outputs={
          "DAB":s.attention_budget(q("0.8"),q("0.9"),q("0.4"),q("0.2")),
          "CEG":s.context_entropy([q("0.5"),q("0.25"),q("0.25")]),
          "SDI":s.semantic_drift([q("0.2"),q("0.8")],[q("0.3"),q("0.7")]),
          "ICP":s.compression_priority(q("0.2"),q("0.8"),q("0.9")),
          "UFF":s.friction_score(7,1,q("0.3"),q("0.4")),
          "DVS":s.deferred_value(q("0.9"),q("0.05"),4,q("0.1")),
          "IGR":s.information_gain(q("0.8"),q("0.75"),q("0.5")),
          "TICS":s.tool_efficiency(q("0.95"),q("0.9"),q("0.2"),q("0.1")),
          "EDC":s.explanation_density(12,80,q("0.1")),
          "RPO":s.recovery_priority(q("0.8"),q("0.4"),q("0.9"),q("0.7")),
          "MHUI":s.horizon_utility(q("0.8"),q("0.7"),q("0.6"),q("0.1")),
          "CSM":s.capability_saturation(q("0.7"),q("1"),q("0.4")),
          "IRR":s.rhythm_pressure(q("0.5"),q("0.2"),q("0.3")),
          "DRM":s.reversibility_score(q("0.9"),q("0.8"),q("0.1")),
          "SFDE":s.freshness(q("1"),5,q("0.02")),
          "BESA":s.evidence_sampling_priority(q("0.9"),q("0.7"),q("0.4"),q("0.2")),
          "CCM":s.calibration_mix([(q("0.8"),q("0.9")),(q("0.7"),q("0.8")),(q("0.9"),q("0.7"))]),
          "SCIW":s.change_wavefront(q("0.6"),8,q("0.7"),q("0.4")),
          "DHCE":s.handoff_continuity(q("0.9"),q("0.8"),q("0.9"),q("1")),
          "UVFE":s.user_value_frontier(q("0.9"),q("0.98"),q("0.2"),q("0.15"),q("0.1")),
        }
        self.assertEqual(set(outputs),set(s.SYSTEMS))
        ranking1=[r.key for r in s.rank(outputs)]
        ranking2=[r.key for r in s.rank(dict(reversed(list(outputs.items()))))]
        self.assertEqual(ranking1,ranking2)
        self.assertEqual(len(ranking1),20)

    def test_float_injection_cannot_enter_representative_pipeline(self):
        with self.assertRaises(TypeError):
            s.attention_budget(Q64.coerce(0.1),q("1"),q("1"),q("1"))

if __name__=="__main__": unittest.main()
