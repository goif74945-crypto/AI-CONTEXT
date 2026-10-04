import os
import sys
import unittest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))

from uis import ContractError, ImpactModel, Rule, Variable


class UnknownImpactSlicerTests(unittest.TestCase):
    def test_irrelevant_unknown_is_proven_non_material(self):
        model = ImpactModel(
            [Variable.build("risk", ["low", "high"]), Variable.build("theme", ["dark", "light"])],
            [Rule.build("block-high", {"risk": ["high"]}, "FREEZE")],
            default_output="RUN",
        )
        report = model.analyze({"risk": "low"})
        self.assertEqual(report.status, "STABLE")
        self.assertEqual(report.outputs, ("RUN",))
        self.assertEqual(report.non_material_unknowns, ("theme",))

    def test_material_unknown_detected(self):
        model = ImpactModel(
            [Variable.build("risk", ["low", "high"])],
            [Rule.build("block-high", {"risk": ["high"]}, "FREEZE")],
            default_output="RUN",
        )
        report = model.analyze()
        self.assertEqual(report.status, "MATERIAL_UNKNOWNS")
        self.assertEqual(report.material_unknowns, ("risk",))
        self.assertEqual(set(report.outputs), {"FREEZE", "RUN"})

    def test_only_truly_influential_unknown_is_material(self):
        model = ImpactModel(
            [
                Variable.build("risk", ["low", "high"]),
                Variable.build("theme", ["dark", "light"]),
            ],
            [Rule.build("block-high", {"risk": ["high"]}, "FREEZE")],
            default_output="RUN",
        )
        report = model.analyze()
        self.assertEqual(report.material_unknowns, ("risk",))
        self.assertEqual(report.non_material_unknowns, ("theme",))

    def test_conflicting_rules_freeze(self):
        model = ImpactModel(
            [Variable.build("x", [1])],
            [
                Rule.build("r1", {"x": [1]}, "A"),
                Rule.build("r2", {"x": [1]}, "B"),
            ],
            default_output="D",
        )
        report = model.analyze()
        self.assertEqual(report.status, "FREEZE")
        self.assertIn("CONFLICTING_MATCHED_RULES", report.reason_codes)

    def test_same_output_overlapping_rules_is_not_conflict(self):
        model = ImpactModel(
            [Variable.build("x", [1])],
            [Rule.build("r1", {"x": [1]}, "A"), Rule.build("r2", {}, "A")],
            default_output="D",
        )
        self.assertEqual(model.analyze().status, "STABLE")

    def test_enumeration_limit_freezes(self):
        model = ImpactModel(
            [Variable.build("a", range(10)), Variable.build("b", range(10))],
            [], default_output="X", max_states=50,
        )
        report = model.analyze()
        self.assertEqual(report.status, "FREEZE")
        self.assertEqual(report.reason_codes, ("ENUMERATION_LIMIT_EXCEEDED",))

    def test_known_value_outside_domain_rejected(self):
        model = ImpactModel([Variable.build("x", [1, 2])], [], default_output="X")
        with self.assertRaises(ContractError):
            model.analyze({"x": 3})

    def test_rule_value_outside_domain_rejected(self):
        with self.assertRaises(ContractError):
            ImpactModel(
                [Variable.build("x", [1])],
                [Rule.build("bad", {"x": [2]}, "A")],
                default_output="D",
            )

    def test_variable_and_rule_order_do_not_change_fingerprint(self):
        vars1 = [Variable.build("a", [2, 1]), Variable.build("b", [False, True])]
        vars2 = [Variable.build("b", [True, False]), Variable.build("a", [1, 2])]
        rules1 = [Rule.build("r2", {"b": [True]}, "Y"), Rule.build("r1", {"a": [1]}, "Y")]
        rules2 = [Rule.build("r1", {"a": [1]}, "Y"), Rule.build("r2", {"b": [True]}, "Y")]
        a = ImpactModel(vars1, rules1, default_output="Y").analyze()
        b = ImpactModel(vars2, rules2, default_output="Y").analyze()
        self.assertEqual(a.fingerprint, b.fingerprint)

    def test_known_all_variables_evaluates_one_state(self):
        model = ImpactModel([Variable.build("x", [1, 2])], [], default_output="X")
        report = model.analyze({"x": 1})
        self.assertEqual(report.states_evaluated, 1)
        self.assertEqual(report.material_unknowns, ())


if __name__ == "__main__":
    unittest.main()
