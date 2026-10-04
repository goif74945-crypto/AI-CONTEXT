import unittest

from frontier5 import (
    Ambiguity,
    Capability,
    CapabilityRouter,
    Claim,
    DecisionPatchCompressor,
    DecisionRule,
    DecisionSnapshot,
    Experiment,
    ExperimentCompiler,
    ExperimentError,
    FailureScenario,
    MeshError,
    MissionStep,
    Plan,
    ResilienceEngine,
    UncertaintyMesh,
)


class UncertaintyMeshTests(unittest.TestCase):
    def test_stale_source_blocks_downstream_decision(self):
        mesh = UncertaintyMesh()
        mesh.add(Claim("source", 0.99, evidence_age_s=11, ttl_s=10))
        mesh.add(Claim("derived", 0.95, dependencies=("source",)))
        status = mesh.decision_status(DecisionRule("ship", ("derived",), 0.8))
        self.assertEqual(status["status"], "BLOCKED")
        self.assertEqual(status["scores"]["derived"], 0.0)

    def test_impact_propagates_transitively(self):
        mesh = UncertaintyMesh()
        mesh.add(Claim("a", 1.0))
        mesh.add(Claim("b", 1.0, dependencies=("a",)))
        mesh.add(Claim("c", 1.0, dependencies=("b",)))
        self.assertEqual(mesh.impacted_by(["a"]), ["a", "b", "c"])

    def test_cycle_is_rejected(self):
        mesh = UncertaintyMesh({
            "a": Claim("a", 1.0, dependencies=("b",)),
            "b": Claim("b", 1.0, dependencies=("a",)),
        })
        with self.assertRaises(MeshError):
            mesh.validate()

    def test_5000_node_chain_avoids_recursion_limit(self):
        mesh = UncertaintyMesh()
        mesh.add(Claim("n0", 1.0))
        for index in range(1, 5000):
            mesh.add(Claim(f"n{index}", 1.0, dependencies=(f"n{index - 1}",)))
        self.assertEqual(mesh.effective_confidence("n4999"), 1.0)
        self.assertEqual(len(mesh.impacted_by(["n0"])), 5000)


class ExperimentCompilerTests(unittest.TestCase):
    def test_rejects_irreversible_and_picks_safe_cover(self):
        ambiguities = [Ambiguity("auth", 10, 2, True), Ambiguity("format", 3, 3)]
        experiments = [
            Experiment("danger", ("auth", "format"), 10, 0, 0, False),
            Experiment("probe-auth", ("auth",), 3, 1, 0.1, True),
            Experiment("probe-format", ("format",), 2, 1, 0, True),
        ]
        chosen = ExperimentCompiler().compile(ambiguities, experiments)
        self.assertNotIn("danger", chosen)
        self.assertEqual(set(chosen), {"probe-auth", "probe-format"})

    def test_uncoverable_ambiguity_fails_closed(self):
        with self.assertRaises(ExperimentError):
            ExperimentCompiler().compile([Ambiguity("x", 1, 2)], [])

    def test_duplicate_experiment_ids_are_rejected(self):
        ambiguity = [Ambiguity("x", 1, 2)]
        experiment = Experiment("dup", ("x",), 1, 1, 0, True)
        with self.assertRaises(ExperimentError):
            ExperimentCompiler().compile(ambiguity, [experiment, experiment])


class CapabilityRouterTests(unittest.TestCase):
    def test_does_not_relax_permission_or_reversibility(self):
        capabilities = [
            Capability("fast-write", frozenset({"mutate"}), frozenset({"write"}), 0.99, 10, False),
            Capability("safe-write", frozenset({"mutate"}), frozenset({"write"}), 0.98, 20, True),
        ]
        route = CapabilityRouter(capabilities).route([
            MissionStep("s", "mutate", "write", require_reversible=True)
        ])
        self.assertEqual(route[0]["tool_id"], "safe-write")

    def test_freshness_requirement_blocks_stale_tool(self):
        capabilities = [
            Capability("cached", frozenset({"facts"}), frozenset(), 1.0, 1, True, freshness_s=100)
        ]
        route = CapabilityRouter(capabilities).route([
            MissionStep("s", "facts", max_freshness_s=10)
        ])
        self.assertEqual(route[0]["status"], "BLOCKED")


