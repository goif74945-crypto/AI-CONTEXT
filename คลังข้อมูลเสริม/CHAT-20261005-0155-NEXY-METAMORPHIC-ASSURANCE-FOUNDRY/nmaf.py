from __future__ import annotations

import hashlib
import json
import math
from copy import deepcopy
from dataclasses import dataclass
from math import isfinite
from typing import Any, Callable, Protocol


class CanonicalizationError(ValueError):
    pass


def _validate(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, (bool, str, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise CanonicalizationError(f"non-finite float at {path}")
        return
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError(f"non-string mapping key at {path}")
            _validate(child, f"{path}.{key}")
        return
    if isinstance(value, list):
        for idx, child in enumerate(value):
            _validate(child, f"{path}[{idx}]")
        return
    raise CanonicalizationError(f"unsupported type {type(value).__name__} at {path}")


def canonical_json(value: Any) -> str:
    _validate(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


class Executor(Protocol):
    def __call__(self, value: Any) -> Any: ...


Transform = Callable[[Any], Any]
Invariant = Callable[[Any, Any], bool]


@dataclass(frozen=True)
class MetamorphicRelation:
    relation_id: str
    description: str
    transform: Transform
    invariant: Invariant

    def __post_init__(self) -> None:
        if not self.relation_id.strip() or not self.description.strip():
            raise ValueError("relation_id and description must be non-empty")


@dataclass(frozen=True)
class RelationResult:
    relation_id: str
    passed: bool
    base_input_hash: str
    mutated_input_hash: str
    base_output_hash: str
    mutated_output_hash: str
    base_input: Any
    mutated_input: Any
    base_output: Any
    mutated_output: Any


def run_relation(relation: MetamorphicRelation, base_input: Any, executor: Executor) -> RelationResult:
    safe_base = deepcopy(base_input)
    mutated = relation.transform(deepcopy(base_input))
    base_output = executor(deepcopy(safe_base))
    mutated_output = executor(deepcopy(mutated))
    passed = bool(relation.invariant(deepcopy(base_output), deepcopy(mutated_output)))
    return RelationResult(
        relation.relation_id,
        passed,
        canonical_sha256(safe_base),
        canonical_sha256(mutated),
        canonical_sha256(base_output),
        canonical_sha256(mutated_output),
        safe_base,
        mutated,
        base_output,
        mutated_output,
    )


def reorder_mapping_insertion(value: Any) -> Any:
    if isinstance(value, dict):
        keys = list(value.keys())
        return {key: reorder_mapping_insertion(value[key]) for key in reversed(keys)}
    if isinstance(value, list):
        return [reorder_mapping_insertion(item) for item in value]
    return deepcopy(value)


def set_path(value: Any, path: tuple[str | int, ...], replacement: Any) -> Any:
    if not path:
        return deepcopy(replacement)
    out = deepcopy(value)
    cursor = out
    for component in path[:-1]:
        if isinstance(component, str) and isinstance(cursor, dict) and component in cursor:
            cursor = cursor[component]
        elif isinstance(component, int) and isinstance(cursor, list) and 0 <= component < len(cursor):
            cursor = cursor[component]
        else:
            raise KeyError(f"path component not found: {component!r}")
    last = path[-1]
    if isinstance(last, str) and isinstance(cursor, dict) and last in cursor:
        cursor[last] = deepcopy(replacement)
    elif isinstance(last, int) and isinstance(cursor, list) and 0 <= last < len(cursor):
        cursor[last] = deepcopy(replacement)
    else:
        raise KeyError(f"path component not found: {last!r}")
    return out


def outputs_equal(a: Any, b: Any) -> bool:
    return canonical_sha256(a) == canonical_sha256(b)


@dataclass(frozen=True)
class ShrinkResult:
    original_hash: str
    minimized_hash: str
    minimized: Any
    evaluations: int
    exhausted_budget: bool


def _complexity(value: Any) -> tuple[int, int]:
    if isinstance(value, dict):
        return (1 + sum(_complexity(v)[0] for v in value.values()), len(value))
    if isinstance(value, list):
        return (1 + sum(_complexity(v)[0] for v in value), len(value))
    if isinstance(value, str):
        return (1, len(value))
    return (1, 1)


def _candidate_reductions(value: Any) -> list[Any]:
    out: list[Any] = []
    if isinstance(value, dict):
        for key in sorted(value):
            candidate = deepcopy(value)
            del candidate[key]
            out.append(candidate)
        for key in sorted(value):
            for child in _candidate_reductions(value[key]):
                candidate = deepcopy(value)
                candidate[key] = child
                out.append(candidate)
    elif isinstance(value, list):
        n = len(value)
        if n:
            chunk = max(1, n // 2)
            while chunk >= 1:
                for start in range(0, n - chunk + 1):
                    out.append(deepcopy(value[:start] + value[start + chunk :]))
                if chunk == 1:
                    break
                chunk //= 2
            for idx, child_value in enumerate(value):
                for child in _candidate_reductions(child_value):
                    candidate = deepcopy(value)
                    candidate[idx] = child
                    out.append(candidate)
    elif isinstance(value, str) and value:
        out.extend(["", value[: len(value) // 2], value[:1]])
    elif isinstance(value, bool) and value:
        out.append(False)
    elif isinstance(value, (int, float)) and not isinstance(value, bool) and value != 0:
        out.append(type(value)(0))

    unique: list[Any] = []
    seen: set[str] = set()
    for candidate in out:
        if _complexity(candidate) >= _complexity(value):
            continue
        digest = canonical_sha256(candidate)
        if digest not in seen:
            seen.add(digest)
            unique.append(candidate)
    return unique


def minimize_counterexample(value: Any, fails: Callable[[Any], bool], max_evaluations: int = 256) -> ShrinkResult:
    if max_evaluations < 1:
        raise ValueError("max_evaluations must be >= 1")
    original = deepcopy(value)
    evaluations = 1
    if not bool(fails(deepcopy(original))):
        raise ValueError("baseline value is not a failing counterexample")
    current = original
    exhausted = False
    while True:
        improved = False
        for candidate in _candidate_reductions(current):
            if evaluations >= max_evaluations:
                exhausted = True
                break
            evaluations += 1
            if bool(fails(deepcopy(candidate))):
                current = candidate
                improved = True
                break
        if exhausted or not improved:
            break
    return ShrinkResult(canonical_sha256(original), canonical_sha256(current), current, evaluations, exhausted)


@dataclass(frozen=True)
class ArtifactDescriptor:
    name: str
    source_labels: frozenset[str]
    logic_fingerprint: str | None = None

    def __post_init__(self) -> None:
        if not self.name.strip() or any(not x.strip() for x in self.source_labels):
            raise ValueError("artifact/source labels must be non-empty")


@dataclass(frozen=True)
class IndependenceReport:
    independent: bool
    shared_unapproved_sources: tuple[str, ...]
    identical_logic_fingerprint: bool
    reason_codes: tuple[str, ...]


def audit_oracle_independence(system: ArtifactDescriptor, oracle: ArtifactDescriptor, *, approved_shared_sources: frozenset[str] = frozenset()) -> IndependenceReport:
    unapproved = tuple(sorted((system.source_labels & oracle.source_labels) - approved_shared_sources))
    same_logic = bool(system.logic_fingerprint and oracle.logic_fingerprint and system.logic_fingerprint == oracle.logic_fingerprint)
    reasons = tuple(code for code, active in (
        ("ORACLE_SHARED_SOURCE", bool(unapproved)),
        ("ORACLE_IDENTICAL_LOGIC_FINGERPRINT", same_logic),
    ) if active)
    return IndependenceReport(not reasons, unapproved, same_logic, reasons)


@dataclass(frozen=True)
class TestCandidate:
    test_id: str
    risk: float
    coverage: frozenset[str]
    estimated_cost: float
    novelty: float = 0.0
    mandatory: bool = False

    def __post_init__(self) -> None:
        if not self.test_id.strip():
            raise ValueError("test_id must be non-empty")
        if not isfinite(self.risk) or not 0 <= self.risk <= 1:
            raise ValueError("risk must be finite in [0,1]")
        if not isfinite(self.novelty) or not 0 <= self.novelty <= 1:
            raise ValueError("novelty must be finite in [0,1]")
        if not isfinite(self.estimated_cost) or self.estimated_cost <= 0:
            raise ValueError("estimated_cost must be finite and > 0")


@dataclass(frozen=True)
class ScheduleResult:
    selected_ids: tuple[str, ...]
    total_cost: float
    covered_invariants: frozenset[str]
    unscheduled_mandatory: tuple[str, ...]
    freeze_required: bool


def _score(c: TestCandidate, covered: frozenset[str]) -> tuple[float, float, str]:
    new_coverage = len(c.coverage - covered)
    utility = 3 * c.risk + 2 * new_coverage + c.novelty
    return utility / c.estimated_cost, utility, c.test_id


def schedule_tests(candidates: list[TestCandidate], budget: float) -> ScheduleResult:
    if not isfinite(budget) or budget < 0:
        raise ValueError("budget must be finite and >= 0")
    ids = [c.test_id for c in candidates]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate test_id")
    mandatory = sorted((c for c in candidates if c.mandatory), key=lambda c: c.test_id)
    mandatory_cost = sum(c.estimated_cost for c in mandatory)
    if mandatory_cost > budget + 1e-12:
        return ScheduleResult((), 0.0, frozenset(), tuple(c.test_id for c in mandatory), True)

    selected = list(mandatory)
    selected_ids = {c.test_id for c in selected}
    cost = mandatory_cost
    covered = frozenset().union(*(c.coverage for c in selected)) if selected else frozenset()
    remaining = [c for c in candidates if c.test_id not in selected_ids]
    while remaining:
        affordable = [c for c in remaining if cost + c.estimated_cost <= budget + 1e-12]
        if not affordable:
            break
        ranked = sorted(affordable, key=lambda c: (-_score(c, covered)[0], -_score(c, covered)[1], c.test_id))
        best = ranked[0]
        selected.append(best)
        cost += best.estimated_cost
        covered = frozenset(set(covered) | set(best.coverage))
        remaining = [c for c in remaining if c.test_id != best.test_id]
    return ScheduleResult(tuple(c.test_id for c in selected), cost, covered, (), False)


@dataclass(frozen=True)
class FailureRecord:
    invariant_id: str
    phase: str
    relation_id: str
    root_cause_code: str
    witness: Any

    def __post_init__(self) -> None:
        for field in ("invariant_id", "phase", "relation_id", "root_cause_code"):
            if not getattr(self, field).strip():
                raise ValueError(f"{field} must be non-empty")


def _remove_volatile_paths(value: Any, paths: tuple[tuple[str | int, ...], ...]) -> Any:
    out = deepcopy(value)
    for path in paths:
        if not path:
            continue
        cursor = out
        valid = True
        for component in path[:-1]:
            if isinstance(component, str) and isinstance(cursor, dict) and component in cursor:
                cursor = cursor[component]
            elif isinstance(component, int) and isinstance(cursor, list) and 0 <= component < len(cursor):
                cursor = cursor[component]
            else:
                valid = False
                break
        if not valid:
            continue
        leaf = path[-1]
        if isinstance(leaf, str) and isinstance(cursor, dict):
            cursor.pop(leaf, None)
        elif isinstance(leaf, int) and isinstance(cursor, list) and 0 <= leaf < len(cursor):
            cursor[leaf] = "<VOLATILE>"
    return out


def semantic_failure_fingerprint(record: FailureRecord, *, volatile_paths: tuple[tuple[str | int, ...], ...] = ()) -> str:
    return canonical_sha256({
        "invariant_id": record.invariant_id,
        "phase": record.phase,
        "relation_id": record.relation_id,
        "root_cause_code": record.root_cause_code,
        "witness": _remove_volatile_paths(record.witness, volatile_paths),
    })


@dataclass(frozen=True)
class TruthSurface:
    status: str
    state: str
    data: Any
    error_code: str | None
    freeze_reason: str | None


def extract_truth_surface(envelope: dict[str, Any]) -> TruthSurface:
    status, state = envelope.get("status"), envelope.get("state")
    if not isinstance(status, str) or not status:
        raise ValueError("missing/invalid envelope.status")
    if not isinstance(state, str) or not state:
        raise ValueError("missing/invalid envelope.state")
    error = envelope.get("error")
    error_code = error.get("code") if isinstance(error, dict) and isinstance(error.get("code"), str) else None
    freeze_reason = envelope.get("freeze_reason")
    if freeze_reason is not None and not isinstance(freeze_reason, str):
        raise ValueError("invalid envelope.freeze_reason")
    return TruthSurface(status, state, envelope.get("data"), error_code, freeze_reason)
