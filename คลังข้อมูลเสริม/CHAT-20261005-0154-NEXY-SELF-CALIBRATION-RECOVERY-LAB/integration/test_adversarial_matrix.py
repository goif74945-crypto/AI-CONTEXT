from __future__ import annotations

import itertools
import random
import unittest

from concepts.calibration_observatory.calibrator import PredictionRecord, calibration_report
from concepts.contract_archaeologist.miner import mine_contracts
from concepts.evidence_genealogy.auditor import EvidenceItem, audit_independence
from concepts.failure_atomizer.atomizer import ddmin
from concepts.pausesafe_kernel.kernel import StepState, StepStatus, preemption_assessment


class AdversarialMatrixTests(unittest.TestCase):
    def test_contract_miner_permutation_stability_24_orders(self) -> None:
        rows = [
            {"phase": "v", "decision": "f", "risk": 9},
            {"phase": "v", "decision": "f", "risk": 8},
            {"phase": "r", "decision": "p", "risk": 1},
            {"phase": "r", "decision": "p", "risk": 2},
        ]
        baseline = mine_contracts(rows).as_dict()
        for perm in itertools.permutations(rows):
            self.assertEqual(mine_contracts(perm).as_dict(), baseline)

    def test_atomizer_all_28_trigger_pairs_are_one_minimal(self) -> None:
        universe = tuple(f"x{i}" for i in range(8))
        for i in range(8):
            for j in range(i + 1, 8):
                a, b = universe[i], universe[j]
                r = ddmin(universe, lambda xs, a=a, b=b: a in xs and b in xs)
                self.assertEqual(set(r.minimal), {a, b})
                self.assertEqual(len(r.minimal), 2)

    def test_evidence_transitive_genealogy_collapses(self) -> None:
        items = [
            EvidenceItem("a", "c", "root-1", "m1", "h1", "rev"),
            EvidenceItem("b", "c", "root-1", "m2", "h2", "rev"),
            EvidenceItem("c", "c", "root-3", "m3", "h2", "rev"),
            EvidenceItem("d", "c", "root-4", "m4", "h4", "rev"),
        ]
        r = audit_independence(items, target_revision="rev", required_independent_groups=3)
        self.assertEqual(r["independent_group_count"], 2)
        self.assertEqual(r["status"], "INSUFFICIENT_INDEPENDENCE")

    def test_pausesafe_state_matrix(self) -> None:
        statuses = list(StepStatus)
        for status in statuses:
            for idempotent in (False, True):
                for checkpointed in (False, True):
                    for compensated in (False, True):
                        step = StepState("s", status, idempotent, checkpointed, compensated)
                        r = preemption_assessment([step])
                        if status is not StepStatus.RUNNING:
                            self.assertEqual(r["status"], "PREEMPT_SAFE")
                        elif checkpointed:
                            self.assertEqual(r["status"], "PREEMPT_SAFE")
                        elif not idempotent and not compensated:
                            self.assertEqual(r["status"], "BLOCKED_UNSAFE_INFLIGHT")
                        else:
                            self.assertEqual(r["status"], "DRAIN_REQUIRED")

    def test_calibration_balanced_population(self) -> None:
        # Ten 0.1-confidence records with one success; ten 0.9-confidence records with nine successes.
        rows = []
        for i in range(10):
            rows.append(PredictionRecord(f"low-{i}", 0.1, i == 0, "E2"))
        for i in range(10):
            rows.append(PredictionRecord(f"high-{i}", 0.9, i < 9, "E2"))
        random.Random(7).shuffle(rows)
        r = calibration_report(rows, min_records=20, gap_threshold=0.01)
        self.assertEqual(r["status"], "CALIBRATION_WITHIN_THRESHOLD")
        self.assertAlmostEqual(r["ece"], 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
