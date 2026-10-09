"""Negative/positive tests for the AI.AI catalog gate (stdlib only)."""
from __future__ import annotations
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from validate_catalog import validate

SOURCE = Path(__file__).resolve().parent.parent

class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory(prefix="ai-ai-catalog-")
        self.root = Path(self.t.name) / "AI.AI"
        shutil.copytree(SOURCE, self.root)
        self.proposal = next((self.root / "PROPOSALS").iterdir())

    def tearDown(self):
        self.t.cleanup()

    def test_valid_catalog(self):
        self.assertEqual(validate(self.root), [])

    def test_hash_tamper(self):
        p = self.proposal / "integration.patch"
        with p.open("a", encoding="utf-8") as f:
            f.write("\n# tampered\n")
        self.assertTrue(any("SHA mismatch" in x for x in validate(self.root)))

    def test_duplicate_fingerprint(self):
        new = self.root / "PROPOSALS" / "AAI-20261009-002-duplicate"
        shutil.copytree(self.proposal, new)
        manifest = new / "manifest.json"
        obj = json.loads(manifest.read_text(encoding="utf-8"))
        obj["id"] = "AAI-20261009-002"
        obj["title"] = "Other name same idea"
        manifest.write_text(json.dumps(obj), encoding="utf-8")
        self.assertTrue(any("duplicate fingerprint" in x for x in validate(self.root)))

    def test_forbidden_folder_even_with_rehashed_patch(self):
        patch = self.proposal / "integration.patch"
        value = patch.read_text(encoding="utf-8").replace(
            "diff --git a/ai_ai/executor.py b/ai_ai/executor.py",
            "diff --git a/โค้ดโปรเจคปัจจุบัน/executor.py b/โค้ดโปรเจคปัจจุบัน/executor.py",
            1)
        patch.write_text(value, encoding="utf-8")
        manifest = self.proposal / "manifest.json"
        obj = json.loads(manifest.read_text(encoding="utf-8"))
        obj["patch_sha256"] = hashlib.sha256(patch.read_bytes()).hexdigest()
        manifest.write_text(json.dumps(obj), encoding="utf-8")
        self.assertTrue(any("unsafe diff" in x for x in validate(self.root)))

if __name__ == "__main__":
    unittest.main()
