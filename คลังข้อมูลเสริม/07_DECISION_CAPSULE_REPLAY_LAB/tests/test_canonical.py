from __future__ import annotations

import math
import unittest

from nexy_dcr.canonical import canonical_json, sha256_hex
from nexy_dcr.errors import CanonicalizationError
from nexy_dcr.model import AuthorityRef, authority_fingerprint


class CanonicalTests(unittest.TestCase):
    def test_mapping_order_does_not_change_digest(self) -> None:
        self.assertEqual(sha256_hex({"b": 2, "a": 1}), sha256_hex({"a": 1, "b": 2}))

    def test_list_order_changes_digest(self) -> None:
        self.assertNotEqual(sha256_hex([1, 2]), sha256_hex([2, 1]))

    def test_unicode_is_preserved(self) -> None:
        rendered = canonical_json({"ภาษา": "ไทย"})
        self.assertIn("ไทย", rendered)

    def test_nan_is_rejected(self) -> None:
        with self.assertRaises(CanonicalizationError):
            canonical_json({"bad": math.nan})

    def test_non_string_mapping_key_is_rejected(self) -> None:
        with self.assertRaises(CanonicalizationError):
            canonical_json({1: "nope"})

    def test_authority_order_is_normalized(self) -> None:
        a = AuthorityRef(path="a", sha="a" * 64, role="A", rank=1)
        b = AuthorityRef(path="b", sha="b" * 64, role="B", rank=2)
        self.assertEqual(authority_fingerprint([a, b]), authority_fingerprint([b, a]))


if __name__ == "__main__":
    unittest.main()
