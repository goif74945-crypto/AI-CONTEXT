import unittest

from concepts.assurance_budget_planner.engine import plan_assurance


class AssuranceBudgetPlannerTests(unittest.TestCase):
    def setUp(self):
        self.validators = [
            {"id": "unit", "domain": "local", "covers": ["correctness"], "cost": 1, "latency_ms": 10},
            {"id": "review-a", "domain": "provider-a", "covers": ["correctness", "security"], "cost": 3, "latency_ms": 30},
            {"id": "review-b", "domain": "provider-b", "covers": ["security"], "cost": 2, "latency_ms": 20},
            {"id": "expensive", "domain": "provider-c", "covers": ["correctness", "security"], "cost": 20, "latency_ms": 100},
        ]

    def test_selects_cheapest_independent_assurance(self):
        result = plan_assurance({
            "requirements": {"correctness": 1, "security": 2},
            "validators": self.validators,
            "max_cost": 10,
        })
        self.assertEqual(result["status"], "PLAN")
        self.assertEqual([v["id"] for v in result["selected_validators"]], ["review-a", "review-b"])
        self.assertEqual(result["total_cost"], 5)

    def test_budget_freezes_even_when_coverage_exists(self):
        result = plan_assurance({
            "requirements": {"security": 2},
            "validators": self.validators,
            "max_cost": 4,
        })
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "ASSURANCE_BUDGET_EXCEEDED")

    def test_missing_independence_freezes(self):
        result = plan_assurance({
            "requirements": {"security": 2},
            "validators": [{"id": "x", "domain": "same", "covers": ["security"], "cost": 1, "latency_ms": 1}],
        })
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "INSUFFICIENT_INDEPENDENT_ASSURANCE")

    def test_same_domain_does_not_fake_independence(self):
        result = plan_assurance({
            "requirements": {"security": 2},
            "validators": [
                {"id": "a", "domain": "same", "covers": ["security"], "cost": 1, "latency_ms": 1},
                {"id": "b", "domain": "same", "covers": ["security"], "cost": 1, "latency_ms": 1},
            ],
        })
        self.assertEqual(result["status"], "FREEZE")

    def test_order_independent(self):
        payload = {"requirements": {"security": 2}, "max_cost": 10}
        one = plan_assurance({**payload, "validators": self.validators})
        two = plan_assurance({**payload, "validators": list(reversed(self.validators))})
        self.assertEqual(one["plan_id"], two["plan_id"])


if __name__ == "__main__":
    unittest.main()
