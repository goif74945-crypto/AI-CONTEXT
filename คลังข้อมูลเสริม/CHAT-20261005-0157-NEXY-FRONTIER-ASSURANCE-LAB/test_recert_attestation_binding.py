import random
import unittest
from collections import UserDict

from frontier_assurance_lab import FreezeError, RecoveryPolicy
from recert_attestation_binding import (
    RecertAttestationBindingAssurance,
    RecoveryAttestationContract,
)
from recert_path_integrity import PointerRecoveryPolicy


def contract(**overrides):
    values = {
        "attestation_id": "recert-attestation-1",
        "incident_id": "incident-17",
        "before_revision": "rev-before",
        "after_revision": "rev-after",
    }
    values.update(overrides)
    return RecoveryAttestationContract(**values)


def assess(before=None, after=None, original=None, pointer=None, binding=None):
    return RecertAttestationBindingAssurance().assess(
        binding or contract(),
        {"law": {"epoch": 7}} if before is None else before,
        {"law": {"epoch": 7}} if after is None else after,
        original or RecoveryPolicy(),
        pointer or PointerRecoveryPolicy(),
    )


class RecertAttestationPositiveTests(unittest.TestCase):
    def test_certified_result_binds_contract_states_and_policies(self):
        result = assess()
        self.assertEqual(result["status"], "CERTIFIED")
        for name in (
            "attestation_contract_hash",
            "before_state_hash",
            "after_state_hash",
            "original_policy_hash",
            "pointer_policy_hash",
            "binding_hash",
            "base_result_hash",
            "result_hash",
        ):
            self.assertRegex(result[name], r"^[0-9a-f]{64}$")

    def test_equal_states_have_equal_state_hashes(self):
        result = assess()
        self.assertEqual(result["before_state_hash"], result["after_state_hash"])

    def test_changed_state_changes_certificate_even_when_base_result_collides(self):
        first = assess(before={"epoch": 1}, after={"epoch": 1})
        second = assess(before={"epoch": 2}, after={"epoch": 2})
        self.assertEqual(first["base_result_hash"], second["base_result_hash"])
        self.assertNotEqual(first["binding_hash"], second["binding_hash"])
        self.assertNotEqual(first["result_hash"], second["result_hash"])

    def test_changed_policy_changes_certificate_even_when_base_result_collides(self):
        exact = assess(before={"epoch": 1}, after={"epoch": 1})
        present = assess(
            before={"epoch": 1},
            after={"epoch": 1},
            original=RecoveryPolicy(modes={"epoch": "PRESENT"}),
            pointer=PointerRecoveryPolicy(modes={"/epoch": "PRESENT"}),
        )
        self.assertEqual(exact["base_result_hash"], present["base_result_hash"])
        self.assertNotEqual(exact["binding_hash"], present["binding_hash"])


class RecertAttestationNegativeTests(unittest.TestCase):
    def test_contract_requires_nonempty_identity_fields(self):
        for field in ("attestation_id", "incident_id", "before_revision", "after_revision"):
            with self.subTest(field=field), self.assertRaises(FreezeError):
                contract(**{field: " "})

    def test_top_level_state_must_be_builtin_dict(self):
        with self.assertRaises(FreezeError):
            assess(before=UserDict({"epoch": 1}), after={"epoch": 1})

    def test_nested_custom_mapping_is_rejected(self):
        with self.assertRaises(FreezeError):
            assess(before={"nested": UserDict({"epoch": 1})}, after={"nested": {"epoch": 1}})

    def test_policy_modes_must_be_builtin_dict(self):
        with self.assertRaises(FreezeError):
            assess(original=RecoveryPolicy(modes=UserDict({"epoch": "EXACT"})))

    def test_policy_ignore_prefixes_must_be_tuple(self):
        with self.assertRaises(FreezeError):
            assess(original=RecoveryPolicy(ignore_prefixes=["runtime"]))

    def test_cyclic_list_state_is_rejected(self):
        cycle = []
        cycle.append(cycle)
        with self.assertRaises(FreezeError):
            assess(before={"cycle": cycle}, after={"cycle": []})

    def test_noncanonical_leaf_is_rejected(self):
        with self.assertRaises(FreezeError):
            assess(before={"bad": object()}, after={"bad": object()})


class RecertAttestationAdversarialTests(unittest.TestCase):
    def test_list_and_tuple_states_have_distinct_bindings(self):
        list_state = assess(before={"items": [1]}, after={"items": [1]})
        tuple_state = assess(before={"items": (1,)}, after={"items": (1,)})
        self.assertEqual(list_state["status"], "CERTIFIED")
        self.assertEqual(tuple_state["status"], "CERTIFIED")
        self.assertEqual(list_state["base_result_hash"], tuple_state["base_result_hash"])
        self.assertNotEqual(list_state["before_state_hash"], tuple_state["before_state_hash"])
        self.assertNotEqual(list_state["binding_hash"], tuple_state["binding_hash"])

    def test_mapping_order_permutations_are_deterministic(self):
        pairs = [("a", {"x": 1}), ("b", [1, 2]), ("c", "value")]
        baseline = assess(before=dict(pairs), after=dict(pairs))
        rng = random.Random(74945)
        for _ in range(50):
            left = pairs[:]
            right = pairs[:]
            rng.shuffle(left)
            rng.shuffle(right)
            self.assertEqual(assess(before=dict(left), after=dict(right)), baseline)

    def test_post_assessment_caller_mutation_cannot_change_result(self):
        before = {"law": {"epoch": 7}}
        after = {"law": {"epoch": 7}}
        result = assess(before=before, after=after)
        frozen = dict(result)
        before["law"]["epoch"] = 999
        after["extra"] = True
        self.assertEqual(result, frozen)

    def test_contract_identity_changes_binding(self):
        first = assess()
        second = assess(binding=contract(attestation_id="recert-attestation-2"))
        self.assertNotEqual(first["attestation_contract_hash"], second["attestation_contract_hash"])
        self.assertNotEqual(first["binding_hash"], second["binding_hash"])


class RecertAttestationIntegrationTests(unittest.TestCase):
    def test_pointer_safe_failure_is_preserved_with_binding(self):
        result = assess(
            before={"a": {"b": 1}, "a.b": 9},
            after={"a": {"b": 2}, "a.b": 9},
        )
        self.assertEqual(result["status"], "FREEZE")
        self.assertEqual(result["reason"], "PATH_ALIAS_OR_STRICTNESS_DISAGREEMENT")
        self.assertEqual(result["original"]["status"], "CERTIFIED")
        self.assertEqual(result["pointer_safe"]["status"], "FREEZE")
        self.assertRegex(result["binding_hash"], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
