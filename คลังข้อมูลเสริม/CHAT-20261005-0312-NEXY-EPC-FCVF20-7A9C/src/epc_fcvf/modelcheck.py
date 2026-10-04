from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Callable, Iterable, Sequence

from .canonical import canonical_hash
from .engine import Constitution, STRICT_CONSTITUTION, transition
from .model import CourtState, Event, TransitionResult
from .systems import evaluate_all


@dataclass(frozen=True, slots=True)
class ExplorationReport:
    depth: int
    unique_states: int
    transitions_examined: int
    accepted_transitions: int
    blocked_transitions: int
    unsafe_states: int
    digest: str
    first_failure: str = ""


def state_key(state: CourtState) -> str:
    return canonical_hash(state)


def explore(
    initial: CourtState,
    alphabet: Sequence[Event],
    *,
    depth: int,
    constitution: Constitution = STRICT_CONSTITUTION,
) -> ExplorationReport:
    if depth < 0:
        raise ValueError("DEPTH_NEGATIVE")
    current: dict[str, CourtState] = {state_key(initial): initial}
    all_states: dict[str, CourtState] = dict(current)
    examined = accepted = blocked = unsafe = 0
    first_failure = ""

    for _ in range(depth):
        nxt: dict[str, CourtState] = {}
        for key in sorted(current):
            state = current[key]
            for event in alphabet:
                examined += 1
                result = transition(state, event, constitution)
                if result.accepted:
                    accepted += 1
                else:
                    blocked += 1
                child = result.state
                findings = evaluate_all(child)
                failed = [f for f in findings if not f.passed]
                if failed:
                    unsafe += 1
                    if not first_failure:
                        first_failure = ";".join(f"{f.system_id}:{f.code}" for f in failed)
                child_key = state_key(child)
                if child_key not in all_states:
                    all_states[child_key] = child
                    nxt[child_key] = child
        current = nxt
        if not current:
            break

    digest_material = "\n".join(sorted(all_states)).encode("ascii")
    digest = hashlib.sha256(digest_material).hexdigest()
    return ExplorationReport(
        depth=depth,
        unique_states=len(all_states),
        transitions_examined=examined,
        accepted_transitions=accepted,
        blocked_transitions=blocked,
        unsafe_states=unsafe,
        digest=digest,
        first_failure=first_failure,
    )


def execute_trace(
    initial: CourtState,
    trace: Sequence[Event],
    constitution: Constitution = STRICT_CONSTITUTION,
) -> tuple[CourtState, tuple[TransitionResult, ...]]:
    state = initial
    results = []
    for event in trace:
        result = transition(state, event, constitution)
        results.append(result)
        state = result.state
    return state, tuple(results)


def minimize_counterexample(
    trace: Sequence[Event],
    violates: Callable[[Sequence[Event]], bool],
) -> tuple[Event, ...]:
    """Deterministic 1-minimal greedy reducer.

    It never uses randomness. Removal restarts at index 0 after every successful shrink.
    """
    candidate = list(trace)
    if not violates(candidate):
        raise ValueError("TRACE_IS_NOT_COUNTEREXAMPLE")
    changed = True
    while changed:
        changed = False
        index = 0
        while index < len(candidate):
            trial = candidate[:index] + candidate[index + 1 :]
            if trial and violates(trial):
                candidate = trial
                changed = True
                index = 0
            else:
                index += 1
    return tuple(candidate)
