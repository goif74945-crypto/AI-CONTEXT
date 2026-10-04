import unittest

from integration.fabric import evaluate_execution


def safe_payload():
    return {
        "goal_spec": {
            "required_facts": {"target": "AI-CONTEXT", "tests": "green"},
            "forbidden_facts": {"nexy_repo_mutated": True},
            "required_capabilities": ["context-write"],
            "forbidden_effects": ["force-push"],
            "required_outputs": ["evidence"],
        },
        "observed": {
            "facts": {"target": "AI-CONTEXT", "tests": "green", "nexy_repo_mutated": False},
            "capabilities": ["context-write"],
            "effects": [],
            "outputs": {"evidence": "present"},
        },
        "uncertainty": {"requirements": [], "known": [], "probes": []},
        "assurance": {
            "requirements": {"correctness": 1, "security": 1},
            "validators": [
                {"id": "unit", "domain": "local", "covers": ["correctness"], "cost": 1, "latency_ms": 5},
                {"id": "static", "domain": "static", "covers": ["security"], "cost": 1, "latency_ms": 2},
            ],
            "max_cost": 5,
        },
        "actions": {"actions": [
            {"id": "write-context", "depends_on": [], "reversible": True, "compensation": "restore-context"},
            {"id": "verify", "depends_on": ["write-context"], "reversible": True, "compensation": "discard-evidence"},
        ]},
        "input_schema": {"fields": {
            "task": {"type": "string", "required": True, "min_length": 1, "max_length": 64},
            "mode": {"type": "enum", "required": True, "values": ["strict", "safe"]},
        }},
        "valid_case": {"task": "build", "mode": "strict"},
    }


class FabricIntegrationTests(unittest.TestCase):
    def test_safe_mission_is_ready(self):
        result = evaluate_execution(safe_payload())
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["goal"]["status"], "PASS")
        self.assertEqual(result["reversibility"]["status"], "PLAN")
        self.assertGreater(result["counterexamples"]["count"], 0)

    def test_unknown_path_asks_minimum_question(self):
        payload = safe_payload()
        payload["uncertainty"] = {
            "requirements": [{"id": "r1", "blocked_by": ["branch"]}],
            "known": [],
            "probes": [{"id": "ask-branch", "cost": 1, "resolves": ["branch"], "question": "Which branch?"}],
        }
        result = evaluate_execution(payload)
        self.assertEqual(result["status"], "ASK")
        self.assertEqual(result["unknown_closure"]["questions"], ["Which branch?"])

    def test_unrelated_question_cannot_mask_missing_goal_evidence(self):
        payload = safe_payload()
        payload["observed"]["facts"].pop("tests")
        payload["uncertainty"] = {
            "requirements": [{"id": "r", "blocked_by": ["branch"]}],
            "known": [],
            "probes": [{"id": "q", "cost": 1, "resolves": ["branch"], "question": "Which branch?"}],
        }
        result = evaluate_execution(payload)
        self.assertEqual(result["status"], "FREEZE")
        self.assertIn("goal:NOT_VERIFIED_WITHOUT_COMPLETE_RESOLUTION_PATH", result["freeze_reasons"])

    def test_matching_question_can_resolve_missing_goal_evidence(self):
        payload = safe_payload()
        payload["observed"]["facts"].pop("tests")
        payload["uncertainty"] = {
            "requirements": [{"id": "r", "blocked_by": ["fact:tests"]}],
            "known": [],
            "probes": [{"id": "q", "cost": 1, "resolves": ["fact:tests"], "question": "What is the test state?"}],
        }
        result = evaluate_execution(payload)
        self.assertEqual(result["status"], "ASK")

    def test_irreversible_action_freezes(self):
        payload = safe_payload()
        payload["actions"] = {"actions": [{"id": "delete", "depends_on": [], "reversible": False}]}
        result = evaluate_execution(payload)
        self.assertEqual(result["status"], "FREEZE")
        self.assertTrue(any("UNAPPROVED_IRREVERSIBLE_ACTION" in x for x in result["freeze_reasons"]))

    def test_repeat_is_byte_stable(self):
        first = evaluate_execution(safe_payload())
        second = evaluate_execution(safe_payload())
        self.assertEqual(first["decision_id"], second["decision_id"])
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
