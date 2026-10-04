import unittest

from lo4_flight_chamber import (
    AuthorityClass, BehaviorContract, Capability, Decision, TournamentCandidate,
    behavioral_similarity, contract_fingerprint, novelty_report,
    challenge_invariants, discover_invariants, review_eligibility,
    minimize_integration_surface, distill_guard, run_tournament,
)


class NoveltyTests(unittest.TestCase):
    def test_identical_contract_is_high_overlap(self):
        c = BehaviorContract("A", frozenset({"request"}), frozenset({"decision"}), frozenset({"freeze_on_unknown"}), frozenset({"unknown"}), frozenset(), frozenset({"unit"}))
        r = novelty_report(c, [c])
        self.assertEqual(r["classification"], "HIGH_OVERLAP")
        self.assertEqual(r["top_score"], 1.0)

    def test_distinct_failure_and_side_effect_contract_stays_distinct(self):
        a = BehaviorContract("A", failures=frozenset({"schema drift"}), side_effects=frozenset({"none"}))
        b = BehaviorContract("B", failures=frozenset({"human authority conflict"}), side_effects=frozenset({"write tool"}))
        self.assertLess(behavioral_similarity(a, b), 0.82)

    def test_fingerprint_is_deterministic_and_order_independent(self):
        a = BehaviorContract("A", inputs=frozenset({"B", "a"}))
        b = BehaviorContract("A", inputs=frozenset({"a", "B"}))
        self.assertEqual(contract_fingerprint(a), contract_fingerprint(b))

    def test_negative_weight_rejected(self):
        a = BehaviorContract("A")
        with self.assertRaises(ValueError):
            behavioral_similarity(a, a, {"inputs": -1.0})


class InvariantTests(unittest.TestCase):
    def setUp(self):
        self.traces = [
            {"mode": "safe", "seq": 1, "status": "PASS"},
            {"mode": "safe", "seq": 2, "status": "PASS"},
            {"mode": "safe", "seq": 3, "status": "PASS"},
        ]

    def test_discovers_constant_and_monotonic_candidates(self):
        invs = discover_invariants(self.traces)
        exprs = {x.expression for x in invs}
        self.assertIn("mode == 'safe'", exprs)
        self.assertIn("seq is nondecreasing", exprs)

    def test_discovery_is_experimental_only(self):
        self.assertTrue(all(i.authority == AuthorityClass.EXPERIMENTAL for i in discover_invariants(self.traces)))

    def test_counterexample_falsifies_candidate(self):
        invs = discover_invariants(self.traces)
        challenged = challenge_invariants(invs, [{"mode": "unsafe", "seq": 4, "status": "PASS"}])
        mode = next(i for i in challenged if i.kind == "constant" and i.field == "mode")
        self.assertTrue(mode.falsified)
        self.assertEqual(review_eligibility(mode), AuthorityClass.EXPERIMENTAL)

    def test_clean_candidate_can_only_become_review_eligible(self):
        inv = next(i for i in discover_invariants(self.traces) if i.kind == "nondecreasing" and i.field == "seq")
        checked = challenge_invariants([inv], [{"seq": 4}, {"seq": 5}])[0]
        self.assertEqual(review_eligibility(checked, 5), AuthorityClass.ELIGIBLE_FOR_HUMAN_REVIEW)
        self.assertNotEqual(review_eligibility(checked, 5), AuthorityClass.AI_PROPOSED)

    def test_too_few_traces_yields_no_invariants(self):
        self.assertEqual(discover_invariants([{"x": 1}]), ())


