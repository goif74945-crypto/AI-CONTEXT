# Future Proposals

Every item below is **`PROPOSAL_BY_AI`**. None is a current NEXY.AI requirement or implemented production feature.

## P-01 Commit Lease Binding
Bind `COMMIT_READY` to a short-lived single-use lease consumed atomically by the state owner. This narrows the TOCTOU gap. Lease outage must FREEZE, never bypass.

## P-02 Durable Transaction Journal
Persist plan hash, seal hash, wave, completed action IDs, external receipt hashes and compensation state in an append-oriented journal for crash recovery and forensic replay.

## P-03 Effect Capability Tokens
Issue plan-bound capability tokens scoped to exact effect class, resources, operations, actor, plan hash and lease epoch. This reduces confused-deputy risk.

## P-04 Compensation Recompiler
Translate compensation steps into fresh actions and pass them through the same compile + preflight path under an explicit recovery policy. Rollback must not be a privilege bypass.

## P-05 Resource Namespace Registry
Define canonical namespaces such as `repo:`, `file:`, `db:`, `queue:`, `net:`, `device:` and alias rules so two names cannot hide one underlying resource.

## P-06 Effect Summary Compiler
Statically derive candidate effect/resource summaries from approved action implementations and compare them with caller declarations. Unknown dynamic targets must widen or FREEZE, never underapproximate silently.

## P-07 Distributed Conflict Reservation
Reserve resource intents by plan hash and acquire in canonical order across executors. Requires deadlock, lease expiry, split-brain and abandoned-reservation recovery proof.

## P-08 Proof Capsule
Emit one immutable capsule containing policy hash, plan hash, normalized effect summary, preflight seal, authority-proof references, executor receipts and final/compensation outcome.

## P-09 Counterfactual Side-Effect Preview
Run a deterministic expected-state-delta model before higher-risk commits and compare invariants. Simulation PASS must not substitute for runtime proof.

## P-10 Cross-Plan Conflict Broker
The current planner reasons inside one plan. A future broker could compare concurrently admitted plans and serialize shared-resource conflicts without turning every plan into one global lock.

## P-11 Risk-Adaptive Evidence Class
Map risk/effect class to minimum evidence requirements. Higher consequence should require stronger independent evidence; incorrect risk classification must be treated as an authority-sensitive path.

## P-12 Transaction Mutation Budget
Bound not only action count but resource count, bytes, external calls, process launches and device commands. Unknown dynamic cost must not default to zero.

These proposals are intentionally stored for future design work only. They are not silently included in the reference implementation.
