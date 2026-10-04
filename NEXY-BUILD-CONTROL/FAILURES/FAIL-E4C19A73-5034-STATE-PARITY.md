FAILURE_ID: FAIL-E4C19A73-5034-STATE-PARITY
REPORTER_CHAT: C-E4C19A73
TASK_ID: T-D4A71C2E
SEVERITY: P1
STATUS: OPEN
ORIGINAL_EXECUTION_HEAD_SHA: 5034debdadb1f21c7d5312e6f0ad7fd44280718c
CURRENT_OBSERVED_HEAD_SHA: d1d80ce99d533a79294425ebcfe132551b26cc43
RAILWAY_EXECUTION_DEPLOYMENT: 3356b6d7-a35c-4aa5-b25c-aedc67367ded

ORIGINAL_EXECUTION_EVIDENCE:
- Exact 5034debd validation reached npm run test:contract.
- Test Files: 3 failed | 114 passed (117)
- Tests: 5 failed | 647 passed (652)
- Build failed at npm run test:contract, exit code 1.
- Failures proved TypeScript/Rust/bootstrap-persistence state semantics were inconsistent.

AUTHORITY_RECONCILIATION:
- Authoritative FINAL VERDICT says DOC-C is build authority.
- Final DOC-C 5.2 matrix has error->FREEZE only from RUNNING and VERIFYING.
- Final DOC-C 5.4 is Owner Actions.
- Earlier pre-final text contains ANY except STOP + error -> FREEZE, but it is not the final DOC-C matrix.
- Independent reviewer C-5E4C5301 separately inspected the DOCX and confirmed commit 27af7f's 21-edge relation matches final DOC-C: 11 nonfatal final-matrix edges + 7 fatal edges + 3 owner hard-kill cancel edges.

CURRENT_BRANCH_REGRESSION:
- 18451169d54f733a032a9dd0f2f11250b5db0810 restored five broad TypeScript error edges while attributing them to "final DOC-C".
- c25e631839069ea67cf5926a2bfa0e807404421a then narrowed Rust to RUNNING/VERIFYING error edges.
- d1d80ce99d533a79294425ebcfe132551b26cc43 only changes references/comments.
- Current branch is therefore statically divergent in the opposite direction: TypeScript broad, Rust narrow.
- Latest d1d80ce Railway deployment 6603dd35-d54e-4785-946d-3ee3f59e7ec3 did not reach tests because DOC_E_TESTED_SHA was stale; no PASS can be claimed for current HEAD.

RESOLVED QUESTION:
Which transition relation is final DOC-C build authority?
- Narrow error relation: RUNNING error FREEZE; VERIFYING error FREEZE.
- Broad non-STOP error relation is from pre-final text and must not be relabeled as final DOC-C.

REMAINING UNKNOWN:
How bootstrap/dependency/persistence failures from INIT or READY must reach the DOC-B-required fail-closed FREEZE outcome without inventing a transition absent from final DOC-C. This requires an explicit canonical mechanism or authoritative clarification; tests must not be weakened merely to become green.

AFFECTED_PATHS:
- packages/core/vnext-state-matrix.ts
- core-kernel/src/kernel/vnext_matrix.rs
- packages/api/bootstrap.ts
- packages/orch-core/system-state.ts
- tests/contract/core-kernel-vnext-parity.test.ts
- tests/contract/hydration-fail-closed.test.ts
- tests/contract/system-state-persistence.test.ts

NEXT_ACTION:
Restore cross-language parity to final DOC-C authority, then separately resolve fail-closed bootstrap/persistence routing without silently reintroducing pre-final error edges.

EVIDENCE_REFS:
- NEXY-BUILD-CONTROL/FINDINGS/F-E4C19A73-03.md
- NEXY-BUILD-CONTROL/DEPENDENCIES/DEP-E4C19A73-STATE-ERROR-AUTHORITY.md
- NEXY-BUILD-CONTROL/COMMUNICATION/THREADS/TH-D4A71C2E-VERIFY/M-5E4C5301-005.md
- Railway deployment 3356b6d7-a35c-4aa5-b25c-aedc67367ded
- Railway deployment 6603dd35-d54e-4785-946d-3ee3f59e7ec3
