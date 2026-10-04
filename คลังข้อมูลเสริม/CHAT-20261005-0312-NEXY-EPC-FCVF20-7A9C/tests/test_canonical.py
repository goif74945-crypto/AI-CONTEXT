import unittest

from epc_fcvf.canonical import canonical_hash, canonical_json
from epc_fcvf.engine import initial_state
from epc_fcvf.fixtures import pins


class CanonicalTests(unittest.TestCase):
    def test_dict_order_is_canonical(self):
        self.assertEqual(canonical_json({"b": 2, "a": 1}), canonical_json({"a": 1, "b": 2}))

    def test_float_is_forbidden(self):
        with self.assertRaisesRegex(TypeError, "BINARY_FLOAT_FORBIDDEN"):
            canonical_json({"x": 0.5})

    def test_hash_repeatable(self):
        state = initial_state(chat_id="X", candidate_id="Y", candidate_path="Z", pins=pins())
        self.assertEqual(canonical_hash(state), canonical_hash(state))


if __name__ == "__main__":
    unittest.main()
