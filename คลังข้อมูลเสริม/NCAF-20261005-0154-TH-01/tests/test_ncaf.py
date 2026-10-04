from __future__ import annotations

import unittest

from ncaf.common import ContractError
from ncaf.context_budget import ContextBudgetAllocator, ContextItem
from ncaf.evidence_resolver import Claim, EvidenceConflictResolver, ResolutionStatus
from ncaf.execution_journal import JournalEvent, ResumableExecutionJournal, StepState
from ncaf.failure_containment import Action, CircuitState, DependencyPolicy, FailureContainmentEngine
from ncaf.pareto_router import ParetoRoutePlanner, RouteCandidate


class ContextBudgetTests(unittest.TestCase):
    def test_dependency_closure_and_budget(self):
        items = [
            ContextItem("spec", 30, 100, 100, mandatory=True),
            ContextItem("schema", 20, 80, 90, dependencies=("spec",)),
            ContextItem("history", 40, 30, 10),
            ContextItem("task", 25, 95, 100, dependencies=("schema",)),
        ]
        result = ContextBudgetAllocator(items).allocate(80)
        self.assertEqual(result.selected, ("schema", "spec", "task"))
        self.assertEqual(result.used_tokens, 75)
        self.assertEqual(result.omitted, ("history",))

    def test_mandatory_overflow_fails_closed(self):
        allocator = ContextBudgetAllocator([ContextItem("must", 100, 1, 1, mandatory=True)])
        with self.assertRaises(ContractError):
            allocator.allocate(99)

    def test_cycle_rejected(self):
        with self.assertRaises(ContractError):
            ContextBudgetAllocator([
                ContextItem("a", 1, 1, 1, dependencies=("b",)),
                ContextItem("b", 1, 1, 1, dependencies=("a",)),
            ])


class EvidenceResolverTests(unittest.TestCase):
    def test_resolves_strong_aggregate(self):
        claims = [
            Claim("version", "2", "official", 95, 3),
            Claim("version", "2", "tests", 90, 2),
            Claim("version", "1", "stale", 60, 1),
        ]
        result = EvidenceConflictResolver(conflict_margin=20).resolve(claims)
        self.assertEqual(result.status, ResolutionStatus.RESOLVED)
        self.assertEqual(result.value, "2")

    def test_close_conflict_freezes(self):
        claims = [Claim("k", "A", "s1", 80, 0), Claim("k", "B", "s2", 75, 0)]
        result = EvidenceConflictResolver(conflict_margin=10).resolve(claims)
        self.assertEqual(result.status, ResolutionStatus.CONFLICT)
        self.assertIsNone(result.value)

    def test_mixed_keys_rejected(self):
        with self.assertRaises(ContractError):
            EvidenceConflictResolver().resolve([Claim("a", "1", "s1", 90, 1), Claim("b", "2", "s2", 90, 1)])


class ParetoRouterTests(unittest.TestCase):
    def test_dominated_route_removed_and_constraint_respected(self):
        routes = [
            RouteCandidate("fast", 85, 100, 5, 10, frozenset({"tools"})),
            RouteCandidate("slow_bad", 80, 200, 7, 20, frozenset({"tools"})),
            RouteCandidate("quality", 98, 400, 20, 15, frozenset({"tools", "vision"})),
        ]
        decision = ParetoRoutePlanner().choose(routes, required_capabilities=frozenset({"tools"}), min_quality=80, max_risk=20)
        self.assertNotIn("slow_bad", decision.frontier)
        self.assertIn(decision.selected, decision.frontier)

    def test_no_eligible_fails_closed(self):
        with self.assertRaises(ContractError):
            ParetoRoutePlanner().choose([RouteCandidate("r", 50, 10, 1, 90, frozenset())], min_quality=90)


class JournalTests(unittest.TestCase):
    def test_valid_chain_replays(self):
        journal = ResumableExecutionJournal()
        e1 = journal.append("s1", StepState.PLANNED, "k1")
        e2 = journal.append("s1", StepState.RUNNING, "k1")
        e3 = journal.append("s1", StepState.SUCCEEDED, "k1")
        replayed = ResumableExecutionJournal([e1, e2, e3])
        self.assertEqual(replayed.resumable_steps(), ())

    def test_illegal_transition_rejected_without_mutation(self):
        journal = ResumableExecutionJournal()
        journal.append("s1", StepState.PLANNED, "k1")
        before = journal.events
        with self.assertRaises(ContractError):
            journal.append("s1", StepState.SUCCEEDED, "k1")
        self.assertEqual(journal.events, before)

    def test_tamper_detected(self):
        journal = ResumableExecutionJournal()
        e1 = journal.append("s1", StepState.PLANNED, "k1")
        bad = JournalEvent(e1.seq, e1.step_id, e1.state, e1.idempotency_key, e1.previous_hash, "0" * 64)
        with self.assertRaises(ContractError):
            ResumableExecutionJournal([bad])


class FailureContainmentTests(unittest.TestCase):
    def test_opens_blocks_probes_and_recovers(self):
        engine = FailureContainmentEngine(DependencyPolicy(failure_threshold=2, cooldown_ticks=3))
        self.assertEqual(engine.before_call("api", tick=0), Action.ATTEMPT)
        engine.record_failure("api", tick=0)
        engine.record_failure("api", tick=1)
        self.assertEqual(engine.state("api"), CircuitState.OPEN)
        self.assertEqual(engine.before_call("api", tick=2), Action.BLOCK)
        self.assertEqual(engine.before_call("api", tick=4), Action.PROBE)
        self.assertEqual(engine.before_call("api", tick=4), Action.BLOCK)
        engine.record_success("api")
        self.assertEqual(engine.state("api"), CircuitState.CLOSED)
        self.assertEqual(engine.before_call("api", tick=5), Action.ATTEMPT)

    def test_failed_probe_reopens(self):
        engine = FailureContainmentEngine(DependencyPolicy(failure_threshold=1, cooldown_ticks=1))
        engine.record_failure("db", tick=0)
        self.assertEqual(engine.before_call("db", tick=1), Action.PROBE)
        engine.record_failure("db", tick=1)
        self.assertEqual(engine.state("db"), CircuitState.OPEN)


if __name__ == "__main__":
    unittest.main()

from ncaf.integration import AUTHORITY, CLASSIFICATION, assert_advisory_boundary, companion_envelope


class IntegrationBoundaryTests(unittest.TestCase):
    def test_envelope_is_advisory_and_non_mutating(self):
        envelope = companion_envelope("context-budget", {"selected": ["a", "b"]})
        self.assertEqual(envelope.classification, CLASSIFICATION)
        self.assertEqual(envelope.authority, AUTHORITY)
        self.assertFalse(envelope.may_mutate_core)
        self.assertEqual(len(envelope.payload_hash), 64)
        assert_advisory_boundary(envelope)
