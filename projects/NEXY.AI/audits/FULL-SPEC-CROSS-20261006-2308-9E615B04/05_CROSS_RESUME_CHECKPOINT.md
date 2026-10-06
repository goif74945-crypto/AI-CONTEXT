# FULL-SPEC-CROSS resume checkpoint

STATUS: IN_PROGRESS
MODE: AUDIT_ONLY / CROSS_CHAT / READ_ONLY_PRODUCT_REPOSITORY
PRODUCT_REPOSITORY: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.ai
HEAD_SHA: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
TREE_SHA: a809bc5f4cc2d8f806e500d1d3a09a4e66450c7c
SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
PRODUCT_MUTATION: NONE

## Revalidated facts
- Actual NEXY.ai HEAD equals INITIAL_EXPECTED_HEAD.
- Recursive Git tree is non-truncated: 1084 entries, 881 blobs, 203 trees.
- Canonical DOCX was materialized as an OOXML Word container and re-hashed to the canonical SHA-256 above.
- DOCX body contains 12537 paragraphs, 10979 non-empty.
- All 837 normalized matrix rows were linked back to the source paragraph/anchor after whitespace normalization; no semantic anchor mismatch was found.
- Existing requirement ledger has 773/773 current-scope records. Its pre-resume evidence state was PASS_VERIFIED=162, PARTIAL_VERIFIED=15, FAIL_VERIFIED=3, MISSING_PROVEN=1, SCOPE_VIOLATION=7, NOT_VERIFIED=585.

## Revalidated proven findings

### FIND-P0-0003 / REQ-0207
Global FREEZE does not atomically close the output-emission boundary for an already STABLE/releaseable run.
Evidence:
- packages/queue/run-state.ts::emitAuthorizedPipelineOutput locks only the pipeline-run namespace, reads PipelineRun state/authorization/hash, and can mark outputEmittedTick without reading or locking global SystemState.
- packages/orch-core/system-state.ts serializes global FSM state with a different global lock and durable orchestrationEnvelope.
- No common synchronization boundary was found between global FREEZE commit and output emission.
Status: FAIL_VERIFIED / P0.

### FIND-P1-0002 / REQ-0289
The 60-second OTAC resend cooldown is configured and advertised but not enforced as a one-resend-per-60s admission rule.
Evidence:
- packages/api/vnext-config.ts: otac_resend_cooldown_ms = 60000.
- packages/api/auth.ts uses that value only to return cooldown_seconds after successful issuance.
- packages/api/middleware/rate-limit.ts requestOtacLimiter allows max=3 in windowMs=60000.
- Broad exact-symbol/semantic searches found no separate cooldown enforcement path.
- tests/integration/auth/request-otac.spec.ts mocks the limiter and checks only that cooldown_seconds is numeric.
Status: FAIL_VERIFIED / P1.
Repair boundary: AUTH/request-OTAC admission only. Do not invent scope key beyond authoritative spec. Must be durable/race-safe for multi-process issuance and preserve existing rate limiting.

## Exact-head CI evidence
At HEAD 9e615b04..., GitHub reports failing checks including:
Contract tests; TypeScript typecheck; Integration tests; Browser E2E; Full test suite; Coverage measurement; Production web build; Static determinism gate; exact-head-evidence; six-system-evidence; cargo-lock.
Deploy, release-attestation, and DOC-C static gate were skipped in the observed run.
GitHub connector exposes job conclusions but not step/annotation details for these jobs, so exact failure root causes remain BLOCKED and must not be guessed.

## Additional inspected surfaces
- AUTH: OTAC CSPRNG/hash/device binding, session rotation/cap, CSRF, trusted proxy IP, security incidents, logout/revoke-all, session refresh.
- QUEUE: canonical states, producer/consumer Zod validation, stale TTL, durable dispatch, failed retry policy default-disabled with safe-code allowlist.
- STORAGE/VAULT: Prisma lineage schema, revision allocation lock, commit-chain integrity, soft-delete, restore eligibility, lifecycle/retention/archive/hard-delete control plane.
- CONFIG: immutable config identifiers; versioned mutable config with OCC, idempotency, audit/event evidence and rollback target.
- Playwright is present as a pinned deployment/browser-test runtime and browser test source, despite not being a root package.json dependency.

## Known boot limitation
The requested root file FINAL-SINGLE-BRANCH-NEXY-ai-20261006.json was not found at the specified root path during boot lookup. This remains a traceable bootstrap limitation; no replacement authority was inferred.

## Next required work
Continue requirement-by-requirement semantic audit for remaining NOT_VERIFIED rows, update the requirement ledger only from proven evidence, run final dedup/staleness/negative gates, then and only then create BUILDER_EXECUTION_COMMAND from fresh proven findings.
