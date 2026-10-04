from __future__ import annotations
import json,unittest
from pathlib import Path
from compile_json import compile_mapping

class Conformance(unittest.TestCase):
    def test_locked_vectors(self):
        data=json.loads((Path(__file__).parent/"conformance"/"cases.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema"],"proof-capsule-conformance/v1-proposal")
        self.assertEqual(len(data["cases"]),6)
        for case in data["cases"]:
            with self.subTest(case=case["name"]):
                self.assertEqual(compile_mapping(case["input"]),case["expected"])

if __name__=="__main__": unittest.main(verbosity=2)
