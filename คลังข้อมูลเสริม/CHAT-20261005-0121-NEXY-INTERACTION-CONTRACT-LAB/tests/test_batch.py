from __future__ import annotations

import copy
import unittest

from interaction_contract.batch import analyze_batch
from interaction_contract.canonical import canonical_sha256
from interaction_contract.model import ValidationError
from test_analyzer import base_contract


class BatchTests(unittest.TestCase):
    def test_batch_aggregates_pass_and_block(self) -> None:
        good = base_contract()
        bad = copy.deepcopy(good)
        bad["contract_id"] = "demo-002"
        bad["events"] = [bad["events"][0]]
        report = analyze_batch([good, bad])
        self.assertEqual(report["contracts"], 2)
        self.assertEqual(report["pass_count"], 1)
        self.assertEqual(report["block_count"], 1)
        self.assertLess(report["mean_retention_score"], 100)

    def test_empty_batch_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            analyze_batch([])

    def test_canonical_hash_ignores_dict_key_order(self) -> None:
        self.assertEqual(canonical_sha256({"a": 1, "b": 2}), canonical_sha256({"b": 2, "a": 1}))

    def test_batch_is_deterministic(self) -> None:
        raw = [base_contract()]
        self.assertEqual(analyze_batch(raw), analyze_batch(raw))


if __name__ == "__main__":
    unittest.main()
