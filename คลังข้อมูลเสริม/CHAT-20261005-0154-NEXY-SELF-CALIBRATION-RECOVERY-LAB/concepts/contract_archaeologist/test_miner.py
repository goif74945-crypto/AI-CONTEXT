from __future__ import annotations

import unittest

from concepts.contract_archaeologist.miner import OBSERVED_ONLY, mine_contracts


class ContractArchaeologistTests(unittest.TestCase):
    def setUp(self) -> None:
        self.events = [
            {"phase": "verify", "status": "freeze", "risk": 8, "actor": "judge"},
            {"phase": "verify", "status": "freeze", "risk": 9, "actor": "judge"},
            {"phase": "release", "status": "pass", "risk": 2, "actor": "judge"},
            {"phase": "release", "status": "pass", "risk": 3, "actor": "judge"},
        ]

    def test_mines_required_constant_range_and_implication(self) -> None:
        report = mine_contracts(self.events, min_implication_support=2)
        kinds = {(p.kind, p.field) for p in report.patterns}
        self.assertIn(("REQUIRED_FIELD", "phase"), kinds)
        self.assertIn(("CONSTANT", "actor"), kinds)
        self.assertIn(("OBSERVED_NUMERIC_RANGE", "risk"), kinds)
        implications = [p for p in report.patterns if p.kind == "OBSERVED_IMPLICATION"]
        self.assertTrue(any(p.field == "phase" and p.detail.get("if_equals") == "verify" and p.detail.get("then_equals") == "freeze" for p in implications))
        self.assertTrue(all(p.authority == OBSERVED_ONLY for p in report.patterns))

    def test_order_independent(self) -> None:
        a = mine_contracts(self.events)
        b = mine_contracts(reversed(self.events))
        self.assertEqual(a.as_dict(), b.as_dict())

    def test_no_data_is_explicit(self) -> None:
        report = mine_contracts([])
        self.assertEqual(report.status, "NO_DATA")
        self.assertEqual(report.patterns, ())

    def test_boolean_not_numeric(self) -> None:
        report = mine_contracts([{"x": True}, {"x": False}])
        self.assertFalse(any(p.kind == "OBSERVED_NUMERIC_RANGE" for p in report.patterns))

    def test_type_collision_true_vs_one_not_conflated(self) -> None:
        events = [
            {"x": True, "y": "bool"},
            {"x": True, "y": "bool"},
            {"x": 1, "y": "int"},
            {"x": 1, "y": "int"},
        ]
        r = mine_contracts(events, min_implication_support=2)
        implications = [p for p in r.patterns if p.kind == "OBSERVED_IMPLICATION" and p.field == "x"]
        self.assertTrue(any(p.detail.get("if_equals") is True and p.detail.get("then_equals") == "bool" for p in implications))
        self.assertTrue(any(type(p.detail.get("if_equals")) is int and p.detail.get("if_equals") == 1 and p.detail.get("then_equals") == "int" for p in implications))

    def test_nonfinite_float_rejected(self) -> None:
        with self.assertRaises(ValueError):
            mine_contracts([{"x": float("nan")}])

    def test_non_mapping_input_rejected(self) -> None:
        with self.assertRaises(TypeError):
            mine_contracts([["not", "a", "mapping"]])

    def test_bad_limits_rejected(self) -> None:
        with self.assertRaises(ValueError):
            mine_contracts(self.events, max_enum_cardinality=0)
        with self.assertRaises(ValueError):
            mine_contracts(self.events, min_implication_support=0)


if __name__ == "__main__":
    unittest.main()
