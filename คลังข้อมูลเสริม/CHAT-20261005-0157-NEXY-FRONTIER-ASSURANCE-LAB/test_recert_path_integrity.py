import random
import unittest

from frontier_assurance_lab import FreezeError, RecoveryPolicy
from recert_path_integrity import (
    PointerRecoveryCertifier,
    PointerRecoveryPolicy,
    RecertPathIntegrityAssurance,
)


class PointerRecoveryPositiveTests(unittest.TestCase):
    def setUp(self):
        self.certifier = PointerRecoveryCertifier()

    def test_exact_nested_state_certified(self):
        state = {"law": {"epoch": 7}, "ready": True}
        result = self.certifier.certify(state, state, PointerRecoveryPolicy())
        self.assertEqual(result["status"], "CERTIFIED")
        self.assertEqual(result["compared_pointer_count"], 2)

    def test_escaped_tokens_have_distinct_identity(self):
        state = {"a/b": {"~x": 4}, "a": {"b": 4}}
        result = self.certifier.certify(state, state, PointerRecoveryPolicy())
        self.assertEqual(result["status"], "CERTIFIED")
        self.assertEqual(result["compared_pointer_count"], 2)

    def test_integer_nondecreasing_certified(self):
        policy = PointerRecoveryPolicy(modes={"/metrics/retries": "NONDECREASING"})
        result = self.certifier.certify(
            {"metrics": {"retries": 2}}, {"metrics": {"retries": 3}}, policy
        )
        self.assertEqual(result["status"], "CERTIFIED")

    def test_present_absent_any_modes(self):
        policy = PointerRecoveryPolicy(
            modes={"/new": "PRESENT", "/old": "ABSENT", "/volatile": "ANY"}
        )
        result = self.certifier.certify(
            {"old": 1, "volatile": "before"},
            {"new": 1, "volatile": "after"},
            policy,
        )
        self.assertEqual(result["status"], "CERTIFIED")

    def test_ignore_prefix_uses_segment_boundary(self):
        policy = PointerRecoveryPolicy(ignore_prefixes=("/runtime/temp",))
        result = self.certifier.certify(
            {"runtime": {"temp": {"pid": 1}, "temporary": 4}},
            {"runtime": {"temp": {"pid": 9}, "temporary": 4}},
            policy,
        )
        self.assertEqual(result["status"], "CERTIFIED")


class PointerRecoveryNegativeTests(unittest.TestCase):
    def setUp(self):
        self.certifier = PointerRecoveryCertifier()

    def test_dotted_key_alias_attack_freezes(self):
        before = {"a": {"b": 1}, "a.b": 9}
        after = {"a": {"b": 2}, "a.b": 9}
        result = self.certifier.certify(before, after, PointerRecoveryPolicy())
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["mismatches"][0]["pointer"], "/a/b")

    def test_exact_is_type_sensitive(self):
        result = self.certifier.certify(
            {"approved": True}, {"approved": 1}, PointerRecoveryPolicy()
        )
        self.assertEqual(result["status"], "FREEZE")

    def test_exact_is_deeply_type_sensitive_for_array_leaf(self):
        result = self.certifier.certify(
            {"values": [True]}, {"values": [1]}, PointerRecoveryPolicy()
        )
        self.assertEqual(result["status"], "FREEZE")

    def test_nondecreasing_rejects_boolean_as_integer(self):
        policy = PointerRecoveryPolicy(modes={"/count": "NONDECREASING"})
        result = self.certifier.certify({"count": False}, {"count": True}, policy)
        self.assertEqual(result["status"], "FREEZE")

    def test_invalid_pointer_escape_rejected(self):
        with self.assertRaises(FreezeError):
            PointerRecoveryPolicy(modes={"/a~2b": "EXACT"})

    def test_root_wide_ignore_rejected(self):
        with self.assertRaises(FreezeError):
            PointerRecoveryPolicy(ignore_prefixes=("",))

    def test_policy_hidden_by_ignore_rejected(self):
        with self.assertRaises(FreezeError):
            PointerRecoveryPolicy(
                modes={"/runtime/temp/pid": "EXACT"},
                ignore_prefixes=("/runtime/temp",),
            )

    def test_non_string_mapping_key_rejected(self):
        with self.assertRaises(FreezeError):
            self.certifier.certify({1: "x"}, {1: "x"}, PointerRecoveryPolicy())

    def test_mixed_key_types_fail_closed_before_sort(self):
        with self.assertRaises(FreezeError):
            self.certifier.certify(
                {"1": "text", 1: "integer"},
                {"1": "text", 1: "integer"},
                PointerRecoveryPolicy(),
            )

    def test_cyclic_state_rejected(self):
        cyclic = {}
        cyclic["self"] = cyclic
        with self.assertRaises(FreezeError):
            self.certifier.certify(cyclic, cyclic, PointerRecoveryPolicy())


class PointerRecoveryAdversarialTests(unittest.TestCase):
    def test_mapping_order_permutations_are_deterministic(self):
        certifier = PointerRecoveryCertifier()
        pairs = [("a.b", 9), ("a", {"b": 1}), ("x/y", {"~z": 3})]
        baseline = certifier.certify(dict(pairs), dict(pairs), PointerRecoveryPolicy())
        rng = random.Random(74945)
        for _ in range(100):
            left = pairs[:]
            right = pairs[:]
            rng.shuffle(left)
            rng.shuffle(right)
            self.assertEqual(
                certifier.certify(dict(left), dict(right), PointerRecoveryPolicy()),
                baseline,
            )


class RecertPathIntegrityIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.assurance = RecertPathIntegrityAssurance()

    def test_normal_state_requires_both_certifiers(self):
        result = self.assurance.assess(
            {"law": {"epoch": 7}},
            {"law": {"epoch": 7}},
            RecoveryPolicy(),
            PointerRecoveryPolicy(),
        )
        self.assertEqual(result["status"], "CERTIFIED")
        self.assertEqual(result["reason"], "BOTH_CERTIFIERS_AGREE")

    def test_legacy_false_certification_is_blocked(self):
        before = {"a": {"b": 1}, "a.b": 9}
        after = {"a": {"b": 2}, "a.b": 9}
        result = self.assurance.assess(
            before,
            after,
            RecoveryPolicy(),
            PointerRecoveryPolicy(),
        )
        self.assertEqual(result["original"]["status"], "CERTIFIED")
        self.assertEqual(result["pointer_safe"]["status"], "FREEZE")
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "PATH_ALIAS_OR_STRICTNESS_DISAGREEMENT")


if __name__ == "__main__":
    unittest.main()
