# EX009 isolated PostgreSQL + Redis executable harness (NOT_RUN)
Product HEAD constraint: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08; checked dispatch.ts blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29.
Run ONLY in disposable local checkout of NEXY.AI-/NEXY.ai matching expected blob; never on production.
Copy TESTS/009/ex009-crossstore-pg-redis.mts to PRODUCT/scripts/ex009-crossstore-pg-redis.mts.
This harness uses real Prisma, real BullMQ and real product claim/cancel/complete/Law-release exports. Producer is direct BullMQ test operation; it DOES NOT call trusted TSA-dependent dispatchDirective. Thus it validates only stated subsets.
Preconditions: isolated Docker daemon, no production containers or DB; use explicit database name nexy_ex009 and Redis port 6389. The harness will reject any non-loopback hosts, wrong database/ports or missing opt-in. Do not reuse databases and do not supply production credentials.
Commands in LOCAL PRODUCT CHECKOUT (Linux/bash):
```bash
test "$(git rev-parse HEAD)" = "44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08"
test "$(git hash-object packages/queue/dispatch.ts)" = "002eef253ce836e2cd0e200f5d15cb5042cdeb29"
docker compose -p nexyex009 -f ../AI-CONTEXT/TESTS/009/docker-compose.yml up -d
export DATABASE_URL='postgresql://ex009:ex009_dev_only@127.0.0.1:5439/nexy_ex009?schema=public'
export REDIS_HOST=127.0.0.1 REDIS_PORT=6389 NEXY_EX009_ISOLATED_TEST_ONLY=CONFIRMED
npm ci --no-audit --no-fund
npx prisma generate
npx prisma migrate deploy
node --import tsx scripts/ex009-crossstore-pg-redis.mts
docker compose -p nexyex009 -f ../AI-CONTEXT/TESTS/009/docker-compose.yml down -v
```
Do not run compose cleanup against any other project; protect checkout and logs. For patch-candidate tests apply just ONE exact-SHA patch to the clean checkout before invoking the harness, save the resulting source Git blob, then revert after testing. Never treat cross-candidate results as interchangeable.
Expected: T00 real Postgres/Redis AOF precheck; T01 cancel-before-publish; T04 real BullMQ job published then durable CAS loses cancel, worker CLAIMED? No, must return CANCELLED, no test-provider calls; T06 real duplicate BullMQ jobId; T07 actual retry predicate only (NOT BullMQ failed-job retry); T11 actual LAW release transaction rejects CANCELLED. T02/T03/T05/T08/T09/T10/T12/T13/T14 NOT_RUN and require independent barriers/service-failure/test trusted TSA as applicable.
MOCKING: none in script, but Worker processor is deliberately a test probe and NOT packages/queue/workers.ts. This is boundary integration, not full production-worker E2E.
Safety: test fixture metadata fixed ISO date is NOT trusted TSA; no fake TSA or signature injected; BullMQ internal timestamps are not used to prove TTL. No API credentials. Output no user data.
Current execution: test runner Windows lacks Docker/Podman, Redis/Postgres and WSL, Linux sandbox apt update timed out. The source compiles under repo tsc; preflight missing DATABASE_URL deliberately returns EX009_BLOCKED exit=1. Actual PG/Redis SERVICE TEST NOT_RUN.
