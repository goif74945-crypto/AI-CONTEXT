# CASES

Execution 010 / CROSS / SINGLE_WRITER
PRODUCT_START_HEAD=44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL_START_HEAD=f1cfe8706d8ba656c5061e802761b02965f1ba63
SOURCE_DISPATCH_BLOB=002eef253ce836e2cd0e200f5d15cb5042cdeb29
SOURCE_RELEASE_BLOB=e162efc8b2a45014bcefbd60dc67a95d8a1e1003
TEST_HARNESS_BLOB=ffff2888b8fc921415b0f1e6c77d2df9f5aa3036


G3-P1 through G3-P5 are runnable guarded source-linked tests on an EMPTY local nexy_ex010 DB port 5440 and Redis port 6390. Each calls actual Product producer; test-only interception waits AFTER real BullMQ Queue.add. P1 cancel after job published before CAS, P2 error after publish and owner cancel, P3 worker claim wins before producer CAS, P4 concurrent same-key producer, P5 probe Worker must not invoke provider for cancelled jobs.

EX010 does NOT claim that ACK wrapper reproduces network packet loss, real Postgres server shutdown or process crash. The `Worker` in the harness is a probe, not packages/queue/workers.ts. TRUE_PRODUCER_REAL=NOT_RUN; PROBE_WORKER_REAL=NOT_RUN; FULL_WORKER_REAL=NOT_RUN.

Independent issue: run-state.ts release transaction lock and cancellation updateMany do not share serialization primitive in visible source. Need deterministic live interleave before calling it exploitable/closed. Signed time and release receipt safety remain unknown.
