# CASES 20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS
Product HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
Control precommit HEAD: fdb9ebf97ac7e993bdcf656c87c268ee7ab71ed2
Task ID: 20261008-NEXY-QUEUE-CAGE-EXECUTION-008-CROSS
Canonical DOCX SHA256 matched in this conversation: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7
SOURCE: NEXY.ai packages/queue/dispatch.ts blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29; local patched blob 36e56aef98a5b8b52f644a0178eb3638d2c4b9af.

QUEUE-CANCEL-RACE-006 reproduced by real product module invocation with mocked durable DB and Redis boundaries: 5 expected original-source failures (cancel-success, cancel-failure, PENDING worker claim while enqueuing, DB write failure handling, concurrent dispatch attempts). Candidate uses status+attempts CAS in Prisma updateMany and re-reads durable status if CAS loses; splits enqueue catch from database state write to avoid failure overwrite. SOURCE+MOCK boundary coverage only. Cross-store window after Redis publish before DB CAS: worker claim allows PENDING and uses conditional CAS; cancelled row cannot be claimed. No real Redis lifecycle nor provider zero-execution proof yet. RELEASE FENCE: run-state.ts includes pg_advisory_xact_lock plus assertDispatchNotCancelled on output release, but actual DB transaction race not exercised.
CAGE-ISOLATION-006 independent high-risk finding remains: Linux bwrap false fallback direct spawn, JSON seccomp non-enforced path. NOT_EXECUTED Linux test; do not lower sandbox security.
