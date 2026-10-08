# TASK — NEXY handoff 006 CROSS
MODE: EXECUTE_NOW; STATUS: PARTIAL
PRODUCT_TARGET: goif74945-crypto/NEXY.AI- NEXY.ai @ 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL_BASE: 0f17aa37322d8b9a6e1b21dc94cafc44176079a3
COMPLETED: live HEAD / permissions check, direct DOCX SHA-256, source comparison on 5-file auth/sandbox commit, source-only OTAC/logout/queue/TSA/cage audit, matrix inventory, CI dispatch attempt.
CHANGED_PRODUCT_FILES: NONE BY CHAT 006.
TEST_RUNNER: absent; Repo Code Bridge CI dispatch was refused 403 REPOSITORY_READ_ONLY; no product integration/CI result.
READY_CASE: QUEUE-CANCEL-RACE-006 (conditional state+attempt CAS around enqueue success and failure; negative concurrent cancellation/retry test required).
RISK_CASE: CAGE-ISOLATION-006 (Linux fallback runs executable without bwrap; seccomp policy application not evidenced); do not weaken isolation.
FROZEN_PATH: TSA bootstrap/source authority, pending verified signed-time boundary. No Date.now-based workaround.
CURRENT_HEAD_GATE: DOC-E signoffs, monitoring, rollback, incident drills NOT_VERIFIED.
NEXT: acquire live current product HEAD; run PostgreSQL+Redis interleaving race test; patch only upon concurrency proof and atomic expected-HEAD fence; check CI job logs; re-evaluate 98 rows from DOC-C.
