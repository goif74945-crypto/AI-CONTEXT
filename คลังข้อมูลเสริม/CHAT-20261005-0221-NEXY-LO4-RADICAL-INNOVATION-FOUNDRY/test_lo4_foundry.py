from __future__ import annotations

import itertools
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lo4_foundry import (  # noqa: E402
    ActionCandidate,
    Alternative,
    AntiFeaturePolicy,
    ArchitectureChoice,
    Authority,
    BenefitClaim,
    ConflictSet,
    ConstraintRef,
    Decision,
    FutureOption,
    Lo4Error,
    NoveltyDimension,
    OptionPolicy,
    RegretPolicy,
    RelaxationPolicy,
    SurprisePolicy,
    choose_minimax_regret,
    evaluate_surprise_budget,
    integrate_foundry,
    propose_minimal_relaxation,
    refute_feature,
    select_option_preserving_choice,
)


class SurpriseBudgetTests(unittest.TestCase):
    def test_allows_bounded_experimental_novelty(self):
        r = evaluate_surprise_budget([
            NoveltyDimension("ux", 3000, 4000),
            NoveltyDimension("routing", 2000, 2000),
        ])
        self.assertEqual(r.status, Decision.ALLOW_EXPERIMENT)
        self.assertEqual(r.total_cost, 1600)

    def test_freezes_canon_drift(self):
        r = evaluate_surprise_budget([
            NoveltyDimension("canon-law", 1, 10000, Authority.CANON),
        ])
        self.assertEqual(r.status, Decision.FREEZE)
        self.assertTrue(any(x.startswith("PROTECTED_AUTHORITY_DRIFT") for x in r.reason_codes))

    def test_freezes_total_budget_overrun(self):
        r = evaluate_surprise_budget([
            NoveltyDimension("a", 10000, 6000),
            NoveltyDimension("b", 10000, 6000),
        ], SurprisePolicy(total_budget=10000, max_single_dimension_cost=10000))
        self.assertEqual(r.status, Decision.FREEZE)
        self.assertIn("TOTAL_SURPRISE_BUDGET_EXCEEDED", r.reason_codes)

    def test_duplicate_dimension_rejected(self):
        with self.assertRaises(Lo4Error):
            evaluate_surprise_budget([
                NoveltyDimension("a", 1, 1),
                NoveltyDimension("a", 1, 1),
            ])

    def test_permutation_determinism(self):
        dims = [
            NoveltyDimension("c", 300, 400),
            NoveltyDimension("a", 100, 200),
            NoveltyDimension("b", 200, 300),
        ]
        fps = {evaluate_surprise_budget(p).fingerprint for p in itertools.permutations(dims)}
        self.assertEqual(len(fps), 1)


class AntiFeatureTests(unittest.TestCase):
    def test_keeps_evidenced_high_value_experiment(self):
        r = refute_feature(
            [BenefitClaim("faster-task", 7000, 3)],
            proposed_complexity_bps=2500,
            proposed_risk_bps=2000,
        )
        self.assertEqual(r.status, Decision.KEEP_EXPERIMENT)

    def test_requires_evidence(self):
        r = refute_feature(
            [BenefitClaim("nice-sounding", 9000, 0)],
            proposed_complexity_bps=100,
            proposed_risk_bps=100,
        )
        self.assertEqual(r.status, Decision.NEED_EVIDENCE)

    def test_rejects_low_value(self):
        r = refute_feature(
            [BenefitClaim("minor", 1000, 3)],
            proposed_complexity_bps=100,
            proposed_risk_bps=100,
        )
        self.assertEqual(r.status, Decision.REJECT_EXPERIMENT)
        self.assertIn("INSUFFICIENT_USER_VALUE", r.reason_codes)

    def test_rejects_subsumed_feature(self):
        r = refute_feature(
            [BenefitClaim("value", 8000, 3)],
            proposed_complexity_bps=8000,
            proposed_risk_bps=4000,
            alternatives=[Alternative("existing-simple", 9500, 2000, 1000)],
        )
        self.assertEqual(r.status, Decision.REJECT_EXPERIMENT)
        self.assertEqual(r.strongest_alternative, "existing-simple")

    def test_high_risk_rejected(self):
        r = refute_feature(
            [BenefitClaim("value", 9000, 4)],
            proposed_complexity_bps=1000,
            proposed_risk_bps=9000,
        )
        self.assertEqual(r.status, Decision.REJECT_EXPERIMENT)
        self.assertIn("EXPERIMENTAL_RISK_TOO_HIGH", r.reason_codes)


