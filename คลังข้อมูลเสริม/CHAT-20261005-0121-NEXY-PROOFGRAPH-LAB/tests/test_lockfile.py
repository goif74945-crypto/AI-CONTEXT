from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from nexy_proofgraph.lockfile import build_lock, verify_lock


class LockfileTests(unittest.TestCase):
    def test_lock_passes_then_detects_staleness(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "authority.md").write_text("v1", encoding="utf-8")
            lock = build_lock(root, ["authority.md"])
            self.assertTrue(verify_lock(root, lock)["ok"])
            (root / "authority.md").write_text("v2", encoding="utf-8")
            result = verify_lock(root, lock)
            self.assertFalse(result["ok"])
            self.assertEqual(result["changed"][0]["path"], "authority.md")


    def test_lock_is_deterministic_across_input_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("a", encoding="utf-8")
            (root / "b.md").write_text("b", encoding="utf-8")
            self.assertEqual(build_lock(root, ["b.md", "a.md"]), build_lock(root, ["a.md", "b.md"]))

    def test_missing_locked_file_fails_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("a", encoding="utf-8")
            lock = build_lock(root, ["a.md"])
            (root / "a.md").unlink()
            result = verify_lock(root, lock)
            self.assertFalse(result["ok"])
            self.assertEqual(result["missing"], ["a.md"])

    def test_invalid_lock_schema_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = verify_lock(Path(tmp), {"schema": "wrong", "version": 1, "files": []})
            self.assertFalse(result["ok"])
            self.assertTrue(result["invalid_lock"])

    def test_path_escape_is_rejected_when_building(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                build_lock(Path(tmp), ["../outside.md"])


if __name__ == "__main__":
    unittest.main()
