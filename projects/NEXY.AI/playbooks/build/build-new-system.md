# NEXY Playbook Contract

Every playbook follows:

1. PRECONDITIONS
2. REQUIRED_CONTEXT
3. AUTHORITY / SCOPE CHECK
4. CHANGE IMPACT
5. IMPLEMENTATION_SEQUENCE
6. VALIDATION
7. NEGATIVE_TESTS
8. REGRESSION
9. ROLLBACK
10. DONE

Global rules:
- refresh repository branch/HEAD before implementation claims or edits;
- if HEAD differs from the task lock, STOP/FREEZE;
- source design ≠ implementation ≠ test ≠ evidence ≠ deployment proof;
- never patch a CANDIDATE implementation mapping without opening/confirming the file;
- resolve Authority + Scope + Supersession + Conflict before coding;
- preserve S5 invariants;
- UI is not authority;
- SWARM/model output is not final authority;
- no test execution evidence = no PASS;
- do not use stale evidence for current HEAD.

# Build New System

## PRECONDITIONS
- exact task scope and target ontology/system ID are known;
- current source authority permits the system in this build scope;
- no unresolved governance conflict blocks semantics;
- repository/branch/HEAD is refreshed.

## REQUIRED_CONTEXT
Load:
- ontology entity + parent/dependencies/dependents;
- governing requirements;
- authority/scope/supersession/conflicts;
- dependency graph;
- relevant contracts/invariants/FSM;
- implementation map near parent/dependencies;
- failure library;
- test/evidence traceability.

## CHANGE IMPACT
Derive affected systems from dependency graph and all linked S4/S5 invariants.
Do not infer “isolated change” from one directory.

## IMPLEMENTATION_SEQUENCE
1. lock contract/schema first;
2. create module boundary with no forbidden reverse dependency;
3. implement state/data ownership;
4. implement failure behavior before happy-path release;
5. add observability/audit;
6. integrate through canonical authority path;
7. add tests;
8. update implementation/traceability registries only after code exists.

## VALIDATION
- type/build/static checks;
- contract tests;
- integration tests;
- FSM/invariant tests;
- security/negative tests;
- exact-head evidence.

## NEGATIVE_TESTS
At minimum: malformed input, unauthorized actor, dependency unavailable, timeout, duplicate/idempotent replay, illegal state, proof/evidence shortage.

## REGRESSION
Run all tests tied to affected invariants and dependents.

## ROLLBACK
Revert implementation while preserving immutable history/migrations/evidence. If rollback itself changes schema/state, use migration registry.

## DONE
Done only when implementation + required tests + evidence obligations for the task type are satisfied. Build success alone is not DONE.
