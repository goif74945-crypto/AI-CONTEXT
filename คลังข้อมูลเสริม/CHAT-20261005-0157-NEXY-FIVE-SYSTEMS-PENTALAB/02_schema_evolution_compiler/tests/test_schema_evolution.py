import itertools
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from schema_evolution import ContractSchema, FieldSpec, SchemaInputError, compile_evolution


class SchemaEvolutionTests(unittest.TestCase):
    def test_optional_addition_is_minor(self):
        old = ContractSchema("1.0.0", (FieldSpec("id", "string", True),))
        new = ContractSchema("1.1.0", (FieldSpec("id", "string", True), FieldSpec("note", "string")))
        r = compile_evolution(old, new)
        self.assertEqual(r.classification, "ADDITIVE_COMPATIBLE")
        self.assertEqual(r.recommended_semver_bump, "MINOR")

    def test_required_addition_breaks_without_default(self):
        old = ContractSchema("1", (FieldSpec("id", "string", True),))
        new = ContractSchema("2", (FieldSpec("id", "string", True), FieldSpec("tenant", "string", True)))
        r = compile_evolution(old, new)
        self.assertEqual(r.classification, "BREAKING")
        self.assertIn("REQUIRED_ADDITION", r.reason_codes)

    def test_required_addition_with_default_requires_migration(self):
        old = ContractSchema("1", (FieldSpec("id", "string", True),))
        new = ContractSchema("2", (FieldSpec("id", "string", True), FieldSpec("tenant", "string", True, has_default=True)))
        r = compile_evolution(old, new)
        self.assertEqual(r.classification, "MIGRATION_REQUIRED")
        self.assertTrue(any("BACKFILL" in step for step in r.migration_steps))

    def test_enum_narrowing_is_breaking(self):
        old = ContractSchema("1", (FieldSpec("state", "string", True, ("A", "B", "C")),))
        new = ContractSchema("2", (FieldSpec("state", "string", True, ("A", "B")),))
        r = compile_evolution(old, new)
        self.assertEqual(r.classification, "BREAKING")
        self.assertIn("ENUM_NARROWING", r.reason_codes)

    def test_integer_to_number_is_widening(self):
        old = ContractSchema("1", (FieldSpec("count", "integer", True),))
        new = ContractSchema("1.1", (FieldSpec("count", "number", True),))
        self.assertEqual(compile_evolution(old, new).classification, "ADDITIVE_COMPATIBLE")

    def test_explicit_rename_is_migration_not_guess(self):
        old = ContractSchema("1", (FieldSpec("name", "string", True),))
        new = ContractSchema("2", (FieldSpec("display_name", "string", True),))
        self.assertEqual(compile_evolution(old, new).classification, "BREAKING")
        r = compile_evolution(old, new, explicit_renames={"name": "display_name"})
        self.assertEqual(r.classification, "MIGRATION_REQUIRED")
        self.assertIn("EXPLICIT_RENAME_REQUIRES_MIGRATION", r.reason_codes)

    def test_field_order_is_canonical(self):
        fields = [FieldSpec("a", "string"), FieldSpec("b", "integer")]
        fps = set()
        for p in itertools.permutations(fields):
            fps.add(compile_evolution(
                ContractSchema("1", tuple(p)),
                ContractSchema("1.1", tuple(p) + (FieldSpec("c", "string"),)),
            ).fingerprint)
        self.assertEqual(len(fps), 1)

    def test_rename_cannot_collapse_two_old_fields_into_one_target(self):
        old = ContractSchema("1", (FieldSpec("a", "string"), FieldSpec("b", "string")))
        new = ContractSchema("2", (FieldSpec("b", "string"),))
        with self.assertRaises(SchemaInputError):
            compile_evolution(old, new, explicit_renames={"a": "b"})

    def test_duplicate_field_rejected(self):
        with self.assertRaises(SchemaInputError):
            compile_evolution(
                ContractSchema("1", (FieldSpec("a", "string"), FieldSpec("a", "string"))),
                ContractSchema("2", (FieldSpec("a", "string"),)),
            )


if __name__ == "__main__":
    unittest.main()
