FINDING_ID: F-C5D62B7F0-DOC-C5-QUARANTINE-RECOVERY
REQ_ID: REQ-DOC-C-5-STATE-EVENT-MATRIX
TASK_ID: TASK-DOC-C5-STATE-MATRIX-001
FROM: C-5D62B7F0
TO: POD-DOC-C5-STATE-MATRIX-001
SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P0
TYPE: DESIGN_COUNTEREXAMPLE
STATUS: OPEN

OBSERVED_DESIGN:
- TASK-STATE-ERROR-MATRIX-001-DESIGN proposes quarantineSystemStateForBootstrapFailure() that changes only process-local runtime state to FREEZE and deliberately does not persist a durable FSM transition.
- Earlier candidate commit 67252bb7980926b2ab686682d02d697c77ffc461 implemented exactly that helper; 533748e07ebc50a1a6122fea79ac4dab0a4bc1e0 wired it into bootstrap.

COUNTEREXAMPLE:
1. Durable FSM state is READY (or INIT) and hydrateSystemState() succeeds.
2. Later bootstrap tick/dependency read fails.
3. Proposed helper changes runtime state to FREEZE only; durable state remains READY/INIT.
4. A canonical recovery attempt calls transitionSystemState('recover','OWNER', guards={freeze_recovery_allowed:true,not_in_stop:true}).
5. system-state.ts preflight uses runtime FREEZE, so FREEZE+recover->READY passes.
6. Inside the SERIALIZABLE transaction, readDurableSystemStateTx() returns durable READY/INIT.
7. vnextTransition(observedFrom,'recover',...) rejects because final DOC-C allows recover only from FREEZE.
8. The VNextStateTransitionDeniedError catch assigns runtimeState.state = observedFrom before rethrowing.
9. Result: the recovery call fails but runtime state is silently restored to READY/INIT, defeating the process-local quarantine.

EXACT_SOURCE_EVIDENCE:
- packages/orch-core/system-state.ts@1883414a3d8b2034d06ef30e039b537319e2e0f1: transitionSystemState preflights runtime state, then rechecks durable state, and on transition denial writes runtimeState.state = observedFrom.
- Final DOC-C §5.2 permits FREEZE+recover->READY but not READY/INIT+recover.
- Final DOC-C §5.6 requires legal transition evidence; the quarantine intentionally creates none, so runtime/durable divergence is inherent in the proposed mechanism.

EXPECTED:
- A pre-admission fail-closed mechanism must not be escapable by a failed recovery attempt.
- Runtime and durable truth must not be reconciled toward a less-safe state merely because a transition was denied.
- Recovery semantics for a non-durable bootstrap quarantine must be explicitly defined and tested before implementation.

REPRODUCTION_TEST_TO_ADD:
- Start with durable READY and runtime READY.
- invoke proposed bootstrap quarantine -> runtime FREEZE, durable READY.
- attempt recover.
- assert recovery is denied AND runtime remains fail-closed; it must not become READY/INIT.

ALTERNATIVES_FOR_DESIGN_REVIEW:
- represent bootstrap admission quarantine separately from canonical FSM state and gate admission explicitly, or
- make transition denial preserve a stronger local quarantine when durable state is less safe, or
- define another Spec-supported durable quarantine/recovery mechanism.
Do not choose among these without authority/evidence.

NO_SOURCE_MUTATION: true
