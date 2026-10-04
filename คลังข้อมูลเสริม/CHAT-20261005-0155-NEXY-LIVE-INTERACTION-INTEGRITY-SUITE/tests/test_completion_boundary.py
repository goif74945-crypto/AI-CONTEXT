import unittest

from nexy_live_integrity import CompletionBoundaryGate, GateStatus, StreamChunk

C = "a" * 64


class CompletionBoundaryTests(unittest.TestCase):
    def stream(self, parts=("hello ", "world"), run_id="r1", contract=C):
        payload = "".join(parts)
        digest = CompletionBoundaryGate.payload_sha256(payload)
        return tuple(
            StreamChunk(
                run_id=run_id,
                sequence=i,
                data=part,
                contract_hash=contract,
                final=(i == len(parts) - 1),
                final_payload_sha256=(digest if i == len(parts) - 1 else None),
            )
            for i, part in enumerate(parts)
        )

    def test_complete_stream_passes(self):
        result = CompletionBoundaryGate.verify(self.stream(), expected_run_id="r1", expected_contract_hash=C, expected_chunk_count=2)
        self.assertTrue(result.allowed)
        self.assertEqual(result.code, "COMPLETION_BOUNDARY_VALID")

    def test_missing_final_marker_freezes(self):
        chunks = (
            StreamChunk("r1", 0, "hello", C),
            StreamChunk("r1", 1, " world", C),
        )
        result = CompletionBoundaryGate.verify(chunks, expected_run_id="r1", expected_contract_hash=C)
        self.assertEqual(result.status, GateStatus.FREEZE)
        self.assertIn("missing_final_marker", result.problems)

    def test_sequence_gap_freezes(self):
        digest = CompletionBoundaryGate.payload_sha256("ab")
        chunks = (
            StreamChunk("r1", 0, "a", C),
            StreamChunk("r1", 2, "b", C, True, digest),
        )
        result = CompletionBoundaryGate.verify(chunks, expected_run_id="r1", expected_contract_hash=C)
        self.assertIn("sequence_gap_or_reorder", result.problems)

    def test_final_hash_mismatch_freezes(self):
        chunks = (StreamChunk("r1", 0, "hello", C, True, "b" * 64),)
        result = CompletionBoundaryGate.verify(chunks, expected_run_id="r1", expected_contract_hash=C)
        self.assertIn("final_payload_hash_mismatch", result.problems)

    def test_run_identity_mismatch_freezes(self):
        result = CompletionBoundaryGate.verify(self.stream(run_id="foreign"), expected_run_id="r1", expected_contract_hash=C)
        self.assertTrue(any(p.startswith("run_id_mismatch:") for p in result.problems))

    def test_contract_mismatch_freezes(self):
        result = CompletionBoundaryGate.verify(self.stream(contract="b" * 64), expected_run_id="r1", expected_contract_hash=C)
        self.assertTrue(any(p.startswith("contract_hash_mismatch:") for p in result.problems))

    def test_final_marker_must_be_last(self):
        payload = "ab"
        digest = CompletionBoundaryGate.payload_sha256(payload)
        chunks = (
            StreamChunk("r1", 0, "a", C, True, digest),
            StreamChunk("r1", 1, "b", C),
        )
        result = CompletionBoundaryGate.verify(chunks, expected_run_id="r1", expected_contract_hash=C)
        self.assertIn("final_marker_not_last", result.problems)

    def test_multiple_final_markers_freeze(self):
        digest = CompletionBoundaryGate.payload_sha256("ab")
        chunks = (
            StreamChunk("r1", 0, "a", C, True, digest),
            StreamChunk("r1", 1, "b", C, True, digest),
        )
        result = CompletionBoundaryGate.verify(chunks, expected_run_id="r1", expected_contract_hash=C)
        self.assertIn("multiple_final_markers", result.problems)

    def test_expected_chunk_count_mismatch_freezes(self):
        result = CompletionBoundaryGate.verify(self.stream(), expected_run_id="r1", expected_contract_hash=C, expected_chunk_count=3)
        self.assertIn("chunk_count_mismatch", result.problems)


if __name__ == "__main__":
    unittest.main()
