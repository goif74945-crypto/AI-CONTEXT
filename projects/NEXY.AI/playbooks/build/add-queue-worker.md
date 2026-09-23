# PLAYBOOK — Add Queue Worker

## PRECONDITIONS
- Queue/job requirement is in current authorized scope.
- Job ownership, payload contract, idempotency semantics, stale behavior and failure policy are explicit.
- Queue worker cannot bypass CORE/LAW/JUDGE/VAULT ownership boundaries.

## REQUIRED CONTEXT
- DOC-C Queue Law;
- queue-job FSM;
- event/message contracts;
- idempotency requirements;
- incident/observability requirements;
- state ownership/persistence maps;
- current queue implementation mapping;
- known failures/regressions.

## IMPLEMENTATION SEQUENCE
1. Define job type and producer.
2. Define payload schema and runtime validation at enqueue.
3. Define validation again at consume.
4. Define stable idempotency key.
5. Define QUEUED/RUNNING/SUCCEEDED/FAILED/CANCELLED/EXPIRED behavior.
6. Define stale-job TTL and expiry action.
7. Define retry policy. Default: no automatic retry unless explicitly proven safe.
8. Define FREEZE/STOP cancellation behavior.
9. Define worker concurrency/resource limits.
10. Define trace/request/correlation propagation.
11. Define audit/event/incident emission.
12. Implement producer + worker without giving worker unauthorized state mutation.
13. Add duplicate, stale, crash, timeout and cancellation tests.
14. Verify no duplicate authoritative execution after restart/re-delivery.

## NEGATIVE TESTS
- invalid payload;
- duplicate idempotency key;
- worker crash after side effect/before ACK;
- duplicate delivery;
- stale job;
- FREEZE while queued/running;
- STOP;
- dependency timeout;
- retry of unsafe mutation.

## DONE
Queue semantics are proven to be idempotent at the required boundary and consistent with queue FSM/freeze/incident contracts.
