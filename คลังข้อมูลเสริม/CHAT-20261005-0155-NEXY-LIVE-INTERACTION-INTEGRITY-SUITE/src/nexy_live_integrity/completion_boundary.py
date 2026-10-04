from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Sequence

from .common import GateStatus, canonical_digest, require_digest, require_nonempty


@dataclass(frozen=True, slots=True)
class StreamChunk:
    run_id: str
    sequence: int
    data: str
    contract_hash: str
    final: bool = False
    final_payload_sha256: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "run_id", require_nonempty("run_id", self.run_id))
        if type(self.sequence) is not int or self.sequence < 0:
            raise ValueError("sequence must be a non-negative integer")
        if not isinstance(self.data, str):
            raise TypeError("data must be text")
        if type(self.final) is not bool:
            raise TypeError("final must be boolean")
        object.__setattr__(self, "contract_hash", require_digest("contract_hash", self.contract_hash))
        if self.final_payload_sha256 is not None:
            object.__setattr__(self, "final_payload_sha256", require_digest("final_payload_sha256", self.final_payload_sha256))


@dataclass(frozen=True, slots=True)
class CompletionResult:
    status: GateStatus
    code: str
    payload_sha256: str | None
    release_fingerprint: str
    problems: tuple[str, ...]

    @property
    def allowed(self) -> bool:
        return self.status is GateStatus.PASS


class CompletionBoundaryGate:
    """Proves that a streamed textual result reached an explicit intact boundary.

    The gate refuses to release outputs with sequence gaps, mixed run/contract
    identity, missing/early/multiple final markers, or a final payload hash that
    does not match the assembled bytes. It does not infer that network EOF means
    semantic completion.
    """

    @staticmethod
    def payload_sha256(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @classmethod
    def verify(
        cls,
        chunks: Sequence[StreamChunk],
        *,
        expected_run_id: str,
        expected_contract_hash: str,
        expected_chunk_count: int | None = None,
    ) -> CompletionResult:
        expected_run_id = require_nonempty("expected_run_id", expected_run_id)
        expected_contract_hash = require_digest("expected_contract_hash", expected_contract_hash)
        if expected_chunk_count is not None and (type(expected_chunk_count) is not int or expected_chunk_count < 1):
            raise ValueError("expected_chunk_count must be a positive integer")

        release_material = {
            "expected_run_id": expected_run_id,
            "expected_contract_hash": expected_contract_hash,
            "expected_chunk_count": expected_chunk_count,
            "chunks": chunks,
        }
        release_fingerprint = canonical_digest(release_material)
        if not chunks:
            return CompletionResult(GateStatus.FREEZE, "COMPLETION_EMPTY_STREAM", None, release_fingerprint, ("empty_stream",))

        problems: list[str] = []
        sequences = [chunk.sequence for chunk in chunks]
        if sequences != list(range(len(chunks))):
            problems.append("sequence_gap_or_reorder")
        if len(set(sequences)) != len(sequences):
            problems.append("duplicate_sequence")
        if expected_chunk_count is not None and len(chunks) != expected_chunk_count:
            problems.append("chunk_count_mismatch")

        for index, chunk in enumerate(chunks):
            if chunk.run_id != expected_run_id:
                problems.append(f"run_id_mismatch:{index}")
            if chunk.contract_hash != expected_contract_hash:
                problems.append(f"contract_hash_mismatch:{index}")
            if not chunk.final and chunk.final_payload_sha256 is not None:
                problems.append(f"premature_payload_hash:{index}")

        final_indexes = [i for i, chunk in enumerate(chunks) if chunk.final]
        if not final_indexes:
            problems.append("missing_final_marker")
        elif len(final_indexes) > 1:
            problems.append("multiple_final_markers")
        elif final_indexes[0] != len(chunks) - 1:
            problems.append("final_marker_not_last")

        assembled = "".join(chunk.data for chunk in chunks)
        payload_sha = cls.payload_sha256(assembled)
        if len(final_indexes) == 1:
            final_chunk = chunks[final_indexes[0]]
            if final_chunk.final_payload_sha256 is None:
                problems.append("missing_final_payload_hash")
            elif final_chunk.final_payload_sha256 != payload_sha:
                problems.append("final_payload_hash_mismatch")

        if problems:
            return CompletionResult(
                GateStatus.FREEZE,
                "COMPLETION_BOUNDARY_INVALID",
                payload_sha,
                release_fingerprint,
                tuple(sorted(set(problems))),
            )
        return CompletionResult(GateStatus.PASS, "COMPLETION_BOUNDARY_VALID", payload_sha, release_fingerprint, ())
