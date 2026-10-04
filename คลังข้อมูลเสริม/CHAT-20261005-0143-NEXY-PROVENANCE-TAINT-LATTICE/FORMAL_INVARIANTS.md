# FORMAL INVARIANTS

> AI-PROPOSED CONCEPT. These are reference-kernel invariants, not canonical NEXY.AI law.

Let `T(P1..Pn, C)` be a normal transform under contract `C`.

## I1 — Authority non-promotion

`authority(T) = min(authority(P1), ..., authority(Pn))`

Therefore for every parent `Pi`:

`authority(T) <= authority(Pi)`

A normal transform cannot upgrade the weakest authority in its lineage.

## I2 — Assurance non-inflation

`assurance(T) = intersection(assurance(Pi)) ∩ preserve(C)`

Therefore:

`assurance(T) ⊆ assurance(Pi)` for every parent, and `assurance(T) ⊆ preserve(C)`.

A transform cannot invent an assurance tag.

## I3 — Taint monotonicity under normal transform

`taint(T) = union(taint(Pi)) ∪ introduced(C)`

Therefore:

`taint(Pi) ⊆ taint(T)` for every parent.

No ordinary transform removes taint.

## I4 — Verification exception is explicit and bounded

Verification is not a normal transform. A receipt may add assurance and clear only non-protected taints. It does not increase authority.

Protected taints cannot be cleared by the generic verification path.

## I5 — Exact binding

Artifact ID is SHA-256 of canonical identity fields.
Receipt ID is SHA-256 of canonical receipt fields.

Any identity-relevant field mutation invalidates the stored ID.

## I6 — Stable release decision

For fixed `(artifact, policy, current_epoch)`, the decision is deterministic because:
- all inputs are immutable values;
- reason creation is set-based;
- returned reason codes are sorted;
- no external I/O, clock read, randomness, or model call occurs inside `release_decision()`.

## I7 — Evidence-class non-ordering

The kernel stores exact assurance tags instead of assuming `E6 > E2`, because evidence class suitability depends on the claim. A policy must request the exact evidence/assurance it requires.

## Executed proof strategy

The unit/property suite executes finite representatives for:
- pairwise authority ranks;
- assurance-set intersections;
- protected-taint union propagation;
- a 64-transform chain;
- receipt binding/tamper cases;
- release determinism and freshness boundaries;
- strict wire parsing.

This is executed evidence for the tested domain, not a machine-checked universal proof.
