# 008 exact product-linked patch/test candidate, NOT_RUN
TASK_ID: 20261008-NEXY-NORMAL-CHAT-EXECUTION-008-CROSS
PRODUCT HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL MAIN PREWRITE: 8e787a81e11fc00f2bd7d5ca68474f0b774085c1
SPEC SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7 (recomputed from mounted DOCX 2026-10-08)
SOURCE BLOBS: dispatch.ts 002eef253ce836e2cd0e200f5d15cb5042cdeb29; cage.ts 5afd464ed39470381ef1df643a630e1f431817dc; vnext-config.ts a3141a649be7e40ec79f417f53bba9b73081232b; matrix historical f18b4874b875ca713dd007c7feddffba13d0f380

STATUS: UNTESTED_CANDIDATE. DO NOT COPY DIRECTLY TO PRODUCTION WITHOUT REAL POSTGRES+REDIS/WORKER TESTS. No product mutations performed.
Apply queue patch on NEXY.ai only IF dispatch.ts blob still 002eef253ce836e2cd0e200f5d15cb5042cdeb29; preserve branch/head fencing:
  git apply --check PATCHES/008/queue-dispatch-cas.patch
  git apply PATCHES/008/queue-dispatch-cas.patch
  mkdir -p tests/integration
  cp PATCHES/008/queue-cancel-race-008.spec.ts tests/integration/queue-cancel-race-008.spec.ts
  npm ci
  npx vitest run tests/integration/queue-cancel-race-008.spec.ts --reporter=verbose
  npm run typecheck:backend
  npm run check:boundaries
  npm run check:static-determinism
  # with isolated Postgres/Redis: npm run test:integration ; real E7 gate; additional isolated schedule barriers required
These instructions assume execution FROM the product repo root with the patch and test paths copied from AI-CONTEXT into the product workspace; do not commit untested code.
Test file IMPORTS actual packages/queue/dispatch.js, mocks DB and BullMQ at boundary. It does NOT copy dispatch logic. Expected baseline RED cases: cancel while enqueue awaits; error while cancellation; stale worker claim/complete, database CAS rejection. Expected candidate GREEN NOT YET EXECUTED.
CROSS-STORE LIMIT: job in Redis can exist with DB status PENDING or CANCELLED. CAS protects DB status only; worker claim of PENDING, pending release abort, duplicate scheduling and retry of completed BullMQ job require executable Redis+DB proof. Never claim RACE_CLOSED based on mocks.
CAGE patch separately blocks bwrap=false direct spawn, but does not prove seccomp/cgroup enforcement; Windows/macOS/dev-naive alternative paths and existing insecure-fallback acceptance tests require separate remediation. DO NOT APPLY cage patch as complete sandbox remediation.
