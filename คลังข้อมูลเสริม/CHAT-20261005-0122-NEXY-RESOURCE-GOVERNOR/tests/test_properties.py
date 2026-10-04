from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import (  # noqa: E402
    DATA_CLASS_RANK,
    AgentProfile,
    DataClass,
    ResourceGovernor,
    RiskTier,
    TaskProfile,
)


CAPS = ("code", "text", "vision")
DATA = tuple(DataClass)
RISKS = tuple(RiskTier)


def make_case(seed: int) -> tuple[TaskProfile, list[AgentProfile]]:
    rng = random.Random(seed)
    required_cap = rng.choice(CAPS)
    evidence = rng.randint(0, 4)
    worker_in = rng.randint(100, 4000)
    worker_out = rng.randint(100, 2000)
    verifier_in = rng.randint(100, 2000)
    verifier_out = rng.randint(50, 800)
    task = TaskProfile(
        task_id=f"property-{seed}",
        required_capabilities=frozenset({required_cap}),
        data_class=rng.choice(DATA),
        risk_tier=rng.choice(RISKS),
        required_evidence_class=evidence,
        worker_input_tokens=worker_in,
        worker_output_tokens=worker_out,
        verifier_input_tokens=verifier_in,
        verifier_output_tokens=verifier_out,
        require_independent_verifier=rng.random() < 0.2,
        min_quality_bps=rng.randint(0, 7000),
        max_total_tokens=None if rng.random() < 0.7 else rng.randint(500, 9000),
        max_cost_microunits=None if rng.random() < 0.7 else rng.randint(1, 8000),
        max_latency_ms=None if rng.random() < 0.7 else rng.randint(10, 5000),
    )
    agents: list[AgentProfile] = []
    for index in range(rng.randint(4, 20)):
        role_roll = rng.random()
        if role_roll < 0.4:
            roles = frozenset({"worker"})
        elif role_roll < 0.8:
            roles = frozenset({"verifier"})
        else:
            roles = frozenset({"worker", "verifier"})
        capabilities = frozenset(cap for cap in CAPS if rng.random() < 0.6)
        agents.append(
            AgentProfile(
                agent_id=f"a-{seed:03d}-{index:02d}",
                provider_domain=f"provider-{rng.randint(0, 4)}",
                roles=roles,
                capabilities=capabilities,
                clearance=rng.choice(DATA),
                max_context_tokens=rng.randint(500, 12000),
                input_cost_microunits_per_1k=rng.randint(0, 2000),
                output_cost_microunits_per_1k=rng.randint(0, 3000),
                estimated_latency_ms=rng.randint(0, 3000),
                quality_bps=rng.randint(4000, 10000),
                max_evidence_class=rng.randint(0, 7),
                active=rng.random() >= 0.08,
                quarantined=rng.random() < 0.08,
            )
        )
    return task, agents


def price(tokens: int, rate: int) -> int:
    return (tokens * rate + 999) // 1000


class GovernorPropertyTests(unittest.TestCase):
    def test_300_generated_cases_are_order_deterministic_and_preserve_hard_gates(self) -> None:
        governor = ResourceGovernor()
        for seed in range(300):
            task, agents = make_case(seed)
            with self.subTest(seed=seed):
                direct = governor.plan(task, agents)
                reversed_decision = governor.plan(task, list(reversed(agents)))
                self.assertEqual(direct.to_dict(), reversed_decision.to_dict())

                if direct.decision != "PLAN_READY":
                    self.assertIsNone(direct.plan)
                    self.assertTrue(direct.freeze_reasons)
                    continue

                self.assertIsNotNone(direct.plan)
                by_id = {item.agent_id: item for item in agents}
                worker = by_id[direct.plan.worker_id]
                verifier = by_id[direct.plan.verifier_id] if direct.plan.verifier_id is not None else None

                self.assertTrue(worker.active)
                self.assertFalse(worker.quarantined)
                self.assertIn("worker", worker.roles)
                self.assertTrue(task.required_capabilities.issubset(worker.capabilities))
                self.assertGreaterEqual(DATA_CLASS_RANK[worker.clearance], DATA_CLASS_RANK[task.data_class])
                self.assertGreaterEqual(worker.max_context_tokens, task.worker_input_tokens + task.worker_output_tokens)
                self.assertGreaterEqual(worker.quality_bps, task.min_quality_bps)
                self.assertEqual(direct.plan.verification_status, "NOT_VERIFIED")

                effective_verifier_required = (
                    task.required_evidence_class >= governor.policy.verifier_required_from_evidence_class
                    or task.require_independent_verifier
                    or task.risk_tier in governor.policy.independence_required_risk
                )
                self.assertEqual(direct.effective_verifier_required, effective_verifier_required)
                if effective_verifier_required:
                    self.assertIsNotNone(verifier)

                total_tokens = task.worker_input_tokens + task.worker_output_tokens
                total_cost = price(task.worker_input_tokens, worker.input_cost_microunits_per_1k)
                total_cost += price(task.worker_output_tokens, worker.output_cost_microunits_per_1k)
                total_latency = worker.estimated_latency_ms

                if verifier is not None:
                    self.assertNotEqual(worker.agent_id, verifier.agent_id)
                    self.assertTrue(verifier.active)
                    self.assertFalse(verifier.quarantined)
                    self.assertIn("verifier", verifier.roles)
                    self.assertGreaterEqual(DATA_CLASS_RANK[verifier.clearance], DATA_CLASS_RANK[task.data_class])
                    self.assertGreaterEqual(verifier.max_evidence_class, task.required_evidence_class)
                    self.assertGreaterEqual(verifier.max_context_tokens, task.verifier_input_tokens + task.verifier_output_tokens)
                    total_tokens += task.verifier_input_tokens + task.verifier_output_tokens
                    total_cost += price(task.verifier_input_tokens, verifier.input_cost_microunits_per_1k)
                    total_cost += price(task.verifier_output_tokens, verifier.output_cost_microunits_per_1k)
                    total_latency += verifier.estimated_latency_ms

                if direct.effective_independent_verifier_required:
                    self.assertIsNotNone(verifier)
                    self.assertNotEqual(worker.provider_domain, verifier.provider_domain)

                self.assertEqual(direct.plan.estimated_total_tokens, total_tokens)
                self.assertEqual(direct.plan.estimated_cost_microunits, total_cost)
                self.assertEqual(direct.plan.estimated_latency_ms, total_latency)
                if task.max_total_tokens is not None:
                    self.assertLessEqual(total_tokens, task.max_total_tokens)
                if task.max_cost_microunits is not None:
                    self.assertLessEqual(total_cost, task.max_cost_microunits)
                if task.max_latency_ms is not None:
                    self.assertLessEqual(total_latency, task.max_latency_ms)


if __name__ == "__main__":
    unittest.main()
