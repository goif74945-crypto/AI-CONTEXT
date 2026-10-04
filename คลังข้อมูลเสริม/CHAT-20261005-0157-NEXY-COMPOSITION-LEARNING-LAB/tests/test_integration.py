import unittest

from nexy_aux.emergence import analyze_plan
from nexy_aux.integration import distill_emergent_risk


class IntegrationTests(unittest.TestCase):
    def test_risk_analyzer_plus_distiller_produces_minimal_repro(self):
        plan = {
            "artifacts": {"credential": ["SECRET"], "public": []},
            "steps": [
                {"id": "normalize", "consumes": ["credential"], "produces": ["normalized"], "capabilities": []},
                {"id": "noise", "consumes": ["public"], "produces": ["noise_out"], "capabilities": []},
                {"id": "send", "consumes": ["normalized"], "produces": [], "capabilities": ["EXTERNAL_EGRESS"]},
            ],
        }
        original = analyze_plan(plan)
        self.assertIn("E_SECRET_EGRESS", {x["code"] for x in original["findings"]})
        reduced = distill_emergent_risk(plan, "E_SECRET_EGRESS")
        self.assertEqual(reduced["status"], "PASS")
        self.assertEqual([x["id"] for x in reduced["minimal_items"]], ["normalize", "send"])

    def test_minimal_repro_reanalyzes_to_same_finding(self):
        plan = {
            "artifacts": {"input": ["UNTRUSTED"]},
            "steps": [
                {"id": "copy", "consumes": ["input"], "produces": ["x"], "capabilities": []},
                {"id": "exec", "consumes": ["x"], "produces": [], "capabilities": ["EXECUTE_CODE"]},
            ],
        }
        reduced = distill_emergent_risk(plan, "E_UNTRUSTED_EXECUTION")
        replay = analyze_plan({"artifacts": plan["artifacts"], "steps": reduced["minimal_items"]})
        self.assertIn("E_UNTRUSTED_EXECUTION", {x["code"] for x in replay["findings"]})


if __name__ == "__main__":
    unittest.main()
