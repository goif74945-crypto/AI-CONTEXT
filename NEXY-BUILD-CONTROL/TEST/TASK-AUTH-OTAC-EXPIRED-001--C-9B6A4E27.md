TASK_ID: TASK-AUTH-OTAC-EXPIRED-001
REQ_ID: REQ-DOC-C-AUTH-VERIFY-EXPIRED-001
TEST_DESIGNER_CHAT: C-9B6A4E27
BASE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
STATUS: DESIGNED_NOT_EXECUTED
EXECUTION_BLOCKER: INC-BRANCH-NAMESPACE-001

# Red-first test design

Target: tests/coverage/auth-decision-paths.test.ts

Existing fixture support already provides:
- matchingCodeHash(email, device, code, salt)
- validOtacRow(overrides)
- mocked prisma.otacPending.findMany
- mocked security incident/event/audit transaction surfaces

## T1 exact expired unconsumed credential
Fixture:
- one row from validOtacRow({ expiresAt: new Date(0), consumed: false })
- submit EMAIL / DEVICE / CODE
Expected baseline:
- 401 AUTH_INVALID (current defect)
Expected candidate:
- 401 AUTH_EXPIRED
- no session creation
- no OTAC consumption
- AUTH_VERIFY_FAILED evidence persists; evidence failure remains fail-closed

## T2 expired wrong code does not inherit expiry
Fixture:
- expired unconsumed same-device row whose codeHash does not match CODE
Expected:
- 401 AUTH_INVALID
- never 200
- no session creation
- do not assert AUTH_EXPIRED merely from expired-row existence

## T3 consumed replay after expiry
Fixture:
- valid hash for submitted CODE
- same device
- consumed=true
- expiresAt <= now
Expected:
- 401 AUTH_INVALID
- OTAC_REPLAY suspicious-auth/security evidence is persisted
- never AUTH_EXPIRED
This directly covers F-71A0F5E7-OTAC-REPLAY-AFTER-EXPIRY.

## T4 live wrong code regression
Fixture:
- valid live row with nonmatching codeHash
Expected:
- 401 AUTH_INVALID
- failed-attempt persistence still increments according to existing behavior

## T5 live device mismatch regression
Fixture:
- live unconsumed row bound to another device
Expected:
- 403 DEVICE_MISMATCH according to current canonical route behavior
- no session creation

## T6 lock precedence regression
Fixture:
- active lock returned by readOtacLock path
Expected:
- 409 OTAC_LOCKED
- OTAC row scan is not used to bypass the lock

## T7 fixed-width scan structural evidence
The current production function directly imports node:crypto timingSafeEqual, while the coverage test does not instrument it.
Required evidence for candidate:
- source review confirms for-loop remains bounded by SLOTS with no match-dependent break/return
- place the only valid live match in the final real slot and verify success
- include padding case with fewer than SLOTS rows and verify behavior
If exact call-count instrumentation is introduced, it must be test-only and must not alter production comparison semantics.

## T8 audit fail-closed on expired classification
Force event/audit persistence failure during expired-match rejection.
Expected:
- dependency/freeze-class failure envelope per existing auth persistence boundary
- never emit AUTH_EXPIRED without required audit evidence when the contract requires AUTH_VERIFY_FAILED

# Execution law
No PASS may be recorded until these tests execute on the exact worker candidate SHA and then again after integration on NEXY.AI-Test-AI.
