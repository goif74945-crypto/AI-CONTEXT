import unittest

from nexy_aux.corrections import compile_correction, compile_corrections, evaluate, is_applicable


class CorrectionTests(unittest.TestCase):
    def correction(self):
        return {
            "id": "CORR-1",
            "authority": "USER_DIRECTIVE",
            "scope_mode": "BOUNDED",
            "selector": {"project": "NEXY", "surface": "status-report"},
            "assertions": [
                {"field": "status", "op": "neq", "value": "COMPLETE"},
                {"field": "evidence", "op": "exists"},
            ],
        }

    def test_compiles_deterministically(self):
        c1 = compile_correction(self.correction())
        raw = self.correction()
        raw["selector"] = {"surface": "status-report", "project": "NEXY"}
        raw["assertions"] = list(reversed(raw["assertions"]))
        c2 = compile_correction(raw)
        self.assertEqual(c1, c2)

    def test_scope_does_not_leak(self):
        contract = compile_correction(self.correction())
        self.assertTrue(is_applicable(contract, {"project": "NEXY", "surface": "status-report"}))
        self.assertFalse(is_applicable(contract, {"project": "OTHER", "surface": "status-report"}))
        result = evaluate(contract, {"project": "OTHER", "surface": "status-report"}, {"status": "COMPLETE"})
        self.assertEqual(result["status"], "NOT_APPLICABLE")

    def test_detects_regression(self):
        contract = compile_correction(self.correction())
        context = {"project": "NEXY", "surface": "status-report"}
        result = evaluate(contract, context, {"status": "COMPLETE"})
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(len(result["violations"]), 2)

    def test_passes_compliant_output(self):
        contract = compile_correction(self.correction())
        context = {"project": "NEXY", "surface": "status-report"}
        result = evaluate(contract, context, {"status": "NOT_VERIFIED", "evidence": []})
        self.assertEqual(result["status"], "PASS")

    def test_rejects_overbroad_bounded_scope(self):
        raw = self.correction()
        raw["selector"] = {"project": "NEXY"}
        with self.assertRaises(ValueError):
            compile_correction(raw)

    def test_global_requires_explicit_user_law(self):
        raw = self.correction()
        raw.update({"scope_mode": "GLOBAL_EXPLICIT", "selector": {"global": True}, "authority": "USER_DIRECTIVE"})
        with self.assertRaises(ValueError):
            compile_correction(raw)
        raw["authority"] = "USER_LAW"
        self.assertEqual(compile_correction(raw)["scope_mode"], "GLOBAL_EXPLICIT")

    def test_conflicting_corrections_freeze(self):
        left = self.correction()
        left["assertions"] = [{"field": "mode", "op": "eq", "value": "safe"}]
        right = self.correction()
        right["id"] = "CORR-2"
        right["assertions"] = [{"field": "mode", "op": "neq", "value": "safe"}]
        result = compile_corrections([left, right])
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["conflicts"][0]["field"], "mode")


if __name__ == "__main__":
    unittest.main()
