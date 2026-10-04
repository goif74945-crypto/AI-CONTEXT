import unittest

from lo4q64.q64 import MAX_RAW, MIN_RAW, ONE, Q64, Q64DomainError, Q64OverflowError, ratio01, weighted_mean


class Q64Tests(unittest.TestCase):
    def test_exact_integer_roundtrip(self):
        for value in (-1_000_000, -1, 0, 1, 1_000_000):
            self.assertEqual(Q64.from_int(value).raw, value << 64)

    def test_ratio_is_integer_only_and_deterministic(self):
        one_third = Q64.from_ratio(1, 3)
        self.assertEqual(one_third.raw, ((1 << 64) // 3))
        self.assertEqual(one_third, Q64.from_ratio(1, 3))

    def test_mul_div(self):
        # Exact dyadic products stay exact.
        self.assertEqual((Q64.from_ratio(1, 2) * Q64.from_ratio(1, 2)).raw, Q64.from_ratio(1, 4).raw)
        # Non-dyadic inputs are truncated at construction, so composed error is bounded in raw ULPs.
        a = Q64.from_ratio(3, 4)
        b = Q64.from_ratio(2, 3)
        self.assertLessEqual(abs((a * b).raw - Q64.from_ratio(1, 2).raw), 1)
        self.assertEqual((a / Q64.from_ratio(3, 2)).raw, Q64.from_ratio(1, 2).raw)

    def test_float_inputs_are_rejected(self):
        with self.assertRaises(TypeError):
            Q64.from_int(1.0)
        with self.assertRaises(TypeError):
            Q64.from_ratio(1, 2.0)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            _ = ONE / Q64.zero()

    def test_overflow_guards(self):
        with self.assertRaises(Q64OverflowError):
            Q64(MAX_RAW) + Q64(1)
        with self.assertRaises(Q64OverflowError):
            Q64(MIN_RAW) - Q64(1)

    def test_unit_domain(self):
        with self.assertRaises(Q64DomainError):
            Q64.from_int(2).complement01()

    def test_ratio01_zero_zero(self):
        self.assertEqual(ratio01(Q64.zero(), Q64.zero()), Q64.zero())

    def test_weighted_mean(self):
        x = weighted_mean(((Q64.from_ratio(1, 4), 1), (Q64.from_ratio(3, 4), 1)))
        self.assertEqual(x, Q64.from_ratio(1, 2))


if __name__ == "__main__":
    unittest.main()
