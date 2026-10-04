"""NEXY Evidence Independence Kernel (NEIK) v0.1.0
Standalone advisory reference implementation.
"""
from __future__ import annotations


# ===== model.py =====

from dataclasses import dataclass
from enum import IntEnum
from typing import Mapping, Tuple


class EvidenceClass(IntEnum):
    E0 = 0
    E1 = 1
    E2 = 2
    E3 = 3
    E4 = 4
    E5 = 5
    E6 = 6
    E7 = 7

    @classmethod
    def parse(cls, value: str) -> "EvidenceClass":
        try:
            return cls[value]
        except KeyError as exc:
            raise ValueError(f"invalid evidence class: {value!r}") from exc


CONFIGURABLE_DIMENSIONS = (
    "source_lineage",
    "producer_lineage",
    "oracle_lineage",
)
INTRINSIC_DIMENSIONS = ("artifact_identity",)
ALL_DIMENSIONS = CONFIGURABLE_DIMENSIONS + INTRINSIC_DIMENSIONS


@dataclass(frozen=True)
class Claim:
    id: str
    target_revision: str
    required_evidence_class: EvidenceClass
    required_independent_confirmations: int


@dataclass(frozen=True)
class Policy:
    independence_dimensions: Tuple[str, ...]
    require_blind: bool
    forbid_self_verification_without_external_oracle: bool
    max_evidence_nodes: int
    max_solver_states: int


@dataclass(frozen=True)
class Evidence:
    id: str
    claim_id: str
    target_revision: str
    evidence_class: EvidenceClass
    verdict: str
    producer_id: str
    subjects_under_test: Tuple[str, ...]
    external_oracle: bool
    blind: bool
    derived_from: Tuple[str, ...]
    source_lineage: Tuple[str, ...]
    producer_lineage: Tuple[str, ...]
    oracle_lineage: Tuple[str, ...]
    artifact_hash: str

    def dimension(self, name: str) -> Tuple[str, ...]:
        if name in CONFIGURABLE_DIMENSIONS:
            return getattr(self, name)
        if name == "artifact_identity":
            return (self.artifact_hash,)
        raise KeyError(name)


@dataclass(frozen=True)
class Envelope:
    schema_version: str
    claim: Claim
    policy: Policy
    evidence: Tuple[Evidence, ...]


@dataclass(frozen=True)
class ClosedEvidence:
    evidence: Evidence
    closed_lineage: Mapping[str, Tuple[str, ...]]

# ===== parser.py =====

from typing import Any, Iterable, Mapping



class ContractError(ValueError):
    pass


