from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
import unittest

from nnik.fixed128 import I128_MAX, I128_MIN, project_exact, project_fraction_to_i128, restore_i128

ROOT = Path(__file__).resolve().parents[1]


class Fixed128ProjectionTests(unittest.TestCase):
    def test_doc_c_confidence_threshold_exact_at_centiscale(self):
        projection = project_exact("0.85", "0.01")
        self.assertEqual(projection["integer"], 85)
        self.assertEqual(projection["exact_value"], "17/20")

    def test_deterministic_match_threshold_exact_at_centiscale(self):
        projection = project_exact("0.90", "0.01")
        self.assertEqual(projection["integer"], 90)
        self.assertEqual(projection["exact_value"], "9/10")

    def test_nonrepresentable_value_freezes(self):
        with self.assertRaisesRegex(Exception, "NOT_EXACTLY_REPRESENTABLE_FIXED128"):
            project_exact("1/3", "0.01")

    def test_positive_overflow_freezes(self):
        with self.assertRaisesRegex(Exception, "FIXED128_OVERFLOW"):
            project_fraction_to_i128(Fraction(I128_MAX + 1), Fraction(1))

    def test_negative_overflow_freezes(self):
        with self.assertRaisesRegex(Exception, "FIXED128_OVERFLOW"):
            project_fraction_to_i128(Fraction(I128_MIN - 1), Fraction(1))

    def test_boundaries_round_trip(self):
        q = Fraction(1, 1000)
        for integer in (I128_MIN, -1, 0, 1, I128_MAX):
            value = restore_i128(integer, q)
            self.assertEqual(project_fraction_to_i128(value, q), integer)

    def test_cli_projection_accept(self):
        proc = subprocess.run(
            [sys.executable, "-m", "nnik.cli", "project-fixed128", "--value", "0.85", "--quantum", "0.01"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["verdict"], "ACCEPT")
        self.assertEqual(data["projection"]["integer"], 85)

    def test_cli_projection_freeze_is_domain_result(self):
        proc = subprocess.run(
            [sys.executable, "-m", "nnik.cli", "project-fixed128", "--value", "1/3", "--quantum", "0.01"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertEqual(data["verdict"], "FREEZE")
        self.assertEqual(data["reason_code"], "NOT_EXACTLY_REPRESENTABLE_FIXED128")


if __name__ == "__main__":
    unittest.main()
