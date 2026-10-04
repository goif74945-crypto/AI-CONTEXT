# Requirement Traceability Graph
SPEC -> REQUIREMENT -> DESIGN_DECISION -> IMPLEMENTATION_TARGET -> TEST -> EVIDENCE -> RELEASE_GATE.

Requirement atom: req_id, source_locator, statement, priority, immutable, scope, dependencies, implementation_targets, verification_targets, status, evidence_ids.

Rules:
T1 Requirement without verifier is incomplete.
T2 Negative requirements are first-class and require adversarial tests.
T3 A material change invalidates dependent evidence until reverified.
T4 Unmapped tests require justification as cross-cutting quality infrastructure or scope review.

Change impact: enumerate touched contracts; reverse-traverse dependents; select gates; run narrow tests; run cross-cutting gates; update evidence ledger.

Cross-cutting gates: authn/authz, data isolation, schema compatibility, identity/routing, error semantics, observability, specified performance budgets, accessibility for UI, recovery/idempotency for mutations.

Release predicate: critical requirements PASS AND critical regressions PASS AND evidence fresh.
