# PLAYBOOK — Add Event / Message Contract

## PRECONDITIONS
- Producer/consumer and authority are explicit.
- Event is not being used to bypass a direct ownership rule.
- Ordering/idempotency/delivery semantics are known.

## REQUIRED CONTEXT
- Event Registry;
- event contracts;
- FSM event ownership;
- queue/idempotency;
- state/persistence owner;
- observability/audit;
- relevant requirements/invariants.

## IMPLEMENTATION SEQUENCE
1. Define stable event_id/name/version.
2. Define producer and allowed consumers.
3. Define canonical schema.
4. Define ordering key/sequence semantics.
5. Define delivery semantics: at-most-once/at-least-once/etc. only if source/implementation supports it.
6. Define idempotency/dedup key.
7. Define timeout/retry/dead-letter behavior.
8. Define authorization/security classification.
9. Define audit/trace propagation.
10. Define FSM transition effects.
11. Implement producer and consumer validation.
12. Add duplicate/reorder/malformed/late-event tests.

## DONE
Event behavior is deterministic enough for its authority class, replay behavior is explicit, and consumer side effects are protected from duplicates.
