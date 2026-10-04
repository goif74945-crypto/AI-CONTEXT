from __future__ import annotations

from typing import Any, Iterable, Sequence

from .models import (
    DATA_CLASS_RANK,
    AgentProfile,
    AllocationPlan,
    ContractError,
    Elimination,
    GovernorDecision,
    GovernorPolicy,
    RiskTier,
    TaskProfile,
    _CandidatePlan,
)


class ResourceGovernor:
    """
    Deterministic advisory resource planner.

    The governor can select a feasible worker/verifier allocation, but it cannot
    prove correctness or satisfy the required evidence class merely by planning.
    Every successful plan therefore carries verification_status=NOT_VERIFIED.
    """

    def __init__(self, policy: GovernorPolicy | None = None) -> None:
        self._policy = policy or GovernorPolicy()

    @property
    def policy(self) -> GovernorPolicy:
        return self._policy

    def plan(self, task: TaskProfile, agents: Sequence[AgentProfile]) -> GovernorDecision:
        ordered_agents = tuple(sorted(agents, key=lambda agent: agent.agent_id))
        self._validate_unique_agent_ids(ordered_agents)

        independent_required = (
            task.require_independent_verifier
            or task.risk_tier in self._policy.independence_required_risk
        )
        verifier_required = (
            independent_required
            or task.required_evidence_class >= self._policy.verifier_required_from_evidence_class
        )

        policy_trace = (
            f"required_evidence=E{task.required_evidence_class}",
            f"verifier_required={str(verifier_required).lower()}",
            f"independent_verifier_required={str(independent_required).lower()}",
            f"risk_tier={task.risk_tier.value}",
            f"data_class={task.data_class.value}",
            "planning_does_not_equal_verification",
        )

        eliminations: list[Elimination] = []
        workers: list[AgentProfile] = []
        verifiers: list[AgentProfile] = []

        for agent in ordered_agents:
            worker_reasons = self._worker_reasons(task, agent)
            if not worker_reasons:
                workers.append(agent)
            elif "worker" in agent.roles:
                eliminations.append(Elimination("worker", agent.agent_id, tuple(worker_reasons)))

            if verifier_required:
                verifier_reasons = self._verifier_reasons(task, agent)
                if not verifier_reasons:
                    verifiers.append(agent)
                elif "verifier" in agent.roles:
                    eliminations.append(Elimination("verifier", agent.agent_id, tuple(verifier_reasons)))

        if not workers:
            return self._freeze(
                task,
                independent_required,
                verifier_required,
                ("NO_ELIGIBLE_WORKER",),
                eliminations,
                policy_trace,
            )

        if verifier_required and not verifiers:
            return self._freeze(
                task,
                independent_required,
                verifier_required,
                ("NO_ELIGIBLE_VERIFIER",),
                eliminations,
                policy_trace,
            )

        selected: _CandidatePlan | None = None
        selected_key: tuple[Any, ...] | None = None
        pair_rejection_reasons: set[str] = set()
        pair_diagnostics = 0

        for worker in workers:
            verifier_options: Iterable[AgentProfile | None] = verifiers if verifier_required else (None,)
            for verifier in verifier_options:
                candidate = self._build_candidate(task, worker, verifier)
                reasons = self._candidate_reasons(task, candidate, independent_required)
                if reasons:
                    pair_rejection_reasons.update(reasons)
                    if pair_diagnostics < self._policy.max_pair_diagnostics:
                        subject = f"{worker.agent_id}+{verifier.agent_id if verifier else 'none'}"
                        eliminations.append(Elimination("pair", subject, tuple(reasons)))
                        pair_diagnostics += 1
                    continue

                candidate_key = self._ranking_key(candidate)
                if selected is None or selected_key is None or candidate_key < selected_key:
                    selected = candidate
                    selected_key = candidate_key

        if selected is None:
            reasons = tuple(sorted(pair_rejection_reasons)) or ("NO_FEASIBLE_ALLOCATION",)
            return self._freeze(
                task,
                independent_required,
                verifier_required,
                reasons,
                eliminations,
                policy_trace,
            )
        plan = AllocationPlan(
            worker_id=selected.worker.agent_id,
            verifier_id=selected.verifier.agent_id if selected.verifier is not None else None,
            estimated_total_tokens=selected.total_tokens,
            estimated_cost_microunits=selected.cost_microunits,
            estimated_latency_ms=selected.latency_ms,
            optimization_quality_bps=selected.quality_bps,
            required_evidence_class=task.required_evidence_class,
        )
        return GovernorDecision(
            task_id=task.task_id,
            decision="PLAN_READY",
            plan=plan,
            effective_independent_verifier_required=independent_required,
            effective_verifier_required=verifier_required,
            freeze_reasons=(),
            eliminations=tuple(eliminations),
            policy_trace=policy_trace,
        )

    @staticmethod
    def _validate_unique_agent_ids(agents: Sequence[AgentProfile]) -> None:
        seen: set[str] = set()
        duplicates: set[str] = set()
        for agent in agents:
            if agent.agent_id in seen:
                duplicates.add(agent.agent_id)
            seen.add(agent.agent_id)
        if duplicates:
            raise ContractError(f"duplicate agent_id values: {sorted(duplicates)}")

    @staticmethod
    def _common_reasons(task: TaskProfile, agent: AgentProfile) -> list[str]:
        reasons: list[str] = []
        if not agent.active:
            reasons.append("AGENT_INACTIVE")
        if agent.quarantined:
            reasons.append("AGENT_QUARANTINED")
        if DATA_CLASS_RANK[agent.clearance] < DATA_CLASS_RANK[task.data_class]:
            reasons.append("DATA_CLEARANCE_INSUFFICIENT")
        return reasons

    def _worker_reasons(self, task: TaskProfile, agent: AgentProfile) -> list[str]:
        reasons = self._common_reasons(task, agent)
        if "worker" not in agent.roles:
            reasons.append("ROLE_WORKER_MISSING")
        if not task.required_capabilities.issubset(agent.capabilities):
            reasons.append("REQUIRED_CAPABILITY_MISSING")
        required_context = task.worker_input_tokens + task.worker_output_tokens
        if agent.max_context_tokens < required_context:
            reasons.append("WORKER_CONTEXT_INSUFFICIENT")
        if agent.quality_bps < task.min_quality_bps:
            reasons.append("QUALITY_FLOOR_NOT_MET")
        return reasons

    def _verifier_reasons(self, task: TaskProfile, agent: AgentProfile) -> list[str]:
        reasons = self._common_reasons(task, agent)
        if "verifier" not in agent.roles:
            reasons.append("ROLE_VERIFIER_MISSING")
        required_context = task.verifier_input_tokens + task.verifier_output_tokens
        if required_context > 0 and agent.max_context_tokens < required_context:
            reasons.append("VERIFIER_CONTEXT_INSUFFICIENT")
        if agent.max_evidence_class < task.required_evidence_class:
            reasons.append("EVIDENCE_CAPABILITY_INSUFFICIENT")
        return reasons

    @staticmethod
    def _candidate_reasons(
        task: TaskProfile,
        candidate: _CandidatePlan,
        independent_required: bool,
    ) -> list[str]:
        reasons: list[str] = []
        worker = candidate.worker
        verifier = candidate.verifier
        if verifier is not None and worker.agent_id == verifier.agent_id:
            reasons.append("SELF_VERIFICATION_FORBIDDEN")
        if independent_required and verifier is not None:
            if worker.provider_domain == verifier.provider_domain:
                reasons.append("INDEPENDENCE_DOMAIN_COLLISION")

        if task.max_total_tokens is not None and candidate.total_tokens > task.max_total_tokens:
            reasons.append("TOKEN_BUDGET_EXCEEDED")
        if task.max_cost_microunits is not None and candidate.cost_microunits > task.max_cost_microunits:
            reasons.append("COST_BUDGET_EXCEEDED")
        if task.max_latency_ms is not None and candidate.latency_ms > task.max_latency_ms:
            reasons.append("LATENCY_BUDGET_EXCEEDED")
        return reasons

    @staticmethod
    def _price(tokens: int, rate_per_1k: int) -> int:
        # Integer ceil(tokens * rate / 1000) avoids floating-point ambiguity.
        return (tokens * rate_per_1k + 999) // 1000

    def _build_candidate(
        self,
        task: TaskProfile,
        worker: AgentProfile,
        verifier: AgentProfile | None,
    ) -> _CandidatePlan:
        worker_cost = self._price(task.worker_input_tokens, worker.input_cost_microunits_per_1k)
        worker_cost += self._price(task.worker_output_tokens, worker.output_cost_microunits_per_1k)
        total_tokens = task.worker_input_tokens + task.worker_output_tokens
        latency_ms = worker.estimated_latency_ms
        quality_bps = worker.quality_bps

        if verifier is not None:
            worker_cost += self._price(task.verifier_input_tokens, verifier.input_cost_microunits_per_1k)
            worker_cost += self._price(task.verifier_output_tokens, verifier.output_cost_microunits_per_1k)
            total_tokens += task.verifier_input_tokens + task.verifier_output_tokens
            latency_ms += verifier.estimated_latency_ms
            quality_bps = min(quality_bps, verifier.quality_bps)

        return _CandidatePlan(
            worker=worker,
            verifier=verifier,
            total_tokens=total_tokens,
            cost_microunits=worker_cost,
            latency_ms=latency_ms,
            quality_bps=quality_bps,
        )

    def _ranking_key(self, candidate: _CandidatePlan) -> tuple[Any, ...]:
        values: list[Any] = []
        for objective in self._policy.objective_order:
            if objective == "cost":
                values.append(candidate.cost_microunits)
            elif objective == "latency":
                values.append(candidate.latency_ms)
            elif objective == "quality":
                values.append(-candidate.quality_bps)
            else:  # Defensive: GovernorPolicy validates this already.
                raise ContractError(f"unsupported objective: {objective}")
        values.append(candidate.worker.agent_id)
        values.append(candidate.verifier.agent_id if candidate.verifier else "")
        return tuple(values)

    @staticmethod
    def _freeze(
        task: TaskProfile,
        independent_required: bool,
        verifier_required: bool,
        reasons: tuple[str, ...],
        eliminations: list[Elimination],
        policy_trace: tuple[str, ...],
    ) -> GovernorDecision:
        return GovernorDecision(
            task_id=task.task_id,
            decision="FREEZE",
            plan=None,
            effective_independent_verifier_required=independent_required,
            effective_verifier_required=verifier_required,
            freeze_reasons=reasons,
            eliminations=tuple(eliminations),
            policy_trace=policy_trace,
        )