class MinimalRelaxationTests(unittest.TestCase):
    def setUp(self):
        self.constraints = [
            ConstraintRef("CANON_A", Authority.CANON, False, 1000),
            ConstraintRef("EXP_X", Authority.EXPERIMENTAL, True, 5),
            ConstraintRef("EXP_Y", Authority.EXPERIMENTAL, True, 2),
            ConstraintRef("EXP_Z", Authority.EXPERIMENTAL, True, 1),
        ]

    def test_no_conflict_is_plan(self):
        r = propose_minimal_relaxation(self.constraints, [])
        self.assertEqual(r.status, Decision.PLAN)
        self.assertEqual(r.relax_constraint_ids, ())

    def test_never_relaxes_canon(self):
        r = propose_minimal_relaxation(
            self.constraints,
            [ConflictSet("c1", ("CANON_A",))],
        )
        self.assertEqual(r.status, Decision.FREEZE)
        self.assertIn("UNRELAXABLE_CONFLICT:c1", r.reason_codes)

    def test_exact_weighted_hitting_set(self):
        r = propose_minimal_relaxation(
            self.constraints,
            [
                ConflictSet("c1", ("CANON_A", "EXP_X", "EXP_Y")),
                ConflictSet("c2", ("EXP_X", "EXP_Z")),
                ConflictSet("c3", ("EXP_Y", "EXP_Z")),
            ],
        )
        self.assertEqual(r.status, Decision.PROPOSE_RELAXATION)
        # EXP_Z hits c2+c3 but not c1, so pair EXP_Y+EXP_Z costs 3 and wins.
        self.assertEqual(r.relax_constraint_ids, ("EXP_Y", "EXP_Z"))
        self.assertEqual(r.total_cost, 3)
        self.assertIn("PROPOSAL_ONLY_NO_AUTOMATIC_MUTATION", r.reason_codes)

    def test_search_bound_fail_closed(self):
        cs = [ConstraintRef(f"E{i}", Authority.EXPERIMENTAL, True, 1) for i in range(5)]
        r = propose_minimal_relaxation(
            cs,
            [ConflictSet("all", tuple(c.constraint_id for c in cs))],
            RelaxationPolicy(max_relaxations=2, max_search_candidates=3),
        )
        self.assertEqual(r.status, Decision.FREEZE)
        self.assertIn("SEARCH_BOUND_EXCEEDED", r.reason_codes)

    def test_unknown_constraint_rejected(self):
        with self.assertRaises(Lo4Error):
            propose_minimal_relaxation(self.constraints, [ConflictSet("bad", ("MISSING",))])

    def test_permutation_determinism(self):
        conflicts = [
            ConflictSet("c2", ("EXP_Z", "EXP_X")),
            ConflictSet("c1", ("EXP_Y", "EXP_X")),
        ]
        fps = set()
        for c_order in itertools.permutations(self.constraints):
            for x_order in itertools.permutations(conflicts):
                fps.add(propose_minimal_relaxation(c_order, x_order).fingerprint)
        self.assertEqual(len(fps), 1)


class RegretEnvelopeTests(unittest.TestCase):
    def test_selects_minimax_regret(self):
        actions = [
            ActionCandidate("fast", True, False, True, {"normal": 100, "outage": 0}),
            ActionCandidate("robust", True, False, True, {"normal": 70, "outage": 60}),
            ActionCandidate("safe", True, False, True, {"normal": 40, "outage": 65}),
        ]
        r = choose_minimax_regret(actions, RegretPolicy(max_worst_case_regret=1000))
        self.assertEqual(r.status, Decision.PLAN)
        self.assertEqual(r.selected_action_id, "robust")

    def test_illegal_action_does_not_define_regret_baseline(self):
        actions = [
            ActionCandidate("illegal-super", True, False, False, {"a": 100000, "b": 100000}),
            ActionCandidate("legal", True, False, True, {"a": 10, "b": 10}),
        ]
        r = choose_minimax_regret(actions, RegretPolicy(max_worst_case_regret=0))
        self.assertEqual(r.status, Decision.PLAN)
        self.assertEqual(r.selected_action_id, "legal")

    def test_irreversible_without_human_gate_blocked(self):
        r = choose_minimax_regret([
            ActionCandidate("wipe", False, False, True, {"s": 100}),
        ])
        self.assertEqual(r.status, Decision.FREEZE)
        self.assertIn("IRREVERSIBLE_WITHOUT_HUMAN_GATE:wipe", r.reason_codes)

    def test_irreversible_with_explicit_human_gate_can_be_considered(self):
        r = choose_minimax_regret([
            ActionCandidate("migration", False, True, True, {"s": 100}),
        ], RegretPolicy(max_worst_case_regret=0))
        self.assertEqual(r.status, Decision.PLAN)

    def test_scenario_mismatch_rejected(self):
        with self.assertRaises(Lo4Error):
            choose_minimax_regret([
                ActionCandidate("a", True, False, True, {"x": 1}),
                ActionCandidate("b", True, False, True, {"y": 1}),
            ])

    def test_permutation_determinism(self):
        actions = [
            ActionCandidate("a", True, False, True, {"x": 10, "y": 0}),
            ActionCandidate("b", True, False, True, {"x": 7, "y": 7}),
            ActionCandidate("c", True, False, True, {"x": 0, "y": 10}),
        ]
        fps = {choose_minimax_regret(p).fingerprint for p in itertools.permutations(actions)}
        self.assertEqual(len(fps), 1)


