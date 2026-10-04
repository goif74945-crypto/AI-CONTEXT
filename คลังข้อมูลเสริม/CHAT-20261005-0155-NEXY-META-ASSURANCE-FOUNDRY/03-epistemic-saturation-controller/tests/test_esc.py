import os
import sys
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from esc import ContractError, Contribution, Round, analyze_rounds


def c(agent, domain, claims=(), evidence=()):
    return Contribution.build(agent_id=agent, independence_domain=domain, claim_ids=claims, evidence_refs=evidence)


def r(round_id, *contribs):
    return Round.build(round_id=round_id, contributions=contribs)


class EpistemicSaturationControllerTests(unittest.TestCase):
    def test_repetition_saturates(self):
        rounds = [
            r("r1", c("a1", "p1", ["C"], ["E"])),
            r("r2", c("a2", "p1", ["C"], ["E"])),
            r("r3", c("a3", "p1", ["C"], ["E"])),
        ]
        report = analyze_rounds(rounds, patience=2, min_rounds=2)
        self.assertEqual(report.status, "SATURATED")
        self.assertEqual(report.metrics[-1].novelty_score, 0)

    def test_new_independence_domain_counts_as_novel(self):
        rounds = [
            r("r1", c("a1", "provider-A", ["C"], ["E"])),
            r("r2", c("a2", "provider-B", ["C"], ["E"])),
        ]
        report = analyze_rounds(rounds, patience=1, min_rounds=2)
        self.assertEqual(report.status, "ACTIVE")
        self.assertIn("C@provider-B", report.metrics[1].new_independent_support)

    def test_new_evidence_counts_as_novel(self):
        rounds = [
            r("r1", c("a1", "p", ["C"], ["E1"])),
            r("r2", c("a2", "p", ["C"], ["E2"])),
        ]
        report = analyze_rounds(rounds, patience=1, min_rounds=2)
        self.assertEqual(report.status, "ACTIVE")
        self.assertEqual(report.metrics[1].new_evidence, ("E2",))

    def test_new_claim_counts_as_novel(self):
        rounds = [
            r("r1", c("a1", "p", ["C1"], [])),
            r("r2", c("a2", "p", ["C2"], [])),
        ]
        self.assertEqual(analyze_rounds(rounds, patience=1, min_rounds=2).status, "ACTIVE")

    def test_saturation_never_claims_release(self):
        rounds = [
            r("r1", c("a1", "p", ["C"], [])),
            r("r2", c("a2", "p", ["C"], [])),
        ]
        report = analyze_rounds(rounds, patience=1, min_rounds=2)
        self.assertEqual(report.action, "STOP_EXPANSION")
        self.assertIn("NOT_A_RELEASE_DECISION", report.reason_codes)

    def test_round_contribution_order_does_not_change_fingerprint(self):
        x = r("r1", c("b", "p2", ["C2"], ["E2"]), c("a", "p1", ["C1"], ["E1"]))
        y = r("r1", c("a", "p1", ["C1"], ["E1"]), c("b", "p2", ["C2"], ["E2"]))
        self.assertEqual(analyze_rounds([x]).fingerprint, analyze_rounds([y]).fingerprint)

    def test_duplicate_agent_in_round_rejected(self):
        with self.assertRaises(ContractError):
            r("r1", c("a", "p1"), c("a", "p2"))

    def test_duplicate_round_rejected(self):
        one = r("r", c("a", "p"))
        two = r("r", c("b", "p"))
        with self.assertRaises(ContractError):
            analyze_rounds([one, two])

    def test_invalid_tuning_rejected(self):
        one = r("r", c("a", "p"))
        with self.assertRaises(ContractError):
            analyze_rounds([one], patience=0)
        with self.assertRaises(ContractError):
            analyze_rounds([one], min_rounds=0)


if __name__ == "__main__":
    unittest.main()
