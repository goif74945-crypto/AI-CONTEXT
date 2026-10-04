from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .errors import WireContractError
from .model import CanonicalEvent
from .replay import ReplayReport, TranscriptReplayer


@dataclass(frozen=True, slots=True)
class BoundaryResult:
    accepted: bool
    frozen: bool
    report: ReplayReport | None = None
    error_code: str | None = None
    error_message: str | None = None


class WireBoundary:
    """NEXY-facing fail-closed gate for canonical provider event transcripts."""

    def __init__(self) -> None:
        self._replayer = TranscriptReplayer()

    def validate(self, events: Iterable[CanonicalEvent]) -> BoundaryResult:
        materialized = tuple(events)
        try:
            report = self._replayer.replay(materialized)
            if not report.closed:
                return BoundaryResult(
                    accepted=False,
                    frozen=True,
                    report=report,
                    error_code="STREAM_NOT_CLOSED",
                    error_message="canonical transcript ended without stream.close",
                )
            return BoundaryResult(accepted=True, frozen=False, report=report)
        except WireContractError as exc:
            return BoundaryResult(
                accepted=False,
                frozen=True,
                error_code=exc.code,
                error_message=str(exc),
            )
