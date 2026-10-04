# Architecture — AI-Proposed NEXY Proof-Preserving Resource Governor

## Position in authority graph

```text
USER LAW / NEXY LAW
        ↓ hard constraints
CORE / JUDGE
        ↓ authorized task + resource policy
RESOURCE GOVERNOR  (this proposal)
        ↓ one feasible allocation or FREEZE
AGENT / SWARM workers + verifier executor
        ↓ candidate work / evidence jobs
CORE / JUDGE / verification pipeline
        ↓
FINAL OUTPUT or FREEZE
```

The governor is intentionally **not** an authority layer. It cannot reinterpret law, waive evidence, promote an output, or make a correctness claim.

## Inputs

### TaskProfile
- required capabilities;
- data classification;
- risk tier;
- required E0-E7 evidence class;
- worker/verifier token estimates;
- optional independent-verifier requirement;
- optional optimization quality floor;
- hard total-token, cost and latency ceilings.

### AgentProfile
- stable agent identity;
- provider independence domain;
- allowed roles;
- declared capabilities;
- data clearance;
- context window;
- integer price coefficients;
- latency estimate;
- policy-controlled quality optimization score;
- maximum evidence class the verifier executor is allowed/capable to service;
- active/quarantine state.

Metadata such as price, latency, quality and capabilities is **input state**, not self-proving truth. A production version would require provenance/freshness signatures and must freeze on materially unknown metadata.

## Deterministic pipeline

1. Validate contract and unique agent identities.
2. Derive effective verifier requirement.
3. Derive effective verifier-independence requirement from explicit task flag + risk policy.
4. Sort agents by stable `agent_id`.
5. Filter worker candidates through hard constraints.
6. Filter verifier candidates through hard constraints.
7. Enumerate legal worker/verifier pairs.
8. Reject pairs that violate independence or budgets.
9. Rank remaining plans lexicographically using policy-declared objective order.
10. Break complete ties by stable worker/verifier IDs.
11. Emit exactly one `PLAN_READY` allocation or `FREEZE`.

## Constraint classes

### Non-negotiable gates
- active state;
- quarantine state;
- role eligibility;
- capability set;
- data clearance;
- context capacity;
- evidence execution floor;
- required independence;
- hard token/cost/latency ceilings.

### Optimization signals
- estimated cost;
- estimated latency;
- quality basis-points score.

An optimization signal cannot override a gate.

## Evidence semantics
The field `max_evidence_class` means only that the verifier executor is declared eligible to service work up to that evidence class. It does **not** mean the selected plan has produced that evidence. Every returned plan therefore has `verification_status=NOT_VERIFIED`.

## Arithmetic
Costs use integer microunits and integer ceiling division:

`ceil(tokens × rate_per_1k / 1000)`

No floating-point arithmetic is required for canonical plan comparison.

## Complexity
Let W be eligible workers and V eligible verifiers.
- verifier-free task: O(W log W) dominated by stable preprocessing/ranking;
- verifier-required task: O(W×V) pair enumeration.

The implementation streams the current best legal candidate instead of retaining every feasible pair, so feasible-plan working memory is O(1) beyond agent lists and bounded diagnostics. Time remains O(W×V) for verifier-required tasks. Production-scale optimization can add Pareto pruning/indexing only if equivalence to exhaustive legal-plan selection is proven.

## State/output
The planner itself is pure with respect to external state. Given the same task, policy and agent metadata, it returns the same structural decision.

No external mutation, billing, credential use, model invocation or NEXY runtime operation occurs in this reference implementation.
