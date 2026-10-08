# Evidence: EX010 real-producer-path harness

Execution 010 / CROSS / SINGLE_WRITER
PRODUCT_START_HEAD=44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL_START_HEAD=f1cfe8706d8ba656c5061e802761b02965f1ba63
SOURCE_DISPATCH_BLOB=002eef253ce836e2cd0e200f5d15cb5042cdeb29
SOURCE_RELEASE_BLOB=e162efc8b2a45014bcefbd60dc67a95d8a1e1003
TEST_HARNESS_BLOB=ffff2888b8fc921415b0f1e6c77d2df9f5aa3036


Ran on authorized DESKTOP-FOB7IK8 Windows, Node v24.21.0. Fresh isolated temp clone NEXY.ai at product start HEAD. Actual Product packages/queue/dispatch.ts source Git blob verified, no Product mutation.

NEW: TESTS/010/ex010-real-producer-crossstore.mts. Imports live `dispatchDirective`, `enqueueDirective` through call path, actual Prisma and BullMQ. Test instrumentation intercepts `Queue.prototype.add` only AFTER real Redis publish and pauses the return value; it does NOT replace producer transitions. Planned G3-P1 cancel-after-real-publish, G3-P2 ACK error-after-real-publish, G3-P3 claim PENDING-before-producer-CAS, G3-P4 duplicate live producers, G3-P5 probe Worker zero provider execution after cancellation. None run against real PG/Redis in this turn.

EXECUTED: node node_modules/typescript/bin/tsc --ignoreConfig --noEmit --strict --target ES2022 --module NodeNext --moduleResolution NodeNext --skipLibCheck --types node scripts/ex010-real-producer-crossstore.mts => EXIT=0 after correcting initial local script typing and duplicate identifiers. With A FIXED patch: git apply --check=0, git apply=0, candidate blob 36e56aef98a5b8b52f644a0178eb3638d2c4b9af, standalone harness tsc EXIT=0, git diff --check=0, git apply --reverse=0, original dispatch blob exactly restored.

EXECUTED: node --import tsx scripts/ex010-real-producer-crossstore.mts with DATABASE_URL absent -> expected `EX010_BLOCKED: isolated DATABASE_URL missing`, EXIT=1. Preflight stops before dynamic DB/Redis imports. Not service-level PASS.

CAPABILITIES: Windows no Docker/Podman/psql/postgres/pg_ctl/redis-server; Termalin zero hosts. Isolated Linux sandbox no Docker/Postgres/Redis; apt-get update bounded timeout exit124. Read-only Railway inventory NEXY Validation R2 has redis/postgres services but only production environment, deliberately never tested or mutated. No cloud resources created or billing changed. TRUE_REAL_PG_REDIS=NOT_RUN, PRODUCTION_WORKER_E2E=NOT_RUN.

TIME: harness injectTsaBatchTime(1800000000000n) ONLY in test process and explicitly marks TEST_ONLY_TIME_INJECTION_NOT_SIGNED; no authenticated TSA witness, no clock/signature spoof in Product. No TTL authority PASS.

CAGE: current source 5afd464ed39470381ef1df643a630e1f431817dc: unavailable bwrap causes direct spawn; seccomp JSON written, not proof kernel enforcement. Linux runtime NOT_RUN.

LAW RISK: run-state.ts obtains pg_advisory_xact_lock and tests cancellation within release transaction, but dispatch.cancelDirectiveDispatch is separate updateMany without the same shared advisory, and emitAuthorizedPipelineOutput has no dispatch cancellation reread. Cancellation-after-check-before-commit is plausible by source interleaving; **NOT** live exploit proof or formal violation proof. Requires real database adversarial transaction test.

CI: exact product-head E7 run37741650376 attempt2 failed; latest job steps=[], cause UNKNOWN. Extra REST /actions/jobs and check annotations rejected as INVALID_ARGUMENT by connected GitHub fetch; nothing supports blame of code, billing or settings.

Release DOC-E NOT_AUTHORIZED. Audit in EX010 scoped to 18 IDs with varying depths, 80 IDs NOT_REASSESSED, completion NOT_COMPUTABLE. No Product code patch commit, no deploy.
