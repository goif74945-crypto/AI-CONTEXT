from __future__ import annotations

import copy
import itertools
import json
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from blocker_core import SpecError, evaluate_spec  # noqa: E402


REV = "9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43"


def leaf(status: str, *, cost: float = 1.0, observed_class: str = "E2_UNIT", **extra):
    value = {
        "status": status,
        "required_class": "E2_UNIT",
        "observed_class": observed_class,
        "target_revision": REV,
        "observed_revision": REV,
        "repair_cost": cost,
        "repair_kind": "EVIDENCE",
    }
    value.update(extra)
    return value


def spec(evidence, gate):
    return {
        "schema_version": "1.0",
        "certificate_id": "TEST-CERT",
        "target": {"name": "unit-test", "revision": REV},
        "evidence": evidence,
        "gate": gate,
    }


class BlockerCoreTests(unittest.TestCase):
    def test_all_pass_allows(self):
        result = evaluate_spec(
            spec({"a": leaf("PASS"), "b": leaf("PASS")}, {"all_of": [{"leaf": "a"}, {"leaf": "b"}]})
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["decision"], "ALLOW")
        self.assertIsNone(result["recommended_repair_set"])
        self.assertEqual(result["minimal_repair_sets"][0]["evidence_ids"], [])

    def test_all_of_requires_union_of_blockers(self):
        result = evaluate_spec(
            spec({"a": leaf("FAIL"), "b": leaf("UNKNOWN")}, {"all_of": [{"leaf": "a"}, {"leaf": "b"}]})
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["decision"], "FREEZE")
        self.assertEqual(result["recommended_repair_set"]["evidence_ids"], ["a", "b"])

    def test_any_of_exposes_alternative_minimal_repairs(self):
        result = evaluate_spec(
            spec(
                {"a": leaf("BLOCKED", cost=5), "b": leaf("UNKNOWN", cost=1)},
                {"any_of": [{"leaf": "a"}, {"leaf": "b"}]},
            )
        )
        self.assertEqual(result["status"], "BLOCKED")
        sets = [record["evidence_ids"] for record in result["minimal_repair_sets"]]
        self.assertEqual(sets, [["b"], ["a"]])  # sorted by cost after minimization
        self.assertEqual(result["recommended_repair_set"]["evidence_ids"], ["b"])

    def test_threshold_repair_with_one_existing_pass(self):
        result = evaluate_spec(
            spec(
                {"a": leaf("PASS"), "b": leaf("FAIL", cost=3), "c": leaf("UNKNOWN", cost=1)},
                {"at_least": {"k": 2, "of": [{"leaf": "a"}, {"leaf": "b"}, {"leaf": "c"}]}},
            )
        )
        self.assertEqual(result["status"], "UNKNOWN")
        sets = [record["evidence_ids"] for record in result["minimal_repair_sets"]]
        self.assertEqual(sets, [["c"], ["b"]])

    def test_stale_revision_downgrades_declared_pass(self):
        evidence = {
            "freshness": leaf("PASS", observed_revision="old-revision", remediation="rerun exact-head proof")
        }
        result = evaluate_spec(spec(evidence, {"leaf": "freshness"}))
        item = result["unsatisfied_evidence"][0]
        self.assertEqual(result["status"], "NOT_VERIFIED")
        self.assertIn("STALE_OR_WRONG_REVISION", item["downgrade_reasons"])

    def test_insufficient_evidence_class_downgrades_declared_pass(self):
        evidence = {
            "runtime": leaf(
                "PASS",
                required_class="E5_RUNTIME",
                observed_class="E1_STATIC",
                remediation="run runtime recovery proof",
            )
        }
        result = evaluate_spec(spec(evidence, {"leaf": "runtime"}))
        self.assertEqual(result["status"], "NOT_VERIFIED")
        self.assertIn(
            "INSUFFICIENT_EVIDENCE_CLASS",
            result["unsatisfied_evidence"][0]["downgrade_reasons"],
        )

    def test_conflict_dominates_aggregate_status(self):
        result = evaluate_spec(
            spec(
                {"a": leaf("FAIL"), "b": leaf("CONFLICT")},
                {"all_of": [{"leaf": "a"}, {"leaf": "b"}]},
            )
        )
        self.assertEqual(result["status"], "CONFLICT")

    def test_hash_is_independent_of_mapping_insertion_order(self):
        first = spec(
            {"a": leaf("UNKNOWN"), "b": leaf("PASS")},
            {"all_of": [{"leaf": "a"}, {"leaf": "b"}]},
        )
        second = copy.deepcopy(first)
        second["evidence"] = {"b": second["evidence"]["b"], "a": second["evidence"]["a"]}
        self.assertEqual(evaluate_spec(first)["certificate_sha256"], evaluate_spec(second)["certificate_sha256"])

    def test_unknown_leaf_is_rejected(self):
        with self.assertRaises(SpecError):
            evaluate_spec(spec({"a": leaf("PASS")}, {"leaf": "missing"}))

    def test_invalid_threshold_is_rejected(self):
        with self.assertRaises(SpecError):
            evaluate_spec(spec({"a": leaf("PASS")}, {"at_least": {"k": 2, "of": [{"leaf": "a"}]}}))

    def test_inclusion_minimal_repairs_remove_supersets(self):
        # (a) OR (a AND b) should require only {a}; {a,b} is dominated.
        result = evaluate_spec(
            spec(
                {"a": leaf("UNKNOWN"), "b": leaf("UNKNOWN")},
                {"any_of": [{"leaf": "a"}, {"all_of": [{"leaf": "a"}, {"leaf": "b"}]}]},
            )
        )
        self.assertEqual([r["evidence_ids"] for r in result["minimal_repair_sets"]], [["a"]])

    def test_nested_gate_repairs_match_bruteforce_oracle(self):
        # Gate: (a OR b) AND at_least(2, [b,c,d]).
        evidence = {name: leaf("UNKNOWN") for name in "abcd"}
        gate = {
            "all_of": [
                {"any_of": [{"leaf": "a"}, {"leaf": "b"}]},
                {"at_least": {"k": 2, "of": [{"leaf": "b"}, {"leaf": "c"}, {"leaf": "d"}]}},
            ]
        }
        result = evaluate_spec(spec(evidence, gate))
        actual = {frozenset(r["evidence_ids"]) for r in result["minimal_repair_sets"]}

        def gate_passes(passed):
            first = "a" in passed or "b" in passed
            second = sum(name in passed for name in "bcd") >= 2
            return first and second

        satisfying = []
        names = "abcd"
        for size in range(len(names) + 1):
            for combo in itertools.combinations(names, size):
                chosen = frozenset(combo)
                if gate_passes(chosen):
                    satisfying.append(chosen)
        oracle = {
            candidate
            for candidate in satisfying
            if not any(other < candidate for other in satisfying)
        }
        self.assertEqual(actual, oracle)

    def test_deterministic_fuzz_small_monotone_formulas(self):
        # Seeded structural regression: reordering evidence map must not change certificate.
        rng = random.Random(74945)
        for iteration in range(50):
            statuses = [rng.choice(["PASS", "UNKNOWN", "FAIL", "NOT_VERIFIED"]) for _ in range(4)]
            evidence = {chr(97 + i): leaf(statuses[i]) for i in range(4)}
            gate = {
                "at_least": {
                    "k": rng.randint(1, 4),
                    "of": [{"leaf": name} for name in evidence],
                }
            }
            first = spec(evidence, gate)
            shuffled_items = list(evidence.items())
            rng.shuffle(shuffled_items)
            second = spec(dict(shuffled_items), copy.deepcopy(gate))
            self.assertEqual(
                evaluate_spec(first)["certificate_sha256"],
                evaluate_spec(second)["certificate_sha256"],
                msg=f"iteration {iteration}",
            )

    def test_repair_limit_is_reported(self):
        evidence = {name: leaf("UNKNOWN") for name in "abcdef"}
        gate = {"any_of": [{"leaf": name} for name in evidence]}
        result = evaluate_spec(spec(evidence, gate), max_repair_sets=3)
        self.assertEqual(len(result["minimal_repair_sets"]), 3)
        self.assertTrue(result["evaluation"]["repair_sets_truncated"])


if __name__ == "__main__":
    unittest.main()
