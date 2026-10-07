# Case — NEXY Repair Capability Block

CASE_ID: CASE-20261007-NEXY-REPAIR-BLOCK-001
TYPE: Permission boundary / exact-head release blocker
SOURCE: Live Repo Code Bridge runtime_status, repo_catalog, and repo_status in this execution.
PRODUCT: goif74945-crypto/NEXY.AI-
BRANCH: NEXY.ai
PRODUCT_HEAD: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43
CONFLICT: The requested command authorizes repair on NEXY.ai, but the configured product gateway reports read_only=true, gateway_write_policy=DENY, and ci_dispatch=false.
IMPACT: Any product patch, commit, CI dispatch, or repair-complete claim would violate the active mutation boundary or lack exact-head proof.
FIX: Preserve the frozen product state, write an explicit blocked checkpoint and a locked repair command to AI-CONTEXT/main, and resume only after capability status changes to write/CI ALLOW.
REGRESSION_CHECK: Repeated live status at the pre-write checkpoint reported the same product HEAD and DENY policy; AI-CONTEXT main remained writable.
LIMITS: This case does not prove a product defect root cause beyond the exact-head failures and stale evidence already recorded; missing CI logs prevent deeper causal closure.
STATUS: RECORDED_WITH_LIMITS
