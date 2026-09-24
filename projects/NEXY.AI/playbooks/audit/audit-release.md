# NEXY Auditor Playbook

## Universal audit law
1. Pin exact repository/branch/HEAD and observed environment.
2. Resolve source authority/scope before implementation.
3. Separate SOURCE / IMPLEMENTATION / TEST / RUNTIME / DEPLOYMENT / PHYSICAL evidence.
4. Never infer PASS from code/docs/build alone.
5. Preserve failure evidence and unresolved UNKNOWN explicitly.

# Workflow: Audit Release / Deployment Gate

## Sequence
1. Pin exact release artifact/commit/environment.
2. Resolve required DOC-E evidence set.
3. Validate contract/API/FSM/RBAC/auth-abuse/queue/observability/incident/migration/rollback evidence freshness.
4. Verify release policy thresholds and LAW/JUDGE gates.
5. Run negative freeze path in target-like environment.
6. Verify canary/rollback/monitoring commands are executable, not prose placeholders.
7. Confirm evidence metadata binds to exact release.
8. Reject stale evidence from another commit/environment.
9. Confirm no source-only/future/physical claim is promoted into deployment PASS.
10. Produce release verdict with missing evidence listed explicitly.

## DONE
Deployment PASS requires current, exact, executed proof—not repository completeness.
