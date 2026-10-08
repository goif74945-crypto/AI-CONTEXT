# CASE 20261008-NEXY-NORMAL-CHAT-EXECUTION-010
CATEGORY: INTEGRATION_COVERAGE / EVIDENCE_CONSISTENCY
STATUS: OPEN
CASE: EX009 harness may become service-backed but it does not call actual CAS-patched dispatchDirective; it uses direct BullMQ queue.add and handwritten Prisma CAS, while substituting a test probe Worker for product worker. Passing T00/T01/T04/T06/T07/T11 would prove only bounded boundary behavior.
ROOT_CAUSE: test-harness development preceded availability of real PostgreSQL/Redis and integration with actual producer path.
RISK: False promotion to CROSS-STORE VERIFIED based on tests not executing the fix; worker release/output may still be untested; multiple CAS candidates create version ambiguity.
SOURCES: TESTS/009/ex009-crossstore-pg-redis.mts at blob 3973fa0fae81c385b1f93617e66c2f67c8358c39; README blob 1971c4a190242494f0161767cdc7a507be8487f0; product dispatch.ts blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29.
REMEDY: locate safe actual runner; create tests importing dispatchDirective of exact candidate with real DB/Redis and cancellation/proxy release; report test depth separately; no unfounded pass.
EXCLUSIONS: no production incident proof, no release signoffs, no paid resource authorization.
NEXT: COMMANDS/20261008-NEXY-NORMAL-CHAT-EXECUTION-010.md
