# Failures — NEXY Full Repair

FAILURE_ID: FAILURE-20261007-NEXY-PRODUCT-WRITE-DENY-001
CONTEXT: The requested repair requires a product commit and exact-head CI.
CAUSE: Repo Code Bridge product policy reports read_only=true, gateway_write_policy=DENY, and ci_dispatch=false.
IMPACT: Product source, tests, workflows, attestation, and release evidence cannot be repaired or regenerated through the authorized path.
RECOVERY: Freeze product HEAD; continue read-only inspection; persist blocked evidence and a deterministic builder command in AI-CONTEXT/main.
BOUNDARY: Product mutation and CI execution unavailable; AI-CONTEXT evidence write remains allowed.
PREVENTION: Preflight capability check must precede every product mutation and must fail closed.

FAILURE_ID: FAILURE-20261007-NEXY-CI-LOG-ARTIFACT-MISSING-002
CONTEXT: Four exact-head workflow runs exist at product HEAD 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43.
CAUSE: All four runs concluded failure; workflow artifacts are empty; job-log downloads returned BlobNotFound/404.
IMPACT: Failure conclusions are real evidence of non-pass, but exact root causes cannot be independently classified from logs in this execution.
RECOVERY: Retain the failed run IDs and mark causal diagnosis NOT_VERIFIED; do not convert missing logs into a guessed fix.
BOUNDARY: Evidence availability failure; not proof that a particular source line is the sole cause.
PREVENTION: Required CI gates must retain downloadable logs/artifacts tied to the exact SHA.

FAILURE_ID: FAILURE-20261007-NEXY-DOCX-PARAGRAPH-MAPPING-003
CONTEXT: Prior audit material text associates P10970-P10979 with the DOCX closing design gap.
CAUSE: Direct full-DOCX paragraph inspection shows P10970-P10981 are release runbook/signoff paragraphs; closing design gap text is P12532-P12536.
IMPACT: A future builder could repair the wrong requirement family or omit release/signoff requirements.
RECOVERY: Record both paragraph ranges separately in the locked command and evidence.
BOUNDARY: Audit mapping/evidence issue; no product mutation performed.
PREVENTION: Every normalized row must include immutable DOCX paragraph/source location and a separate semantic category.
STATUS: RECORDED_WITH_LIMITS