class SurfaceTests(unittest.TestCase):
    def test_transitive_closure_is_minimal(self):
        caps = {
            "read_context": Capability("read_context", "read"),
            "evaluate": Capability("evaluate", "compute", frozenset({"read_context"})),
            "render": Capability("render", "output", frozenset({"evaluate"})),
            "unused": Capability("unused", "read"),
        }
        p = minimize_integration_surface(["render"], caps)
        self.assertEqual(p.decision, Decision.PASS)
        self.assertEqual(set(p.required_capabilities), {"read_context", "evaluate", "render"})
        self.assertNotIn("unused", p.required_capabilities)

    def test_protected_capability_freezes(self):
        caps = {"write_canon": Capability("write_canon", "write", protected=True)}
        p = minimize_integration_surface(["write_canon"], caps)
        self.assertEqual(p.decision, Decision.FREEZE)
        self.assertIn("write_canon", p.blocked_capabilities)

    def test_missing_capability_freezes(self):
        self.assertEqual(minimize_integration_surface(["missing"], {}).decision, Decision.FREEZE)

    def test_cycle_freezes(self):
        caps = {
            "a": Capability("a", "compute", frozenset({"b"})),
            "b": Capability("b", "compute", frozenset({"a"})),
        }
        self.assertEqual(minimize_integration_surface(["a"], caps).decision, Decision.FREEZE)

    def test_forbidden_dependency_freezes_parent(self):
        caps = {
            "secret": Capability("secret", "read"),
            "task": Capability("task", "compute", frozenset({"secret"})),
        }
        p = minimize_integration_surface(["task"], caps, forbidden={"secret"})
        self.assertEqual(p.decision, Decision.FREEZE)
        self.assertIn("task", p.blocked_capabilities)


class GuardTests(unittest.TestCase):
    def test_finds_smallest_guard(self):
        positives = [("p1", {"verified": True, "risk": 1}), ("p2", {"verified": True, "risk": 2})]
        negatives = [("n1", {"verified": False, "risk": 1}), ("n2", {"verified": False, "risk": 9})]
        predicates = {
            "verified": lambda x: x.get("verified") is True,
            "risk_under_5": lambda x: x.get("risk", 99) < 5,
        }
        g = distill_guard(positives, negatives, predicates)
        self.assertEqual(g.decision, Decision.REVIEW)
        self.assertEqual(g.predicates, ("verified",))

    def test_no_safe_guard_freezes(self):
        positives = [("p", {"x": 1})]
        negatives = [("n", {"x": 1})]
        g = distill_guard(positives, negatives, {"x1": lambda r: r["x"] == 1})
        self.assertEqual(g.decision, Decision.FREEZE)

    def test_guard_is_experimental(self):
        g = distill_guard([("p", {"ok": True})], [("n", {"ok": False})], {"ok": lambda r: r["ok"]})
        self.assertEqual(g.authority, AuthorityClass.EXPERIMENTAL)

    def test_empty_negative_set_freezes(self):
        g = distill_guard([("p", {"ok": True})], [], {"ok": lambda r: r["ok"]})
        self.assertEqual(g.decision, Decision.FREEZE)


class TournamentTests(unittest.TestCase):
    def candidate(self, name, score, hard=True, evidence=("E1",)):
        return TournamentCandidate(name, {"utility": score, "safety": score}, {"canon": hard}, evidence)

    def test_hard_constraint_excludes_candidate(self):
        r = run_tournament([self.candidate("unsafe", 1.0, hard=False), self.candidate("safe", 0.7)], {"utility": 0.5, "safety": 0.5})
        self.assertEqual(r.winner, "safe")
        self.assertIn(("unsafe", "hard_constraint_failed"), r.excluded)

    def test_missing_evidence_excludes_candidate(self):
        r = run_tournament([self.candidate("a", 1.0, evidence=()), self.candidate("b", 0.5)], {"utility": 1.0})
        self.assertEqual(r.winner, "b")

    def test_tie_freezes_instead_of_arbitrary_choice(self):
        r = run_tournament([self.candidate("a", 0.5), self.candidate("b", 0.5)], {"utility": 1.0})
        self.assertEqual(r.decision, Decision.FREEZE)
        self.assertIsNone(r.winner)

    def test_winner_is_review_not_canon(self):
        r = run_tournament([self.candidate("a", 0.8), self.candidate("b", 0.5)], {"utility": 1.0})
        self.assertEqual(r.decision, Decision.REVIEW)
        self.assertEqual(r.authority, AuthorityClass.AI_PROPOSED)

    def test_missing_metric_excludes(self):
        c = TournamentCandidate("a", {"utility": 1.0}, {"canon": True}, ("E1",))
        r = run_tournament([c], {"utility": 1.0, "safety": 1.0})
        self.assertEqual(r.decision, Decision.FREEZE)


