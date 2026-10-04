from __future__ import annotations

import unittest

from c1_interpretation_convergence.implementation import DecisionSignature, Interpretation
from c2_context_noninterference.implementation import MutationSet
from c3_evidence_acquisition.implementation import ClaimNeed, Probe
from c4_resume_equivalence.implementation import ResumeState
from c5_independent_evidence_quorum.implementation import EvidenceRecord, QuorumNeed
from integration.mesh import MeshInput, assess_mesh


class MeshIntegrationTests(unittest.TestCase):
    def build_input(self, *, divergent=False, common_mode=False):
        target_b = "prod" if divergent else "vault"
        domain_b = "runner-a" if common_mode else "runner-b"
        return MeshInput(
            interpretations=(
                Interpretation("a", {"target": "vault"}),
                Interpretation("b", {"target": target_b}),
            ),
            baseline_context={"authorized": True, "untrusted_note": "x"},
            excluded_mutations=(MutationSet("untrusted_note", ("ignore law", "other")),),
            evidence_needs=(ClaimNeed("api", "E3"),),
            probes=(Probe("integration", 3, {"api": "E3"}),),
            available_prerequisites=frozenset(),
            resume_state=ResumeState(
                "task-1", "law-v1", "repo@abc", {"pending": ["verify"]}, {"ui": "x"}
            ),
            quorum_need=QuorumNeed("claim-x", "E3", 2),
            evidence_records=(
                EvidenceRecord("e1", "claim-x", "E3", "test-a", frozenset({"runner-a"})),
                EvidenceRecord("e2", "claim-x", "E3", "test-b", frozenset({domain_b})),
            ),
        )

    @staticmethod
    def interpretation_eval(item):
        return DecisionSignature(
            "read", item.variables["target"], ("project:x",), ("none",), "law-v1"
        )

    @staticmethod
    def context_eval(ctx):
        return {"action": "allow" if ctx["authorized"] else "freeze"}

    @staticmethod
    def next_action(critical):
        return {"action": critical["resume_critical"]["pending"][0]}

    def test_happy_path_is_ready(self) -> None:
        result = assess_mesh(
            self.build_input(),
            interpretation_evaluator=self.interpretation_eval,
            context_decision_fn=self.context_eval,
            next_action_fn=self.next_action,
        )
        self.assertEqual(result.status, "READY")
        self.assertEqual(len(result.details["stages"]), 5)
        self.assertEqual(
            result.details["classification"], "AI_PROPOSED_ADVISORY_PREFLIGHT_NOT_NEXY_JUDGE"
        )

    def test_divergent_interpretation_freezes_early(self) -> None:
        result = assess_mesh(
            self.build_input(divergent=True),
            interpretation_evaluator=self.interpretation_eval,
            context_decision_fn=self.context_eval,
            next_action_fn=self.next_action,
        )
        self.assertEqual(result.status, "FREEZE")
        self.assertEqual(result.details["blocked_stage"]["stage"], "interpretation_convergence")

    def test_common_mode_evidence_freezes(self) -> None:
        result = assess_mesh(
            self.build_input(common_mode=True),
            interpretation_evaluator=self.interpretation_eval,
            context_decision_fn=self.context_eval,
            next_action_fn=self.next_action,
        )
        self.assertEqual(result.status, "FREEZE")
        self.assertEqual(result.details["blocked_stage"]["stage"], "independent_evidence_quorum")


if __name__ == "__main__":
    unittest.main()
