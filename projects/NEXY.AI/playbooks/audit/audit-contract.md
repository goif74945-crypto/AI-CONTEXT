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

# Audit Contract

Check:
- producer/consumer;
- exact input/output schema;
- pre/postconditions;
- errors;
- timeout;
- idempotency;
- authorization;
- versioning;
- runtime validation at every trust boundary.

Compare Contract Registry to observed code; mark schema narrowing/widening explicitly.

Negative tests:
malformed input, missing field, extra/invalid field where strict, unauthorized actor, duplicate mutation, timeout, stale version.

Do not call a contract PASS from TypeScript types alone.
