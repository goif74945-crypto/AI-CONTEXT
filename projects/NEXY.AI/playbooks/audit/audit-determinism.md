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

# Audit Determinism

Check domain first: Core, Game, Queue, Recovery, Robotics have different numeric/time semantics.

Audit:
- canonical mutator count;
- event ordering;
- FP/RNG/system-clock usage inside authoritative path;
- environment/build identity;
- WAL-before-mutation;
- snapshot sequence;
- replay/state hash;
- concurrency/race behavior;
- cross-architecture reproducibility where required.

A deterministic-looking unit test is not cross-system proof.
