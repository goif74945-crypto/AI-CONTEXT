import unittest

from nexy_lo4_frontier import (
    AuthorityRule,
    Capability,
    DecisionCase,
    EvidenceArtifact,
    ForbiddenPrivilegeSet,
    Observation,
    ProofClaim,
    ReplayCapsule,
    analyze_capability_composition,
    assess_evidence_debt,
    differential_oracle,
    evaluate_lo4_candidate,
    falsify_shadow_invariants,
    mine_shadow_invariants,
    simulate_authority_change,
)


class FrontierFiveIntegrationTests(unittest.TestCase):
    def _invariants(self):
        mined = mine_shadow_invariants([
            Observation("a", (("state", "PASS"), ("x", 1), ("y", 1))),
            Observation("b", (("state", "PASS"), ("x", 2), ("y", 2))),
        ])
        return falsify_shadow_invariants(mined.candidates, [Observation("fault", (("state", "FREEZE"), ("x", 3), ("y", 2)))])

    def _replay(self, divergent=False):
        cap = ReplayCapsule("r", {"x": 1}, {"s": 2}, "f" * 64, (("tool", "1"),), 1)
        executors = {"a": lambda c: {"v": 3}, "b": (lambda c: {"v": 4}) if divergent else (lambda c: {"v": 3})}
        return differential_oracle(cap, executors)

    def test_all_clear_prototype_gate_passes_but_stays_proposal_only(self):
        rules = [AuthorityRule("deny-delete", 10, "DENY", "delete", "*")]
        wind = simulate_authority_change(rules, rules, [DecisionCase("c", "u", "delete", "r")])
        debt = assess_evidence_debt(
            [ProofClaim("claim", 2, 10, ("module",))],
            [EvidenceArtifact("ev", ("claim",), 2, (("module", "1"),))],
            {"module": "1"},
        )
        cap = analyze_capability_composition(
            [Capability("safe", frozenset({"auth"}), frozenset({"read-public"}), "project")],
            ["auth"],
            [ForbiddenPrivilegeSet("exfil", frozenset({"secret-read", "network-egress"}))],
            allowed_scopes=frozenset({"project"}),
        )
        gate = evaluate_lo4_candidate(wind, debt, cap, self._invariants(), self._replay())
        self.assertEqual(gate.status, "PASS")
        self.assertIn("Lo4_AI_PROPOSAL_ONLY", gate.advisory_codes)
        self.assertIn("CANON_PROMOTION_REQUIRES_FORMAL_AUTHORITY", gate.advisory_codes)

    def test_any_critical_frontier_risk_freezes(self):
        base = [AuthorityRule("deny-read", 10, "DENY", "read", "secret/*")]
        candidate = [AuthorityRule("allow-read", 10, "ALLOW", "read", "secret/*")]
        wind = simulate_authority_change(base, candidate, [DecisionCase("c", "u", "read", "secret/a")])
        debt = assess_evidence_debt([ProofClaim("claim", 2, 10, ("m",))], [], {"m": "2"})
        cap = analyze_capability_composition(
            [
                Capability("read", frozenset({"auth"}), frozenset({"secret-read"}), "p"),
                Capability("send", frozenset({"auth"}), frozenset({"network-egress"}), "p"),
            ],
            ["auth"],
            [ForbiddenPrivilegeSet("exfil", frozenset({"secret-read", "network-egress"}))],
            allowed_scopes=frozenset({"p"}),
        )
        gate = evaluate_lo4_candidate(wind, debt, cap, self._invariants(), self._replay(divergent=True))
        self.assertEqual(gate.status, "FREEZE")
        self.assertEqual(
            set(gate.blocking_codes),
            {"COUNTERFACTUAL_AUTHORITY_RISK", "EVIDENCE_DEBT_PRESENT", "CAPABILITY_COMPOSITION_RISK", "REPLAY_DIVERGENCE"},
        )


if __name__ == "__main__":
    unittest.main()
