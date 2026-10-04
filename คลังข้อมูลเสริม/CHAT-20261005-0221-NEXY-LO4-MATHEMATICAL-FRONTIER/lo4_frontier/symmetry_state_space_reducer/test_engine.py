import unittest
from lo4_frontier.symmetry_state_space_reducer.engine import canonical_partition_key

class SymmetryTests(unittest.TestCase):
    def test_swapped_equivalent_entities_collapse(self):
        s1 = {"agent-a":{"class":"worker","state":{"queue":2}},"agent-b":{"class":"worker","state":{"queue":0}}}
        s2 = {"agent-x":{"class":"worker","state":{"queue":0}},"agent-y":{"class":"worker","state":{"queue":2}}}
        self.assertEqual(canonical_partition_key(s1), canonical_partition_key(s2))

    def test_non_equivalent_state_does_not_collapse(self):
        a = {"a":{"class":"worker","state":{"queue":1}}}
        b = {"a":{"class":"worker","state":{"queue":2}}}
        self.assertNotEqual(canonical_partition_key(a), canonical_partition_key(b))

    def test_class_boundary_is_preserved(self):
        a = {"a":{"class":"worker","state":{"queue":1}}}
        b = {"a":{"class":"judge","state":{"queue":1}}}
        self.assertNotEqual(canonical_partition_key(a), canonical_partition_key(b))
