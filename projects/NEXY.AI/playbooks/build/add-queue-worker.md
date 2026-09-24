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

# Add Queue Worker

## PRECONDITIONS
- queue payload contract canonical;
- producer/consumer validation defined;
- durability/idempotency/stale TTL/retry policy explicit.

## REQUIRED_CONTEXT
Queue contracts/FSM, Redis durability rule, dispatch/idempotency, release law, incident/audit behavior.

## IMPLEMENTATION_SEQUENCE
1. validate before enqueue;
2. bind idempotency identity;
3. assert durable queue backend;
4. revalidate before consume;
5. claim durable dispatch before side effects;
6. load authoritative durable domain record;
7. execute bounded work;
8. handle failure through incident/audit;
9. no automatic retry unless explicitly safe.

## NEGATIVE_TESTS
duplicate delivery, stale job, malformed payload, Redis non-durable/unavailable, worker crash, DB failure, release rejection.

## DONE
Real service boundary exercised; mock-only success cannot satisfy runtime-readiness proof.
