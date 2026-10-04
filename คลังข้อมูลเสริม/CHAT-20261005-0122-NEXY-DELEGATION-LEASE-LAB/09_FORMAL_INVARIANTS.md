# 09 — Formal Invariants and Proof Obligations

Let `L` be immutable lease, `S` lease state, `P` plan, `H(P)` plan fingerprint, `A_i` action, `t` logical tick.

## Safety invariants
- I-01 Plan binding: `Allow => H(P) = L.plan_hash`.
- I-02 Temporal validity: `Allow => issued <= t <= expiry`.
- I-03 Revocation: `S.revoked => not Allow`.
- I-04 Resource containment: `Allow => A_i.resource in L.resource_scope`.
- I-05 Verb containment: `Allow => A_i.verb in L.allowed_verbs`.
- I-06 Effect containment: `Allow => A_i.effect in L.allowed_effects`.
- I-07 High-impact two-gate: high-impact + Allow implies `L.allow_high_impact=true`.
- I-08 Action bound: `used_actions + 1 <= max_actions`.
- I-09 Cost bound: `used_cost + action_cost <= max_cost`.
- I-10 Policy binding: `Allow => L.policy_version = Executor.policy_version`.
- I-11 Monotonic child authority: verbs/effects/resources narrow; budgets/time cannot expand; high-impact cannot appear.
- I-12 No mutation on denied decision: FREEZE cannot be committed.
- I-13 No implicit recovery: drift/expiry/revocation/exhaustion/version mismatch never auto-renews/rebinds.

## Liveness boundary
This design prioritizes safety over liveness. Conservative false freezes, especially scope subset proofs, are allowed. Reduce them only with stronger proofs, never silent weakening.

## Production proof obligations
1. check + reserve + dispatch is race-safe;
2. revocation wins correctly against concurrent dispatch;
3. canonical resource identity resists aliases;
4. issuer/subject identity cannot be forged;
5. replay receipts cannot duplicate effects;
6. crash recovery cannot spend budget twice;
7. policy upgrade cannot permissively reinterpret old leases;
8. provider-specific child-scope proofs are sound;
9. audit evidence is durably ordered and attributable;
10. upstream RBAC/LAW denial always dominates lease allow.

## Suggested model-check state
Lease status, plan hash/version, budgets, revocation epoch, executor epoch, pending dispatches, committed receipts.

Primary property: no committed side effect exists without a unique prior authorization valid for the same plan, resource, effect, destination, budget, and policy version.
