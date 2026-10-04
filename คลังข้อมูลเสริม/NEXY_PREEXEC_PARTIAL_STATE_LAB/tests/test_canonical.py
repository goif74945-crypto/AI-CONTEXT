from __future__ import annotations

import unittest

from nexy_pepsa.canonical import CanonicalizationError, canonical_hash, canonical_json


class CanonicalTests(unittest.TestCase):
    def test_object_key_order_does_not_change_output(self) -> None:
        left = {"b": 2, "a": [3, {"y": 2, "x": 1}]}
        right = {"a": [3, {"x": 1, "y": 2}], "b": 2}
        self.assertEqual(canonical_json(left), canonical_json(right))
        self.assertEqual(canonical_hash(left), canonical_hash(right))

    def test_utf8_is_preserved(self) -> None:
        encoded = canonical_json({"name": "คลังข้อมูลเสริม"})
        self.assertIn("คลังข้อมูลเสริม", encoded)

    def test_float_is_rejected(self) -> None:
        with self.assertRaises(CanonicalizationError):
            canonical_json({"value": 0.1})

    def test_non_string_object_key_is_rejected(self) -> None:
        with self.assertRaises(CanonicalizationError):
            canonical_json({1: "bad"})


if __name__ == "__main__":
    unittest.main()
