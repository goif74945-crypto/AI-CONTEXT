from __future__ import annotations

# ===== model.py =====
from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Mapping, Tuple


class AuthorityClass(str, Enum):
    AI_PROPOSED = "AI_PROPOSED_LO4"
    EXPERIMENTAL = "EXPERIMENTAL"
    ELIGIBLE_FOR_HUMAN_REVIEW = "ELIGIBLE_FOR_HUMAN_REVIEW"


class Decision(str, Enum):
    PASS = "PASS"
    FREEZE = "FREEZE"
    REVIEW = "REVIEW"


@dataclass(frozen=True)
class BehaviorContract:
    name: str
    inputs: FrozenSet[str] = frozenset()
    outputs: FrozenSet[str] = frozenset()
    invariants: FrozenSet[str] = frozenset()
    failures: FrozenSet[str] = frozenset()
    side_effects: FrozenSet[str] = frozenset()
    evidence: FrozenSet[str] = frozenset()
    authority: AuthorityClass = AuthorityClass.AI_PROPOSED


@dataclass(frozen=True)
class Capability:
    name: str
    kind: str
    dependencies: FrozenSet[str] = frozenset()
    protected: bool = False


@dataclass(frozen=True)
class IntegrationPlan:
    decision: Decision
    required_capabilities: Tuple[str, ...]
    blocked_capabilities: Tuple[str, ...] = ()
    reason: str = ""
    authority: AuthorityClass = AuthorityClass.AI_PROPOSED


@dataclass(frozen=True)
class InvariantCandidate:
    invariant_id: str
    expression: str
    kind: str
    field: str
    support: int
    observations: int
    counterexamples: Tuple[int, ...] = ()
    authority: AuthorityClass = AuthorityClass.EXPERIMENTAL

    @property
    def falsified(self) -> bool:
        return bool(self.counterexamples)


@dataclass(frozen=True)
class GuardProposal:
    predicates: Tuple[str, ...]
    rejected_negative_ids: Tuple[str, ...]
    preserved_positive_ids: Tuple[str, ...]
    decision: Decision
    authority: AuthorityClass = AuthorityClass.EXPERIMENTAL


@dataclass(frozen=True)
class TournamentCandidate:
    name: str
    metrics: Mapping[str, float]
    hard_constraints: Mapping[str, bool]
    evidence_ids: Tuple[str, ...]
    authority: AuthorityClass = AuthorityClass.AI_PROPOSED


@dataclass(frozen=True)
class TournamentResult:
    decision: Decision
    winner: str | None
    ranking: Tuple[str, ...]
    excluded: Tuple[Tuple[str, str], ...] = ()
    authority: AuthorityClass = AuthorityClass.AI_PROPOSED


# ===== novelty.py =====
import hashlib
import json
from dataclasses import asdict
from typing import Iterable, Mapping



DEFAULT_WEIGHTS: Mapping[str, float] = {
    "inputs": 1.0,
    "outputs": 1.2,
    "invariants": 2.2,
    "failures": 2.0,
    "side_effects": 2.4,
    "evidence": 1.6,
}


def _normalize(values: Iterable[str]) -> frozenset[str]:
    return frozenset(v.strip().casefold() for v in values if v.strip())


def _jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    return len(a & b) / len(union) if union else 1.0


def behavioral_similarity(
    left: BehaviorContract,
    right: BehaviorContract,
    weights: Mapping[str, float] = DEFAULT_WEIGHTS,
) -> float:
    weighted = 0.0
    total = 0.0
    for field, weight in sorted(weights.items()):
        if weight < 0:
            raise ValueError(f"negative weight for {field}")
        lv = _normalize(getattr(left, field))
        rv = _normalize(getattr(right, field))
        weighted += weight * _jaccard(lv, rv)
        total += weight
    if total <= 0:
        raise ValueError("total weight must be positive")
    return round(weighted / total, 6)


def novelty_report(
    candidate: BehaviorContract,
    existing: Iterable[BehaviorContract],
    duplicate_threshold: float = 0.82,
) -> dict:
    if not 0.0 <= duplicate_threshold <= 1.0:
        raise ValueError("duplicate_threshold must be within [0,1]")
    matches = sorted(
        ((behavioral_similarity(candidate, item), item.name) for item in existing),
        key=lambda x: (-x[0], x[1]),
    )
    top_score, top_name = matches[0] if matches else (0.0, None)
    classification = "DISTINCT" if top_score < duplicate_threshold else "HIGH_OVERLAP"
    return {
        "candidate": candidate.name,
        "classification": classification,
        "threshold": duplicate_threshold,
        "top_match": top_name,
        "top_score": top_score,
        "matches": [{"name": n, "score": s} for s, n in matches],
        "authority": candidate.authority.value,
    }


