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

# Audit Security

Load trust-boundary map + permission matrix + threat-relevant failures.

Test:
- user/UI/API/Core trust boundaries;
- auth/session/OTAC/CSRF;
- RBAC server-side;
- rate limiting and dependency failure;
- secret exposure;
- prompt/provider injection;
- queue boundary;
- sandbox/capability escape;
- tenant/universe crossing;
- audit evidence persistence.

Do not treat UI-hidden controls as authorization.
Do not treat in-memory alarm emission as proof of external monitoring delivery.
