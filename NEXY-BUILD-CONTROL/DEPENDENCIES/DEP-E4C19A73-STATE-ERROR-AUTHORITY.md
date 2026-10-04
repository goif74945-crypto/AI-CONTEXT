DEPENDENCY_ID: DEP-E4C19A73-STATE-ERROR-AUTHORITY
REPORTER_CHAT: C-E4C19A73
TASK_ID: T-D4A71C2E
STATUS: NEEDS_HELP
PRIORITY: P1
HEAD_SHA: 5034debdadb1f21c7d5312e6f0ad7fd44280718c

FACT:
1. The authoritative document's FINAL VERDICT says DOC-C is the build authority.
2. Final DOC-C matrix lists error->FREEZE only for RUNNING and VERIFYING.
3. The same final document's DOC-B Freeze Law says unresolved contradiction, policy conflict, or undefined behavior => FREEZE, with no patch/guess/mask.
4. Final DOC-C contains no explicit bootstrap/dependency-failure transition from INIT or READY to FREEZE.
5. Existing Rust kernel and bootstrap/persistence contracts implement/expect broader error->FREEZE behavior.
6. Exact-head Railway validation proves the narrowed TypeScript matrix breaks those consumers.

AUTHORITATIVE_SPEC_EVIDENCE:
- FINAL VERDICT: DOC-C = BUILD SPEC; build obligation comes from DOC-C only.
- Final DOC-B 1.5 Freeze Law: unresolved contradiction / policy conflict / undefined behavior => FREEZE; no patch / no guess / no mask.
- Final DOC-C 5.2 Matrix:
  RUNNING + error => FREEZE
  VERIFYING + error => FREEZE
  no INIT/READY/CONSENSUS/STABLE/FREEZE error rows.
- Earlier pre-final executable state-machine section contains ANY except STOP + error => FREEZE, but that section precedes the FINAL VERDICT pack and therefore cannot silently override final DOC-C.

UNKNOWN:
The canonical mechanism for fail-closed bootstrap/dependency failure while current state is INIT or READY. Restoring the five removed error edges contradicts the final matrix; simply deleting/changing fail-closed consumers can contradict DOC-B freeze behavior and existing operational contracts.

SAFE_BOUNDARY:
Do not mutate the transition relation, Rust parity, or bootstrap/persistence failure semantics until this authority gap is independently reconciled. Independent unrelated work remains unblocked.

EVIDENCE_REFS:
- authoritative spec paragraphs around FINAL VERDICT / DOC-B 1.5 / DOC-C 5.2
- NEXY-BUILD-CONTROL/FAILURES/FAIL-E4C19A73-5034-STATE-PARITY.md
- Railway deployment 3356b6d7-a35c-4aa5-b25c-aedc67367ded