class OptionPreservationTests(unittest.TestCase):
    def setUp(self):
        self.options = [FutureOption("local-model", 5000), FutureOption("new-provider", 3000), FutureOption("offline", 2000)]

    def test_prefers_future_flexibility_when_values_close(self):
        choices = [
            ArchitectureChoice("locked", True, ("new-provider",), 8000, 9000, 8000),
            ArchitectureChoice("adapter", True, ("local-model", "new-provider", "offline"), 1000, 1000, 7000),
        ]
        r = select_option_preserving_choice(self.options, choices)
        self.assertEqual(r.status, Decision.PLAN)
        self.assertEqual(r.selected_choice_id, "adapter")

    def test_hard_constraint_block(self):
        r = select_option_preserving_choice(
            self.options,
            [ArchitectureChoice("bad", False, tuple(), 0, 0, 10000)],
        )
        self.assertEqual(r.status, Decision.FREEZE)

    def test_unknown_option_rejected(self):
        with self.assertRaises(Lo4Error):
            select_option_preserving_choice(
                self.options,
                [ArchitectureChoice("x", True, ("unknown",), 0, 0, 0)],
            )

    def test_permutation_determinism(self):
        choices = [
            ArchitectureChoice("a", True, ("offline",), 3000, 3000, 6000),
            ArchitectureChoice("b", True, ("local-model", "offline"), 2000, 2000, 5500),
            ArchitectureChoice("c", True, ("new-provider",), 1000, 1000, 5000),
        ]
        fps = set()
        for o in itertools.permutations(self.options):
            for c in itertools.permutations(choices):
                fps.add(select_option_preserving_choice(o, c).fingerprint)
        self.assertEqual(len(fps), 1)


class IntegrationTests(unittest.TestCase):
    def _good_stage_results(self):
        surprise = evaluate_surprise_budget([
            NoveltyDimension("experiment-shape", 1000, 1000),
        ])
        anti = refute_feature([BenefitClaim("user-benefit", 8000, 3)], 2000, 1000)
        relax = propose_minimal_relaxation(
            [ConstraintRef("EXP", Authority.EXPERIMENTAL, True, 1)],
            [],
        )
        regret = choose_minimax_regret([
            ActionCandidate("reversible-probe", True, False, True, {"normal": 50, "failure": 40})
        ], RegretPolicy(max_worst_case_regret=0))
        option = select_option_preserving_choice(
            [FutureOption("future", 10000)],
            [ArchitectureChoice("modular", True, ("future",), 0, 0, 5000)],
        )
        return surprise, anti, relax, regret, option

    def test_integrated_lo4_plan_never_claims_canon(self):
        r = integrate_foundry(*self._good_stage_results())
        self.assertEqual(r.status, Decision.PLAN)
        self.assertEqual(r.stage, "lo4_experiment_ready")
        self.assertIn("LO4_ONLY_NOT_CANON", r.reason_codes)
        self.assertIn("HUMAN_OR_FORMAL_PROMOTION_REQUIRED", r.reason_codes)

    def test_freeze_propagates_at_first_failed_stage(self):
        surprise, anti, relax, regret, option = self._good_stage_results()
        bad = evaluate_surprise_budget([
            NoveltyDimension("canon", 1, 10000, Authority.CANON),
        ])
        r = integrate_foundry(bad, anti, relax, regret, option)
        self.assertEqual(r.status, Decision.FREEZE)
        self.assertEqual(r.stage, "surprise_budget")

    def test_need_evidence_blocks_integration(self):
        surprise, _, relax, regret, option = self._good_stage_results()
        anti = refute_feature([BenefitClaim("claim", 9000, 0)], 100, 100)
        r = integrate_foundry(surprise, anti, relax, regret, option)
        self.assertEqual(r.status, Decision.FREEZE)
        self.assertEqual(r.stage, "anti_feature")

    def test_relaxation_proposal_can_reach_human_review_path(self):
        surprise, anti, _, regret, option = self._good_stage_results()
        relax = propose_minimal_relaxation(
            [ConstraintRef("EXP", Authority.EXPERIMENTAL, True, 1)],
            [ConflictSet("c", ("EXP",))],
        )
        r = integrate_foundry(surprise, anti, relax, regret, option)
        self.assertEqual(r.status, Decision.PLAN)
        self.assertEqual(r.stage, "lo4_experiment_ready")
        self.assertIn("EXPERIMENTAL_RELAXATION_REVIEW_REQUIRED", r.reason_codes)

    def test_seeded_fuzz_invariants(self):
        rng = random.Random(20261005)
        for _ in range(250):
            dims = [
                NoveltyDimension(f"d{i}", rng.randint(0, 10000), rng.randint(0, 10000))
                for i in range(rng.randint(1, 8))
            ]
            r = evaluate_surprise_budget(dims, SurprisePolicy(total_budget=20000, max_single_dimension_cost=10000))
            self.assertGreaterEqual(r.total_cost, 0)
            self.assertEqual(tuple(sorted(name for name, _ in r.dimension_costs)), tuple(name for name, _ in r.dimension_costs))


if __name__ == "__main__":
    unittest.main()
