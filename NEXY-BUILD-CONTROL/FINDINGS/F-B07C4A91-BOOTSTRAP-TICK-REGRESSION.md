FINDING_ID: F-B07C4A91-BOOTSTRAP-TICK-REGRESSION
REQ_ID: REQ-DOC-C-STATE-MATRIX-ERROR-001
TASK_ID: T-B07C4A91
FROM: C-B07C4A91
TO: CORE; INTEGRATION; T-D4A71C2E
SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SEVERITY: P0
STATUS: REPRODUCED_BY_SOURCE_TRACE

OBSERVED:
bootstrap() reads the persisted maximum tick before admitting INIT -> READY. If readMaxPersistedTick() throws, the catch currently attempts transitionSystemState("error", "CORE", ...).

SOURCE TRACE:
1. packages/api/bootstrap.ts requires ratcheting the epoch from the persisted maximum before admission.
2. packages/core/tick.ts starts an unsealed process from the genesis floor until setEpochBase(maxPersisted) succeeds.
3. packages/orch-core/system-state.ts persistSystemStateTx() calls currentTick() before terminal incident, audit, envelope and event writes.
4. A transient max-tick read failure followed by successful transition writes can therefore persist a transition with a tick lower than already durable rows.
5. State hydration orders orchestrationEnvelope by createdTick descending, so a lower-tick freeze envelope can fail to become the durable tail even though runtimeState changes after commit.

EXPECTED:
Failure to establish the durable tick floor must not perform durable FSM/event writes using an unratcheted tick source. Startup must remain fail-closed without lower-order evidence.

SPEC/CONTROL CONTEXT:
- Locked final DOC-C does not authorize INIT/READY error -> FREEZE.
- REQ-DOC-C-5-STATE-EVENT-MATRIX forbids those extra error edges.
- DOC-B freeze law requires fail-closed behavior, but does not authorize corrupt ordering evidence.

COUNTEREXAMPLE:
Persisted ledger max tick = T_high.
Process restarts with an unsealed genesis-based epoch.
readMaxPersistedTick() fails transiently.
The catch invokes transitionSystemState("error").
Database writes recover and succeed.
currentTick() emits T_low where T_low < T_high.
A FREEZE transition can commit at T_low while an older higher-tick envelope remains the hydration tail.

IMPACT:
- monotonic event ordering can regress
- durable-tail semantics can diverge from runtime state
- bootstrap failure evidence can become non-canonical
- retaining broad INIT/READY error edges does not solve the integrity defect

SAFE_DIRECTION:
Do not issue a durable state transition from the catch path until the authoritative tick floor is established. Preserve fail-closed admission by aborting startup or another explicitly authorized non-durable boundary mechanism. Exact repair remains DESIGNING and must not invent a DOC-C transition.
