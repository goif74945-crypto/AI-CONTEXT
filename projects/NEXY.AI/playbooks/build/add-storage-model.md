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

# Add Storage Model

## PRECONDITIONS
- authoritative owner/writer/readers/lifetime/recovery defined;
- mutability classification explicit.

## REQUIRED_CONTEXT
State ownership, persistence map, Vault invariants, audit/event rules, migration obligations.

## IMPLEMENTATION_SEQUENCE
1. define schema + owner;
2. define FK/delete/update policy;
3. define version/idempotency/OCC;
4. define transaction boundary;
5. define audit/event correlation;
6. create forward migration;
7. create tested rollback or irreversible migration declaration;
8. run concurrency/crash tests.

## NEGATIVE_TESTS
stale version, duplicate commit, partial blob/DB failure, FK violation, illegal delete/update, rollback interruption.

## DONE
Forward + rollback behavior proven in target-like DB for exact revision when deployment-bound.
