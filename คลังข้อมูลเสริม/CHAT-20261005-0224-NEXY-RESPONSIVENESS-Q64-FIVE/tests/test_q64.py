import unittest
from fractions import Fraction
from nexy_responsiveness.q64 import MAX_RAW,MIN_RAW,Q64,SCALE,q
class Q64Tests(unittest.TestCase):
    def test_integer_roundtrip(self): self.assertEqual(Q64.from_int(7).raw,7*SCALE)
    def test_decimal(self): self.assertEqual(q("0.5").raw,SCALE//2)
    def test_mul_div(self): self.assertEqual((q("3")/q("2")).to_fraction(),Fraction(3,2))
    def test_bounds(self):
        Q64.from_raw(MIN_RAW);Q64.from_raw(MAX_RAW)
        with self.assertRaises(OverflowError):Q64.from_raw(MAX_RAW+1)
    def test_div_zero(self):
        with self.assertRaises(ZeroDivisionError): _=Q64.one()/Q64.zero()
