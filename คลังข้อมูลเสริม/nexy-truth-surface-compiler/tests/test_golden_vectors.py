from __future__ import annotations

import json
import unittest
from pathlib import Path

from nxts import compile_payload


class GoldenVectorTests(unittest.TestCase):
    def test_golden_vectors_match_current_compiler(self):
        root = Path(__file__).resolve().parents[1]
        vectors = json.loads((root / "fixtures" / "golden-vectors.json").read_text(encoding="utf-8"))
        self.assertEqual(vectors["schema"], "nxts.golden-vectors.v0")
        for vector in vectors["vectors"]:
            with self.subTest(fixture=vector["fixture"]):
                payload = json.loads((root / "fixtures" / vector["fixture"]).read_text(encoding="utf-8"))
                result = compile_payload(payload)
                self.assertEqual(result["receipt"]["input_sha256"], vector["input_sha256"])
                self.assertEqual(result["receipt"]["output_sha256"], vector["output_sha256"])
                self.assertEqual(result["decision"], vector["decision"])
                self.assertEqual([x["code"] for x in result["freeze_reasons"]], vector["freeze_codes"])
                self.assertEqual(result, vector["canonical_output"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
