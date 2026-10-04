"""NEXY Independent Assurance Five-Pack.

AI-PROPOSED reference implementation only. This file is intentionally standalone
and has no dependency on the NEXY.AI implementation repository.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import FrozenSet, Iterable, Literal

# ---------------------------------------------------------------------------
# 1) IAQ — Independence-Aware Quorum
# ---------------------------------------------------------------------------
Verdict = Literal["PASS", "FAIL", "FREEZE"]


@dataclass(frozen=True, slots=True)
class AgentVote:
    agent_id: str
    verdict: Verdict
    provider: str
    model_family: str
    data_lineage: FrozenSet[str]
    toolchain_fingerprint: str
    weight: float = 1.0

    def __post_init__(self) -> None:
        if not self.agent_id.strip():
            raise ValueError("agent_id must be non-empty")
        if self.verdict not in {"PASS", "FAIL", "FREEZE"}:
            raise ValueError(f"unsupported verdict: {self.verdict}")
        if self.weight <= 0:
            raise ValueError("weight must be > 0")


@dataclass(frozen=True, slots=True)
class QuorumPolicy:
    min_independent_clusters: int = 2
    min_support_ratio: float = 2 / 3
    lineage_overlap_threshold: float = 0.5
    correlate_same_provider_and_family: bool = True
    correlate_same_toolchain: bool = True
    allow_independent_failures: bool = False

    def __post_init__(self) -> None:
        if self.min_independent_clusters < 1:
            raise ValueError("min_independent_clusters must be >= 1")
        if not 0.0 <= self.min_support_ratio <= 1.0:
            raise ValueError("min_support_ratio must be in [0, 1]")
        if not 0.0 <= self.lineage_overlap_threshold <= 1.0:
            raise ValueError("lineage_overlap_threshold must be in [0, 1]")


@dataclass(frozen=True, slots=True)
class QuorumResult:
    verdict: Verdict
    independent_clusters: int
    pass_clusters: int
    fail_clusters: int
    freeze_clusters: int
    support_ratio: float
    clusters: tuple[tuple[str, ...], ...]
    reasons: tuple[str, ...]


class _DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, item: int) -> int:
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, left: int, right: int) -> None:
        a, b = self.find(left), self.find(right)
        if a == b:
            return
        if self.rank[a] < self.rank[b]:
            a, b = b, a
        self.parent[b] = a
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1


def _jaccard(left: FrozenSet[str], right: FrozenSet[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def _votes_correlated(left: AgentVote, right: AgentVote, policy: QuorumPolicy) -> bool:
    if policy.correlate_same_provider_and_family and (
        left.provider == right.provider and left.model_family == right.model_family
    ):
        return True
    if policy.correlate_same_toolchain and left.toolchain_fingerprint and (
        left.toolchain_fingerprint == right.toolchain_fingerprint
    ):
        return True
    overlap = _jaccard(left.data_lineage, right.data_lineage)
    return overlap > 0.0 and overlap >= policy.lineage_overlap_threshold


def evaluate_quorum(votes: Iterable[AgentVote], policy: QuorumPolicy | None = None) -> QuorumResult:
    policy = policy or QuorumPolicy()
    items = tuple(votes)
    if not items:
        return QuorumResult("FREEZE", 0, 0, 0, 0, 0.0, (), ("no-votes",))
    ids = [vote.agent_id for vote in items]
    if len(ids) != len(set(ids)):
        raise ValueError("agent_id values must be unique within one quorum")

    dsu = _DisjointSet(len(items))
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if _votes_correlated(items[i], items[j], policy):
                dsu.union(i, j)

    grouped: dict[int, list[AgentVote]] = {}
    for index, vote in enumerate(items):
        grouped.setdefault(dsu.find(index), []).append(vote)
    groups = sorted(grouped.values(), key=lambda g: tuple(sorted(v.agent_id for v in g)))

    cluster_verdicts: list[Verdict] = []
    for group in groups:
        if any(v.verdict == "FAIL" for v in group):
            cluster_verdicts.append("FAIL")
        elif all(v.verdict == "PASS" for v in group):
            cluster_verdicts.append("PASS")
        else:
            cluster_verdicts.append("FREEZE")

    total = len(groups)
    passed = cluster_verdicts.count("PASS")
    failed = cluster_verdicts.count("FAIL")
    frozen = cluster_verdicts.count("FREEZE")
    ratio = passed / total if total else 0.0
    reasons: list[str] = []
    if total < policy.min_independent_clusters:
        reasons.append("insufficient-independent-clusters")
    if ratio < policy.min_support_ratio:
        reasons.append("insufficient-independent-support")
    if failed and not policy.allow_independent_failures:
        reasons.append("independent-failure-present")
    if frozen:
        reasons.append("unresolved-cluster-present")
    return QuorumResult(
        "PASS" if not reasons else "FREEZE",
        total,
        passed,
        failed,
        frozen,
        ratio,
        tuple(tuple(sorted(v.agent_id for v in g)) for g in groups),
        tuple(reasons),
    )


# ---------------------------------------------------------------------------
# 2) ECG — Evidence Contamination Guard
# ---------------------------------------------------------------------------
EvidenceStatus = Literal["CLEAN", "CONTAMINATED", "INDETERMINATE"]


@dataclass(frozen=True, slots=True)
class EvidenceClaim:
    claim_id: str
    target_artifacts: FrozenSet[str]
    oracle_artifacts: FrozenSet[str]
    derivation_edges: tuple[tuple[str, str], ...] = ()
    trusted_roots: FrozenSet[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.claim_id.strip() or not self.target_artifacts or not self.oracle_artifacts:
            raise ValueError("claim_id, target_artifacts and oracle_artifacts are required")
        if any(not child or not parent for child, parent in self.derivation_edges):
            raise ValueError("derivation edge endpoints must be non-empty")


@dataclass(frozen=True, slots=True)
class ContaminationResult:
    status: EvidenceStatus
    reasons: tuple[str, ...]
    shared_untrusted_roots: tuple[str, ...]
    cycles: tuple[tuple[str, ...], ...]


def _lineage_graph(edges: Iterable[tuple[str, str]]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    for child, parent in edges:
        graph.setdefault(child, set()).add(parent)
        graph.setdefault(parent, set())
    return graph


def _lineage_cycles(graph: dict[str, set[str]]) -> tuple[tuple[str, ...], ...]:
    state: dict[str, int] = {}
    stack: list[str] = []
    found: set[tuple[str, ...]] = set()

    def visit(node: str) -> None:
        state[node] = 1
        stack.append(node)
        for parent in sorted(graph.get(node, ())):
            if state.get(parent, 0) == 0:
                visit(parent)
            elif state.get(parent) == 1:
                start = stack.index(parent)
                found.add(tuple(stack[start:] + [parent]))
        stack.pop()
        state[node] = 2

    for node in sorted(graph):
        if state.get(node, 0) == 0:
            visit(node)
    return tuple(sorted(found))


def _ancestors(node: str, graph: dict[str, set[str]]) -> set[str]:
    seen: set[str] = set()
    pending = list(graph.get(node, ()))
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)
        pending.extend(graph.get(current, ()))
    return seen


def _roots(node: str, graph: dict[str, set[str]]) -> set[str]:
    roots: set[str] = set()
    seen: set[str] = set()
    pending = [node]
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)
        parents = graph.get(current, set())
        if parents:
            pending.extend(parents)
        else:
            roots.add(current)
    return roots


def analyze_evidence(claim: EvidenceClaim) -> ContaminationResult:
    graph = _lineage_graph(claim.derivation_edges)
    for node in claim.target_artifacts | claim.oracle_artifacts | claim.trusted_roots:
        graph.setdefault(node, set())
    cycles = _lineage_cycles(graph)
    if cycles:
        return ContaminationResult("INDETERMINATE", ("lineage-cycle",), (), cycles)

    reasons: list[str] = []
    if claim.target_artifacts & claim.oracle_artifacts:
        reasons.append("target-oracle-overlap")
    if any(_ancestors(oracle, graph) & claim.target_artifacts for oracle in claim.oracle_artifacts):
        reasons.append("oracle-derived-from-target")

    target_roots = set().union(*(_roots(x, graph) for x in claim.target_artifacts))
    oracle_roots = set().union(*(_roots(x, graph) for x in claim.oracle_artifacts))
    shared = tuple(sorted((target_roots & oracle_roots) - claim.trusted_roots))
    reasons.extend(f"shared-untrusted-root:{root}" for root in shared)
    return ContaminationResult(
        "CONTAMINATED" if reasons else "CLEAN",
        tuple(dict.fromkeys(reasons)),
        shared,
        (),
    )


# ---------------------------------------------------------------------------
# 3) RAAS — Risk-Adaptive Assurance Scheduler
# ---------------------------------------------------------------------------
EvidenceClass = Literal["E1", "E2", "E3", "E4", "E5", "E6"]
Disposition = Literal["ALLOW_WITH_ASSURANCE", "FREEZE"]


@dataclass(frozen=True, slots=True)
class ActionRisk:
    impact: int
    irreversibility: int
    externality: int
    sensitivity: int
    production: bool = False
    permission_change: bool = False
    compensation_available: bool = True

    def __post_init__(self) -> None:
        for name in ("impact", "irreversibility", "externality", "sensitivity"):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 5:
                raise ValueError(f"{name} must be an integer in [0, 5]")


@dataclass(frozen=True, slots=True)
class AssurancePolicy:
    confirmation_impact_threshold: int = 4
    confirmation_irreversibility_threshold: int = 3
    independent_quorum_impact_threshold: int = 4
    freeze_irreversible_without_compensation: bool = True


@dataclass(frozen=True, slots=True)
class AssurancePlan:
    disposition: Disposition
    risk_score: int
    required_evidence: EvidenceClass
    explicit_confirmation_required: bool
    rollback_or_compensation_required: bool
    independent_quorum_required: bool
    negative_path_tests_required: bool
    reasons: tuple[str, ...]


def plan_assurance(risk: ActionRisk, policy: AssurancePolicy | None = None) -> AssurancePlan:
    policy = policy or AssurancePolicy()
    score = (
        risk.impact * 2
        + risk.irreversibility * 2
        + risk.externality
        + risk.sensitivity
        + (3 if risk.production else 0)
        + (2 if risk.permission_change else 0)
    )
    if risk.production and (risk.impact >= 4 or risk.irreversibility >= 4):
        evidence: EvidenceClass = "E6"
    elif score <= 3:
        evidence = "E1"
    elif score <= 6:
        evidence = "E2"
    elif score <= 9:
        evidence = "E3"
    elif score <= 12:
        evidence = "E4"
    elif score <= 17:
        evidence = "E5"
    else:
        evidence = "E6"

    confirmation = (
        risk.impact >= policy.confirmation_impact_threshold
        and risk.irreversibility >= policy.confirmation_irreversibility_threshold
    ) or risk.permission_change
    independent = (
        risk.impact >= policy.independent_quorum_impact_threshold
        or risk.externality >= 4
        or risk.permission_change
    )
    rollback = score >= 10 or risk.irreversibility >= 3
    negative = score >= 7 or risk.production or risk.permission_change
    freeze = (
        policy.freeze_irreversible_without_compensation
        and risk.impact >= 4
        and risk.irreversibility >= 4
        and not risk.compensation_available
    )
    reasons = tuple(
        reason
        for enabled, reason in (
            (confirmation, "explicit-confirmation-required"),
            (independent, "independent-quorum-required"),
            (rollback, "rollback-or-compensation-required"),
            (negative, "negative-path-tests-required"),
            (freeze, "irreversible-high-impact-without-compensation"),
        )
        if enabled
    )
    return AssurancePlan(
        "FREEZE" if freeze else "ALLOW_WITH_ASSURANCE",
        score,
        evidence,
        confirmation,
        rollback,
        independent,
        negative,
        reasons,
    )


# ---------------------------------------------------------------------------
# 4) CTR — Capability Tombstone Registry
# ---------------------------------------------------------------------------
RegistryAction = Literal["RETIRE", "RESTORE"]


@dataclass(frozen=True, slots=True)
class CapabilityCandidate:
    capability_id: str
    snapshot_epoch: int

    def __post_init__(self) -> None:
        if not self.capability_id.strip() or self.snapshot_epoch < 0:
            raise ValueError("capability_id must be non-empty and snapshot_epoch >= 0")


@dataclass(frozen=True, slots=True)
class RegistryEvent:
    capability_id: str
    epoch: int
    action: RegistryAction
    reason: str
    replacement: str | None = None


@dataclass(frozen=True, slots=True)
class AdmissionResult:
    allowed: bool
    reason: str
    governing_epoch: int | None = None
    replacement: str | None = None


class TombstoneRegistry:
    def __init__(self) -> None:
        self._events: list[RegistryEvent] = []

    def _latest(self, capability_id: str) -> RegistryEvent | None:
        items = [e for e in self._events if e.capability_id == capability_id]
        return max(items, key=lambda e: e.epoch) if items else None

    def retire(self, capability_id: str, epoch: int, reason: str, replacement: str | None = None) -> None:
        capability_id = capability_id.strip()
        if not capability_id or epoch < 0 or not reason.strip():
            raise ValueError("invalid retirement event")
        if replacement is not None:
            replacement = replacement.strip()
            if not replacement or replacement == capability_id:
                raise ValueError("replacement must be non-empty and different")
        latest = self._latest(capability_id)
        if latest and epoch <= latest.epoch:
            raise ValueError("epoch must strictly increase")
        self._events.append(RegistryEvent(capability_id, epoch, "RETIRE", reason.strip(), replacement))

    def restore(self, capability_id: str, epoch: int, reason: str) -> None:
        capability_id = capability_id.strip()
        latest = self._latest(capability_id)
        if not latest or latest.action != "RETIRE" or epoch <= latest.epoch or not reason.strip():
            raise ValueError("restore requires a newer epoch after active retirement")
        self._events.append(RegistryEvent(capability_id, epoch, "RESTORE", reason.strip()))

    def admit(self, candidate: CapabilityCandidate) -> AdmissionResult:
        latest = self._latest(candidate.capability_id)
        if not latest:
            return AdmissionResult(True, "not-tombstoned")
        if latest.action == "RETIRE":
            return AdmissionResult(False, "tombstoned", latest.epoch, latest.replacement)
        if candidate.snapshot_epoch < latest.epoch:
            return AdmissionResult(False, "snapshot-predates-restoration", latest.epoch)
        return AdmissionResult(True, "explicitly-restored", latest.epoch)

    def digest(self) -> str:
        payload = [
            asdict(event)
            for event in sorted(self._events, key=lambda e: (e.capability_id, e.epoch, e.action))
        ]
        raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        return sha256(raw).hexdigest()


# ---------------------------------------------------------------------------
# 5) AIG — Attention Integrity Governor
# ---------------------------------------------------------------------------
Severity = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
AttentionAction = Literal["DELIVER", "SUPPRESS", "COALESCE"]


@dataclass(frozen=True, slots=True)
class Alert:
    semantic_key: str
    severity: Severity
    evidence_fingerprint: str
    state_fingerprint: str
    timestamp: int

    def __post_init__(self) -> None:
        if not self.semantic_key.strip() or not self.evidence_fingerprint or not self.state_fingerprint:
            raise ValueError("alert identity/evidence/state must be non-empty")
        if self.severity not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"} or self.timestamp < 0:
            raise ValueError("invalid severity or timestamp")


@dataclass(frozen=True, slots=True)
class AttentionPolicy:
    dedup_window_seconds: int = 300
    budget_window_seconds: int = 60
    max_noncritical_per_window: int = 5

    def __post_init__(self) -> None:
        if self.dedup_window_seconds < 0 or self.budget_window_seconds <= 0 or self.max_noncritical_per_window < 0:
            raise ValueError("invalid attention policy")


@dataclass(frozen=True, slots=True)
class AttentionDecision:
    action: AttentionAction
    reason: str


class AttentionGovernor:
    def __init__(self, policy: AttentionPolicy | None = None) -> None:
        self.policy = policy or AttentionPolicy()
        self._last_by_key: dict[str, Alert] = {}
        self._noncritical_deliveries: list[int] = []
        self._last_timestamp: int | None = None

    def decide(self, alert: Alert) -> AttentionDecision:
        if self._last_timestamp is not None and alert.timestamp < self._last_timestamp:
            raise ValueError("alerts must be processed in non-decreasing timestamp order")
        self._last_timestamp = alert.timestamp
        previous = self._last_by_key.get(alert.semantic_key)

        if alert.severity == "CRITICAL" and previous and previous.state_fingerprint != alert.state_fingerprint:
            self._last_by_key[alert.semantic_key] = alert
            return AttentionDecision("DELIVER", "critical-state-changed")

        if previous:
            exact_duplicate = (
                previous.state_fingerprint == alert.state_fingerprint
                and previous.evidence_fingerprint == alert.evidence_fingerprint
            )
            if exact_duplicate and alert.timestamp - previous.timestamp <= self.policy.dedup_window_seconds:
                return AttentionDecision("SUPPRESS", "duplicate-within-dedup-window")

        if alert.severity != "CRITICAL":
            cutoff = alert.timestamp - self.policy.budget_window_seconds
            self._noncritical_deliveries = [t for t in self._noncritical_deliveries if t > cutoff]
            if len(self._noncritical_deliveries) >= self.policy.max_noncritical_per_window:
                return AttentionDecision("COALESCE", "noncritical-attention-budget-exhausted")
            self._noncritical_deliveries.append(alert.timestamp)

        self._last_by_key[alert.semantic_key] = alert
        return AttentionDecision("DELIVER", "new-or-materially-changed")