class DecisionPatchTests(unittest.TestCase):
    def test_no_change_is_silent(self):
        snapshot = DecisionSnapshot({"x": "1"}, ("a",), (), ("do",))
        compressor = DecisionPatchCompressor()
        self.assertEqual(compressor.render_lines(compressor.diff(snapshot, snapshot)), ["NO_DECISION_CHANGE"])

    def test_patch_only_contains_delta(self):
        before = DecisionSnapshot({"price": "10", "stock": "yes"}, ("buy",), (), ("checkout",))
        after = DecisionSnapshot({"price": "12", "stock": "yes"}, ("wait",), ("price-rise",), ())
        compressor = DecisionPatchCompressor()
        lines = compressor.render_lines(compressor.diff(before, after))
        self.assertTrue(any("price" in line for line in lines))
        self.assertFalse(any("stock" in line for line in lines))
        self.assertIn("RECOMMENDATION REMOVED: buy", lines)


class ResilienceEngineTests(unittest.TestCase):
    def test_fallback_recovers_tool_outage(self):
        plan = Plan("p", required_tools=frozenset({"primary"}), fallbacks={"tool:primary": "secondary"})
        result = ResilienceEngine().evaluate(
            plan,
            FailureScenario("outage", unavailable_tools=frozenset({"primary"})),
        )
        self.assertEqual(result["status"], "SURVIVES")
        self.assertEqual(result["recovered"], ["tool:primary->secondary"])

    def test_missing_schema_fallback_fails(self):
        plan = Plan("p", schema_dependencies=frozenset({"v2"}))
        result = ResilienceEngine().evaluate(
            plan,
            FailureScenario("drift", schema_breaks=frozenset({"v2"})),
        )
        self.assertEqual(result["status"], "FAILS")

    def test_matrix_ratio(self):
        plan = Plan("p", required_tools=frozenset({"a"}), fallbacks={"tool:a": "b"})
        scenarios = [FailureScenario("ok"), FailureScenario("out", unavailable_tools=frozenset({"a"}))]
        self.assertEqual(ResilienceEngine().matrix(plan, scenarios)["survival_ratio"], 1.0)


class IntegratedFlowTests(unittest.TestCase):
    def test_frontier_five_pipeline(self):
        mesh = UncertaintyMesh()
        mesh.add(Claim("availability", 0.99, evidence_age_s=120, ttl_s=60))
        self.assertEqual(
            mesh.decision_status(DecisionRule("book", ("availability",)))["status"],
            "BLOCKED",
        )

        selected = ExperimentCompiler().compile(
            [Ambiguity("availability-freshness", 9, 2)],
            [Experiment("read-only-refresh", ("availability-freshness",), 4, 1, 0, True)],
        )
        self.assertEqual(selected, ["read-only-refresh"])

        router = CapabilityRouter([
            Capability("cache", frozenset({"availability"}), frozenset({"read"}), 1.0, 1, True, freshness_s=120),
            Capability("live", frozenset({"availability"}), frozenset({"read"}), 0.99, 20, True, freshness_s=2),
        ])
        routed = router.route([
            MissionStep("refresh", "availability", "read", 0.9, True, 10)
        ])
        self.assertEqual(routed[0]["tool_id"], "live")

        before = DecisionSnapshot({"availability": "stale"}, (), ("needs-refresh",), ())
        after = DecisionSnapshot({"availability": "confirmed"}, ("book",), (), ("book-now",))
        compressor = DecisionPatchCompressor()
        lines = compressor.render_lines(compressor.diff(before, after))
        self.assertTrue(any("availability" in line for line in lines))
        self.assertTrue(any("book-now" in line for line in lines))

        plan = Plan(
            "booking",
            required_tools=frozenset({"live"}),
            fallbacks={"tool:live": "alternate-live"},
        )
        verdict = ResilienceEngine().evaluate(
            plan,
            FailureScenario("live-outage", unavailable_tools=frozenset({"live"})),
        )
        self.assertEqual(verdict["status"], "SURVIVES")


if __name__ == "__main__":
    unittest.main(verbosity=2)
