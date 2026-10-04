import unittest

from concepts.unknown_closure_planner.engine import plan_unknown_closure


class UnknownClosurePlannerTests(unittest.TestCase):
    def test_selects_minimum_cost_cover(self):
        payload = {
            "requirements": [
                {"id": "r1", "blocked_by": ["account", "region"]},
                {"id": "r2", "blocked_by": ["branch"]},
            ],
            "known": [],
            "probes": [
                {"id": "p_account", "cost": 2, "resolves": ["account"], "question": "Which account?"},
                {"id": "p_combo", "cost": 2, "resolves": ["account", "region"], "question": "Which account and region?"},
                {"id": "p_region", "cost": 3, "resolves": ["region"], "question": "Which region?"},
                {"id": "p_branch", "cost": 1, "resolves": ["branch"], "question": "Which branch?"},
            ],
        }
        result = plan_unknown_closure(payload)
        self.assertEqual(result["status"], "ASK")
        self.assertEqual([p["id"] for p in result["selected_probes"]], ["p_branch", "p_combo"])
        self.assertEqual(result["total_cost"], 3)

    def test_unresolvable_unknown_freezes(self):
        result = plan_unknown_closure({
            "requirements": [{"id": "r", "blocked_by": ["secret_fact"]}],
            "known": [],
            "probes": [],
        })
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["unresolvable"], ["secret_fact"])

    def test_known_unknowns_need_no_question(self):
        result = plan_unknown_closure({
            "requirements": [{"id": "r", "blocked_by": ["branch"]}],
            "known": ["branch"],
            "probes": [],
        })
        self.assertEqual(result["status"], "PROCEED")

    def test_input_order_does_not_change_plan(self):
        probes = [
            {"id": "b", "cost": 1, "resolves": ["u2"], "question": "b?"},
            {"id": "a", "cost": 1, "resolves": ["u1"], "question": "a?"},
        ]
        base = {"requirements": [{"id": "r", "blocked_by": ["u1", "u2"]}], "known": []}
        one = plan_unknown_closure({**base, "probes": probes})
        two = plan_unknown_closure({**base, "probes": list(reversed(probes))})
        self.assertEqual(one["plan_id"], two["plan_id"])


if __name__ == "__main__":
    unittest.main()
