# CASE 20261008-NEXY-NORMAL-CHAT-EXECUTION-009
CATEGORY: CONCURRENCY / EVIDENCE_PROVENANCE / PATCH_SELECTION
STATUS: OPEN
CAUSE: Multiple 008 candidate CAS diffs and test suites have similar GREEN 9/9 but differ in RED count, patched source blobs and setup outcomes. The original first-family patch lost terminal LF in AI-CONTEXT persistence; corrected version is available.
VERIFIED: product code remains unchanged at 44bcb851; id-only enqueue success/failure transition after await is source-reachable. Original patch lacks newline; FIXED has it.
RISK: selecting patch solely from 9/9 mock tests may introduce false cross-store confidence, ignore BullMQ job already published, worker claim or release race.
REMEDY: patch-decision table keyed by blob SHA, rerun single candidate on exact frozen HEAD, real PG/Redis tests, worker cancel/release check, safe atomic commit gate.
PREVENTION: never mix RED/GREEN results from different patch/test families; retain defective artifact history; require read-back and git-apply round-trip.
NO_PRODUCTION_INCIDENT_ASSERTED: TRUE.
