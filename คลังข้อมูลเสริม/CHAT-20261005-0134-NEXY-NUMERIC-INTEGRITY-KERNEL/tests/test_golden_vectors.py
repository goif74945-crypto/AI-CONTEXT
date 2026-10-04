from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from generate_golden_vectors import build_vectors
from nnik.canonical import canonical_dumps

ROOT = Path(__file__).resolve().parents[1]


class GoldenVectorTests(unittest.TestCase):
    def test_committed_vectors_match_current_engine(self):
        committed = json.loads((ROOT / "GOLDEN_VECTORS.json").read_text(encoding="utf-8"))
        generated = build_vectors()
        self.assertEqual(committed, generated)

    def test_vectors_are_canonicalizable_without_float(self):
        committed = json.loads((ROOT / "GOLDEN_VECTORS.json").read_text(encoding="utf-8"))
        first = canonical_dumps(committed)
        second = canonical_dumps(json.loads(first))
        self.assertEqual(first, second)

    def test_vector_names_unique(self):
        committed = json.loads((ROOT / "GOLDEN_VECTORS.json").read_text(encoding="utf-8"))
        names = [v["name"] for v in committed["evaluation_vectors"] + committed["fixed128_vectors"]]
        self.assertEqual(len(names), len(set(names)))


if __name__ == "__main__":
    unittest.main()
