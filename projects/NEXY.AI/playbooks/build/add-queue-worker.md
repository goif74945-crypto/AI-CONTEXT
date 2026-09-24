# NEXY Builder Playbook

## Universal preconditions
1. Pin repository + branch + exact HEAD.
2. Resolve ontology entity, requirements, authority/scope/supersession/conflicts.
3. Resolve dependencies, implementation refs, contracts, FSM, atomic invariants, security/state/event/config.
4. Check failure/recovery library.
5. Do not infer PASS from file presence, build success, or docs.

# Workflow: Add Queue Worker

## Required context
- queue payload contract;
- job lifecycle FSM;
- producer/consumer validation;
- idempotency and stale-job policy;
- concurrency limits;
- failure/audit semantics.

## Sequence
1. Define/confirm payload schema.
2. Validate before enqueue.
3. Use canonical idempotency key/job identity.
4. Enforce configured concurrency cap.
5. Revalidate before consume.
6. Enforce stale TTL before execution.
7. Keep failed-job auto-retry disabled unless explicitly proven safe.
8. Record run state/event/audit/incident atomically where required.
9. Add duplicate, stale, malformed, worker-down and recovery tests.
10. Update event/traceability/failure registries.

## DONE
No duplicate mutation, stale execution or silent retry path remains.
