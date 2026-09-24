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

# Modify Existing System

## PRECONDITIONS
- identify exact entity in `system-to-code.jsonl`;
- open all EXACT refs needed;
- confirm CANDIDATE refs before use;
- refresh HEAD.

## REQUIRED_CONTEXT
Entity → requirements → contracts → FSM → invariants → dependencies/dependents → known failures → test/evidence links.

## IMPLEMENTATION_SEQUENCE
1. capture BEFORE behavior/contract;
2. compute semantic diff, not only git diff;
3. identify changed requirement/contract/invariant;
4. implement smallest legal mutation;
5. update tests before declaring completion;
6. re-run dependent regression;
7. record new evidence only for exact resulting HEAD.

## NEGATIVE_TESTS
Re-run all known historical failure patterns touching the entity.

## ROLLBACK
Must restore prior legal contract/state semantics, not merely old file text.

## DONE
No unresolved S5 regression, no authority inversion, no stale evidence used as proof.
