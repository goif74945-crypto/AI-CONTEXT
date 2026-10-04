from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .contracts import Decision, Verdict


@dataclass(frozen=True, slots=True)
class SuiteDecision:
    verdict: Verdict
    engine_verdicts: tuple[tuple[str, str], ...]
    fingerprints: tuple[tuple[str, str], ...]


class AssuranceSuite:
    """Compose advisory decisions without letting PASS override a FREEZE."""

    _RANK = {
        Verdict.PASS: 0,
        Verdict.REVIEW: 1,
        Verdict.FAIL: 2,
        Verdict.FREEZE: 3,
    }

    def combine(self, decisions: Iterable[Decision]) -> SuiteDecision:
        ordered = sorted(tuple(decisions), key=lambda d: d.engine)
        if not ordered:
            raise ValueError("at least one decision is required")
        verdict = max((d.verdict for d in ordered), key=self._RANK.__getitem__)
        return SuiteDecision(
            verdict=verdict,
            engine_verdicts=tuple((d.engine, d.verdict.value) for d in ordered),
            fingerprints=tuple((d.engine, d.fingerprint()) for d in ordered),
        )
