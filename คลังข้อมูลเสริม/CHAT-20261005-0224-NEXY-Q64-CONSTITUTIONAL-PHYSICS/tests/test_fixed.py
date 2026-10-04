import unittest

from qcp.fixed import Q64, Q64Overflow, Q64DomainError


class Q64Tests(unittest.TestCase):
    def test_exact_integer_and_decimal_parse(self):
        self.assertEqual(Q64.from_int(3).to_decimal(6), "3.000000")
        self.assertEqual(Q64.from_decimal("0.5").raw, 1 << 63)
        self.assertEqual(Q64.from_decimal("-1.25").to_decimal(4), "-1.2500")

    def test_float_is_forbidden(self):
        with self.assertRaises(TypeError):
            Q64.from_value(0.5)

    def test_add_sub_mul_div(self):
        a = Q64.from_decimal("1.5")
        b = Q64.from_decimal("0.25")
        self.assertEqual((a + b).to_decimal(4), "1.7500")
        self.assertEqual((a - b).to_decimal(4), "1.2500")
        self.assertEqual((a * b).to_decimal(4), "0.3750")
        self.assertEqual((a / b).to_decimal(4), "6.0000")

    def test_divide_by_zero_rejected(self):
        with self.assertRaises(Q64DomainError):
            Q64.one() / Q64.zero()

    def test_overflow_is_fail_closed(self):
        with self.assertRaises(Q64Overflow):
            Q64.from_raw((1 << 127) - 1) + Q64.one()

    def test_ratio_rounding_is_deterministic(self):
        a = Q64.from_ratio(1, 3)
        b = Q64.from_ratio(2, 6)
        self.assertEqual(a, b)
        self.assertEqual((a * Q64.from_int(3)).to_decimal(18), "1.000000000000000000")


if __name__ == "__main__":
    unittest.main()

class Q64AdversarialTests(unittest.TestCase):
    def test_minimum_negation_overflow_is_rejected(self):
        with self.assertRaises(Q64Overflow):
            -Q64.from_raw(Q64.RAW_MIN)

    def test_malformed_decimal_is_rejected(self):
        for bad in ("nan", "inf", "1e3", "", ".5", "--1"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    Q64.from_decimal(bad)

    def test_boolean_is_not_accepted_as_integer(self):
        with self.assertRaises(TypeError):
            Q64.from_value(True)
