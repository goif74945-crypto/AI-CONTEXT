# PLAYBOOK — Add State Transition

## PRECONDITIONS
- Correct FSM identified; never merge semantic FSMs.
- New transition is authorized by governing law/spec.
- FROM/EVENT/GUARD/ACTION/TO semantics are explicit.
- Existing impossible/illegal transitions remain illegal.

## REQUIRED CONTEXT
- target FSM JSON;
- FSM entity and requirements;
- invariants;
- event registry;
- persistence/recovery rules;
- audit/incident behavior;
- implementation mapping;
- transition tests.

## IMPLEMENTATION SEQUENCE
1. Verify current state set and legal transition matrix.
2. Define transition:
   FROM / EVENT / GUARD / ACTION / TO / FAILURE / AUDIT_EVENT.
3. Confirm no shortcut bypasses required intermediate states.
4. Add event ownership and authorization.
5. Define failure behavior when guard fails.
6. Define persistence/transaction boundary.
7. Define recovery/replay behavior.
8. Implement transition.
9. Add positive and forbidden-transition tests.
10. Run replay/idempotency/race tests if asynchronous.
11. Update FSM registry only after source/authority supports the semantic change.

## NEGATIVE TESTS
- wrong FROM state;
- wrong actor/event owner;
- guard false;
- duplicate event;
- crash between action/persist;
- recovery from partial transition;
- STOP/FREEZE bypass attempts.

## DONE
No invalid new path, regression of old transitions, or audit/replay ambiguity remains.
