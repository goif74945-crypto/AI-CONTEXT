FAILURE_ID: FAIL-E4C19A73-5034-STATE-PARITY
REPORTER_CHAT: C-E4C19A73
TASK_ID: T-D4A71C2E
SEVERITY: P1
STATUS: OPEN
HEAD_SHA: 5034debdadb1f21c7d5312e6f0ad7fd44280718c
RAILWAY_DEPLOYMENT: 3356b6d7-a35c-4aa5-b25c-aedc67367ded

SUMMARY:
Exact work-branch validation reached npm run test:contract and failed because the TypeScript VNext transition matrix now permits error->FREEZE only from RUNNING and VERIFYING, while Rust parity and bootstrap/persistence contracts still require error->FREEZE from additional non-STOP states.

EXECUTION_EVIDENCE:
- Test Files: 3 failed | 114 passed (117)
- Tests: 5 failed | 647 passed (652)
- Build failure stage: npm run test:contract, exit code 1
- Source-identity gate was passed; this is executable source/integration evidence, not the earlier provider-identity drift.

OBSERVED_FAILURES:
1. tests/contract/core-kernel-vnext-parity.test.ts reports five extra Rust transition triples relative to TypeScript:
   - Init|Error|Freeze
   - Ready|Error|Freeze
   - Consensus|Error|Freeze
   - Stable|Error|Freeze
   - Freeze|Error|Freeze
2. tests/contract/hydration-fail-closed.test.ts bootstrap failure path expects FREEZE but remains INIT after the INIT error transition is denied.
3. tests/contract/system-state-persistence.test.ts global incident path from READY is denied instead of freezing.
4. tests/contract/system-state-persistence.test.ts expected AUDIT_PERSIST_FAILED_FREEZE but receives STATE_TRANSITION_DENIED for READY --error--> by CORE.
5. Rust kernel test error_freezes_every_non_stop_state passes, confirming the Rust matrix still implements the broader error law.

FACT:
- TypeScript transition commit 27af7f93893c7589e516c269fae41aa467c2cdb9 removed five non-RUNNING/VERIFYING error edges.
- Exact-head Railway validation at 5034debdadb1f21c7d5312e6f0ad7fd44280718c executed contract tests.
- Rust and multiple higher-level contracts remain semantically broader than the TypeScript matrix.

ASSUMPTION:
- None about which side should be changed. Authority reconciliation is required before mutation because the final DOC-C matrix is narrower while existing fail-closed/bootstrap contracts and Rust kernel encode broader freeze behavior.

UNKNOWN:
- Whether the final DOC-C transition table intentionally supersedes the earlier broad ANY-except-STOP error law for bootstrap/persistence failures, or whether those failures must reach FREEZE via another canonical mechanism.

AFFECTED_PATHS:
- packages/core/vnext-state-matrix.ts
- core-kernel/src/kernel/vnext_matrix.rs
- packages/api/bootstrap.ts
- packages/orch-core/system-state.ts
- tests/contract/core-kernel-vnext-parity.test.ts
- tests/contract/hydration-fail-closed.test.ts
- tests/contract/system-state-persistence.test.ts

NEXT_ACTION:
Reconcile authoritative error/freeze semantics, then repair all language/runtime consumers consistently. Do not weaken parity or delete failing tests.

EVIDENCE_REFS:
- Railway deployment 3356b6d7-a35c-4aa5-b25c-aedc67367ded
- NEXY work HEAD 5034debdadb1f21c7d5312e6f0ad7fd44280718c
- state-matrix repair commit 27af7f93893c7589e516c269fae41aa467c2cdb9
