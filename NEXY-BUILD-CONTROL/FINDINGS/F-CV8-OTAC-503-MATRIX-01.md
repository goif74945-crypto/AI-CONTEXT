FINDING_ID: F-CV8-OTAC-503-MATRIX-01
REQ_ID: REQ-DOC-C-4-2-REQUEST-OTAC
TASK_ID: T-C84E61B2
FROM_CHAT: C-V8-SOL-BOOT-1912
TO_CHAT: C-4F2A9C71; M-AUTH; INTEGRATION
HEAD_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_BLOB: packages/api/middleware/rate-limit.ts@d6c99adcbb17365a505032acbb8da4da16537ff9
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SEVERITY: P1
TYPE: CONTRACT_DRIFT / INVALID_ERROR_PATH
STATUS: OPEN

OBSERVED:
The request-OTAC rate-limit path can return HTTP 503 with ErrorCode DEPENDENCY_UNHEALTHY:
- runtime rate-limit config resolution failure -> rate-limit.ts lines 292-304
- Redis fail-closed backend failure -> rate-limit.ts lines 327-339

requestOtacLimiter composes requestOtacAbuseLimiter with runtimeProfile="request_otac", so both paths are reachable before handleRequestOtac() processes the route.

EXPECTED:
Locked Final DOC-C §4.1 requires each route to declare its error matrix.
Locked Final DOC-C §4.2 POST /api/auth/request-otac declares:
- 422 SCHEMA_VIOLATION
- 429 RATE_LIMIT_EXCEEDED
- 409 OTAC_LOCKED
- 503 DEPENDENCY_FAILURE
No DEPENDENCY_UNHEALTHY row is declared for this route.

SPEC_EVIDENCE:
- P10029: all responses use SystemEnvelope<T>
- P10032-P10036: all routes must declare auth/RBAC/retry/audit/error matrix
- P10039-P10070: request-OTAC route and exact Errors list
- P9986-P9987: DEPENDENCY_FAILURE and DEPENDENCY_UNHEALTHY are distinct canonical ErrorCode values

COUNTEREXAMPLE:
If resolveRuntimeConfig() throws before OTAC issuance, the route returns:
HTTP 503 + error.code="DEPENDENCY_UNHEALTHY".
That status/code pair is not present in the request-OTAC route matrix.

BOUNDARY:
This does not require weakening fail-closed rate limiting. The defect is the route-visible error contract. A repair must preserve fail-closed admission and required AUTH_OTAC_REQUESTED failure auditing.

HOTSPOT:
packages/api/middleware/rate-limit.ts is currently owned by active T-C84E61B2. No source mutation by this reviewer. Owner/integration must reconcile this finding rather than creating a second writer.

TEST_GAP:
Current requestOtacLimiter tests assert 429 behavior but do not assert the exact 503 route error-code matrix for runtime-config or Redis dependency failure.

SOURCE_MUTATION: NONE
RUNTIME_EXECUTION: NOT_RUN_BY_REVIEWER
