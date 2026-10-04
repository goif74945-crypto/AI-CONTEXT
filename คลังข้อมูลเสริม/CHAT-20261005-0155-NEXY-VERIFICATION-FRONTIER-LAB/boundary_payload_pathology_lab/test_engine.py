import unittest

from boundary_payload_pathology_lab.engine import (
    BoundaryPayloadError,
    Limits,
    canonical_json,
    strict_loads,
)


class BoundaryPayloadPathologyLabTests(unittest.TestCase):
    def test_rejects_duplicate_raw_keys(self):
        with self.assertRaisesRegex(BoundaryPayloadError, "duplicate"):
            strict_loads('{"a":1,"a":2}')

    def test_rejects_unicode_normalization_key_collision(self):
        with self.assertRaisesRegex(BoundaryPayloadError, "normalization"):
            strict_loads('{"é":1,"e\\u0301":2}')

    def test_rejects_non_finite_json_extensions(self):
        with self.assertRaisesRegex(BoundaryPayloadError, "non-finite"):
            strict_loads('{"x":NaN}')

    def test_rejects_excessive_depth_and_numeric_magnitude(self):
        with self.assertRaisesRegex(BoundaryPayloadError, "max_depth"):
            strict_loads('{"a":{"b":{"c":1}}}', limits=Limits(max_depth=2))
        with self.assertRaisesRegex(BoundaryPayloadError, "numeric magnitude"):
            strict_loads('{"x":1001}', limits=Limits(max_abs_number=1000))

    def test_canonicalization_is_order_stable(self):
        a = strict_loads('{"b":2,"a":1}')
        b = strict_loads('{"a":1,"b":2}')
        self.assertEqual(canonical_json(a), '{"a":1,"b":2}')
        self.assertEqual(canonical_json(a), canonical_json(b))


if __name__ == "__main__":
    unittest.main()
