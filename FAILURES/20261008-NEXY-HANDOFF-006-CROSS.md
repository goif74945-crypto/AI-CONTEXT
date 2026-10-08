# FAILURES / BLOCKERS — handoff 006 CROSS
PRODUCT_HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
1. CI_DISPATCH_BLOCKED: Repo Code Bridge call to dispatch .github/workflows/exact-head-evidence.yml for exact product revision returned HTTP 403 REPOSITORY_READ_ONLY. Earlier repo_status and repo_catalog reported writable/CI-capable; conflict preserved as unresolved, no pretend-run.
2. CURRENT_CI_OUTCOME_UNKNOWN: GitHub combined-status statuses=[] and fetch_commit_workflow_runs=[] (PR-filtered endpoint). These do not prove green or red at current HEAD.
3. PRODUCT_TESTS_NOT_RUN: no mounted repository/dependencies or authorized executable source runner in this chat. Standalone interleaving model passed but not product test.
4. TSA_BOOTSTRAP_UNRESOLVED: product source needs injected time, spec does not explicitly bind final DOC-C queue TTL to TSA witness validation; do not bypass time authority.
5. BWRAP_RUNTIME_ISOLATION_UNVERIFIED: direct-spawn fallback and seccomp policy application require closure.
6. DOC_E_GATES_UNVERIFIED: human signoffs, production monitoring, application rollback, production deploy all NOT_VERIFIED.
7. HISTORICAL_MATRIX_STALE: base 8b406a63 matrix cannot be called current-head PASS; 98/98 classification is bookkeeping not implementation closure.
PRODUCT_MUTATIONS_BY_CHAT: 0
