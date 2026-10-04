from __future__ import annotations

import unittest

from nexy_proposal_forge.canon import canonical_json, jaccard_basis_points, ngram_units, normalize_text, sha256_fingerprint


class CanonicalizationTests(unittest.TestCase):
    def test_key_order_does_not_change_fingerprint(self) -> None:
        left = {"b": "  beta\nvalue ", "a": ["x", "y"]}
        right = {"a": ["x", "y"], "b": "beta value"}
        self.assertEqual(canonical_json(left), canonical_json(right))
        self.assertEqual(sha256_fingerprint(left), sha256_fingerprint(right))

    def test_list_order_remains_semantic(self) -> None:
        self.assertNotEqual(
            sha256_fingerprint({"items": ["first", "second"]}),
            sha256_fingerprint({"items": ["second", "first"]}),
        )

    def test_float_is_rejected(self) -> None:
        with self.assertRaises(TypeError):
            canonical_json({"score": 0.5})

    def test_unicode_and_whitespace_normalization_is_deterministic(self) -> None:
        self.assertEqual(normalize_text(" ก\n  ข "), "ก ข")
        self.assertEqual(ngram_units("NEXY proposal"), ngram_units("NEXY   proposal"))

    def test_jaccard_basis_points(self) -> None:
        self.assertEqual(jaccard_basis_points(frozenset({"a"}), frozenset({"a"})), 10_000)
        self.assertEqual(jaccard_basis_points(frozenset({"a"}), frozenset({"b"})), 0)

    def test_normalized_key_collision_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            canonical_json({" key ": 1, "key": 2})


if __name__ == "__main__":
    unittest.main()
