# Proposed NEXY.AI Integration Contract

> **`PROPOSAL_BY_AI`**. This is not an instruction to change NEXY.AI and not proof of current integration.

## Observed read-only anchors

At the NEXY revision observed during this session (`9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43` on `NEXY.ai`):

- `packages/phase-f/l1o/l600-support.ts` exposes side-effect classes `NONE`, `MEMORY_ONLY`, `FILESYSTEM`, `NETWORK`, `DATABASE`, `PROCESS`, `DEVICE` and declared-operation rules.
- The same file contains pre-execution intent verification and deterministic parallel-plan constraints.
- `AGENTS.md` requires refresh/preservation/freeze discipline around repository mutation.
- queue/Prisma evidence shows durable dispatch/idempotency patterns.

These facts make this lab structurally compatible as a future concept. They do not authorize it as NEXY law.

## Proposed placement

```text
authorized intent
      |
      v
candidate action construction
      |
      v
Side-Effect Transaction Firewall
      | FREEZE
      | ALLOW
      v
read-only preflight observer
      |
      v
COMMIT_READY seal
      |
      v
future NEXY-controlled executor
```

## Mapping requirements

A future adapter must explicitly map resource namespace, action kind, authority proof source, risk class, precondition observer, idempotency namespace, rollback semantics and irreversible approval source. Missing mapping must FREEZE. It must never be guessed.

## Proposed commit protocol

1. Construct the complete candidate action set before any side effect.
2. Compile under a sealed policy.
3. Abort on `FREEZE`.
4. Gather only requested read-only observations.
5. Seal preflight against the exact `planHash`.
6. Abort unless `COMMIT_READY`.
7. Future executor independently verifies policy hash, plan hash, seal, authority proofs and freshness lease.
8. Execute deterministic waves.
9. Persist completion receipts where crash recovery requires it.
10. On partial failure, generate compensation order, translate to fresh actions and run policy + preflight again.

## Evidence gates still required

- E1 adapter/static compatibility.
- E2 standalone planner behavior is present here.
- E3 real NEXY action-envelope integration.
- E4 actual user/tool E2E.
- E5 crash/restart/locking/contention.
- E6 deployment if ever deployed.
- E7 for physical/device safety.

No E2 result here substitutes for E3-E7.
