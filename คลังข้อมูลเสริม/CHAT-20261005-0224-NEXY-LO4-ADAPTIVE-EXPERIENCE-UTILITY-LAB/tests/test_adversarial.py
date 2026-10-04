import ast
from fractions import Fraction
from pathlib import Path
import random
import unittest

from aeul.q64 import Q64, Q64Overflow, RAW_MAX, SCALE


class AdversarialTests(unittest.TestCase):
    def test_decision_modules_have_no_float_literals_or_float_calls(self):
        root = Path(__file__).parents[1] / "aeul"
        for path in root.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, float):
                    self.fail(f"binary float literal in {path.name}:{node.lineno}")
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "float":
                    self.fail(f"float() call in {path.name}:{node.lineno}")

    def test_random_q64_add_sub_roundtrip(self):
        rng = random.Random(202610050224)
        for _ in range(5000):
            a = Q64(rng.randrange(-(1 << 100), 1 << 100))
            b = Q64(rng.randrange(-(1 << 100), 1 << 100))
            self.assertEqual((a + b) - b, a)

    def test_random_mul_matches_fraction_half_even(self):
        rng = random.Random(224)
        for _ in range(10000):
            a = Q64(rng.randrange(-(1 << 90), 1 << 90))
            b = Q64(rng.randrange(-(1 << 30), 1 << 30))
            expected = round(Fraction(a.raw * b.raw, SCALE))
            self.assertEqual((a * b).raw, expected)

    def test_random_div_matches_fraction_half_even(self):
        rng = random.Random(225)
        for _ in range(10000):
            a = Q64(rng.randrange(-(1 << 80), 1 << 80))
            b_raw = 0
            while b_raw == 0:
                b_raw = rng.randrange(-(1 << 40), 1 << 40)
            b = Q64(b_raw)
            expected = round(Fraction(a.raw * SCALE, b.raw))
            if -(1 << 127) <= expected <= (1 << 127) - 1:
                self.assertEqual((a / b).raw, expected)

    def test_near_overflow_is_fail_closed(self):
        with self.assertRaises(Q64Overflow):
            _ = Q64(RAW_MAX) + Q64.one()
