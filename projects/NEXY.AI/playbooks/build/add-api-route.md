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

# Add API Route

## PRECONDITIONS
- route is inside current scope;
- API method/path/role/idempotency/CSRF contract is explicit.

## REQUIRED_CONTEXT
SystemEnvelope, auth/RBAC/CSRF/rate-limit, target domain contract, error taxonomy, state/freeze behavior.

## IMPLEMENTATION_SEQUENCE
1. define request/response schema in contracts/validation;
2. define canonical errors;
3. enforce auth + RBAC + CSRF for mutation;
4. enforce idempotency where mutation;
5. enforce freeze/state gates;
6. call domain service—do not put authority logic in UI route;
7. return SystemEnvelope;
8. emit audit/event as required.

## NEGATIVE_TESTS
unauthenticated, wrong role, invalid CSRF, invalid schema, duplicate key, frozen system, dependency unhealthy, rate limit.

## DONE
Contract + API + security tests mapped and exact-head evidence available when required.
