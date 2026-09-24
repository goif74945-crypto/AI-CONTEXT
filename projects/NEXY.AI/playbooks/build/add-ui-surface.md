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

# Add UI Surface

## PRECONDITIONS
- backend authority/state already exists or UI is explicitly prototype-only.

## REQUIRED_CONTEXT
DOC-D product design, UI truth invariant, RBAC, state ownership, API contracts.

## IMPLEMENTATION_SEQUENCE
1. identify backend source of truth;
2. define loading/empty/error/freeze states;
3. role-gate presentation but rely on backend authorization;
4. never create optimistic success for blocking actions;
5. preserve visible uncertainty/failure state;
6. add mobile/desktop accessibility/responsive behavior;
7. E2E against real API state.

## NEGATIVE_TESTS
backend FREEZE, 403, 409/OCC, timeout, stale response, unauthorized direct API call.

## DONE
UI cannot mask or create authority state.
