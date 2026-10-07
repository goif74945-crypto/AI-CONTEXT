# CASE — 20261007-REPO-CODE-BRIDGE-CROSS-CAPABILITY-002

CASE_ID: CASE-20261007-RBC-CROSS-002
TYPE: State reconciliation / stale-record conflict
SOURCE: AI-CONTEXT TASKS/20261007-REPO-CODE-BRIDGE-CAPABILITY-CHECK-001.md at AI-CONTEXT HEAD 9ebce59a...
CONFLICT: The task record says AI_CONTEXT_head=dd971b15... and product access BLOCKED; live catalog/status at product HEAD 9e615b04... show exact read-only access is available.
IMPACT: Future chat could incorrectly stop at a resolved allowlist blocker or use a stale AI-CONTEXT head.
FIX: Refresh exact heads and record current live evidence in EVIDENCE/20261007-REPO-CODE-BRIDGE-CROSS-CAPABILITY-002.md.
REGRESSION_CHECK: AI-CONTEXT evidence read back at post-write HEAD 065b539...; product status remained 9e615b04..., read_only=true, gateway_write_policy=DENY.
LIMITS: This reconciles bridge capability only; it does not prove product correctness, CI pass, DOC-C completion, or release readiness.
STATUS: RECORDED_WITH_LIMITS
