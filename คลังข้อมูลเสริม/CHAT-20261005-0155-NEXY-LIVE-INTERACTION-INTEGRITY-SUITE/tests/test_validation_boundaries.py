import unittest

from nexy_live_integrity import (
    CompletionBoundaryGate,
    InputRequirement,
    IntentContract,
    IntentEquivalenceGate,
    StreamChunk,
    canonical_json,
)

H = "a" * 64


class ValidationBoundaryTests(unittest.TestCase):
    def base_intent(self, **overrides):
        data = dict(
            modality="text",
            objective="  Build   exact artifact  ",
            operation="build",
            targets=("artifact:1",),
            mode="STRICT",
            allow_external=False,
            deterministic_required=True,
            authority_scope="project:p",
        )
        data.update(overrides)
        return IntentContract(**data)

    def test_canonical_json_rejects_unsupported_float(self):
        with self.assertRaises(TypeError):
            canonical_json({"x": 1.25})

    def test_stream_sequence_rejects_bool(self):
        with self.assertRaises(ValueError):
            StreamChunk("r", True, "x", H)

    def test_stream_data_must_be_text(self):
        with self.assertRaises(TypeError):
            StreamChunk("r", 0, b"x", H)  # type: ignore[arg-type]

    def test_stream_final_must_be_boolean(self):
        with self.assertRaises(TypeError):
            StreamChunk("r", 0, "x", H, final=1)  # type: ignore[arg-type]

    def test_expected_chunk_count_rejects_bool_and_zero(self):
        chunk = StreamChunk("r", 0, "x", H, True, CompletionBoundaryGate.payload_sha256("x"))
        for invalid in (True, 0, -1):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                CompletionBoundaryGate.verify((chunk,), expected_run_id="r", expected_contract_hash=H, expected_chunk_count=invalid)  # type: ignore[arg-type]

    def test_empty_stream_freezes(self):
        result = CompletionBoundaryGate.verify((), expected_run_id="r", expected_contract_hash=H)
        self.assertEqual(result.code, "COMPLETION_EMPTY_STREAM")

    def test_nonfinal_chunk_cannot_carry_payload_hash(self):
        chunk = StreamChunk("r", 0, "x", H, False, CompletionBoundaryGate.payload_sha256("x"))
        result = CompletionBoundaryGate.verify((chunk,), expected_run_id="r", expected_contract_hash=H)
        self.assertIn("premature_payload_hash:0", result.problems)

    def test_final_chunk_requires_payload_hash(self):
        result = CompletionBoundaryGate.verify((StreamChunk("r", 0, "x", H, True),), expected_run_id="r", expected_contract_hash=H)
        self.assertIn("missing_final_payload_hash", result.problems)

    def test_intent_boolean_fields_are_strict(self):
        with self.assertRaises(TypeError):
            self.base_intent(allow_external=1)
        with self.assertRaises(TypeError):
            self.base_intent(deterministic_required="yes")

    def test_intent_duplicate_constraint_key_rejected(self):
        with self.assertRaises(ValueError):
            self.base_intent(constraints=(("x", "1"), ("x", "2")))

    def test_intent_normalization_is_explicit(self):
        contract = self.base_intent()
        self.assertEqual(contract.objective, "Build exact artifact")
        self.assertEqual(contract.operation, "BUILD")
        self.assertEqual(contract.mode, "strict")
        self.assertEqual(len(contract.semantic_fingerprint), 64)

    def test_no_intent_contracts_reject(self):
        result = IntentEquivalenceGate.compare([])
        self.assertEqual(result.code, "INTENT_NO_CONTRACTS")

    def test_required_modality_must_be_nonempty(self):
        with self.assertRaises(ValueError):
            IntentEquivalenceGate.compare([self.base_intent()], required_modalities=(" ",))

    def test_input_required_flag_is_strict_boolean(self):
        with self.assertRaises(TypeError):
            InputRequirement("f", "file", required=1)  # type: ignore[arg-type]

    def test_input_allowed_trust_must_be_unique_and_nonempty(self):
        with self.assertRaises(ValueError):
            InputRequirement("f", "file", allowed_trust=())
        with self.assertRaises(ValueError):
            InputRequirement("f", "file", allowed_trust=("user", "user"))


if __name__ == "__main__":
    unittest.main()
