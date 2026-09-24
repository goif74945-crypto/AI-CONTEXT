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

# Add State Transition

## PRECONDITIONS
- correct FSM namespace is identified;
- transition is authorized by source, not inferred from matching state names.

## REQUIRED_CONTEXT
FSM registry, event ownership, invariant registry, failure library, state persistence map.

## IMPLEMENTATION_SEQUENCE
1. define FROM/EVENT/GUARD/ACTION/TO/FAILURE/AUDIT_EVENT;
2. define actor ownership;
3. reject all illegal edges;
4. persist transition/audit atomically where required;
5. add negative tests for wrong actor/wrong from-state;
6. update FSM registry only after authoritative source/implementation change.

## NEGATIVE_TESTS
STOP/terminal exits, duplicate events, wrong actor, race, timeout, recovery denial.

## DONE
No cross-FSM conflation and all transition tests pass for exact code revision.
