import unittest

from nexy_meta_assurance.witness import EvidenceItem, WitnessError, extract_minimal_witness


class WitnessTests(unittest.TestCase):
    def test_minimum_cost_cover_is_selected(self):
        result = extract_minimal_witness(
            ["R1", "R2", "R3"],
            [
                EvidenceItem("E1", frozenset({"R1", "R2"}), 4),
                EvidenceItem("E2", frozenset({"R3"}), 2),
                EvidenceItem("E3", frozenset({"R1"}), 1),
                EvidenceItem("E4", frozenset({"R2", "R3"}), 2),
            ],
        )
        self.assertTrue(result.exact)
        self.assertEqual(result.selected_ids, ("E3", "E4"))
        self.assertEqual(result.total_cost, 3)

    def test_tie_break_is_lexicographically_stable(self):
        result = extract_minimal_witness(
            ["R1"],
            [
                EvidenceItem("E-B", frozenset({"R1"}), 1),
                EvidenceItem("E-A", frozenset({"R1"}), 1),
            ],
        )
        self.assertEqual(result.selected_ids, ("E-A",))

    def test_uncovered_requirement_is_explicit(self):
        result = extract_minimal_witness(
            ["R1", "R2"],
            [EvidenceItem("E1", frozenset({"R1"}), 1)],
        )
        self.assertFalse(result.exact)
        self.assertEqual(result.uncovered, frozenset({"R2"}))

    def test_unknown_requirement_reference_fails_closed(self):
        with self.assertRaises(WitnessError):
            extract_minimal_witness(["R1"], [EvidenceItem("E1", frozenset({"R2"}), 1)])

    def test_duplicate_evidence_ids_fail_closed(self):
        with self.assertRaises(WitnessError):
            extract_minimal_witness(
                ["R1"],
                [EvidenceItem("E1", frozenset({"R1"})), EvidenceItem("E1", frozenset({"R1"}))],
            )


if __name__ == "__main__":
    unittest.main()
