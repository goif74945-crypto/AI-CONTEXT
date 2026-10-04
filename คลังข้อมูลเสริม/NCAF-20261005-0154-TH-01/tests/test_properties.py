from __future__ import annotations

import random
import unittest

from ncaf.common import ContractError
from ncaf.context_budget import ContextBudgetAllocator, ContextItem
from ncaf.evidence_resolver import Claim, EvidenceConflictResolver, ResolutionStatus
from ncaf.execution_journal import JournalEvent, ResumableExecutionJournal, StepState
from ncaf.failure_containment import Action, CircuitState, DependencyPolicy, FailureContainmentEngine
from ncaf.pareto_router import ParetoRoutePlanner, RouteCandidate


class PropertyTests(unittest.TestCase):
    def test_context_allocator_randomized_invariants(self):
        rng = random.Random(74945)
        for case in range(1000):
            count = rng.randint(2, 14)
            items = []
            for i in range(count):
                deps = () if i == 0 or rng.random() < 0.55 else (f"i{rng.randrange(i)}",)
                items.append(ContextItem(
                    f"i{i}",
                    rng.randint(1, 40),
                    rng.randint(0, 100),
                    rng.randint(0, 100),
                    mandatory=(i == 0 and rng.random() < 0.2),
                    dependencies=deps,
                ))
            budget = rng.randint(10, 180)
            allocator = ContextBudgetAllocator(items)
            try:
                a = allocator.allocate(budget)
                b = allocator.allocate(budget)
            except ContractError:
                # Only valid fail-closed case here is mandatory closure overflow.
                mandatory = {x.item_id for x in items if x.mandatory}
                mandatory_cost = sum(x.tokens for x in items if x.item_id in mandatory)
                self.assertGreater(mandatory_cost, budget, msg=f"case={case}")
                continue
            self.assertEqual(a, b, msg=f"nondeterministic case={case}")
            self.assertLessEqual(a.used_tokens, budget, msg=f"budget leak case={case}")
            selected = set(a.selected)
            item_map = {x.item_id: x for x in items}
            for sid in selected:
                self.assertTrue(set(item_map[sid].dependencies).issubset(selected), msg=f"dependency leak case={case}")

    def test_router_selected_is_never_dominated(self):
        rng = random.Random(20261005)
        planner = ParetoRoutePlanner()
        for case in range(1000):
            routes = [
                RouteCandidate(
                    f"r{i}", rng.randint(1, 100), rng.randint(1, 1000), rng.randint(0, 50), rng.randint(0, 100),
                    frozenset({"base"} | ({"vision"} if rng.random() < 0.5 else set())),
                )
                for i in range(rng.randint(2, 12))
            ]
            try:
                decision = planner.choose(routes, required_capabilities=frozenset({"base"}), min_quality=20, max_risk=90)
            except ContractError:
                self.assertFalse(any(r.quality >= 20 and r.risk <= 90 for r in routes))
                continue
            selected = next(r for r in routes if r.route_id == decision.selected)
            eligible = [r for r in routes if r.route_id in decision.eligible]
            self.assertFalse(any(planner._dominates(other, selected) for other in eligible if other != selected), msg=f"case={case}")

    def test_evidence_resolver_never_returns_losing_value(self):
        rng = random.Random(111)
        resolver = EvidenceConflictResolver(min_score=20, conflict_margin=10)
        for case in range(1000):
            claims = [
                Claim("k", rng.choice(["A", "B", "C"]), f"s{i}", rng.randint(0, 100), rng.randint(0, 10))
                for i in range(rng.randint(1, 10))
            ]
            result = resolver.resolve(claims)
            if result.status is ResolutionStatus.RESOLVED:
                scores: dict[str, int] = {}
                for c in claims:
                    scores[c.value] = scores.get(c.value, 0) + c.trust + min(c.evidence_count, 20) * 2
                max_score = max(scores.values())
                self.assertEqual(scores[result.value], max_score, msg=f"case={case}")

    def test_journal_single_byte_hash_tampering_is_detected(self):
        journal = ResumableExecutionJournal()
        e = journal.append("step", StepState.PLANNED, "idem")
        for pos in (0, 15, 31, 47, 63):
            chars = list(e.event_hash)
            chars[pos] = "f" if chars[pos] != "f" else "e"
            bad = JournalEvent(e.seq, e.step_id, e.state, e.idempotency_key, e.previous_hash, "".join(chars))
            with self.assertRaises(ContractError):
                ResumableExecutionJournal([bad])

    def test_circuit_breaker_never_attempts_while_open_before_cooldown(self):
        rng = random.Random(55)
        for case in range(1000):
            threshold = rng.randint(1, 5)
            cooldown = rng.randint(1, 10)
            engine = FailureContainmentEngine(DependencyPolicy(threshold, cooldown))
            for tick in range(threshold):
                if tick < threshold - 1:
                    self.assertEqual(engine.before_call("dep", tick=tick), Action.ATTEMPT)
                engine.record_failure("dep", tick=tick)
            opened_tick = threshold - 1
            self.assertEqual(engine.state("dep"), CircuitState.OPEN, msg=f"case={case}")
            for tick in range(opened_tick, opened_tick + cooldown):
                self.assertEqual(engine.before_call("dep", tick=tick), Action.BLOCK, msg=f"case={case} tick={tick}")


if __name__ == "__main__":
    unittest.main()
