from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .engine import Constitution, STRICT_CONSTITUTION
from .model import CourtState, Event
from .modelcheck import execute_trace, minimize_counterexample
from .systems import evaluate_all


@dataclass(frozen=True, slots=True)
class RegressionWitness:
    found: bool
    strict_failure_code: str
    weak_accept_code: str
    minimal_trace: tuple[Event, ...]


def find_weakening_witness(
    initial: CourtState,
    traces: Sequence[Sequence[Event]],
    candidate_constitution: Constitution,
) -> RegressionWitness:
    for trace in traces:
        strict_state, strict_results = execute_trace(initial, trace, STRICT_CONSTITUTION)
        weak_state, weak_results = execute_trace(initial, trace, candidate_constitution)
        weak_failed = [f for f in evaluate_all(weak_state) if not f.passed]
        if weak_failed and not [f for f in evaluate_all(strict_state) if not f.passed]:
            def violates(t: Sequence[Event]) -> bool:
                s, _ = execute_trace(initial, t, candidate_constitution)
                return any(not f.passed for f in evaluate_all(s))

            minimal = minimize_counterexample(trace, violates)
            strict_code = next((r.code for r in strict_results if not r.accepted), "STRICT_SAFE_STATE")
            weak_code = next((r.code for r in reversed(weak_results) if r.accepted), "WEAK_ACCEPTED")
            return RegressionWitness(True, strict_code, weak_code, minimal)
    return RegressionWitness(False, "", "", ())