def _mapping(value: Any, where: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ContractError(f"{where} must be an object")
    return value


def _string(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{where} must be a non-empty string")
    return value


def _bool(value: Any, where: str) -> bool:
    if not isinstance(value, bool):
        raise ContractError(f"{where} must be boolean")
    return value


def _int(value: Any, where: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ContractError(f"{where} must be an integer")
    if value < minimum or value > maximum:
        raise ContractError(f"{where} must be in [{minimum}, {maximum}]")
    return value


def _strings(value: Any, where: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ContractError(f"{where} must be an array")
    out: list[str] = []
    seen: set[str] = set()
    for i, item in enumerate(value):
        s = _string(item, f"{where}[{i}]")
        if s in seen:
            raise ContractError(f"{where} contains duplicate value {s!r}")
        seen.add(s)
        out.append(s)
    return tuple(out)


def _exact_keys(obj: Mapping[str, Any], expected: Iterable[str], where: str) -> None:
    expected_set = set(expected)
    actual = set(obj)
    missing = expected_set - actual
    extra = actual - expected_set
    if missing:
        raise ContractError(f"{where} missing fields: {sorted(missing)}")
    if extra:
        raise ContractError(f"{where} has unknown fields: {sorted(extra)}")


def parse_envelope(data: Mapping[str, Any]) -> Envelope:
    root = _mapping(data, "root")
    _exact_keys(root, ("schema_version", "claim", "policy", "evidence"), "root")
    schema_version = _string(root["schema_version"], "schema_version")
    if schema_version != "neik/0.1":
        raise ContractError(f"unsupported schema_version: {schema_version!r}")

    claim_obj = _mapping(root["claim"], "claim")
    _exact_keys(
        claim_obj,
        ("id", "target_revision", "required_evidence_class", "required_independent_confirmations"),
        "claim",
    )
    try:
        required_class = EvidenceClass.parse(_string(claim_obj["required_evidence_class"], "claim.required_evidence_class"))
    except ValueError as exc:
        raise ContractError(str(exc)) from exc
    claim = Claim(
        id=_string(claim_obj["id"], "claim.id"),
        target_revision=_string(claim_obj["target_revision"], "claim.target_revision"),
        required_evidence_class=required_class,
        required_independent_confirmations=_int(
            claim_obj["required_independent_confirmations"],
            "claim.required_independent_confirmations",
            1,
            32,
        ),
    )

    policy_obj = _mapping(root["policy"], "policy")
    _exact_keys(
        policy_obj,
        (
            "independence_dimensions",
            "require_blind",
            "forbid_self_verification_without_external_oracle",
            "max_evidence_nodes",
            "max_solver_states",
        ),
        "policy",
    )
    dims = _strings(policy_obj["independence_dimensions"], "policy.independence_dimensions")
    if not dims:
        raise ContractError("policy.independence_dimensions must not be empty")
    unknown_dims = [d for d in dims if d not in CONFIGURABLE_DIMENSIONS]
    if unknown_dims:
        raise ContractError(f"unknown independence dimensions: {unknown_dims}")
    policy = Policy(
        independence_dimensions=dims,
        require_blind=_bool(policy_obj["require_blind"], "policy.require_blind"),
        forbid_self_verification_without_external_oracle=_bool(
            policy_obj["forbid_self_verification_without_external_oracle"],
            "policy.forbid_self_verification_without_external_oracle",
        ),
        max_evidence_nodes=_int(policy_obj["max_evidence_nodes"], "policy.max_evidence_nodes", 1, 128),
        max_solver_states=_int(policy_obj["max_solver_states"], "policy.max_solver_states", 1, 10_000_000),
    )

    raw_evidence = root["evidence"]
    if not isinstance(raw_evidence, list):
        raise ContractError("evidence must be an array")
    if len(raw_evidence) > policy.max_evidence_nodes:
        raise ContractError(
            f"evidence count {len(raw_evidence)} exceeds policy.max_evidence_nodes {policy.max_evidence_nodes}"
        )

    evidence: list[Evidence] = []
    ids: set[str] = set()
    expected_fields = (
        "id",
        "claim_id",
        "target_revision",
        "evidence_class",
        "verdict",
        "producer_id",
        "subjects_under_test",
        "external_oracle",
        "blind",
        "derived_from",
        "source_lineage",
        "producer_lineage",
        "oracle_lineage",
        "artifact_hash",
    )
    for i, raw in enumerate(raw_evidence):
        obj = _mapping(raw, f"evidence[{i}]")
        _exact_keys(obj, expected_fields, f"evidence[{i}]")
        eid = _string(obj["id"], f"evidence[{i}].id")
        if eid in ids:
            raise ContractError(f"duplicate evidence id: {eid!r}")
        ids.add(eid)
        try:
            eclass = EvidenceClass.parse(_string(obj["evidence_class"], f"evidence[{i}].evidence_class"))
        except ValueError as exc:
            raise ContractError(str(exc)) from exc
        verdict = _string(obj["verdict"], f"evidence[{i}].verdict")
        if verdict not in {"PASS", "FAIL"}:
            raise ContractError(f"evidence[{i}].verdict must be PASS or FAIL")
        item = Evidence(
            id=eid,
            claim_id=_string(obj["claim_id"], f"evidence[{i}].claim_id"),
            target_revision=_string(obj["target_revision"], f"evidence[{i}].target_revision"),
            evidence_class=eclass,
            verdict=verdict,
            producer_id=_string(obj["producer_id"], f"evidence[{i}].producer_id"),
            subjects_under_test=_strings(obj["subjects_under_test"], f"evidence[{i}].subjects_under_test"),
            external_oracle=_bool(obj["external_oracle"], f"evidence[{i}].external_oracle"),
            blind=_bool(obj["blind"], f"evidence[{i}].blind"),
            derived_from=_strings(obj["derived_from"], f"evidence[{i}].derived_from"),
            source_lineage=_strings(obj["source_lineage"], f"evidence[{i}].source_lineage"),
            producer_lineage=_strings(obj["producer_lineage"], f"evidence[{i}].producer_lineage"),
            oracle_lineage=_strings(obj["oracle_lineage"], f"evidence[{i}].oracle_lineage"),
            artifact_hash=_string(obj["artifact_hash"], f"evidence[{i}].artifact_hash"),
        )
        if item.producer_id not in item.producer_lineage:
            raise ContractError(
                f"evidence {eid!r} producer_lineage must contain producer_id {item.producer_id!r}"
            )
        if item.claim_id != claim.id:
            raise ContractError(f"evidence {eid!r} references claim {item.claim_id!r}, expected {claim.id!r}")
        evidence.append(item)

    known = {e.id for e in evidence}
    for e in evidence:
        for dep in e.derived_from:
            if dep == e.id:
                raise ContractError(f"evidence {e.id!r} directly depends on itself")
            if dep not in known:
                raise ContractError(f"evidence {e.id!r} depends on unknown evidence {dep!r}")

    return Envelope(schema_version=schema_version, claim=claim, policy=policy, evidence=tuple(evidence))

# ===== graph.py =====

from typing import Dict, Iterable, Mapping, Sequence



class EvidenceCycleError(ValueError):
    def __init__(self, cycle: Sequence[str]):
        self.cycle = tuple(cycle)
        super().__init__("evidence dependency cycle: " + " -> ".join(self.cycle))


def detect_cycle(evidence: Iterable[Evidence]) -> tuple[str, ...] | None:
    by_id = {e.id: e for e in evidence}
    state: Dict[str, int] = {eid: 0 for eid in by_id}  # 0 white, 1 gray, 2 black
    stack: list[str] = []
    pos: dict[str, int] = {}

    def visit(eid: str) -> tuple[str, ...] | None:
        state[eid] = 1
        pos[eid] = len(stack)
        stack.append(eid)
        for dep in sorted(by_id[eid].derived_from):
            if state[dep] == 0:
                found = visit(dep)
                if found:
                    return found
            elif state[dep] == 1:
                start = pos[dep]
                return tuple(stack[start:] + [dep])
        stack.pop()
        pos.pop(eid, None)
        state[eid] = 2
        return None

    for eid in sorted(by_id):
        if state[eid] == 0:
            found = visit(eid)
            if found:
                return found
    return None


def close_lineage(evidence: Iterable[Evidence]) -> Mapping[str, ClosedEvidence]:
    items = tuple(evidence)
    cycle = detect_cycle(items)
    if cycle:
        raise EvidenceCycleError(cycle)
    by_id = {e.id: e for e in items}
    memo: dict[str, ClosedEvidence] = {}

    def close(eid: str) -> ClosedEvidence:
        if eid in memo:
            return memo[eid]
        e = by_id[eid]
        accum: dict[str, set[str]] = {d: set(e.dimension(d)) for d in ALL_DIMENSIONS}
        for dep in sorted(e.derived_from):
            parent = close(dep)
            for d in ALL_DIMENSIONS:
                accum[d].update(parent.closed_lineage[d])
        closed = ClosedEvidence(
            evidence=e,
            closed_lineage={d: tuple(sorted(accum[d])) for d in ALL_DIMENSIONS},
        )
        memo[eid] = closed
        return closed

    for eid in sorted(by_id):
        close(eid)
    return memo


def lineage_overlap(a: ClosedEvidence, b: ClosedEvidence, dimensions: Sequence[str]) -> Mapping[str, tuple[str, ...]]:
    overlaps: dict[str, tuple[str, ...]] = {}
    for d in dimensions:
        shared = tuple(sorted(set(a.closed_lineage[d]) & set(b.closed_lineage[d])))
        if shared:
            overlaps[d] = shared
    return overlaps

# ===== solver.py =====

from dataclasses import dataclass
from typing import Sequence



class SearchBudgetExceeded(RuntimeError):
    def __init__(self, states_explored: int, budget: int):
        self.states_explored = states_explored
        self.budget = budget
        super().__init__(f"independence search exceeded deterministic state budget {budget}")


@dataclass(frozen=True)
class WitnessResult:
    ids: tuple[str, ...]
    states_explored: int


def conflict_masks(candidates: Sequence[ClosedEvidence], dimensions: Sequence[str]) -> tuple[int, ...]:
    n = len(candidates)
    masks = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if lineage_overlap(candidates[i], candidates[j], dimensions):
                masks[i] |= 1 << j
                masks[j] |= 1 << i
    return tuple(masks)


def maximum_independent_witness(
    candidates: Sequence[ClosedEvidence],
    dimensions: Sequence[str],
    *,
    max_states: int,
) -> WitnessResult:
    """Return an exact maximum pairwise-independent evidence-id set.

    The search is deterministic. Ties are resolved lexicographically by evidence-id tuple.
    A deterministic state budget prevents combinatorial resource exhaustion.
    """
    ordered = tuple(sorted(candidates, key=lambda c: c.evidence.id))
    n = len(ordered)
    if n == 0:
        return WitnessResult((), 0)
    masks = conflict_masks(ordered, dimensions)
    best_mask = 0
    best_ids: tuple[str, ...] = ()
    states = 0

    def ids_for(mask: int) -> tuple[str, ...]:
        return tuple(ordered[i].evidence.id for i in range(n) if mask & (1 << i))

    def better(mask: int) -> None:
        nonlocal best_mask, best_ids
        count = mask.bit_count()
        best_count = best_mask.bit_count()
        if count < best_count:
            return
        ids = ids_for(mask)
        if count > best_count or not best_ids or ids < best_ids:
            best_mask = mask
            best_ids = ids

    def search(available: int, chosen: int) -> None:
        nonlocal states
        states += 1
        if states > max_states:
            raise SearchBudgetExceeded(states, max_states)
        if chosen.bit_count() + available.bit_count() < best_mask.bit_count():
            return
        if available == 0:
            better(chosen)
            return

        indices = [i for i in range(n) if available & (1 << i)]
        v = min(indices, key=lambda i: (-((masks[i] & available).bit_count()), i))
        vbit = 1 << v

        search(available & ~vbit & ~masks[v], chosen | vbit)
        search(available & ~vbit, chosen)

    search((1 << n) - 1, 0)
    return WitnessResult(best_ids, states)

# ===== canonical.py =====

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_canonical(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

# ===== kernel.py =====

from typing import Any



def _finding(code: str, evidence_id: str | None = None, detail: Any = None) -> dict[str, Any]:
    out: dict[str, Any] = {"code": code}
    if evidence_id is not None:
        out["evidence_id"] = evidence_id
    if detail is not None:
        out["detail"] = detail
    return out


def _seal(body: dict[str, Any]) -> dict[str, Any]:
    return {**body, "decision_sha256": sha256_canonical(body)}


def evaluate(envelope: Envelope) -> dict[str, Any]:
    claim = envelope.claim
    policy = envelope.policy
    findings: list[dict[str, Any]] = []
    independence_dimensions = INTRINSIC_DIMENSIONS + policy.independence_dimensions

    try:
        closed = close_lineage(envelope.evidence)
    except EvidenceCycleError as exc:
        return _seal(
            {
                "schema_version": "neik-decision/0.1",
                "claim_id": claim.id,
                "target_revision": claim.target_revision,
                "status": "FREEZE",
                "reason": "EVIDENCE_DEPENDENCY_CYCLE",
                "required_independent_confirmations": claim.required_independent_confirmations,
                "maximum_independent_confirmations": None,
                "solver_states_explored": 0,
                "witness": [],
                "findings": [_finding("DEPENDENCY_CYCLE", detail=list(exc.cycle))],
                "lineage_closure": {},
                "conflicts": [],
            }
        )

    current_sufficient: list[ClosedEvidence] = []
    admissible_pass: list[ClosedEvidence] = []
    admissible_fail: list[ClosedEvidence] = []

    for eid in sorted(closed):
        item = closed[eid]
        e = item.evidence
        if e.target_revision != claim.target_revision:
            findings.append(_finding("STALE_TARGET_REVISION", eid, {"observed": e.target_revision}))
            continue
        if e.evidence_class < claim.required_evidence_class:
            findings.append(
                _finding(
                    "INSUFFICIENT_EVIDENCE_CLASS",
                    eid,
                    {"observed": e.evidence_class.name, "required": claim.required_evidence_class.name},
                )
            )
            continue
        current_sufficient.append(item)

        missing_dims = [d for d in policy.independence_dimensions if not item.closed_lineage[d]]
        if missing_dims:
            findings.append(_finding("MISSING_INDEPENDENCE_LINEAGE", eid, {"dimensions": missing_dims}))
            continue
        if policy.require_blind and not e.blind:
            findings.append(_finding("NOT_BLIND", eid))
            continue
        if (
            policy.forbid_self_verification_without_external_oracle
            and e.producer_id in set(e.subjects_under_test)
            and (not e.external_oracle or not e.oracle_lineage)
        ):
            findings.append(_finding("SELF_VERIFICATION_WITHOUT_EXTERNAL_ORACLE", eid))
            continue
        if e.verdict == "PASS":
            admissible_pass.append(item)
        else:
            admissible_fail.append(item)

    raw_current_verdicts = {x.evidence.verdict for x in current_sufficient}
    solver_result = WitnessResult((), 0)
    if raw_current_verdicts == {"PASS", "FAIL"}:
        findings.append(_finding("CURRENT_EVIDENCE_VERDICT_CONFLICT"))
        status = "FREEZE"
        reason = "CURRENT_PASS_FAIL_CONFLICT"
    elif admissible_fail:
        findings.append(_finding("ADMISSIBLE_FAIL_EVIDENCE", detail=[x.evidence.id for x in admissible_fail]))
        status = "FREEZE"
        reason = "ADMISSIBLE_FAIL_EVIDENCE"
    else:
        try:
            solver_result = maximum_independent_witness(
                admissible_pass,
                independence_dimensions,
                max_states=policy.max_solver_states,
            )
        except SearchBudgetExceeded as exc:
            findings.append(
                _finding(
                    "SOLVER_BUDGET_EXCEEDED",
                    detail={"states_explored": exc.states_explored, "budget": exc.budget},
                )
            )
            status = "FREEZE"
            reason = "SOLVER_BUDGET_EXCEEDED"
        else:
            if len(solver_result.ids) >= claim.required_independent_confirmations:
                status = "PASS"
                reason = "INDEPENDENT_QUORUM_SATISFIED"
            else:
                status = "NOT_VERIFIED"
                reason = "INDEPENDENT_QUORUM_NOT_MET"

    conflicts: list[dict[str, Any]] = []
    ordered_pass = sorted(admissible_pass, key=lambda x: x.evidence.id)
    for i, left in enumerate(ordered_pass):
        for right in ordered_pass[i + 1 :]:
            overlap = lineage_overlap(left, right, independence_dimensions)
            if overlap:
                conflicts.append(
                    {
                        "left": left.evidence.id,
                        "right": right.evidence.id,
                        "overlap": {k: list(v) for k, v in sorted(overlap.items())},
                    }
                )

    lineage_closure = {
        eid: {d: list(closed[eid].closed_lineage[d]) for d in sorted(closed[eid].closed_lineage)}
        for eid in sorted(closed)
    }
    findings = sorted(findings, key=lambda f: (f["code"], f.get("evidence_id", ""), repr(f.get("detail"))))
    maximum = None if reason == "SOLVER_BUDGET_EXCEEDED" else len(solver_result.ids)
    body = {
        "schema_version": "neik-decision/0.1",
        "claim_id": claim.id,
        "target_revision": claim.target_revision,
        "status": status,
        "reason": reason,
        "required_independent_confirmations": claim.required_independent_confirmations,
        "maximum_independent_confirmations": maximum,
        "solver_states_explored": solver_result.states_explored,
        "witness": list(solver_result.ids),
        "findings": findings,
        "lineage_closure": lineage_closure,
        "conflicts": conflicts,
    }
    return _seal(body)

# ===== cli.py =====

import argparse
import json
import sys
from pathlib import Path
from typing import Any



def _load(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="NEXY Evidence Independence Kernel")
    parser.add_argument("input", help="JSON input path or '-' for stdin")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    args = parser.parse_args(argv)
    try:
        envelope = parse_envelope(_load(args.input))
        result = evaluate(envelope)
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(json.dumps({"status": "INVALID_INPUT", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

    if args.pretty:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        print(canonical_json(result))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
