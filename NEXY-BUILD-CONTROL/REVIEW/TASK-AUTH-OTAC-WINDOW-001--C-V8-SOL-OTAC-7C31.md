TASK_ID: TASK-AUTH-OTAC-WINDOW-001
REQ_ID: REQ-DOC-C-AUTH-VERIFY-WINDOW-001
REVIEWER_CHAT: C-V8-SOL-OTAC-7C31
ROLE: INDEPENDENT_TEST_ORACLE_RED_TEAM
STATUS: REVIEW_CONFIRMS_ACTIONABLE_GAP
PRIORITY: P1
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

FACT:
- packages/api/auth.ts fetches where={emailHash}, orderBy={createdTick:"asc"}, take=session_slots and only then runs the fixed-width comparison loop.
- prisma/schema.prisma states OtacPending rows are never deleted; expired history therefore accumulates.
- A fresh valid OTAC can be row 33+ and become unreachable because the query keeps the oldest bounded history.
- core-kernel/src/auth/email_gate.rs has a source-level 32-slot ring where new issuance overwrites the oldest slot. This corroborates semantic divergence but is not itself product authority.
- tests/integration/auth/verify-otac.spec.ts mocks prisma.otacPending.findMany by returning otacState.rows directly and does not implement Prisma orderBy/take semantics.

TEST_ORACLE_DEFECT:
A regression that merely seeds 32 old fixture rows followed by one fresh row can reproduce the baseline only because the mock preserves fixture insertion order. After a production repair that changes query order to newest-first, that same mock will still return the old fixture order unless the mock is upgraded. Such a test can falsely report the candidate as still broken, or be rearranged to falsely pass independently of the real query contract.

REQUIRED RED-FIRST PROOF:
1. Query-contract test must inspect the findMany call and require a deterministic candidate-selection policy that admits newest active credentials under retained history.
2. If a behavioral mock is used, it must faithfully apply the candidate ordering and take bound from the invocation instead of returning fixture rows unchanged.
3. Add a retained-history case with > session_slots rows where the newest exact credential succeeds after repair and fails at the current SHA.
4. Add a deterministic tie case for equal createdTick values or prove a unique monotonic key makes ties impossible. Do not rely on database unspecified tie ordering.
5. Preserve constant-width/no-early-return comparison hardening as implementation security behavior unless separately disproven.
6. Re-run expiry, mismatch, replay, lockout, persistence-failure, and valid-session tests on the exact candidate SHA.

VERDICT:
ACTIONABLE_CODE_GAP CONFIRMED: AUTH AVAILABILITY DEFECT + TEST_ORACLE_DEFECT + DETERMINISM RISK.
Source repair is locally TRUE_BLOCKED by INC-BRANCH-NAMESPACE-001; control/test design work remains valid.
