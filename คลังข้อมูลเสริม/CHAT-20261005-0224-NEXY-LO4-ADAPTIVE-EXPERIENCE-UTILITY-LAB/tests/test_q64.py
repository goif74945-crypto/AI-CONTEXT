import unittest

from aeul.q64 import Q64, Q64DivisionByZero, Q64Error, Q64Overflow, RAW_MIN, RAW_MAX, SCALE


class Q64Tests(unittest.TestCase):
    def test_integer_roundtrip(self):
        for n in (-7, -1, 0, 1, 7, (1 << 20)):
            self.assertEqual(Q64.from_int(n).raw, n * SCALE)

    def test_decimal_exact_binary_fractions(self):
        self.assertEqual(str(Q64.from_decimal("0.5")), "0.5")
        self.assertEqual(str(Q64.from_decimal("-1.25")), "-1.25")
        self.assertEqual(str(Q64.from_decimal("2")), "2")

    def test_invalid_decimal_rejected(self):
        for text in ("", " 1", "1 ", ".5", "01", "1e-3", "nan", "inf"):
            with self.subTest(text=text), self.assertRaises(Q64Error):
                Q64.from_decimal(text)

    def test_half_even_rounding_from_ratio(self):
        self.assertEqual(Q64.from_ratio(1, 2 * SCALE).raw, 0)
        self.assertEqual(Q64.from_ratio(3, 2 * SCALE).raw, 2)
        self.assertEqual(Q64.from_ratio(-1, 2 * SCALE).raw, 0)
        self.assertEqual(Q64.from_ratio(-3, 2 * SCALE).raw, -2)

    def test_multiplication(self):
        a = Q64.from_decimal("1.5")
        b = Q64.from_decimal("0.25")
        self.assertEqual(a * b, Q64.from_decimal("0.375"))

    def test_division(self):
        self.assertEqual(Q64.from_decimal("0.75") / Q64.from_decimal("0.25"), Q64.from_int(3))
        with self.assertRaises(Q64DivisionByZero):
            _ = Q64.one() / Q64.zero()

    def test_signed_128_boundaries(self):
        self.assertEqual(Q64(RAW_MIN).raw, RAW_MIN)
        self.assertEqual(Q64(RAW_MAX).raw, RAW_MAX)
        self.assertEqual(Q64.from_int(-(1 << 63)).raw, RAW_MIN)
        with self.assertRaises(Q64Overflow):
            Q64.from_int(1 << 63)
        with self.assertRaises(Q64Overflow):
            _ = -Q64(RAW_MIN)

    def test_add_overflow(self):
        with self.assertRaises(Q64Overflow):
            _ = Q64(RAW_MAX) + Q64(1)

    def test_clamp(self):
        self.assertEqual(Q64.from_int(3).clamp(Q64.from_int(0), Q64.from_int(2)), Q64.from_int(2))
        with self.assertRaises(Q64Error):
            Q64.zero().clamp(Q64.one(), Q64.zero())

    def test_no_binary_float_constructor(self):
        with self.assertRaises(TypeError):
            Q64.from_int(1.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            Q64.from_ratio(1, 2.0)  # type: ignore[arg-type]
