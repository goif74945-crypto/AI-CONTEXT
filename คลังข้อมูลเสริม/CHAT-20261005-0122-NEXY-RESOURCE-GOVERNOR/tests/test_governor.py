from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import (  # noqa: E402
    AgentProfile,
    ContractError,
    DataClass,
    GovernorPolicy,
    ResourceGovernor,
    RiskTier,
    TaskProfile,
    agent_from_mapping,
    task_from_mapping,
)


def agent(
    agent_id: str,
    *,
    provider: str = "p1",
    roles: tuple[str, ...] = ("worker",),
    capabilities: tuple[str, ...] = ("code",),
    clearance: DataClass = DataClass.RESTRICTED,
    context: int = 100_000,
    in_cost: int = 100,
    out_cost: int = 100,
    latency: int = 100,
    quality: int = 9000,
    evidence: int = 7,
    active: bool = True,
    quarantined: bool = False,
) -> AgentProfile:
    return AgentProfile(
        agent_id=agent_id,
        provider_domain=provider,
        roles=frozenset(roles),
        capabilities=frozenset(capabilities),
        clearance=clearance,
        max_context_tokens=context,
        input_cost_microunits_per_1k=in_cost,
        output_cost_microunits_per_1k=out_cost,
        estimated_latency_ms=latency,
        quality_bps=quality,
        max_evidence_class=evidence,
        active=active,
        quarantined=quarantined,
    )


def task(**overrides: object) -> TaskProfile:
    values: dict[str, object] = {
        "task_id": "t1",
        "required_capabilities": frozenset({"code"}),
        "data_class": DataClass.INTERNAL,
        "risk_tier": RiskTier.MEDIUM,
        "required_evidence_class": 2,
        "worker_input_tokens": 1000,
        "worker_output_tokens": 1000,
        "verifier_input_tokens": 1000,
        "verifier_output_tokens": 500,
        "require_independent_verifier": False,
        "min_quality_bps": 0,
        "max_total_tokens": None,
        "max_cost_microunits": None,
        "max_latency_ms": None,
    }
    values.update(overrides)
    return TaskProfile(**values)  # type: ignore[arg-type]