class IntegrationTests(unittest.TestCase):
    def test_five_system_pipeline(self):
        existing = [BehaviorContract("old", failures=frozenset({"schema drift"}), side_effects=frozenset({"none"}))]
        candidate_contract = BehaviorContract(
            "flight_chamber",
            inputs=frozenset({"lo4 proposals", "evidence"}),
            outputs=frozenset({"review candidate"}),
            invariants=frozenset({"never auto-promote canon", "freeze on missing proof"}),
            failures=frozenset({"semantic duplicate", "privilege escalation"}),
            side_effects=frozenset({"none"}),
            evidence=frozenset({"unit", "integration"}),
        )
        self.assertEqual(novelty_report(candidate_contract, existing)["classification"], "DISTINCT")

        invs = discover_invariants([
            {"authority": "AI_PROPOSED", "score": 1},
            {"authority": "AI_PROPOSED", "score": 2},
            {"authority": "AI_PROPOSED", "score": 3},
        ])
        authority_inv = next(i for i in invs if i.kind == "constant" and i.field == "authority")
        authority_checked = challenge_invariants([authority_inv], [{"authority": "AI_PROPOSED", "score": 4}, {"authority": "AI_PROPOSED", "score": 5}])[0]
        self.assertEqual(review_eligibility(authority_checked, 5), AuthorityClass.ELIGIBLE_FOR_HUMAN_REVIEW)

        caps = {
            "read_proposals": Capability("read_proposals", "read"),
            "evaluate_offline": Capability("evaluate_offline", "compute", frozenset({"read_proposals"})),
            "publish_review_packet": Capability("publish_review_packet", "write", frozenset({"evaluate_offline"})),
            "write_canon": Capability("write_canon", "write", protected=True),
        }
        plan = minimize_integration_surface(["publish_review_packet"], caps, forbidden={"write_canon"})
        self.assertEqual(plan.decision, Decision.PASS)
        self.assertNotIn("write_canon", plan.required_capabilities)

        guard = distill_guard(
            [("p", {"evidence": 2, "canon_write": False})],
            [("n1", {"evidence": 0, "canon_write": False}), ("n2", {"evidence": 2, "canon_write": True})],
            {
                "evidence_present": lambda r: r["evidence"] > 0,
                "no_canon_write": lambda r: r["canon_write"] is False,
            },
        )
        self.assertEqual(guard.decision, Decision.REVIEW)
        self.assertEqual(set(guard.predicates), {"evidence_present", "no_canon_write"})

        tournament = run_tournament([
            TournamentCandidate("candidate-A", {"benefit": 0.9, "risk_margin": 0.8}, {"canon_safe": True, "novel": True}, ("E-unit", "E-int")),
            TournamentCandidate("candidate-B", {"benefit": 0.8, "risk_margin": 0.95}, {"canon_safe": True, "novel": True}, ("E-unit", "E-int")),
        ], {"benefit": 0.7, "risk_margin": 0.3}, minimum_evidence=2)
        self.assertEqual(tournament.decision, Decision.REVIEW)
        self.assertEqual(tournament.winner, "candidate-A")

    def test_protected_canon_path_blocks_pipeline(self):
        caps = {"write_canon": Capability("write_canon", "write", protected=True)}
        self.assertEqual(minimize_integration_surface(["write_canon"], caps).decision, Decision.FREEZE)


if __name__ == "__main__":
    unittest.main()
