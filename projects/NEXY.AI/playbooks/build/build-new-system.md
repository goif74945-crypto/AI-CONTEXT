# PLAYBOOK — Build New System

## PRECONDITIONS
- New system is in authorized scope.
- Authority/scope registry does not mark it EXCLUDED/SUPERSEDED.
- No existing ontology entity already satisfies the requirement.
- Parent/dependency placement is known.
- Required contracts/invariants can be stated before implementation.

## REQUIRED CONTEXT
- ontology entity + parent;
- requirement IDs;
- dependency graph;
- authority/scope/supersession/conflicts;
- relevant contracts/invariants/FSMs;
- implementation/repository map;
- acceptance/test matrix;
- security/trust boundaries;
- persistence/state/event/config maps where applicable.

## IMPLEMENTATION SEQUENCE
1. Create/confirm requirement ledger entries.
2. Define system responsibility and explicit non-goals.
3. Define authority owner and mutation owner.
4. Define inputs/outputs and contracts.
5. Define state/FSM if stateful.
6. Define persistence and event semantics if durable/asynchronous.
7. Define failure and recovery behavior.
8. Define security/trust boundary.
9. Add dependency edges and validate acyclicity.
10. Implement the smallest complete vertical slice.
11. Add static/contract/unit/integration tests required by the acceptance matrix.
12. Add observability for critical states/failures.
13. Re-run dependency/invariant/security/FSM regression.
14. Register implementation/test/evidence links only after observed proof.

## NEGATIVE TESTS
At minimum test:
- invalid input;
- unauthorized actor;
- dependency unavailable;
- timeout;
- duplicate/idempotency behavior where relevant;
- illegal state transition if stateful;
- persistence failure if durable;
- freeze/block behavior when required.

## ROLLBACK
Rollback must restore:
- contracts;
- state schema;
- dependency graph;
- configuration;
- migrations;
- events;
to the last proven baseline.

## DONE
PASS requires the requirement-specific evidence class. Code presence alone = NOT_VERIFIED.
