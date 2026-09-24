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

# Add Agent / External Model Adapter

## PRECONDITIONS
- provider use is in scope;
- external model is treated as untrusted candidate generator.

## REQUIRED_CONTEXT
AgentAdapter contract, Lo3/security cage, timeout/criticality policy, release policy, cost/resource policy.

## IMPLEMENTATION_SEQUENCE
1. define provider/id/schema/modes/deterministic capability/criticality/timeouts/context;
2. isolate credentials server-side;
3. normalize response;
4. validate schema;
5. enforce deadline/cancel;
6. never grant final truth authority;
7. integrate adversarial/cross verification;
8. record health/latency/evidence.

## NEGATIVE_TESTS
malformed model response, prompt injection, timeout, provider outage, conflicting answer, high-confidence false answer.

## DONE
Adapter failure cannot bypass JUDGE/LAW or silently change truth.
