import unittest

from lo4lab.terminology import TermDefinition, TerminologyError, TerminologyRegistry


class TestTerminology(unittest.TestCase):
    def registry(self):
        return TerminologyRegistry([
            TermDefinition("matrix", "NEXY", "source-normalized requirement matrix", ("build-matrix",)),
            TermDefinition("matrix", "NEXY/runtime", "runtime transition matrix", ("state-matrix",)),
            TermDefinition("canon", "NEXY", "authoritative promoted project law"),
        ])

    def test_most_specific_scope_wins(self):
        result = self.registry().resolve("matrix", "NEXY/runtime/core")
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.definition, "runtime transition matrix")

    def test_parent_scope_used_when_no_override(self):
        result = self.registry().resolve("matrix", "NEXY/docs")
        self.assertEqual(result.definition, "source-normalized requirement matrix")

    def test_alias_resolves_with_scope(self):
        result = self.registry().resolve("state-matrix", "NEXY/runtime")
        self.assertEqual(result.canonical_term, "matrix")
        self.assertEqual(result.scope, "NEXY/runtime")

    def test_unknown_term_remains_unknown(self):
        self.assertEqual(self.registry().resolve("mystery", "NEXY").status, "UNKNOWN")

    def test_conflicting_exact_definition_rejected(self):
        with self.assertRaises(TerminologyError):
            TerminologyRegistry([
                TermDefinition("x", "a", "one"),
                TermDefinition("x", "a", "two"),
            ])

    def test_alias_collision_with_canonical_rejected(self):
        with self.assertRaises(TerminologyError):
            TerminologyRegistry([
                TermDefinition("a", "scope", "A", ("b",)),
                TermDefinition("b", "scope", "B"),
            ])

    def test_same_alias_to_two_terms_rejected(self):
        with self.assertRaises(TerminologyError):
            TerminologyRegistry([
                TermDefinition("a", "scope", "A", ("x",)),
                TermDefinition("b", "scope", "B", ("x",)),
            ])


if __name__ == "__main__":
    unittest.main()
