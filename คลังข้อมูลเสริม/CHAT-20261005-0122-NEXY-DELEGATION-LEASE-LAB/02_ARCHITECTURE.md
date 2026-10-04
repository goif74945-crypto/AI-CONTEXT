# 02 — Architecture

## Status
AI-PROPOSED future architecture. This is not a modification to the current DOC-C dependency graph.

## Candidate placement
```text
AUTHORIZED DIRECTIVE
      |
      v
PLAN COMPILER / CORE-OWNED PLAN
      |
      +---- canonical plan fingerprint ----+
      |                                     |
      v                                     v
AUTHORITY LEASE ISSUANCE              EVIDENCE / OBS
      |
      v
TOOL / SIDE-EFFECT BOUNDARY
      |
      v
LEASE GUARD ---- fail ----> FREEZE + reason + reauthorization requirement
      |
     allow
      v
EXTERNAL / MUTATING ACTION
      |
      v
ATOMIC ACCOUNTING + AUDIT EVENT
```

This must not create a forbidden path such as `SWARM -> VAULT`. If SWARM remains candidate-only labor, LEASE belongs at a CORE-controlled executor/tool boundary.

## Contracts
Action fields: `resource`, `verb`, `effect`, optional `destination`, and `cost_units`.

Reference effect classes:
- `READ`
- `REVERSIBLE_WRITE`
- `IRREVERSIBLE_WRITE`
- `EXTERNAL_SIDE_EFFECT`

These are proposal vocabulary, not current canonical NEXY enums.

An `AuthorityLease` contains stable lease identity, subject, resource patterns, verbs, effects, max cost/actions, logical issue/expiry ticks, exact plan fingerprint, policy version, high-impact gate, and optional parent lease ID.

Mutable accounting is kept in `LeaseState`: used actions, used cost, revoked flag.

## Decision flow
For action index `i` at logical tick `t`:
1. policy version;
2. revocation;
3. activation/expiry;
4. recomputed plan hash;
5. bound-plan equality;
6. action index;
7. resource scope;
8. verb scope;
9. effect scope;
10. high-impact second gate;
11. action budget;
12. cost budget;
13. ALLOW only if every gate passes;
14. otherwise FREEZE with deterministic reason.

No gate silently repairs another failure.

## Deterministic time
The reference policy does not read wall-clock time. Callers provide logical ticks. Real integration needs an authority-approved time/event source.

## Plan fingerprint
Canonical JSON + sorted object keys + fixed separators + UTF-8 + SHA-256 + ordered action arrays. Order changes are drift because ordering can alter effects.

## Delegation law
A child may narrow but never broaden verbs, effects, cost, action budget, time window, high-impact permission, or resource scope. Novel wildcard containment is rejected when subset proof is non-trivial.

## Hash-chain journal
The reference journal binds sequence, logical tick, event type, lease ID, payload hash, and previous hash. It is experiment evidence only, not a NEXY Audit Log/WAL/signature/anchor replacement.

## State model
```text
PLANNED -> AUTHORIZED -> ACTIVE -> REVOKED
                          |  \-> EXPIRED
                          |  \-> EXHAUSTED
                          \----> FROZEN on drift/violation
```

No implicit return to ACTIVE. Reauthorization creates a new lease identity and plan binding.

## Failure semantics
The guard is fail-closed. A future canonical task must decide whether a violation is task-local, execution-local, or global FREEZE.
