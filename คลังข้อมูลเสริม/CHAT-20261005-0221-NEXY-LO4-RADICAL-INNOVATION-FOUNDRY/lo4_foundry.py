
# ===== core.py =====
from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Any


class Lo4Error(ValueError):
    """Raised when an Lo4 input violates an explicit structural contract."""


class Authority(str, Enum):
    USER_LAW = "USER_LAW"
    CANON = "CANON"
    SYSTEM = "SYSTEM"
    EXPERIMENTAL = "EXPERIMENTAL"


class Decision(str, Enum):
    ALLOW_EXPERIMENT = "ALLOW_EXPERIMENT"
    REJECT_EXPERIMENT = "REJECT_EXPERIMENT"
    KEEP_EXPERIMENT = "KEEP_EXPERIMENT"
    NEED_EVIDENCE = "NEED_EVIDENCE"
    PROPOSE_RELAXATION = "PROPOSE_RELAXATION"
    PLAN = "PLAN"
    FREEZE = "FREEZE"


def clean_id(value: str, field: str = "id") -> str:
    if not isinstance(value, str):
        raise Lo4Error(f"{field}:NOT_STRING")
    value = value.strip()
    if not value:
        raise Lo4Error(f"{field}:EMPTY")
    if len(value) > 200:
        raise Lo4Error(f"{field}:TOO_LONG")
    return value


