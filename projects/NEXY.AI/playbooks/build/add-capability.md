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

# Add Capability

## PRECONDITIONS
- correct capability governance scope;
- append-only version semantics;
- admission authority available.

## REQUIRED_CONTEXT
Capability Registry FSM, static verifier, rejection codes, dependency/conflict graph, chaos invariants.

## IMPLEMENTATION_SEQUENCE
1. create new immutable version;
2. declare dependencies/resource caps/forbidden combinations/class;
3. static verification;
4. policy review;
5. quorum/anchor stages;
6. public projection;
7. chaos test;
8. activate only after legal FSM completion.

## NEGATIVE_TESTS
missing dependency, deprecated dependency, conflict, resource cap, authority escalation, bypass, duplicate version.

## DONE
No in-place history rewrite and required admission gates/evidence exist.
