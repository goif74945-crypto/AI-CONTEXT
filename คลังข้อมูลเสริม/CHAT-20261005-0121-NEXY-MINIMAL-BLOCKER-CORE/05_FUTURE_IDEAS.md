# Future Extensions

Every item in this document is **AI-PROPOSED CONCEPT / NOT CURRENT NEXY LAW**.

## 1. Evidence authenticity adapter

Bind each leaf to signed/attested evidence identities rather than caller-provided status strings. The blocker engine should remain pure; authenticity verification belongs in an adapter layer.

## 2. Proof-expiry propagation

Represent evidence validity windows/revocation references so a previously PASS leaf can deterministically become NOT_VERIFIED when its proof expires or its source revision is superseded.

## 3. Multi-objective repair ranking

Replace scalar `repair_cost` with a declared vector such as engineering effort, external dependency risk, blast radius, latency, and evidence strength. Never collapse to one number without an explicit policy.

## 4. Hard/soft obligation separation

Allow advisory optimizations to be reported separately from mandatory release blockers. Soft constraints must never masquerade as authority to bypass a hard gate.

## 5. Counterfactual impact link

For each repair candidate, query a separate impact graph to estimate which previously PASS obligations require revalidation after the repair. This prevents “fix one blocker, silently stale five proofs.”

## 6. Certificate differential

Compare two freeze certificates and explain:

- which evidence changed;
- which blocker cores disappeared/appeared;
- whether the recommendation changed because of status, cost, or gate topology;
- whether the target revision changed.

## 7. Historical blocker mining

Aggregate blocker cores over time to discover high-frequency structural bottlenecks. This should remain analytics, not an automatic permission to weaken recurring gates.

## 8. Formal cross-check

Compile bounded gate instances to SAT/SMT or a model-checking representation and cross-check minimal repair sets against an independent solver. This would materially strengthen correctness evidence for larger formulas.

## 9. Interactive human explanation

Render the certificate as a progressive disclosure UI:

`FREEZE -> primary blocker core -> alternative repairs -> evidence details -> exact provenance`

The UI must clearly label advisory recommendation vs authoritative project requirement.

## 10. Repair transaction planner

Convert a selected repair set into a *proposed* dependency-ordered work plan containing read preconditions, mutation boundaries, verification steps, rollback, and expected evidence. It must not execute automatically from a repair certificate.
