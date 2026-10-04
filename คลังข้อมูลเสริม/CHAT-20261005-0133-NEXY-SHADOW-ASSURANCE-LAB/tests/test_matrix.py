from __future__ import annotations

import unittest

from shadowguard.gate import evaluate_datasets
from shadowguard.models import DecisionRecord


def make(case_id="x", **overrides):
    raw = {
        "case_id": case_id,
        "input_fingerprint": "input:1",
        "revision": "r2",
        "policy_fingerprint": "policy:1",
        "authority_chain": ["USER_LAW", "NEXY_LAW", "JUDGE"],
        "outcome": "RELEASE",
        "action": "A",
        "required_evidence_classes": ["E2"],
        "evidence": [{"class": "E2", "ref": "proof", "revision": "r2"}],
        "safety_labels": ["safe"],
    }
    raw.update(overrides)
    return DecisionRecord.from_mapping(raw)


class ExhaustiveMatrixTests(unittest.TestCase):
    def test_each_evidence_class_can_be_required_without_substitution(self):
        for i in range(8):
            cls = f"E{i}"
            with self.subTest(cls=cls):
                r = make(
                    required_evidence_classes=[cls],
                    evidence=[{"class": cls, "ref": f"proof:{cls}", "revision": "r2"}],
                )
                self.assertEqual("PASS", evaluate_datasets([r], [r]).status)

    def test_all_cross_outcome_pairs_obey_freeze_boundary(self):
        outcomes = ["RELEASE", "FREEZE", "STOP"]
        for stable_outcome in outcomes:
            for candidate_outcome in outcomes:
                with self.subTest(stable=stable_outcome, candidate=candidate_outcome):
                    s = make(outcome=stable_outcome, action="A" if stable_outcome == "RELEASE" else None)
                    c = make(outcome=candidate_outcome, action="A" if candidate_outcome == "RELEASE" else None)
                    report = evaluate_datasets([s], [c])
                    codes = {x.code for x in report.findings}
                    if stable_outcome in {"FREEZE", "STOP"} and candidate_outcome == "RELEASE":
                        self.assertEqual("FAIL", report.status)
                        self.assertIn("FREEZE_BYPASS", codes)
                    elif stable_outcome == "RELEASE" and candidate_outcome in {"FREEZE", "STOP"}:
                        self.assertEqual("NOT_VERIFIED", report.status)
                        self.assertIn("CONSERVATIVE_DIVERGENCE", codes)
                    else:
                        self.assertEqual("PASS", report.status)

    def test_every_single_authority_truncation_blocks(self):
        stable = make()
        chain = list(stable.authority_chain)
        for length in range(len(chain)):
            with self.subTest(length=length):
                candidate_chain = chain[:length]
                if not candidate_chain:
                    candidate_chain = ["UNKNOWN"]
                report = evaluate_datasets([stable], [make(authority_chain=candidate_chain)])
                self.assertEqual("FAIL", report.status)
                self.assertIn("AUTHORITY_REGRESSION", {x.code for x in report.findings})

    def test_1000_case_identity_corpus_passes(self):
        stable = []
        candidate = []
        for i in range(1000):
            case_id = f"case-{i:04d}"
            s = make(case_id=case_id, input_fingerprint=f"input:{i}")
            c = make(case_id=case_id, input_fingerprint=f"input:{i}", revision="candidate-r3",
                     evidence=[{"class": "E2", "ref": f"proof:{i}", "revision": "candidate-r3"}])
            stable.append(s)
            candidate.append(c)
        report = evaluate_datasets(stable, candidate)
        self.assertEqual("PASS", report.status)
        self.assertEqual(1000, report.compared_cases)

    def test_mutation_catalog_is_fail_closed(self):
        stable = make()
        mutations = [
            ("policy", make(policy_fingerprint="policy:changed"), "POLICY_DRIFT"),
            ("authority", make(authority_chain=["USER_LAW", "JUDGE"]), "AUTHORITY_REGRESSION"),
            ("stale", make(evidence=[{"class": "E2", "ref": "proof", "revision": "old"}]), "STALE_EVIDENCE"),
            ("missing-evidence", make(evidence=[]), "MISSING_REQUIRED_EVIDENCE"),
            ("action", make(action="B"), "ACTION_DIVERGENCE"),
            ("label", make(safety_labels=[]), "SAFETY_LABEL_REGRESSION"),
        ]
        for name, candidate, expected in mutations:
            with self.subTest(name=name):
                report = evaluate_datasets([stable], [candidate])
                self.assertEqual("FAIL", report.status)
                self.assertIn(expected, {x.code for x in report.findings})


if __name__ == "__main__":
    unittest.main()
