import itertools
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from correlation_consensus import ConsensusInputError, ConsensusPolicy, Vote, evaluate_consensus


class CorrelationConsensusTests(unittest.TestCase):
    def test_independent_quorum_passes(self):
        votes=[Vote("a","X",8000,("provider:a",),3),Vote("b","X",7000,("provider:b",),3),Vote("c","Y",2000,("provider:c",),3)]
        r=evaluate_consensus(votes,ConsensusPolicy(quorum_bps=7000,min_independent_clusters=2,min_evidence_level=2))
        self.assertEqual(r.status,"CONSENSUS"); self.assertEqual(r.winner,"X"); self.assertGreaterEqual(r.support_bps,7000); self.assertEqual(r.independent_support_clusters,2)

    def test_correlated_agents_do_not_sybil_inflate(self):
        votes=[Vote("a1","X",9000,("provider:a","base:m"),3),Vote("a2","X",9000,("provider:a","retrieval:same"),3),Vote("a3","X",9000,("base:m",),3),Vote("b","Y",9000,("provider:b",),3)]
        r=evaluate_consensus(votes,ConsensusPolicy(quorum_bps=6000,min_independent_clusters=2))
        self.assertEqual(r.status,"FREEZE"); self.assertIn("WEIGHT_TIE",r.reason_codes); self.assertEqual(r.participating_cluster_count,2)

    def test_cluster_disagreement_abstains(self):
        votes=[Vote("a","X",9000,("same",),2),Vote("b","Y",8000,("same",),2),Vote("c","X",9000,("independent-c",),2),Vote("d","X",9000,("independent-d",),2)]
        r=evaluate_consensus(votes,ConsensusPolicy(quorum_bps=9000,min_independent_clusters=2))
        self.assertEqual(r.status,"FREEZE"); self.assertIn("CORRELATED_CLUSTER_DISAGREEMENT",r.reason_codes)

    def test_evidence_floor_filters_members(self):
        r=evaluate_consensus([Vote("a","X",9000,("a",),1),Vote("b","X",9000,("b",),3),Vote("c","X",9000,("c",),3)],ConsensusPolicy(min_evidence_level=2,min_independent_clusters=2))
        self.assertEqual(r.status,"CONSENSUS"); self.assertEqual(r.participating_cluster_count,2)

    def test_input_order_does_not_change_fingerprint(self):
        votes=[Vote("a","X",7000,("p1",),3),Vote("b","X",8000,("p2",),3),Vote("c","Y",2000,("p3",),3)]
        self.assertEqual(len({evaluate_consensus(list(p)).fingerprint for p in itertools.permutations(votes)}),1)

    def test_duplicate_agent_rejected(self):
        with self.assertRaises(ConsensusInputError): evaluate_consensus([Vote("a","X",1,("p1",)),Vote("a","X",1,("p2",))])

    def test_missing_dependency_domain_rejected(self):
        with self.assertRaises(ConsensusInputError): evaluate_consensus([Vote("a","X",1,())])


if __name__=="__main__":
    unittest.main()
