import unittest

from frontierfive.safe_adapter import FieldSpec, apply_adapter, compile_adapter


class SafeAdapterTests(unittest.TestCase):
    def test_exact_and_lossless_integer_to_number(self):
        src = {"id": FieldSpec("id", "string"), "count": FieldSpec("count", "integer")}
        dst = {"id": FieldSpec("id", "string"), "count": FieldSpec("count", "number")}
        v = compile_adapter(src, dst)
        self.assertEqual(v.status, "ALLOW")
        out = apply_adapter({"id": "x", "count": 3}, v.payload["adapter"])
        self.assertEqual(out, {"count": 3, "id": "x"})

    def test_explicit_alias_can_migrate_noncritical_field(self):
        src = {"old": FieldSpec("old", "string")}
        dst = {"new": FieldSpec("new", "string", aliases=("old",))}
        v = compile_adapter(src, dst)
        self.assertEqual(v.status, "ALLOW")
        self.assertEqual(apply_adapter({"old": "v"}, v.payload["adapter"]), {"new": "v"})

    def test_missing_required_freezes(self):
        v = compile_adapter({}, {"x": FieldSpec("x", "string")})
        self.assertIn("MISSING_REQUIRED:x", v.reasons)

    def test_ambiguous_alias_freezes(self):
        src = {"a": FieldSpec("a", "string"), "b": FieldSpec("b", "string")}
        dst = {"x": FieldSpec("x", "string", aliases=("a", "b"))}
        self.assertIn("AMBIGUOUS_MAPPING:x", compile_adapter(src, dst).reasons)

    def test_critical_field_cannot_rename_or_widen(self):
        src = {"old": FieldSpec("old", "integer")}
        dst = {"id": FieldSpec("id", "number", aliases=("old",), critical=True)}
        self.assertIn("CRITICAL_FIELD_DRIFT:id", compile_adapter(src, dst).reasons)

    def test_incompatible_type_freezes(self):
        src = {"x": FieldSpec("x", "string")}
        dst = {"x": FieldSpec("x", "integer")}
        self.assertIn("UNSAFE_TYPE:x->x", compile_adapter(src, dst).reasons)
