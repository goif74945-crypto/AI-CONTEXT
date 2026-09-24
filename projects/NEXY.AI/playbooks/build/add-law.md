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

# Add Law / Invariant

## PRECONDITIONS
- authority source explicitly permits new/changed law;
- supersession relation to old claim/law is known.

## REQUIRED_CONTEXT
Authority graph, supersession graph, conflicts, invariant registry, impacted FSM/contracts.

## IMPLEMENTATION_SEQUENCE
1. write machine-testable statement;
2. define scope and authority;
3. define violation behavior;
4. define proof obligations;
5. wire law before release/mutation boundary;
6. add violation tests;
7. add regression links;
8. preserve old law as historical/superseded when appropriate.

## NEGATIVE_TESTS
authority bypass, UI bypass, SWARM bypass, silent downgrade, conflicting older rule.

## DONE
Law enforcement is executable and tested; prose existence is not enough.
