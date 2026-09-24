# NEXY Audit Playbook Contract

Audit rules:
- refresh exact repository/branch/HEAD before current-state claims;
- source existence ≠ implementation;
- implementation presence ≠ compliance;
- test file presence ≠ execution;
- test execution ≠ deployment proof;
- deployment proof is revision/environment/claim specific;
- future scope absence is not current DOC-C FAIL;
- CANDIDATE code mappings must be opened before use;
- unresolved authority/conflict may block verdict;
- allowed verdicts: PASS / FAIL / PARTIAL / BLOCKED / NOT_TESTED / NOT_VERIFIED / SCOPE / CONFLICT.

# Audit Release

Release audit is exact-revision evidence audit.

Required:
- build/type/static gates;
- required contract/integration/security tests;
- migration + rollback execution;
- FSM proof;
- RBAC/auth-abuse proof;
- queue readiness with real services;
- monitoring/alarm proof;
- incident drill;
- exact deploy runbook;
- authorized signoff;
- rollback execution proof.

Check artifact commit == candidate HEAD.
If not equal: evidence is stale.

No E1–E12 completeness = no deploy PASS.
No authorized human signoff = BLOCKED_EXTERNAL, never fabricate approval.
