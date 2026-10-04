import unittest

from common import ContractError
from concepts.goal_state_compiler.engine import compile_goal, evaluate_goal


class GoalStateCompilerTests(unittest.TestCase):
    def setUp(self):
        self.spec = {
            "required_facts": {"repo": "AI-CONTEXT", "tests": "green"},
            "forbidden_facts": {"protected_repo_mutated": True},
            "required_capabilities": ["write-context", "test"],
            "forbidden_effects": ["force-push", "delete-production"],
            "required_outputs": ["evidence"],
        }
        self.observed = {
            "facts": {"tests": "green", "repo": "AI-CONTEXT", "protected_repo_mutated": False},
            "capabilities": ["test", "write-context"],
            "effects": [],
            "outputs": {"evidence": {"count": 1}},
        }

    def test_pass_and_order_independence(self):
        a = compile_goal(self.spec)
        reordered = dict(reversed(list(self.spec.items())))
        b = compile_goal(reordered)
        self.assertEqual(a["contract_id"], b["contract_id"])
        self.assertEqual(evaluate_goal(a, self.observed)["status"], "PASS")

    def test_missing_fact_is_not_verified(self):
        contract = compile_goal(self.spec)
        observed = {**self.observed, "facts": {"repo": "AI-CONTEXT", "protected_repo_mutated": False}}
        result = evaluate_goal(contract, observed)
        self.assertEqual(result["status"], "NOT_VERIFIED")
        self.assertIn("fact:tests", result["missing"])

    def test_forbidden_effect_freezes(self):
        contract = compile_goal(self.spec)
        observed = {**self.observed, "effects": ["force-push"]}
        self.assertEqual(evaluate_goal(contract, observed)["status"], "FREEZE")

    def test_non_json_fact_rejected(self):
        with self.assertRaises(ContractError):
            compile_goal({"required_facts": {"bad": {1, 2}}})

    def test_tampered_contract_rejected(self):
        contract = compile_goal(self.spec)
        contract["spec"]["required_facts"]["tests"] = "red"
        with self.assertRaises(ContractError):
            evaluate_goal(contract, self.observed)


if __name__ == "__main__":
    unittest.main()
