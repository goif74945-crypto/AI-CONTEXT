from __future__ import annotations

import copy
import math
import unittest

from nexy_outcome.canonical import canonical_json, content_hash
from nexy_outcome.compiler import compile_contract
from nexy_outcome.errors import ContractValidationError

from common import contract_spec


class CompilerTests(unittest.TestCase):
    def test_compile_is_deterministic_and_sorted(self) -> None:
        spec = contract_spec()
        contract1, digest1 = compile_contract(spec)
        shuffled = copy.deepcopy(spec)
        shuffled["criteria"] = list(reversed(shuffled["criteria"]))
        contract2, digest2 = compile_contract(shuffled)
        self.assertEqual(contract1.to_dict(), contract2.to_dict())
        self.assertEqual(digest1, digest2)
        self.assertEqual(digest1, content_hash(contract1.to_dict()))

    def test_unknown_top_field_rejected(self) -> None:
        spec = contract_spec()
        spec["silent_fallback"] = True
        with self.assertRaises(ContractValidationError):
            compile_contract(spec)

    def test_duplicate_criterion_rejected(self) -> None:
        spec = contract_spec()
        spec["criteria"].append(copy.deepcopy(spec["criteria"][0]))
        with self.assertRaisesRegex(ContractValidationError, "duplicate criterion"):
            compile_contract(spec)

    def test_nonfinite_rejected(self) -> None:
        spec = contract_spec()
        spec["criteria"][1]["value"] = math.inf
        with self.assertRaises(ContractValidationError):
            compile_contract(spec)

    def test_hard_weight_must_be_zero(self) -> None:
        spec = contract_spec()
        spec["criteria"][0]["weight"] = 1
        with self.assertRaises(ContractValidationError):
            compile_contract(spec)

    def test_canonical_json_rejects_nan_nested(self) -> None:
        with self.assertRaises(ContractValidationError):
            canonical_json({"a": [float("nan")]})


if __name__ == "__main__":
    unittest.main()
