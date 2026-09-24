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

# Audit FSM

Never merge FSMs by shared state names.

For target namespace:
1. enumerate states;
2. enumerate events;
3. enumerate event owners;
4. enumerate FROM/EVENT/GUARD/ACTION/TO;
5. enumerate terminal states;
6. enumerate recovery edges;
7. compare source table with implementation;
8. attack illegal transitions.

Required negatives:
wrong actor, wrong from-state, STOP/terminal exit, duplicate event, timeout/error/fatal, recovery denial, persistence/audit failure.

Any direct state mutation bypass must be reported.
