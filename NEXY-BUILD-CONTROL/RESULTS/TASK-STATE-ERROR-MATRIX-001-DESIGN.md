# TASK-STATE-ERROR-MATRIX-001 — Authority-safe repair design

## Status

DESIGN_COMPLETE / SOURCE_MUTATION_BLOCKED_BY_INC-BRANCH-NAMESPACE-001

## FACT

- Locked spec SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
- FINAL VERDICT lines 9844-9854: DOC-C is BUILD SPEC and is the sole source of build obligation.
- Final DOC-C matrix lines 10363-10467 includes `timeout` and `cancel` as SystemEvent values.
- Final matrix permits `error -> FREEZE` from `RUNNING` and `VERIFYING`.
- Final matrix permits `fatal -> STOP` from any state except STOP.
- Final DOC-C Log / Incident Law lines 10494-10502 requires EventLog for every legal transition and a primary incident for transitions to FREEZE/STOP.
- Test-AI TypeScript transition table at source SHA `608426cb30398b1f3461866f7079d2a435c96b96` contains extra `error -> FREEZE` rows from INIT, READY, CONSENSUS, STABLE, FREEZE.
- Test-AI Rust transition table contains `error -> FREEZE` only for RUNNING and VERIFYING.
- The exact-parity contract test compares Rust and TypeScript transition triples.
- `hydrateSystemState()` already uses a process-local FREEZE when durable state cannot be established.
- Bootstrap tick-base failure currently attempts an illegal `error` transition from pre-admission INIT/READY, swallows its denial, emits BOOTSTRAP_FAILED_FREEZE, and can leave runtime state non-FREEZE.

## HISTORICAL TEXT

Earlier vNEXT.1 text at lines 8616-8622 contains `ANY except STOP / error / FREEZE`. It precedes the FINAL VERDICT and final DOC-C section. Under V7 temporal-authority rules it is historical for this affected scope.

## Required source repair

### 1. packages/core/vnext-state-matrix.ts

- Keep the full final DOC-C event set, including timeout and cancel.
- Remove TypeScript error transitions from INIT, READY, CONSENSUS, STABLE, FREEZE.
- Keep error transitions from RUNNING and VERIFYING.
- Keep fatal transitions from every non-STOP state.
- Correct comments so timeout/cancel are not mislabeled as non-DOC-C compatibility rails.
- Do not add transitions solely to support bootstrap.

### 2. tests/contract/state-matrix.test.ts

- Define the final DOC-C event set including timeout and cancel.
- Assert error->FREEZE exists exactly for RUNNING and VERIFYING.
- Assert error is rejected from INIT, READY, CONSENSUS, STABLE, FREEZE, STOP.
- Assert timeout rows exactly where final matrix declares them.
- Assert fatal->STOP for every state except STOP.
- Remove the historical oracle that expects error from every non-STOP state.

### 3. packages/orch-core/system-state.ts

Introduce a narrowly named process-local bootstrap quarantine primitive, e.g.
`quarantineSystemStateForBootstrapFailure()`.

Required behavior:
- If runtime state is not STOP, set process-local runtime state to FREEZE.
- Never create a durable FSM transition or fabricate EventLog/incident evidence.
- Never move STOP back to FREEZE.
- No auto-recovery.
- Document that this is a pre-admission fail-closed quarantine, not a legal SystemEvent transition.

This is consistent with the existing hydration-failure behavior, which already makes runtime state FREEZE when durable truth cannot be established.

### 4. packages/api/bootstrap.ts

- On dependency/tick hydration failure before admission, call the process-local quarantine primitive.
- Do not call `transitionSystemState("error", ...)` from INIT/READY.
- Preserve redacted error output and `BOOTSTRAP_FAILED_FREEZE`.
- Do not admit INIT->READY after the failure.

### 5. tests/coverage/bootstrap-control-plane.test.ts

- Mock the quarantine primitive.
- On tick hydration failure assert quarantine was invoked.
- Assert illegal `error` transition was not invoked.
- Assert bootstrap rejects with BOOTSTRAP_FAILED_FREEZE.

### 6. tests/contract/core-kernel-vnext-parity.test.ts

No semantic relaxation. It should remain an exact parity oracle and pass after TS repair.

## Red-team checks

1. STOP irreversibility: quarantine must not mutate STOP.
2. No audit forgery: quarantine must not claim a legal durable FREEZE transition when persistence/integrity is unavailable.
3. No silent admission: bootstrap must never end READY after dependency integrity failure.
4. No stale historical oracle: no test may use vNEXT.1 `ANY except STOP error` as current DOC-C.
5. Cross-language parity: exact transition triples must match.
6. Repeated bootstrap after quarantine must remain fail-closed unless an explicit legal recovery path establishes truth.
7. Error ownership cannot widen transition legality; an authorized actor is still denied where no transition row exists.

## Acceptance commands once a legal worker branch exists

- `npx vitest run tests/contract/state-matrix.test.ts tests/contract/core-kernel-vnext-parity.test.ts --reporter=verbose`
- `npx vitest run tests/coverage/bootstrap-control-plane.test.ts --reporter=verbose`
- Rust tests covering `core-kernel/src/kernel/vnext_matrix.rs`
- `npm run test:contract`
- affected integration/bootstrap tests
- broader suite required by integration wave risk

Every result must be bound to exact repository, branch, commit SHA, tree SHA, spec hash, command, runner, exit code.

## UNKNOWN

- No executed candidate test exists because V7's required worker branch namespace is structurally impossible while `NEXY.AI-Test-AI` exists.
- Runtime deployment validation failure at integration HEAD has not been proven to be caused by this defect.
- A process-local quarantine is the narrowest design supported by current source behavior and final authority, but it must still receive independent review before integration.