def contract_fingerprint(contract: BehaviorContract) -> str:
    payload = {
        "name": contract.name.casefold().strip(),
        "inputs": sorted(_normalize(contract.inputs)),
        "outputs": sorted(_normalize(contract.outputs)),
        "invariants": sorted(_normalize(contract.invariants)),
        "failures": sorted(_normalize(contract.failures)),
        "side_effects": sorted(_normalize(contract.side_effects)),
        "evidence": sorted(_normalize(contract.evidence)),
        "authority": contract.authority.value,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


# ===== invariants.py =====
from collections.abc import Iterable, Mapping, Sequence
from hashlib import sha256
from typing import Any



def _candidate_id(kind: str, field: str, expression: str) -> str:
    raw = f"{kind}|{field}|{expression}".encode()
    return "INV-" + sha256(raw).hexdigest()[:12].upper()


def discover_invariants(traces: Sequence[Mapping[str, Any]]) -> tuple[InvariantCandidate, ...]:
    if len(traces) < 2:
        return ()
    fields = sorted(set.intersection(*(set(t.keys()) for t in traces)))
    found: list[InvariantCandidate] = []
    for field in fields:
        values = [t[field] for t in traces]
        if all(v == values[0] for v in values[1:]):
            expr = f"{field} == {values[0]!r}"
            found.append(InvariantCandidate(_candidate_id("constant", field, expr), expr, "constant", field, len(values), len(values)))
        if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in values):
            if all(b >= a for a, b in zip(values, values[1:])):
                expr = f"{field} is nondecreasing"
                found.append(InvariantCandidate(_candidate_id("nondecreasing", field, expr), expr, "nondecreasing", field, len(values), len(values)))
            lo, hi = min(values), max(values)
            expr = f"{lo!r} <= {field} <= {hi!r}"
            found.append(InvariantCandidate(_candidate_id("observed_range", field, expr), expr, "observed_range", field, len(values), len(values)))
        if all(isinstance(v, str) and bool(v.strip()) for v in values):
            expr = f"{field} is nonempty"
            found.append(InvariantCandidate(_candidate_id("nonempty", field, expr), expr, "nonempty", field, len(values), len(values)))
    return tuple(sorted(found, key=lambda x: x.invariant_id))


def _violates(candidate: InvariantCandidate, trace: Mapping[str, Any], previous: Mapping[str, Any] | None) -> bool:
    if candidate.field not in trace:
        return True
    value = trace[candidate.field]
    if candidate.kind == "constant":
        literal = candidate.expression.split(" == ", 1)[1]
        return repr(value) != literal
    if candidate.kind == "nonempty":
        return not isinstance(value, str) or not value.strip()
    if candidate.kind == "nondecreasing":
        if previous is None or candidate.field not in previous:
            return False
        prev = previous[candidate.field]
        return not (
            isinstance(value, (int, float)) and not isinstance(value, bool)
            and isinstance(prev, (int, float)) and not isinstance(prev, bool)
            and value >= prev
        )
    if candidate.kind == "observed_range":
        bounds = candidate.expression.split(" <= ")
        lo = float(bounds[0])
        hi = float(bounds[2])
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            return True
        return not lo <= numeric <= hi
    raise ValueError(f"unknown invariant kind: {candidate.kind}")


def challenge_invariants(
    candidates: Iterable[InvariantCandidate],
    challenge_traces: Sequence[Mapping[str, Any]],
) -> tuple[InvariantCandidate, ...]:
    challenged: list[InvariantCandidate] = []
    for candidate in candidates:
        violations: list[int] = []
        previous = None
        for index, trace in enumerate(challenge_traces):
            if _violates(candidate, trace, previous):
                violations.append(index)
            previous = trace
        challenged.append(InvariantCandidate(
            invariant_id=candidate.invariant_id,
            expression=candidate.expression,
            kind=candidate.kind,
            field=candidate.field,
            support=candidate.support,
            observations=candidate.observations + len(challenge_traces),
            counterexamples=tuple(violations),
            authority=AuthorityClass.EXPERIMENTAL,
        ))
    return tuple(challenged)