class ResourceGovernorTests(unittest.TestCase):
    def test_selects_lowest_cost_feasible_plan(self) -> None:
        governor = ResourceGovernor()
        agents = [
            agent("worker-expensive", in_cost=900, out_cost=900),
            agent("worker-cheap", in_cost=100, out_cost=100),
            agent("verify", provider="p2", roles=("verifier",), in_cost=50, out_cost=50),
        ]
        decision = governor.plan(task(), agents)
        self.assertEqual(decision.decision, "PLAN_READY")
        self.assertIsNotNone(decision.plan)
        self.assertEqual(decision.plan.worker_id, "worker-cheap")
        self.assertEqual(decision.plan.verifier_id, "verify")
        self.assertEqual(decision.plan.verification_status, "NOT_VERIFIED")

    def test_budget_exhaustion_freezes_instead_of_downgrading_verification(self) -> None:
        governor = ResourceGovernor()
        agents = [
            agent("worker"),
            agent("verify", provider="p2", roles=("verifier",)),
        ]
        decision = governor.plan(task(max_cost_microunits=1), agents)
        self.assertEqual(decision.decision, "FREEZE")
        self.assertIsNone(decision.plan)
        self.assertIn("COST_BUDGET_EXCEEDED", decision.freeze_reasons)
        self.assertTrue(decision.effective_verifier_required)

    def test_high_risk_forces_independent_verifier(self) -> None:
        governor = ResourceGovernor()
        agents = [
            agent("worker", provider="same"),
            agent("verify-same", provider="same", roles=("verifier",)),
        ]
        decision = governor.plan(task(risk_tier=RiskTier.HIGH), agents)
        self.assertEqual(decision.decision, "FREEZE")
        self.assertTrue(decision.effective_independent_verifier_required)
        self.assertIn("INDEPENDENCE_DOMAIN_COLLISION", decision.freeze_reasons)

    def test_high_risk_accepts_independent_verifier(self) -> None:
        governor = ResourceGovernor()
        agents = [
            agent("worker", provider="p1"),
            agent("verify", provider="p2", roles=("verifier",)),
        ]
        decision = governor.plan(task(risk_tier=RiskTier.CRITICAL), agents)
        self.assertEqual(decision.decision, "PLAN_READY")
        self.assertTrue(decision.effective_independent_verifier_required)

    def test_data_clearance_is_hard_constraint(self) -> None:
        governor = ResourceGovernor()
        agents = [
            agent("public-worker", clearance=DataClass.PUBLIC),
            agent("restricted-worker", clearance=DataClass.RESTRICTED, in_cost=200),
            agent("verify", provider="p2", roles=("verifier",), clearance=DataClass.RESTRICTED),
        ]
        decision = governor.plan(task(data_class=DataClass.CONFIDENTIAL), agents)
        self.assertEqual(decision.decision, "PLAN_READY")
        self.assertEqual(decision.plan.worker_id, "restricted-worker")
        public_elimination = [e for e in decision.eliminations if e.subject == "public-worker"]
        self.assertTrue(public_elimination)
        self.assertIn("DATA_CLEARANCE_INSUFFICIENT", public_elimination[0].reasons)

    def test_quarantined_cheapest_agent_is_never_selected(self) -> None:
        governor = ResourceGovernor()
        agents = [
            agent("cheap-quarantined", in_cost=0, out_cost=0, quarantined=True),
            agent("safe-worker", in_cost=200, out_cost=200),
            agent("verify", provider="p2", roles=("verifier",)),
        ]
        decision = governor.plan(task(), agents)
        self.assertEqual(decision.decision, "PLAN_READY")
        self.assertEqual(decision.plan.worker_id, "safe-worker")

    def test_missing_capability_freezes_when_no_alternative_exists(self) -> None:
        governor = ResourceGovernor()
        agents = [
            agent("worker", capabilities=("text",)),
            agent("verify", provider="p2", roles=("verifier",)),
        ]
        decision = governor.plan(task(required_capabilities=frozenset({"code"})), agents)
        self.assertEqual(decision.decision, "FREEZE")
        self.assertIn("NO_ELIGIBLE_WORKER", decision.freeze_reasons)

    def test_evidence_capability_cannot_be_silently_lowered(self) -> None:
        governor = ResourceGovernor()
        agents = [
            agent("worker"),
            agent("weak-verifier", provider="p2", roles=("verifier",), evidence=2),
        ]
        decision = governor.plan(task(required_evidence_class=4), agents)
        self.assertEqual(decision.decision, "FREEZE")
        self.assertIn("NO_ELIGIBLE_VERIFIER", decision.freeze_reasons)

    def test_latency_budget_is_hard_constraint(self) -> None:
        governor = ResourceGovernor()
        agents = [
            agent("worker", latency=1000),
            agent("verify", provider="p2", roles=("verifier",), latency=1000),
        ]
        decision = governor.plan(task(max_latency_ms=500), agents)
        self.assertEqual(decision.decision, "FREEZE")
        self.assertIn("LATENCY_BUDGET_EXCEEDED", decision.freeze_reasons)

    def test_token_budget_is_hard_constraint(self) -> None:
        governor = ResourceGovernor()
        agents = [agent("worker"), agent("verify", provider="p2", roles=("verifier",))]
        decision = governor.plan(task(max_total_tokens=3000), agents)
        self.assertEqual(decision.decision, "FREEZE")
        self.assertIn("TOKEN_BUDGET_EXCEEDED", decision.freeze_reasons)

    def test_tie_break_is_deterministic_by_agent_id(self) -> None:
        governor = ResourceGovernor()
        agents = [
            agent("worker-z"),
            agent("worker-a"),
            agent("verify", provider="p2", roles=("verifier",)),
        ]
        first = governor.plan(task(), list(reversed(agents)))
        second = governor.plan(task(), agents)
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertEqual(first.plan.worker_id, "worker-a")


    def test_self_verification_is_forbidden_even_when_cross_provider_independence_is_not_required(self) -> None:
        governor = ResourceGovernor()
        dual_role = agent("dual", roles=("worker", "verifier"), provider="p1")
        decision = governor.plan(task(), [dual_role])
        self.assertEqual(decision.decision, "FREEZE")
        self.assertIn("SELF_VERIFICATION_FORBIDDEN", decision.freeze_reasons)

    def test_duplicate_agent_ids_are_rejected(self) -> None:
        governor = ResourceGovernor()
        with self.assertRaises(ContractError):
            governor.plan(task(required_evidence_class=0), [agent("dup"), agent("dup")])

    def test_low_evidence_can_plan_without_verifier(self) -> None:
        governor = ResourceGovernor(GovernorPolicy(verifier_required_from_evidence_class=2))
        decision = governor.plan(task(required_evidence_class=1), [agent("worker")])
        self.assertEqual(decision.decision, "PLAN_READY")
        self.assertIsNone(decision.plan.verifier_id)

    def test_fixture_scenarios(self) -> None:
        fixture_path = ROOT / "fixtures" / "scenarios.json"
        payload = json.loads(fixture_path.read_text(encoding="utf-8"))
        governor = ResourceGovernor()
        for scenario in payload["scenarios"]:
            with self.subTest(scenario=scenario["name"]):
                parsed_task = task_from_mapping(scenario["task"])
                parsed_agents = [agent_from_mapping(item) for item in scenario["agents"]]
                decision = governor.plan(parsed_task, parsed_agents)
                self.assertEqual(decision.decision, scenario["expect"]["decision"])
                if decision.plan is not None:
                    self.assertEqual(decision.plan.worker_id, scenario["expect"].get("worker_id"))
                    self.assertEqual(decision.plan.verifier_id, scenario["expect"].get("verifier_id"))
                for reason in scenario["expect"].get("freeze_reasons", []):
                    self.assertIn(reason, decision.freeze_reasons)


if __name__ == "__main__":
    unittest.main()
