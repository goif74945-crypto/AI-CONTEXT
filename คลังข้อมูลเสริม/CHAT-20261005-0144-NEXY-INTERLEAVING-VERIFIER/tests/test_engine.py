from __future__ import annotations

import copy
import unittest

from interleaving_verifier.engine import verify_plan


def action(action_id, effects, *, depends_on=None, requires=None):
    return {
        "id": action_id,
        "depends_on": depends_on or [],
        "requires": requires or [],
        "effects": effects,
    }


def base_plan(actions, *, state=None, invariants=None, limits=None):
    return {
        "schema_version": "1.0",
        "initial_state": state if state is not None else {"x": 0},
        "actions": actions,
        "invariants": invariants or [],
        "limits": limits or {"max_states": 1000, "max_transitions": 5000},
    }


class InterleavingVerifierTests(unittest.TestCase):
    def test_commutative_additions_are_confluent(self):
        plan = base_plan([
            action("A", [{"op": "add", "path": "/x", "value": 1}]),
            action("B", [{"op": "add", "path": "/x", "value": 2}]),
        ])
        report = verify_plan(plan)
        self.assertEqual(report["verification_status"], "PASS")
        self.assertEqual(report["decision"], "CONFLUENT")
        self.assertTrue(report["exploration_complete"])
        self.assertEqual(report["canonical_terminal_state"], {"x": 3})
        self.assertEqual(report["terminal_state_count"], 1)
        self.assertEqual(report["static_conflicts"][0]["actions"], ["A", "B"])

    def test_unordered_sets_produce_divergence_witness(self):
        plan = base_plan([
            action("A", [{"op": "set", "path": "/x", "value": 1}]),
            action("B", [{"op": "set", "path": "/x", "value": 2}]),
        ])
        report = verify_plan(plan)
        self.assertEqual(report["verification_status"], "FAIL")
        self.assertEqual(report["decision"], "DIVERGENT_TERMINAL_STATE")
        witness = report["witnesses"][0]
        self.assertNotEqual(witness["state_a"], witness["state_b"])
        self.assertEqual(witness["candidate_serialization_pair"], ["A", "B"])
        self.assertEqual(witness["state_diff"][0]["path"], "/x")

    def test_dependency_serializes_divergent_writes(self):
        plan = base_plan([
            action("A", [{"op": "set", "path": "/x", "value": 1}]),
            action("B", [{"op": "set", "path": "/x", "value": 2}], depends_on=["A"]),
        ])
        report = verify_plan(plan)
        self.assertEqual(report["verification_status"], "PASS")
        self.assertEqual(report["canonical_terminal_state"], {"x": 2})
        self.assertEqual(report["static_conflicts"], [])

    def test_order_sensitive_precondition_is_failure(self):
        plan = base_plan([
            action(
                "A",
                [{"op": "set", "path": "/y", "value": "done"}],
                requires=[{"op": "eq", "path": "/x", "value": 0}],
            ),
            action("B", [{"op": "set", "path": "/x", "value": 1}]),
        ])
        report = verify_plan(plan)
        self.assertEqual(report["verification_status"], "FAIL")
        self.assertEqual(report["decision"], "PRECONDITION_FAILURE")
        self.assertEqual(report["witnesses"][0]["blocked_action"], "A")
        self.assertEqual(report["witnesses"][0]["schedule_prefix"], ["B"])

    def test_intermediate_invariant_violation_fails_even_if_later_action_could_repair(self):
        plan = base_plan(
            [
                action("A", [{"op": "set", "path": "/x", "value": -1}]),
                action("B", [{"op": "set", "path": "/x", "value": 0}], depends_on=["A"]),
            ],
            invariants=[{"op": "int_range", "path": "/x", "min": 0}],
        )
        report = verify_plan(plan)
        self.assertEqual(report["verification_status"], "FAIL")
        self.assertEqual(report["decision"], "INVARIANT_VIOLATION")
        self.assertEqual(report["witnesses"][0]["schedule"], ["A"])

    def test_initial_invariant_violation(self):
        plan = base_plan(
            [action("A", [{"op": "set", "path": "/x", "value": 1}])],
            state={"x": -1},
            invariants=[{"op": "int_range", "path": "/x", "min": 0}],
        )
        report = verify_plan(plan)
        self.assertEqual(report["decision"], "INVARIANT_VIOLATION")
        self.assertEqual(report["witnesses"][0]["schedule"], [])

    def test_cycle_freezes_as_invalid_input(self):
        plan = base_plan([
            action("A", [{"op": "set", "path": "/x", "value": 1}], depends_on=["B"]),
            action("B", [{"op": "set", "path": "/x", "value": 2}], depends_on=["A"]),
        ])
        report = verify_plan(plan)
        self.assertEqual(report["verification_status"], "NOT_VERIFIED")
        self.assertEqual(report["decision"], "FREEZE_INVALID_INPUT")
        self.assertIn("dependency cycle", report["diagnostics"][0]["message"])

    def test_missing_dependency_freezes(self):
        plan = base_plan([
            action("A", [{"op": "set", "path": "/x", "value": 1}], depends_on=["MISSING"]),
        ])
        report = verify_plan(plan)
        self.assertEqual(report["decision"], "FREEZE_INVALID_INPUT")
        self.assertIn("missing dependencies", report["diagnostics"][0]["message"])

    def test_unknown_field_freezes_closed(self):
        plan = base_plan([action("A", [{"op": "set", "path": "/x", "value": 1}])])
        plan["surprise"] = True
        report = verify_plan(plan)
        self.assertEqual(report["decision"], "FREEZE_INVALID_INPUT")
        self.assertIn("unknown fields", report["diagnostics"][0]["message"])

    def test_state_limit_freezes_instead_of_passing_partial_exploration(self):
        plan = base_plan(
            [
                action("A", [{"op": "set", "path": "/a", "value": 1}]),
                action("B", [{"op": "set", "path": "/b", "value": 1}]),
            ],
            state={},
            limits={"max_states": 1, "max_transitions": 100},
        )
        report = verify_plan(plan)
        self.assertEqual(report["verification_status"], "NOT_VERIFIED")
        self.assertEqual(report["decision"], "FREEZE_LIMIT")
        self.assertEqual(report["diagnostics"][0]["code"], "MAX_STATES_EXCEEDED")

    def test_transition_limit_freezes(self):
        plan = base_plan(
            [
                action("A", [{"op": "set", "path": "/a", "value": 1}]),
                action("B", [{"op": "set", "path": "/b", "value": 1}]),
            ],
            state={},
            limits={"max_states": 100, "max_transitions": 1},
        )
        report = verify_plan(plan)
        self.assertEqual(report["decision"], "FREEZE_LIMIT")
        self.assertEqual(report["diagnostics"][0]["code"], "MAX_TRANSITIONS_EXCEEDED")

    def test_runtime_type_error_is_decisive_plan_failure(self):
        plan = base_plan(
            [action("A", [{"op": "add", "path": "/x", "value": 1}])],
            state={"x": "not-an-int"},
        )
        report = verify_plan(plan)
        self.assertEqual(report["verification_status"], "FAIL")
        self.assertEqual(report["decision"], "EXECUTION_MODEL_ERROR")
        self.assertIn("requires integer", report["witnesses"][0]["message"])

    def test_distinct_paths_have_no_static_conflict(self):
        plan = base_plan(
            [
                action("A", [{"op": "set", "path": "/left", "value": 1}]),
                action("B", [{"op": "set", "path": "/right", "value": 1}]),
            ],
            state={},
        )
        report = verify_plan(plan)
        self.assertEqual(report["verification_status"], "PASS")
        self.assertEqual(report["static_conflicts"], [])

    def test_parent_child_paths_conflict(self):
        plan = base_plan(
            [
                action("A", [{"op": "set", "path": "/obj", "value": {"x": 1}}]),
                action("B", [{"op": "set", "path": "/obj/x", "value": 2}]),
            ],
            state={"obj": {"x": 0}},
        )
        report = verify_plan(plan)
        self.assertTrue(report["static_conflicts"])
        ww = report["static_conflicts"][0]["write_write"]
        self.assertEqual(ww, [["/obj", "/obj/x"]])

    def test_input_action_order_does_not_change_report(self):
        actions = [
            action("A", [{"op": "add", "path": "/x", "value": 1}]),
            action("B", [{"op": "add", "path": "/x", "value": 2}]),
            action("C", [{"op": "set", "path": "/y", "value": 7}]),
        ]
        first = verify_plan(base_plan(actions, state={"x": 0}))
        second = verify_plan(base_plan(list(reversed(actions)), state={"x": 0}))
        self.assertEqual(first, second)
        self.assertEqual(first["report_fingerprint"], second["report_fingerprint"])

    def test_append_unique_is_order_sensitive_when_list_order_is_authoritative(self):
        plan = base_plan(
            [
                action("A", [{"op": "append_unique", "path": "/items", "value": "a"}]),
                action("B", [{"op": "append_unique", "path": "/items", "value": "b"}]),
            ],
            state={"items": []},
            invariants=[{"op": "unique", "path": "/items"}],
        )
        report = verify_plan(plan)
        self.assertEqual(report["decision"], "DIVERGENT_TERMINAL_STATE")

    def test_copy_vs_write_is_detected_as_read_write_conflict(self):
        plan = base_plan(
            [
                action("A", [{"op": "copy", "from": "/x", "to": "/y"}]),
                action("B", [{"op": "set", "path": "/x", "value": 9}]),
            ],
            state={"x": 1},
        )
        report = verify_plan(plan)
        conflict = report["static_conflicts"][0]
        self.assertEqual(conflict["left_read_right_write"], [["/x", "/x"]])
        self.assertEqual(report["decision"], "DIVERGENT_TERMINAL_STATE")

    def test_copy_rejects_irrelevant_value_field(self):
        plan = base_plan([
            action("A", [{"op": "copy", "from": "/x", "to": "/y", "value": 9}]),
        ], state={"x": 1})
        report = verify_plan(plan)
        self.assertEqual(report["decision"], "FREEZE_INVALID_INPUT")

    def test_set_rejects_copy_only_fields(self):
        plan = base_plan([
            action("A", [{"op": "set", "path": "/x", "value": 1, "from": "/y"}]),
        ], state={"x": 0, "y": 2})
        report = verify_plan(plan)
        self.assertEqual(report["decision"], "FREEZE_INVALID_INPUT")

    def test_state_merging_collapses_ten_factorial_commuting_schedules(self):
        actions = [
            action(f"A{i:02d}", [{"op": "add", "path": "/x", "value": 1}])
            for i in range(10)
        ]
        report = verify_plan(base_plan(
            actions,
            state={"x": 0},
            limits={"max_states": 2000, "max_transitions": 10000},
        ))
        self.assertEqual(report["verification_status"], "PASS")
        self.assertEqual(report["canonical_terminal_state"], {"x": 10})
        self.assertEqual(report["states_explored"], 1024)
        self.assertEqual(report["transitions_explored"], 5120)

    def test_float_values_freeze_for_cross_runtime_determinism(self):
        plan = base_plan([
            action("A", [{"op": "set", "path": "/x", "value": 1.5}]),
        ])
        report = verify_plan(plan)
        self.assertEqual(report["decision"], "FREEZE_INVALID_INPUT")
        self.assertIn("floating-point", report["diagnostics"][0]["message"])

    def test_report_fingerprint_changes_when_semantics_change(self):
        p1 = base_plan([action("A", [{"op": "set", "path": "/x", "value": 1}])])
        p2 = copy.deepcopy(p1)
        p2["actions"][0]["effects"][0]["value"] = 2
        r1 = verify_plan(p1)
        r2 = verify_plan(p2)
        self.assertNotEqual(r1["plan_fingerprint"], r2["plan_fingerprint"])
        self.assertNotEqual(r1["report_fingerprint"], r2["report_fingerprint"])


if __name__ == "__main__":
    unittest.main()
