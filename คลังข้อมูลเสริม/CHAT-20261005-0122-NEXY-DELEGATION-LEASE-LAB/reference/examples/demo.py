from nexy_lease import (
    Action,
    AuthorityLease,
    Effect,
    LeaseState,
    Plan,
    POLICY_VERSION,
    evaluate_action,
    plan_fingerprint,
)

plan = Plan((Action("project://demo/report.md", "WRITE", Effect.REVERSIBLE_WRITE, cost_units=2),))
lease = AuthorityLease(
    lease_id="demo-lease",
    subject="demo-agent",
    allowed_resource_patterns=("project://demo/*",),
    allowed_verbs=("WRITE",),
    allowed_effects=(Effect.REVERSIBLE_WRITE,),
    max_cost_units=2,
    max_actions=1,
    issued_at_tick=100,
    expires_at_tick=110,
    plan_hash=plan_fingerprint(plan),
    policy_version=POLICY_VERSION,
)

print(evaluate_action(lease, LeaseState(), plan, 0, logical_tick=100))
