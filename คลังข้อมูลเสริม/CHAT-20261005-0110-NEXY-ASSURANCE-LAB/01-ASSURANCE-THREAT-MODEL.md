# NEXY Assurance Threat Model

## Purpose
Define failure classes that can produce a plausible-looking but invalid NEXY result. This is an assurance model, not a claim that any failure exists in current code.

## Trust boundaries
1. Untrusted input -> canonical framing.
2. Canonical input -> intent/constraint binding.
3. Constraint binding -> deterministic reasoning.
4. Reasoning -> swarm/adversarial verification.
5. Consensus -> release policy.
6. Release policy -> external side effect.
7. Runtime state -> durable evidence.
8. Human/operator -> recovery and approval.

## Failure families
### A. Semantic ambiguity
A request maps to more than one admissible intent while the system silently chooses one.
Required defense: ambiguity must become rejection/freeze, with evidence of competing interpretations.

### B. Canonicalization divergence
Equivalent logical inputs normalize differently, or distinct inputs collide.
Required tests: idempotence, cross-runtime equivalence, collision corpus, Unicode/encoding adversarial cases.

### C. Constraint erosion
A downstream stage sees a weaker constraint envelope than the admitted one.
Required defense: hash-bind the envelope to every decision/evidence record.

### D. Evidence laundering
A claim gains confidence by repeated references to the same underlying source.
Required defense: evidence independence graph; aliases do not increase evidence cardinality.

### E. Consensus illusion
Multiple agents agree because they share the same upstream defect or copied context.
Required defense: diversity accounting and correlated-failure labels. Quorum count is not independence.

### F. Replay nondeterminism
Same canonical input + same law/config/state yields different authoritative output.
Required defense: deterministic replay tuple and bit-level output comparison.

### G. Time-of-check/time-of-use drift
Evidence is verified, then mutable state changes before release.
Required defense: exact-head / exact-state binding and release token invalidation.

### H. Recovery privilege confusion
A recoverable freeze is resumed by an actor without correct authority or with stale evidence.
Required defense: actor, reason, epoch, token purge and recovery evidence must be bound.

### I. Partial-success leakage
One subsystem fails closed while another exposes a provisional output.
Required defense: single commit point for externally visible authoritative result.

### J. Observability-as-authority
Logs, dashboards, README text, or UI state are mistaken for canonical state.
Required defense: projections must carry source identifiers and never mint authority.

## Attack/failure matrix
Each assurance case should record: ID, precondition, injected fault, expected state, forbidden output, evidence required, cleanup, reproducibility seed, and regression owner.

## Stop rule
If a test cannot identify the authoritative oracle, classify it NOT VERIFIED rather than inventing expected behavior.