def ensure_int(value: int, field: str, minimum: int | None = None, maximum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise Lo4Error(f"{field}:NOT_INT")
    if minimum is not None and value < minimum:
        raise Lo4Error(f"{field}:BELOW_MIN")
    if maximum is not None and value > maximum:
        raise Lo4Error(f"{field}:ABOVE_MAX")
    return value


def _normalize(value: Any) -> Any:
    if is_dataclass(value):
        value = asdict(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(k): _normalize(v) for k, v in sorted(value.items(), key=lambda kv: str(kv[0]))}
    if isinstance(value, (tuple, list, set, frozenset)):
        seq = [_normalize(v) for v in value]
        if isinstance(value, (set, frozenset)):
            seq = sorted(seq, key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False))
        return seq
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_normalize(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def fingerprint(value: Any) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()

# ===== surprise_budget.py =====

from dataclasses import dataclass
from typing import Iterable



@dataclass(frozen=True, slots=True)
class NoveltyDimension:
    name: str
    distance_bps: int
    weight_bps: int
    authority: Authority = Authority.EXPERIMENTAL


@dataclass(frozen=True, slots=True)
class SurprisePolicy:
    total_budget: int = 10_000
    max_single_dimension_cost: int = 5_000
    forbidden_authorities: tuple[Authority, ...] = (Authority.USER_LAW, Authority.CANON)


@dataclass(frozen=True, slots=True)
class SurpriseResult:
    status: Decision
    total_cost: int
    dimension_costs: tuple[tuple[str, int], ...]
    reason_codes: tuple[str, ...]
    fingerprint: str


def evaluate_surprise_budget(
    dimensions: Iterable[NoveltyDimension],
    policy: SurprisePolicy = SurprisePolicy(),
) -> SurpriseResult:
    ensure_int(policy.total_budget, "total_budget", 0, 10**9)
    ensure_int(policy.max_single_dimension_cost, "max_single_dimension_cost", 0, 10**9)

    normalized: list[NoveltyDimension] = []
    seen: set[str] = set()
    reasons: list[str] = []
    for raw in dimensions:
        name = clean_id(raw.name, "dimension.name")
        if name in seen:
            raise Lo4Error(f"DUPLICATE_DIMENSION:{name}")
        seen.add(name)
        distance = ensure_int(raw.distance_bps, f"{name}.distance_bps", 0, 10_000)
        weight = ensure_int(raw.weight_bps, f"{name}.weight_bps", 0, 10_000)
        if not isinstance(raw.authority, Authority):
            raise Lo4Error(f"{name}.authority:INVALID")
        normalized.append(NoveltyDimension(name, distance, weight, raw.authority))

    normalized.sort(key=lambda d: d.name)
    costs: list[tuple[str, int]] = []
    for d in normalized:
        # Basis-point multiplication rounded up conservatively so novelty is never understated.
        cost = (d.distance_bps * d.weight_bps + 9_999) // 10_000
        costs.append((d.name, cost))
        if d.authority in policy.forbidden_authorities and d.distance_bps > 0:
            reasons.append(f"PROTECTED_AUTHORITY_DRIFT:{d.name}:{d.authority.value}")
        if cost > policy.max_single_dimension_cost:
            reasons.append(f"DIMENSION_BUDGET_EXCEEDED:{d.name}")

    total = sum(cost for _, cost in costs)
    if total > policy.total_budget:
        reasons.append("TOTAL_SURPRISE_BUDGET_EXCEEDED")

    status = Decision.ALLOW_EXPERIMENT if not reasons else Decision.FREEZE
    payload = {
        "status": status.value,
        "total_cost": total,
        "dimension_costs": costs,
        "reason_codes": sorted(reasons),
        "policy": policy,
    }
    return SurpriseResult(status, total, tuple(costs), tuple(sorted(reasons)), fingerprint(payload))

# ===== anti_feature.py =====

from dataclasses import dataclass
from typing import Iterable



@dataclass(frozen=True, slots=True)
class BenefitClaim:
    claim_id: str
    user_value_bps: int
    evidence_level: int


@dataclass(frozen=True, slots=True)
class Alternative:
    alternative_id: str
    coverage_bps: int
    complexity_bps: int
    risk_bps: int
    available: bool = True


@dataclass(frozen=True, slots=True)
class AntiFeaturePolicy:
    min_evidence_level: int = 2
    min_user_value_bps: int = 3_000
    redundancy_coverage_bps: int = 9_000
    complexity_advantage_bps: int = 1_500
    max_risk_bps: int = 7_500


@dataclass(frozen=True, slots=True)
class AntiFeatureResult:
    status: Decision
    reason_codes: tuple[str, ...]
    strongest_alternative: str | None
    aggregate_value_bps: int
    fingerprint: str


def refute_feature(
    claims: Iterable[BenefitClaim],
    proposed_complexity_bps: int,
    proposed_risk_bps: int,
    alternatives: Iterable[Alternative] = (),
    policy: AntiFeaturePolicy = AntiFeaturePolicy(),
) -> AntiFeatureResult:
    proposed_complexity_bps = ensure_int(proposed_complexity_bps, "proposed_complexity_bps", 0, 10_000)
    proposed_risk_bps = ensure_int(proposed_risk_bps, "proposed_risk_bps", 0, 10_000)
    ensure_int(policy.min_evidence_level, "min_evidence_level", 0, 7)
    ensure_int(policy.min_user_value_bps, "min_user_value_bps", 0, 10_000)
    ensure_int(policy.redundancy_coverage_bps, "redundancy_coverage_bps", 0, 10_000)
    ensure_int(policy.complexity_advantage_bps, "complexity_advantage_bps", 0, 10_000)
    ensure_int(policy.max_risk_bps, "max_risk_bps", 0, 10_000)

    clean_claims: list[BenefitClaim] = []
    seen: set[str] = set()
    for c in claims:
        cid = clean_id(c.claim_id, "claim_id")
        if cid in seen:
            raise Lo4Error(f"DUPLICATE_CLAIM:{cid}")
        seen.add(cid)
        clean_claims.append(BenefitClaim(cid, ensure_int(c.user_value_bps, f"{cid}.user_value_bps", 0, 10_000), ensure_int(c.evidence_level, f"{cid}.evidence_level", 0, 7)))
    clean_claims.sort(key=lambda x: x.claim_id)

    reasons: list[str] = []
    evidenced = [c for c in clean_claims if c.evidence_level >= policy.min_evidence_level]
    if not clean_claims or not evidenced:
        reasons.append("USER_VALUE_NOT_EVIDENCED")
        status = Decision.NEED_EVIDENCE
        agg = 0
    else:
        # Conservative aggregate: use strongest evidenced value, not additive storytelling.
        agg = max(c.user_value_bps for c in evidenced)
        status = Decision.KEEP_EXPERIMENT
        if agg < policy.min_user_value_bps:
            reasons.append("INSUFFICIENT_USER_VALUE")
            status = Decision.REJECT_EXPERIMENT
        if proposed_risk_bps > policy.max_risk_bps:
            reasons.append("EXPERIMENTAL_RISK_TOO_HIGH")
            status = Decision.REJECT_EXPERIMENT

    clean_alts: list[Alternative] = []
    for a in alternatives:
        aid = clean_id(a.alternative_id, "alternative_id")
        clean_alts.append(Alternative(
            aid,
            ensure_int(a.coverage_bps, f"{aid}.coverage_bps", 0, 10_000),
            ensure_int(a.complexity_bps, f"{aid}.complexity_bps", 0, 10_000),
            ensure_int(a.risk_bps, f"{aid}.risk_bps", 0, 10_000),
            bool(a.available),
        ))
    clean_alts.sort(key=lambda a: (a.complexity_bps + a.risk_bps, a.alternative_id))

    strongest: str | None = None
    for a in clean_alts:
        if not a.available:
            continue
        if (
            a.coverage_bps >= policy.redundancy_coverage_bps
            and proposed_complexity_bps - a.complexity_bps >= policy.complexity_advantage_bps
            and a.risk_bps <= proposed_risk_bps
        ):
            strongest = a.alternative_id
            reasons.append(f"SIMPLER_ALTERNATIVE_SUBSUMES:{a.alternative_id}")
            if status != Decision.NEED_EVIDENCE:
                status = Decision.REJECT_EXPERIMENT
            break

    payload = {
        "status": status.value,
        "reasons": sorted(reasons),
        "strongest_alternative": strongest,
        "aggregate_value_bps": agg,
        "claims": clean_claims,
        "alternatives": clean_alts,
        "proposed_complexity_bps": proposed_complexity_bps,
        "proposed_risk_bps": proposed_risk_bps,
        "policy": policy,
    }
    return AntiFeatureResult(status, tuple(sorted(reasons)), strongest, agg, fingerprint(payload))

# ===== minimal_relaxation.py =====

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable



@dataclass(frozen=True, slots=True)
class ConstraintRef:
    constraint_id: str
    authority: Authority
    relaxable: bool
    relaxation_cost: int = 1


@dataclass(frozen=True, slots=True)
class ConflictSet:
    conflict_id: str
    constraint_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RelaxationPolicy:
    max_relaxations: int = 8
    max_search_candidates: int = 20


@dataclass(frozen=True, slots=True)
class RelaxationResult:
    status: Decision
    relax_constraint_ids: tuple[str, ...]
    total_cost: int | None
    reason_codes: tuple[str, ...]
    fingerprint: str


def propose_minimal_relaxation(
    constraints: Iterable[ConstraintRef],
    conflicts: Iterable[ConflictSet],
    policy: RelaxationPolicy = RelaxationPolicy(),
) -> RelaxationResult:
    ensure_int(policy.max_relaxations, "max_relaxations", 0, 64)
    ensure_int(policy.max_search_candidates, "max_search_candidates", 1, 128)

    cmap: dict[str, ConstraintRef] = {}
    for c in constraints:
        cid = clean_id(c.constraint_id, "constraint_id")
        if cid in cmap:
            raise Lo4Error(f"DUPLICATE_CONSTRAINT:{cid}")
        if not isinstance(c.authority, Authority):
            raise Lo4Error(f"{cid}.authority:INVALID")
        cmap[cid] = ConstraintRef(cid, c.authority, bool(c.relaxable), ensure_int(c.relaxation_cost, f"{cid}.relaxation_cost", 0, 10**9))

    clean_conflicts: list[ConflictSet] = []
    for cs in conflicts:
        xid = clean_id(cs.conflict_id, "conflict_id")
        ids = tuple(sorted({clean_id(i, f"{xid}.constraint_id") for i in cs.constraint_ids}))
        if not ids:
            raise Lo4Error(f"{xid}:EMPTY_CONFLICT")
        unknown = [i for i in ids if i not in cmap]
        if unknown:
            raise Lo4Error(f"{xid}:UNKNOWN_CONSTRAINT:{unknown[0]}")
        clean_conflicts.append(ConflictSet(xid, ids))
    clean_conflicts.sort(key=lambda x: x.conflict_id)

    if not clean_conflicts:
        result = RelaxationResult(Decision.PLAN, (), 0, ("NO_CONFLICT",), "")
        payload = {"status": result.status.value, "relax": (), "cost": 0, "reasons": result.reason_codes}
        return RelaxationResult(result.status, result.relax_constraint_ids, result.total_cost, result.reason_codes, fingerprint(payload))

    reasons: list[str] = []
    relaxable_ids = sorted(
        cid for cid, c in cmap.items()
        if c.authority == Authority.EXPERIMENTAL and c.relaxable
    )

    for cs in clean_conflicts:
        if not any(cid in relaxable_ids for cid in cs.constraint_ids):
            reasons.append(f"UNRELAXABLE_CONFLICT:{cs.conflict_id}")

    if reasons:
        payload = {"status": Decision.FREEZE.value, "reasons": sorted(reasons), "conflicts": clean_conflicts}
        return RelaxationResult(Decision.FREEZE, (), None, tuple(sorted(reasons)), fingerprint(payload))

    if len(relaxable_ids) > policy.max_search_candidates:
        reasons.append("SEARCH_BOUND_EXCEEDED")
        payload = {"status": Decision.FREEZE.value, "reasons": reasons, "candidate_count": len(relaxable_ids)}
        return RelaxationResult(Decision.FREEZE, (), None, tuple(reasons), fingerprint(payload))

    best: tuple[int, int, tuple[str, ...]] | None = None
    limit = min(policy.max_relaxations, len(relaxable_ids))
    for size in range(1, limit + 1):
        for combo in combinations(relaxable_ids, size):
            chosen = set(combo)
            if not all(chosen.intersection(cs.constraint_ids) for cs in clean_conflicts):
                continue
            cost = sum(cmap[cid].relaxation_cost for cid in combo)
            candidate = (cost, size, combo)
            if best is None or candidate < best:
                best = candidate
        # We cannot stop solely on size because a larger set could have lower weighted cost.

    if best is None:
        reasons.append("NO_RELAXATION_WITHIN_BOUND")
        payload = {"status": Decision.FREEZE.value, "reasons": reasons, "limit": limit}
        return RelaxationResult(Decision.FREEZE, (), None, tuple(reasons), fingerprint(payload))

    cost, _, combo = best
    reasons.append("PROPOSAL_ONLY_NO_AUTOMATIC_MUTATION")
    payload = {
        "status": Decision.PROPOSE_RELAXATION.value,
        "relax": combo,
        "cost": cost,
        "reasons": sorted(reasons),
        "conflicts": clean_conflicts,
    }
    return RelaxationResult(Decision.PROPOSE_RELAXATION, combo, cost, tuple(sorted(reasons)), fingerprint(payload))

# ===== regret_envelope.py =====

from dataclasses import dataclass
from typing import Iterable, Mapping



@dataclass(frozen=True, slots=True)
class ActionCandidate:
    action_id: str
    reversible: bool
    requires_human_approval: bool
    hard_constraints_satisfied: bool
    utility_by_scenario: Mapping[str, int]


@dataclass(frozen=True, slots=True)
class RegretPolicy:
    max_worst_case_regret: int = 2_500
    allow_irreversible_with_human_approval: bool = True


@dataclass(frozen=True, slots=True)
class ActionRegret:
    action_id: str
    worst_case_regret: int
    total_regret: int


@dataclass(frozen=True, slots=True)
class RegretResult:
    status: Decision
    selected_action_id: str | None
    action_regrets: tuple[ActionRegret, ...]
    reason_codes: tuple[str, ...]
    fingerprint: str


def choose_minimax_regret(
    actions: Iterable[ActionCandidate],
    policy: RegretPolicy = RegretPolicy(),
) -> RegretResult:
    ensure_int(policy.max_worst_case_regret, "max_worst_case_regret", 0, 10**12)
    clean: list[ActionCandidate] = []
    seen: set[str] = set()
    scenario_set: set[str] | None = None

    for a in actions:
        aid = clean_id(a.action_id, "action_id")
        if aid in seen:
            raise Lo4Error(f"DUPLICATE_ACTION:{aid}")
        seen.add(aid)
        utilities: dict[str, int] = {}
        for sid, utility in a.utility_by_scenario.items():
            sid2 = clean_id(sid, f"{aid}.scenario")
            utilities[sid2] = ensure_int(utility, f"{aid}.{sid2}.utility", -10**9, 10**9)
        if not utilities:
            raise Lo4Error(f"{aid}:NO_SCENARIOS")
        sids = set(utilities)
        if scenario_set is None:
            scenario_set = sids
        elif scenario_set != sids:
            raise Lo4Error("SCENARIO_SET_MISMATCH")
        clean.append(ActionCandidate(aid, bool(a.reversible), bool(a.requires_human_approval), bool(a.hard_constraints_satisfied), utilities))

    if not clean:
        raise Lo4Error("NO_ACTIONS")
    clean.sort(key=lambda a: a.action_id)
    assert scenario_set is not None

    eligible: list[ActionCandidate] = []
    reasons: list[str] = []
    for a in clean:
        if not a.hard_constraints_satisfied:
            reasons.append(f"HARD_CONSTRAINT_BLOCK:{a.action_id}")
            continue
        if not a.reversible:
            if not (policy.allow_irreversible_with_human_approval and a.requires_human_approval):
                reasons.append(f"IRREVERSIBLE_WITHOUT_HUMAN_GATE:{a.action_id}")
                continue
        eligible.append(a)

    if not eligible:
        payload = {"status": Decision.FREEZE.value, "reasons": sorted(reasons)}
        return RegretResult(Decision.FREEZE, None, (), tuple(sorted(reasons)), fingerprint(payload))

    # Best utility per scenario uses only eligible actions, preventing illegal actions from defining regret.
    best_by_scenario = {
        sid: max(a.utility_by_scenario[sid] for a in eligible)
        for sid in sorted(scenario_set)
    }
    regrets: list[ActionRegret] = []
    for a in eligible:
        rs = [best_by_scenario[sid] - a.utility_by_scenario[sid] for sid in sorted(scenario_set)]
        regrets.append(ActionRegret(a.action_id, max(rs), sum(rs)))
    regrets.sort(key=lambda r: (r.worst_case_regret, r.total_regret, r.action_id))

    winner = regrets[0]
    if winner.worst_case_regret > policy.max_worst_case_regret:
        reasons.append("REGRET_THRESHOLD_EXCEEDED")
        status = Decision.FREEZE
        selected = None
    else:
        status = Decision.PLAN
        selected = winner.action_id

    payload = {
        "status": status.value,
        "selected": selected,
        "regrets": regrets,
        "reasons": sorted(reasons),
        "policy": policy,
    }
    return RegretResult(status, selected, tuple(regrets), tuple(sorted(reasons)), fingerprint(payload))

# ===== option_preservation.py =====

from dataclasses import dataclass
from typing import Iterable



@dataclass(frozen=True, slots=True)
class FutureOption:
    option_id: str
    importance_bps: int


@dataclass(frozen=True, slots=True)
class ArchitectureChoice:
    choice_id: str
    hard_constraints_satisfied: bool
    preserved_options: tuple[str, ...]
    switching_cost_bps: int
    lock_in_bps: int
    current_value_bps: int


@dataclass(frozen=True, slots=True)
class OptionPolicy:
    future_weight_bps: int = 5_000
    switching_penalty_bps: int = 2_500
    lock_in_penalty_bps: int = 2_500
    min_score: int = 0


@dataclass(frozen=True, slots=True)
class OptionScore:
    choice_id: str
    score: int
    preserved_importance: int


@dataclass(frozen=True, slots=True)
class OptionResult:
    status: Decision
    selected_choice_id: str | None
    scores: tuple[OptionScore, ...]
    reason_codes: tuple[str, ...]
    fingerprint: str


def select_option_preserving_choice(
    future_options: Iterable[FutureOption],
    choices: Iterable[ArchitectureChoice],
    policy: OptionPolicy = OptionPolicy(),
) -> OptionResult:
    for field, value in (
        ("future_weight_bps", policy.future_weight_bps),
        ("switching_penalty_bps", policy.switching_penalty_bps),
        ("lock_in_penalty_bps", policy.lock_in_penalty_bps),
    ):
        ensure_int(value, field, 0, 10_000)
    ensure_int(policy.min_score, "min_score", -10**12, 10**12)

    options: dict[str, int] = {}
    for o in future_options:
        oid = clean_id(o.option_id, "option_id")
        if oid in options:
            raise Lo4Error(f"DUPLICATE_OPTION:{oid}")
        options[oid] = ensure_int(o.importance_bps, f"{oid}.importance_bps", 0, 10_000)
    if not options:
        raise Lo4Error("NO_FUTURE_OPTIONS")

    clean_choices: list[ArchitectureChoice] = []
    seen: set[str] = set()
    for c in choices:
        cid = clean_id(c.choice_id, "choice_id")
        if cid in seen:
            raise Lo4Error(f"DUPLICATE_CHOICE:{cid}")
        seen.add(cid)
        preserved = tuple(sorted({clean_id(x, f"{cid}.preserved_option") for x in c.preserved_options}))
        unknown = [x for x in preserved if x not in options]
        if unknown:
            raise Lo4Error(f"{cid}:UNKNOWN_OPTION:{unknown[0]}")
        clean_choices.append(ArchitectureChoice(
            cid,
            bool(c.hard_constraints_satisfied),
            preserved,
            ensure_int(c.switching_cost_bps, f"{cid}.switching_cost_bps", 0, 10_000),
            ensure_int(c.lock_in_bps, f"{cid}.lock_in_bps", 0, 10_000),
            ensure_int(c.current_value_bps, f"{cid}.current_value_bps", 0, 10_000),
        ))
    clean_choices.sort(key=lambda c: c.choice_id)

    reasons: list[str] = []
    eligible = [c for c in clean_choices if c.hard_constraints_satisfied]
    for c in clean_choices:
        if not c.hard_constraints_satisfied:
            reasons.append(f"HARD_CONSTRAINT_BLOCK:{c.choice_id}")
    if not eligible:
        payload = {"status": Decision.FREEZE.value, "reasons": sorted(reasons)}
        return OptionResult(Decision.FREEZE, None, (), tuple(sorted(reasons)), fingerprint(payload))

    total_importance = sum(options.values()) or 1
    scores: list[OptionScore] = []
    for c in eligible:
        preserved_importance = sum(options[x] for x in c.preserved_options)
        normalized_future = (preserved_importance * 10_000) // total_importance
        future_component = (normalized_future * policy.future_weight_bps) // 10_000
        switching_penalty = (c.switching_cost_bps * policy.switching_penalty_bps) // 10_000
        lock_penalty = (c.lock_in_bps * policy.lock_in_penalty_bps) // 10_000
        score = c.current_value_bps + future_component - switching_penalty - lock_penalty
        scores.append(OptionScore(c.choice_id, score, preserved_importance))
    scores.sort(key=lambda x: (-x.score, -x.preserved_importance, x.choice_id))

    winner = scores[0]
    if winner.score < policy.min_score:
        reasons.append("OPTION_VALUE_BELOW_THRESHOLD")
        status = Decision.FREEZE
        selected = None
    else:
        status = Decision.PLAN
        selected = winner.choice_id

    payload = {"status": status.value, "selected": selected, "scores": scores, "reasons": sorted(reasons), "policy": policy}
    return OptionResult(status, selected, tuple(scores), tuple(sorted(reasons)), fingerprint(payload))

# ===== pipeline.py =====

from dataclasses import dataclass



@dataclass(frozen=True, slots=True)
class FoundryResult:
    status: Decision
    stage: str
    reason_codes: tuple[str, ...]
    fingerprint: str


def integrate_foundry(
    surprise: SurpriseResult,
    anti_feature: AntiFeatureResult,
    relaxation: RelaxationResult,
    regret: RegretResult,
    option: OptionResult,
) -> FoundryResult:
    """Fail-closed integration gate. It never promotes to Canon; it only admits an Lo4 experiment plan."""
    stages = (
        ("surprise_budget", surprise.status, surprise.reason_codes, {Decision.ALLOW_EXPERIMENT}),
        ("anti_feature", anti_feature.status, anti_feature.reason_codes, {Decision.KEEP_EXPERIMENT}),
        # A clean plan or an explicit proposal-only relaxation may continue to human review.
        ("minimal_relaxation", relaxation.status, relaxation.reason_codes, {Decision.PLAN, Decision.PROPOSE_RELAXATION}),
        ("regret_envelope", regret.status, regret.reason_codes, {Decision.PLAN}),
        ("option_preservation", option.status, option.reason_codes, {Decision.PLAN}),
    )
    for name, status, reasons, allowed in stages:
        if status not in allowed:
            payload = {"status": Decision.FREEZE.value, "stage": name, "reasons": reasons}
            return FoundryResult(Decision.FREEZE, name, tuple(reasons), fingerprint(payload))

    reasons_list = [
        "LO4_ONLY_NOT_CANON",
        "HUMAN_OR_FORMAL_PROMOTION_REQUIRED",
        "NO_AUTOMATIC_AUTHORITY_ESCALATION",
    ]
    if relaxation.status == Decision.PROPOSE_RELAXATION:
        reasons_list.append("EXPERIMENTAL_RELAXATION_REVIEW_REQUIRED")
    reasons = tuple(sorted(reasons_list))
    payload = {"status": Decision.PLAN.value, "stage": "lo4_experiment_ready", "reasons": reasons}
    return FoundryResult(Decision.PLAN, "lo4_experiment_ready", reasons, fingerprint(payload))
