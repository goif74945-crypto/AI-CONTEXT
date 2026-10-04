import unittest

from nexy_aux.emergence import analyze_plan


class EmergenceTests(unittest.TestCase):
    def test_detects_secret_egress_created_by_composition(self):
        plan = {
            "artifacts": {"secret": ["SECRET"]},
            "steps": [
                {"id": "transform", "consumes": ["secret"], "produces": ["payload"], "capabilities": []},
                {"id": "send", "consumes": ["payload"], "produces": [], "capabilities": ["EXTERNAL_EGRESS"]},
            ],
        }
        result = analyze_plan(plan)
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual([x["code"] for x in result["findings"]], ["E_SECRET_EGRESS"])

    def test_redaction_breaks_secret_taint_chain(self):
        plan = {
            "artifacts": {"secret": ["SECRET"]},
            "steps": [
                {"id": "redact", "consumes": ["secret"], "produces": ["safe"], "capabilities": ["REDACT_SECRET"]},
                {"id": "send", "consumes": ["safe"], "produces": [], "capabilities": ["EXTERNAL_EGRESS"]},
            ],
        }
        result = analyze_plan(plan)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["findings"], [])

    def test_detects_untrusted_code_execution(self):
        plan = {
            "artifacts": {"input": ["UNTRUSTED"]},
            "steps": [{"id": "exec", "consumes": ["input"], "produces": [], "capabilities": ["EXECUTE_CODE"]}],
        }
        result = analyze_plan(plan)
        self.assertEqual(result["findings"][0]["code"], "E_UNTRUSTED_EXECUTION")

    def test_validation_breaks_untrusted_chain(self):
        plan = {
            "artifacts": {"input": ["UNTRUSTED"]},
            "steps": [
                {"id": "validate", "consumes": ["input"], "produces": ["verified"], "capabilities": ["VALIDATE_UNTRUSTED"]},
                {"id": "exec", "consumes": ["verified"], "produces": [], "capabilities": ["EXECUTE_CODE"]},
            ],
        }
        result = analyze_plan(plan)
        self.assertEqual(result["status"], "PASS")
        self.assertIn("VERIFIED", result["artifacts"]["verified"])

    def test_detects_confused_deputy(self):
        plan = {
            "artifacts": {"request": ["LOW_TRUST_AUTHORITY"]},
            "steps": [{"id": "mutate", "consumes": ["request"], "produces": [], "capabilities": ["MUTATE_PROTECTED"]}],
        }
        result = analyze_plan(plan)
        self.assertEqual(result["findings"][0]["code"], "E_CONFUSED_DEPUTY")

    def test_missing_artifact_freezes(self):
        result = analyze_plan({"artifacts": {}, "steps": [{"id": "x", "consumes": ["ghost"], "produces": [], "capabilities": []}]})
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "MISSING_ARTIFACT")

    def test_output_overwrite_freezes(self):
        result = analyze_plan({
            "artifacts": {"x": []},
            "steps": [{"id": "write", "consumes": [], "produces": ["x"], "capabilities": []}],
        })
        self.assertEqual(result["reason"], "ARTIFACT_OVERWRITE_FORBIDDEN")


if __name__ == "__main__":
    unittest.main()
