# EX018 Prisma source structural tests
HEAD: 58b1200bd61b867e917057d0019eea78ea9f6b2a
FILE: prisma/schema.prisma
GIT_BLOB: be1cbe1481829a2c95b6599929abc86829f37667
RUNNER: Floot isolated Node.js VM, node --test, source bytes fetched via authorized GitHub connector
ACTUAL: 21 tests PASS, 0 FAIL, exit=0, elapsed=53.103216ms.
COVERAGE: model existence 12, uniqueness and personal-data source constraints 9. No Prisma parser or migration applied, no PostgreSQL transactional test. Do NOT claim E3 PASS.
SOURCE_ASSERTIONS: User.emailHash unique, Session.sessionToken unique, DirectiveRecord.idempotencyKey unique, Commit.idempotencyKey unique, Revision(artifactId,revisionNo) composite unique, FreezeIncident.pipelineRunId unique, EventLog.sequenceNum unique, Session.deviceBindingHash field, User has no plaintext email field.
