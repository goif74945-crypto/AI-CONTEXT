# CASE 20261008-NEXY-EX012-LAW-PRODUCT-REPAIR
CATEGORY: LAW input validation correctness
SEVERITY: S3 correction; full exploitability through normal JUDGE path not established.
OBSERVED_FAILURE: isReleaseCandidate previously accepted quorumCount=2 with agentIds length=1 or quorumCount=10 with 2 agent IDs. Quorum validation used default threshold only, ignored agent identity cardinality.
ROOT_CAUSE: Missing upper bound check after validating agentId uniqueness.
FIX: quorumCount <= validated agentIds.length, preserving existing release thresholds. No new public schema fields or API contract changes.
REAL_REGRESSION: Original source RED 2/5 fail, patched 58/58 related green, tsc=0; broad remains 6 failures unrelated by test names (root cause separately unresolved).
PRODUCT_PROOF: commit 90fac4835788e867559858fc92d093ded3dcb1eb, source/test SHA read-back exact.
PREVENTION: source-linked regression rejects fabricated agent quorum claims and keeps 2 valid agents/quorum=2 success.
LIMITS: No proof all 98 spec rows or full runtime release gate. DOC-E NOT_AUTHORIZED.
