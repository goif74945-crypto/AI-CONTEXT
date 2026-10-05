# Shadow Review — Freeze-Recover Error Matrix

CHAT_ID: C-3B5E71A2
TASK_ID: TASK-DOC-C4-FREEZE-RECOVER-ERROR-MATRIX-001
FINDING_ID: FINDING-DOC-C4-FREEZE-RECOVER-ERROR-MATRIX-001
REQ_ID: REQ-DOC-C-4-2-FREEZE-RECOVER
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
DIRECTIVES_BLOB: 8cd214c87e5aa55561e52347802ec8172feadc36
INTEGRATION_TEST_BLOB: d197936bc15b92ce5be4e5119457f2c687c314c6
ROLE: SHADOW_REVIEWER
VERDICT: FINDING_CONFIRMED_P1

## Authoritative facts

Final DOC-C §4.2 declares the route-specific pairs:
- 403 FORBIDDEN
- 409 FREEZE_RECOVERY_DENIED
- 423 SYSTEM_IN_FREEZE

Final DOC-C §5 state/event matrix declares:
- FREEZE + recover -> READY

DOC-C does not provide a finer per-condition explanation for when the freeze-recover route should emit 423 SYSTEM_IN_FREEZE.

## Exact-head drift

- missing incident -> 404 FREEZE_RECOVERY_DENIED (undeclared route-specific pair)
- unowned incident -> 404 FREEZE_RECOVERY_DENIED (undeclared route-specific pair)
- current runtime state != FREEZE -> 423 FREEZE_RECOVERY_DENIED (declared status with wrong declared code)
- durable state changes away from FREEZE before transaction commit -> 423 FREEZE_RECOVERY_DENIED (same wrong pair)
- tests preserve at least the 423 FREEZE_RECOVERY_DENIED drift

## Safe repair constraints

- Missing and unowned incidents must remain externally indistinguishable to preserve tenant isolation.
- A recovery request that is not eligible to recover is semantically a recovery denial; 409 FREEZE_RECOVERY_DENIED is the least-authority route-specific pair for such denial paths.
- Do not manufacture a 423 SYSTEM_IN_FREEZE trigger merely to make every declared pair appear in code. The active DOC-C text lists the pair but does not state the exact trigger for this recovery route.
- Keep 403 FORBIDDEN for authority/RBAC denial.
- Preserve CSRF, session/device binding, project ownership proof, exact idempotency binding, mandatory denial audit, serializable recovery transaction, and fail-closed persistence behavior.

## Required oracle changes

- Remove assertions that 404 FREEZE_RECOVERY_DENIED is canonical.
- Remove assertions that 423 FREEZE_RECOVERY_DENIED is canonical.
- Add closed assertions that any route-specific error pair emitted by tested recovery denial paths belongs to the DOC-C declared set.
- Retain independent tests for tenant non-enumeration and denial-audit persistence failure.

## Unknown requiring fail-closed treatment

TRIGGER_FOR_423_SYSTEM_IN_FREEZE_ON_FREEZE_RECOVER: UNKNOWN_FROM_FINAL_DOC_C.
Do not guess a new semantic trigger. This does not invalidate the reproduced mismatch; it constrains the repair not to invent behavior.

SOURCE_MUTATION: NONE
UPSTREAM_MUTATION: NONE
MUTATION_BLOCKER: INC-BRANCH-NAMESPACE-001
