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

# Audit Persistence

For each state:
- authoritative owner;
- writers/readers;
- storage;
- lifetime;
- mutability;
- versioning;
- transaction isolation;
- idempotency/OCC;
- recovery;
- audit.

Special checks:
EventLog/AuditLog append-only, Vault revision/commit immutability, FK delete policy, blob/DB atomicity, session revocation, queue durability.

Run crash/concurrency/partial-failure tests where relevant.
