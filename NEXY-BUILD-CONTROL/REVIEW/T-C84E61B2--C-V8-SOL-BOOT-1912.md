TASK_ID: T-C84E61B2
REVIEWER_CHAT: C-V8-SOL-BOOT-1912
STATUS: CHANGES_REQUESTED
PRIORITY: P1
RISK: AUTH_SECURITY
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
INTEGRATION_HEAD: 608426cb30398b1f3461866f7079d2a435c96b96
RATE_LIMIT_BLOB: d6c99adcbb17365a505032acbb8da4da16537ff9
CLIENT_IP_BLOB: d5e8f552024dc2ccd26ca9cbaf089a5c1b24b57a
TEST_BLOBS:
- tests/integration/rate-limit-redis.spec.ts a0d8e13325383c1e1aa9fefa9973ef794ff1ad81
- tests/coverage/rate-limit-branches.test.ts 51e96eb3242d378f03e6a1720b3ae6fd0b774a4f

FACT:
- requestOtacLimiter executes before RequestOtacBodySchema parsing in handleRequestOtac().
- requestOtacSubject() returns the raw request-body email string.
- hashAbuseBucket() hashes bytes exactly and performs no trim/case normalization.
- Therefore "User@Example.com" and "user@example.com" produce different cooldown keys.
- Current integration/coverage tests assert same-email cooldown and per-email isolation but do not test case variants.
- T-C84E61B2 TEST_PLAN explicitly requires "email case cannot bypass cooldown bucket".

COUNTEREXAMPLE:
1. POST request-OTAC body email="User@Example.com" -> cooldown key A.
2. Before 60 seconds expires, retry body email="user@example.com" -> cooldown key B.
3. The second request is evaluated as a different bucket and can pass the dedicated cooldown gate.

RESULT:
Current exact integration source does not satisfy the task's own canonical cooldown acceptance criterion.

REPAIR_CONSTRAINT:
Normalize the OTAC subject using the same canonical email identity rule used by auth before hashing the cooldown/abuse key. Do not invent a second identity normalization rule inside the limiter. Add a focused case-variant regression.

RELATED_FINDING:
F-CV8-OTAC-503-MATRIX-01 is separate: route-visible 503 error-code drift.

SOURCE_MUTATION_BY_REVIEWER: NONE
RUNTIME_EXECUTION_BY_REVIEWER: NOT_RUN
