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

# Audit Recovery

Load Failure Library first.

For each failure:
1. trigger;
2. detected state;
3. containment;
4. mandatory evidence;
5. recoverability;
6. authorized actor;
7. recovery sequence;
8. new run/state identity;
9. rollback/replay proof.

Attack:
crash loop, memory pressure, DB failure, audit persistence failure, stale snapshot, hash mismatch, repeated remediation, recovery of nonrecoverable freeze.

Recovery must never erase the original failure history.
