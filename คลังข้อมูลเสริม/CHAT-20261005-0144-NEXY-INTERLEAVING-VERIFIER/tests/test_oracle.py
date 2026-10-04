from __future__ import annotations

import itertools
import unittest

from interleaving_verifier.engine import verify_plan
from interleaving_verifier.model import apply_effect, canonical_json


OPS = (
    {"op": "add", "path": "/x", "value": 1},
    {"op": "add", "path": "/x", "value": 2},
    {"op": "set", "path": "/x", "value": 0},
    {"op": "set", "path": "/x", "value": 1},
)


def build_plan(effects):
    return {
        "schema_version": "1.0",
        "initial_state": {"x": 0},
        "actions": [
            {"id": chr(ord("A") + i), "effects": [dict(effect)]}
            for i, effect in enumerate(effects)
        ],
        "limits": {"max_states": 10000, "max_transitions": 100000},
    }


def brute_force_terminal_states(effects):
    action_ids = [chr(ord("A") + i) for i in range(len(effects))]
    by_id = dict(zip(action_ids, effects))
    terminals = set()
    for order in itertools.permutations(action_ids):
        state = {"x": 0}
        for action_id in order:
            apply_effect(state, by_id[action_id])
        terminals.add(canonical_json(state))
    return terminals


class ExhaustiveOracleTests(unittest.TestCase):
    def test_state_reduction_matches_bruteforce_for_all_three_action_programs(self):
        checked = 0
        for effects in itertools.product(OPS, repeat=3):
            expected_terminals = brute_force_terminal_states(effects)
            report = verify_plan(build_plan(effects))
            expected_confluent = len(expected_terminals) == 1
            self.assertEqual(
                report["verification_status"] == "PASS",
                expected_confluent,
                msg=f"effects={effects}, report={report}",
            )
            if expected_confluent:
                self.assertEqual(report["decision"], "CONFLUENT")
                self.assertEqual(report["terminal_state_count"], 1)
            else:
                self.assertEqual(report["decision"], "DIVERGENT_TERMINAL_STATE")
                self.assertGreaterEqual(report["terminal_state_count"], 2)
            checked += 1
        self.assertEqual(checked, 64)

    def test_action_array_permutations_preserve_semantic_report(self):
        source = build_plan((OPS[0], OPS[1], OPS[0]))
        baseline = verify_plan(source)
        for permutation in itertools.permutations(source["actions"]):
            candidate = dict(source)
            candidate["actions"] = list(permutation)
            self.assertEqual(verify_plan(candidate), baseline)


if __name__ == "__main__":
    unittest.main()
