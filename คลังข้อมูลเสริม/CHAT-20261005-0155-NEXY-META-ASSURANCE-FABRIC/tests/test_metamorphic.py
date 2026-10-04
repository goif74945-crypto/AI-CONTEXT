import unittest

from nexy_meta_assurance.metamorphic import (
    MetamorphicRelation,
    RelationDefinitionError,
    verify_relation,
)


class MetamorphicTests(unittest.TestCase):
    def test_identity_relation_passes(self):
        result = verify_relation(lambda x: x * x, 7, MetamorphicRelation("identity", "identity", "equal"))
        self.assertTrue(result.passed)
        self.assertEqual(result.base_output, 49)

    def test_shift_relation_passes_for_affine_subject(self):
        result = verify_relation(
            lambda x: 3 * x + 2,
            10,
            MetamorphicRelation(
                "affine shift",
                "shift_int",
                "delta_int",
                transform_arg=4,
                expectation_arg=12,
            ),
        )
        self.assertTrue(result.passed)

    def test_wrong_relation_is_reported_not_hidden(self):
        result = verify_relation(
            lambda x: x * x,
            3,
            MetamorphicRelation("false linearity", "scale_int", "scale_int", transform_arg=2, expectation_arg=2),
        )
        self.assertFalse(result.passed)

    def test_unknown_transform_fails_closed(self):
        with self.assertRaises(RelationDefinitionError):
            verify_relation(lambda x: x, 1, MetamorphicRelation("bad", "teleport", "equal"))

    def test_same_multiset_relation_for_sorting_subject(self):
        result = verify_relation(
            lambda xs: sorted(xs),
            [3, 1, 2],
            MetamorphicRelation("reverse input preserves sorted multiset", "reverse_sequence", "same_multiset"),
        )
        self.assertTrue(result.passed)


if __name__ == "__main__":
    unittest.main()
