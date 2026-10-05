# Independent Review — directive idempotency concurrency

REVIEW_ID: RV-DOC-C4-DIRECTIVE-IDEMPOTENCY-RACE-C-SOL-1933-A4C7
CHAT_ID: C-SOL-20261005-1933-V8-QREV-A4C7
TASK_ID: TASK-DOC-C4-DIRECTIVE-IDEMPOTENCY-RACE-001
FINDING_ID: FINDING-DOC-C4-DIRECTIVE-IDEMPOTENCY-RACE-001
SOURCE_BRANCH: NEXY.AI-Test-AI
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96
SOURCE_TREE: e7f603d06db6475a4d72f5d0aed752213d17eb16
SPEC_HASH: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
ROLE: INDEPENDENT_REVIEWER / RED_TEAM
SOURCE_MUTATION: NONE
RESULT: P1_FINDING_INDEPENDENTLY_CONFIRMED

## FACT

Final DOC-C POST /api/directives raw paragraphs 10161-10164 requires idempotency and states that retry with the same key returns the same accepted run.

packages/api/directives.ts@8cd214c87e5aa55561e52347802ec8172feadc36:
- performs prisma.directiveIdempotency.findUnique({ idempotencyKey }) before entering the acceptance transaction;
- binds valid replay to the same session.id and exact canonical requestHash;
- creates DirectiveRecord, DirectiveIdempotency, DirectiveDispatch and acceptance evidence inside a SERIALIZABLE transaction;
- catches Prisma code P2002 after the transaction and returns HTTP 409 INVALID_DIRECTIVE without re-resolving the winning idempotency record.

tests/coverage/directive-create-branches.test.ts@6828546ac8ef13ef924d6cca7be56edd2af08c7c proves sequential existing-idempotency replay only. tests/integration/directives/create.spec.ts@618430867512b4c040b24c54504820af37576b8c contains no forced same-key concurrency interleaving.

Therefore a concurrent equivalent request that loses a unique-key race and surfaces P2002 is mapped to conflict instead of converging to the already accepted run required by DOC-C.

## ASSUMPTION

None is needed for the source-level defect on the existing P2002 path: if the loser reaches the implemented P2002 catch for the same idempotency key, current code cannot return the winning accepted run.

## UNKNOWN

The exact PostgreSQL/Prisma error observed for every possible SERIALIZABLE race interleaving has not been executed in this review. Some contention patterns may surface a serialization error rather than P2002. Repair must not assume every concurrency loser is P2002 without an executed database race test.

## Repair constraints

- Re-resolve durable idempotency only after a collision that can be proven to belong to the same idempotency request.
- Return the existing accepted run only when sessionId and requestHash exactly match.
- Keep different-session, different-payload, conflicting directive identity and unresolved persistence cases fail-closed.
- Do not turn arbitrary P2002 into success.
- Add a deterministic two-request concurrency test that forces both pre-transaction lookups to miss and proves one durable accepted run.
- Preserve SERIALIZABLE transactionality, unique constraints, durable dispatch and security checks.

## Closure effect

ACTIONABLE_CODE_GAP: CONFIRMED
CONCURRENCY_DEFECT: CONFIRMED
IDEMPOTENCY_DEFECT: CONFIRMED
MISSING_REQUIRED_TEST: CONFIRMED
GAP_FIXED: NO
REVERIFY_REQUIRED: YES
SOURCE_REPAIR: BLOCKED_BY_INC-BRANCH-NAMESPACE-001
CODE_CLOSURE_ELIGIBLE: NO
