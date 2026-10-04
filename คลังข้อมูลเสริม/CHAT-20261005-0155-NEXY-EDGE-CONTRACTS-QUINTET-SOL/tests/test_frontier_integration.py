import unittest

from frontierfive import (
    Claim, EvidenceAction, FieldSpec, PolicyPoint, Witness,
    apply_adapter, audit_monotonicity, compile_adapter,
    issue_seal, plan_evidence_closure, verify_independent_quorum, verify_seal,
)


class FrontierIntegrationTests(unittest.TestCase):
    def test_safe_pipeline_composes(self):
        # 1) safe contract migration
        adapter = compile_adapter(
            {"old_id": FieldSpec("old_id", "string")},
            {"id": FieldSpec("id", "string", aliases=("old_id",))},
        )
        self.assertEqual(adapter.status, "ALLOW")
        migrated = apply_adapter({"old_id": "42"}, adapter.payload["adapter"])
        self.assertEqual(migrated, {"id": "42"})

        # 2) plan-bound approval
        plan = {"adapter_hash": adapter.payload["adapter_hash"], "record": migrated}
        key = b"integration-test-key"
        seal = issue_seal(
            plan, authority_id="human", allowed_scope=["tool:adapter"],
            expires_at=10, directive_epoch=2, max_mutations=1, key=key,
        )
        self.assertEqual(
            verify_seal(
                plan, seal, requested_scope=["tool:adapter"], mutation_count=1,
                now=9, current_directive_epoch=2, key=key,
            ).status,
            "ALLOW",
        )

        # 3) minimal evidence closure
        closure = plan_evidence_closure(
            claims={"static": Claim("static", 1), "unit": Claim("unit", 2, ("static",))},
            targets=["unit"], existing={},
            actions=[
                EvidenceAction("compile", (("static", 1),), 1),
                EvidenceAction("unit", (("unit", 2),), 1, requires=(("static", 1),)),
            ],
        )
        self.assertEqual(closure.status, "ALLOW")

        # 4) independent evidence quorum
        quorum = verify_independent_quorum(
            [
                Witness("w1", "unit", "artifact", "PASS", ("model:a", "runtime:a")),
                Witness("w2", "unit", "artifact", "PASS", ("model:b", "runtime:b")),
            ],
            claim_id="unit", artifact_hash="artifact", k=2,
        )
        self.assertEqual(quorum.status, "ALLOW")

        # 5) monotonic policy audit before release
        policy = audit_monotonicity(
            [PolicyPoint("low", (0,), "ALLOW"), PolicyPoint("high", (1,), "FREEZE")],
            directions=(1,), decision_rank={"ALLOW": 0, "FREEZE": 1},
        )
        self.assertEqual(policy.status, "ALLOW")

    def test_verdict_fingerprints_are_stable(self):
        claims = {"c": Claim("c", 1)}
        actions = [EvidenceAction("a", (("c", 1),), 1)]
        a = plan_evidence_closure(claims=claims, targets=["c"], existing={}, actions=actions)
        b = plan_evidence_closure(claims=claims, targets=["c"], existing={}, actions=actions)
        self.assertEqual(a.canonical_dict(), b.canonical_dict())
        self.assertEqual(a.fingerprint, b.fingerprint)
