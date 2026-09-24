# NEXY Auditor Playbook

## Universal audit law
1. Pin exact repository/branch/HEAD and observed environment.
2. Resolve source authority/scope before implementation.
3. Separate SOURCE / IMPLEMENTATION / TEST / RUNTIME / DEPLOYMENT / PHYSICAL evidence.
4. Never infer PASS from code/docs/build alone.
5. Preserve failure evidence and unresolved UNKNOWN explicitly.

# Workflow: Audit Cross-System Composition

## Sequence
1. Select target change/system.
2. Expand dependencies + dependents from graph.
3. Expand linked requirements/contracts/invariants/FSM/state/security/events/config.
4. Inspect authority transitions between systems.
5. Verify uncertainty/failure/state is propagated, not reset.
6. Verify one subsystem cannot convert another subsystem's BLOCK/FREEZE into success.
7. Verify namespaced states/contracts are not conflated.
8. Test end-to-end failure paths across boundaries.
9. Check observability and incident correlation through request/trace IDs.
10. Re-audit all affected systems after any repair.

## DONE
Composition preserves every higher-order invariant, not only local module tests.
