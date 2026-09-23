# PLAYBOOK — Modify Existing System

## PRECONDITIONS
- Exact target entity/system resolved from ontology.
- Current implementation location is observed at current HEAD.
- Change objective maps to explicit requirements or an authorized new requirement.
- Protected branches/files are known.

## REQUIRED CONTEXT
Load:
- entity + dependents;
- inbound/outbound dependency edges;
- governing requirements;
- contracts;
- invariants;
- FSM transitions;
- state/persistence ownership;
- events/config;
- security boundaries;
- known failures/regression history;
- current tests/evidence.

## CHANGE IMPACT
Before editing, construct:
`CHANGE → affected entities → requirements → contracts → invariants → FSMs → state/events/config → tests/evidence`

Do not mutate until high-severity S4/S5 invariants in the impact set are known.

## IMPLEMENTATION SEQUENCE
1. Reproduce current behavior/failure.
2. Identify earliest incorrect state/root cause.
3. Confirm whether behavior change is permitted by authority/supersession.
4. Modify the smallest semantic surface.
5. Update contracts/schema/migration/event definitions when semantics change.
6. Update tests before claiming compatibility.
7. Run focused proof.
8. Run impacted regression set.
9. Inspect final diff for scope creep.
10. Update implementation/traceability only for observed current HEAD.

## FORBIDDEN
- weakening tests to make them pass;
- bypassing LAW/FSM/authorization;
- hidden fallback;
- unversioned config/contract change;
- changing unrelated architecture because it appears cleaner.

## DONE
PASS only if changed behavior and impacted invariants are proven.
