# DESIGN — Provenance Taint Lattice

> **AI-PROPOSED CONCEPT ONLY**
>
> This design is exploratory compatibility infrastructure. It does not modify, supersede, or claim to implement canonical NEXY.AI architecture.

## Objective

Prevent a class of integrity failure called **trust laundering**: weak, unknown, stale, conflicted, or unverified information passing through enough transformations that downstream systems mistakenly treat it as authoritative or verified.

## Non-goals

- Define NEXY's canonical authority hierarchy.
- Replace NEXY::JUDGE, NEXY::LAW, or verification systems.
- Claim deployment/runtime integration.
- Treat evidence classes as a single monotonic score.

## Model

Each artifact carries:
- content-addressed identity;
- payload digest;
- ordered parent identities;
- root origins;
- an authority floor supplied by the caller's policy domain;
- exact assurance tags;
- sticky taints;
- creation epoch;
- canonical metadata;
- applied verification receipt IDs.

A transform has an explicit contract:
- required assurances;
- assurance preservation allowlist;
- deterministic/non-deterministic flag;
- newly introduced taints.

### Lattice-like propagation rules

For parents P1..Pn:

- `authority_floor(out) = min(authority_floor(Pi))`
- `assurances(out) = intersection(assurances(Pi)) ∩ preserved_assurances(contract)`
- `taints(out) = union(taints(Pi)) ∪ introduced_taints(contract)`
- if transform is non-deterministic, add `NONDETERMINISTIC`
- `root_origins(out) = sorted unique union(root_origins(Pi))`

These operators deliberately make ordinary transformation **non-promotional**.

## Verification semantics

A verification receipt:
- is bound to one exact artifact ID;
- can add exact assurance tags;
- can clear only non-protected taints;
- cannot upgrade authority floor;
- expires deterministically by epoch;
- cannot be applied twice to the same artifact lineage state.

Protected taints in this reference design:
- `UNKNOWN_ORIGIN`
- `CONFLICT`
- `EXTERNAL_UNTRUSTED`
- `POLICY_MISMATCH`

The protected set is intentionally conservative. A future specialized adjudication receipt could resolve specific protected conditions, but generic verification must not quietly do so.

## Release gate

A release policy may require:
- minimum authority rank;
- exact assurance tags;
- absence of selected taints;
- allowed root origins;
- maximum artifact age;
- deterministic lineage.

Decision output is either:
- `ALLOW`, or
- `FREEZE` + stable sorted reason codes.

## Security / abuse model

Threats covered by the reference implementation:
1. repeated rewrite laundering;
2. mixed high/low authority merge;
3. assurance inflation by transform;
4. receipt replay against a different artifact;
5. receipt reuse after state change;
6. protected-taint erasure;
7. stale/future artifact release;
8. nondeterministic lineage release;
9. metadata-order identity instability;
10. direct artifact tampering.

## Compatibility surface for future NEXY.AI

Potential adapters, if NEXY maintainers ever choose to adopt the concept:
- map NEXY source/evidence classes to assurance tags;
- map NEXY authority law to policy-local numeric or partially ordered authority domains;
- issue verification receipts from a NEXY::JUDGE-compatible boundary;
- call `release_decision()` immediately before a controlled output boundary;
- persist artifact/receipt IDs into NEXY audit/evidence records.

No adapter is implemented here because touching NEXY.AI is explicitly out of scope.

## Failure behavior

- malformed source/contract/receipt: raise deterministic `ProvenanceError`;
- artifact identity mismatch: raise `IntegrityError`;
- release requirement unmet: do not throw; return `FREEZE` with reasons;
- unknown/protected provenance condition: remain sticky until handled by a future specialized protocol.

## Evolution ideas

All items below are **AI-PROPOSED FUTURE CONCEPTS**:
- vector/partial-order authority domains instead of scalar caller-defined rank;
- signed receipts with external key verification;
- Merkleized lineage compaction for very long chains;
- selective disclosure proofs for privacy-preserving provenance;
- policy compilation from NEXY law to release gates;
- durable lineage graph storage and transitive cycle detection;
- formal property tests / model checking of monotonicity;
- cross-agent provenance envelopes for SWARM handoffs.

## Wire contract v1

The lab includes strict JSON-compatible record converters for artifacts, receipts, and release decisions.

Boundary law:
- schema identifiers are versioned;
- unknown schema versions fail closed;
- missing or extra fields fail closed;
- integer fields reject booleans;
- unknown taint codes fail closed;
- artifact/receipt identities are revalidated after parsing;
- release-decision state/reason invariants are checked before serialization.

This surface is intended as the future adapter boundary instead of importing Python implementation details into another system.