def review_eligibility(candidate: InvariantCandidate, min_observations: int = 5) -> AuthorityClass:
    if candidate.falsified or candidate.observations < min_observations:
        return AuthorityClass.EXPERIMENTAL
    return AuthorityClass.ELIGIBLE_FOR_HUMAN_REVIEW


# ===== surface.py =====
from collections.abc import Iterable, Mapping



def minimize_integration_surface(
    requested: Iterable[str],
    capabilities: Mapping[str, Capability],
    forbidden: Iterable[str] = (),
) -> IntegrationPlan:
    requested_set = set(requested)
    forbidden_set = set(forbidden)
    required: set[str] = set()
    visiting: set[str] = set()
    blocked: set[str] = set()

    def visit(name: str) -> None:
        if name in required or name in blocked:
            return
        cap = capabilities.get(name)
        if cap is None:
            blocked.add(name)
            return
        if cap.protected or name in forbidden_set:
            blocked.add(name)
            return
        if name in visiting:
            blocked.add(name)
            return
        visiting.add(name)
        for dep in sorted(cap.dependencies):
            visit(dep)
        visiting.remove(name)
        if not blocked.intersection(cap.dependencies):
            required.add(name)
        else:
            blocked.add(name)

    for name in sorted(requested_set):
        visit(name)

    if blocked:
        return IntegrationPlan(
            decision=Decision.FREEZE,
            required_capabilities=tuple(sorted(required)),
            blocked_capabilities=tuple(sorted(blocked)),
            reason="protected, missing, cyclic, or forbidden capability detected",
        )
    return IntegrationPlan(
        decision=Decision.PASS,
        required_capabilities=tuple(sorted(required)),
        reason="least transitive capability closure computed",
    )


# ===== guards.py =====
from collections.abc import Callable, Mapping, Sequence
from itertools import combinations
from typing import Any


Predicate = Callable[[Mapping[str, Any]], bool]


def distill_guard(
    positives: Sequence[tuple[str, Mapping[str, Any]]],
    negatives: Sequence[tuple[str, Mapping[str, Any]]],
    predicates: Mapping[str, Predicate],
    max_terms: int = 3,
) -> GuardProposal:
    if not negatives or not predicates or max_terms < 1:
        return GuardProposal((), (), tuple(x[0] for x in positives), Decision.FREEZE)

    names = sorted(predicates)
    for width in range(1, min(max_terms, len(names)) + 1):
        for combo in combinations(names, width):
            def accepts(record: Mapping[str, Any]) -> bool:
                return all(predicates[name](record) for name in combo)

            preserved = tuple(pid for pid, record in positives if accepts(record))
            rejected = tuple(nid for nid, record in negatives if not accepts(record))
            if len(preserved) == len(positives) and len(rejected) == len(negatives):
                return GuardProposal(combo, rejected, preserved, Decision.REVIEW)

    return GuardProposal((), (), tuple(x[0] for x in positives), Decision.FREEZE)


# ===== tournament.py =====
from collections.abc import Iterable, Mapping



def run_tournament(
    candidates: Iterable[TournamentCandidate],
    metric_weights: Mapping[str, float],
    minimum_evidence: int = 1,
) -> TournamentResult:
    pool = sorted(candidates, key=lambda c: c.name)
    excluded: list[tuple[str, str]] = []
    eligible: list[TournamentCandidate] = []

    for candidate in pool:
        if any(not ok for _, ok in sorted(candidate.hard_constraints.items())):
            excluded.append((candidate.name, "hard_constraint_failed"))
            continue
        if len(set(candidate.evidence_ids)) < minimum_evidence:
            excluded.append((candidate.name, "insufficient_evidence"))
            continue
        missing = [m for m in metric_weights if m not in candidate.metrics]
        if missing:
            excluded.append((candidate.name, "missing_metrics:" + ",".join(sorted(missing))))
            continue
        eligible.append(candidate)

    if not eligible:
        return TournamentResult(Decision.FREEZE, None, (), tuple(excluded))

    def score(c: TournamentCandidate) -> float:
        return round(sum(c.metrics[m] * w for m, w in sorted(metric_weights.items())), 12)

    ranked = sorted(eligible, key=lambda c: (-score(c), c.name))
    if len(ranked) > 1 and score(ranked[0]) == score(ranked[1]):
        return TournamentResult(Decision.FREEZE, None, tuple(c.name for c in ranked), tuple(excluded + [(ranked[0].name, "top_score_tie"), (ranked[1].name, "top_score_tie")]))

    return TournamentResult(Decision.REVIEW, ranked[0].name, tuple(c.name for c in ranked), tuple(excluded))
