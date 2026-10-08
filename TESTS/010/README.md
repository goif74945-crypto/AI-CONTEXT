# EX010 real producer path: isolated PostgreSQL + Redis test harness
STATUS: IMPORTABLE / STRICT_TYPESCRIPT_PASS / REAL_SERVICES_NOT_RUN / PRODUCT_NOT_MODIFIED.
Product source HEAD `44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08`; `packages/queue/dispatch.ts` original Git blob `002eef253ce836e2cd0e200f5d15cb5042cdeb29`.
Source-linked harness Git blob `ffff2888b8fc921415b0f1e6c77d2df9f5aa3036`. Candidate A FIXED patch Git blob `b7c9444d4348fd84691cea287c9477e6c90dd734`, candidate dispatch source `36e56aef98a5b8b52f644a0178eb3638d2c4b9af`.
NEVER use corrupted A patch `ac06e695aa6e4944acbbaf6d626b5f2a73e91ac8` (missing EOF LF). Do not combine the test/patch of candidates B or C with A's results.
Run ONLY on an authorized disposable Linux Docker runner with EMPTY loopback-only database `nexy_ex010` port 5440, isolated Redis port 6390, no tenant/production data. No services were deployed in Execution 010.
Product source is not mutated in GitHub. Make an isolated local product checkout and a sibling AI-CONTEXT checkout; run:
```bash
test "$(git rev-parse HEAD)" = "44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08"
test "$(git hash-object packages/queue/dispatch.ts)" = "002eef253ce836e2cd0e200f5d15cb5042cdeb29"
git apply --check ../AI-CONTEXT/EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS-queue-cas-FIXED.patch
git apply ../AI-CONTEXT/EVIDENCE/20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS-queue-cas-FIXED.patch
test "$(git hash-object packages/queue/dispatch.ts)" = "36e56aef98a5b8b52f644a0178eb3638d2c4b9af"
cp ../AI-CONTEXT/TESTS/010/ex010-real-producer-crossstore.mts scripts/ex010-real-producer-crossstore.mts
docker compose -p nexyex010 -f ../AI-CONTEXT/TESTS/010/docker-compose.yml up -d
export DATABASE_URL='postgresql://ex010:ex010_local_fixture_only@127.0.0.1:5440/nexy_ex010?schema=public'
export REDIS_HOST=127.0.0.1 REDIS_PORT=6390 NEXY_EX010_ISOLATED_TEST_ONLY=CONFIRMED
npm ci --no-audit --no-fund
npx prisma generate
npx prisma migrate deploy
node --import tsx scripts/ex010-real-producer-crossstore.mts
docker compose -p nexyex010 -f ../AI-CONTEXT/TESTS/010/docker-compose.yml down -v
```
The `down -v` target must be your EXACT unique Compose project; never clean unrelated or production resources.
Script invokes REAL `dispatchDirective()`/`enqueueDirective()`/Prisma/BullMQ, adding a TEST-ONLY ACK barrier *after* actual Queue.add returns. It does not fake the durable state transitions.
Future service tests: G3-P1 real publish then cancellation before CAS; G3-P2 error after real publication with cancellation; G3-P3 real worker claim before ACK; G3-P4 same-key concurrent producers; G3-P5 zero provider calls in probe worker after cancellation. Also retains EX009 boundary tests. Each requires running the script against real dedicated services; NONE ran in this turn.
Probe Worker is NOT production `packages/queue/workers.ts`; do not label P1-P5 Full Production Worker E2E. Physical crash/restart, real packet loss, service disruption, LAW/cancel commit race and signed TSA proof remain NOT_RUN.
The test-only fixed `injectTsaBatchTime(1800000000000n)` is UNSIGNED; do not treat as authentic TSA timestamp or use in production. No signature is generated.
Runner evidence: Windows Node v24.21, no Docker/Postgres/Redis; connected Railway project's Redis/Postgres were in a production environment, so not used. Missing config correctly throws `EX010_BLOCKED`, exit 1. Harness standalone strict TS checked under A candidate, exit 0. This is NOT G3 pass.
