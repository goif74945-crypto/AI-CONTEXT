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

# Audit Cross-System

Build impact subgraph:
target → dependencies → dependents → contracts → invariants → state → events → security boundaries → tests/evidence.

Look for:
authority inversion;
semantic mismatch between layers;
duplicated state machines;
different error taxonomies leaking across contracts;
stale config constants;
one subsystem bypassing another's guard;
future/current scope contamination;
failure propagation becoming false success.

No local PASS may override a broken cross-system invariant.
