# Design Decisions

## D-001 — Keep proposal authority permanently lower than project authority

Decision: evaluator outputs are advisory only. There is no `APPROVED`, `IMPLEMENT`, or automatic promotion state.

Reason: AI creativity must not silently become NEXY truth.

## D-002 — Integer similarity only

Decision: overlap scores use integer basis points (`0..10000`) and fixed integer weights.

Reason: deterministic comparison without floating-point drift or arbitrary binary rounding behavior.

## D-003 — Typed evidence roles

Decision: evidence records carry both a truth class and an evidence role such as `AUTHORITY` or `DUPLICATE_CHECK`.

Reason: do not infer evidence purpose from natural-language wording or language-specific keywords.

## D-004 — Proposal identity collision freezes

Decision: if a catalog already contains the same `proposal_id` with different canonical content, evaluation returns `FREEZE_CONFLICT`.

Reason: identity reuse with divergent content is ambiguous provenance.

## D-005 — Unknown fields fail validation

Decision: proposal, evidence, and work-manifest objects reject additional fields.

Reason: silently ignored fields can hide authority, state, or semantics from the evaluator.

## D-006 — Collision guard is not a distributed lock

Decision: completed/blocked manifests are ignored for active collision decisions; active path/proposal overlap emits advisory `COLLISION` only.

Reason: repository manifests can become stale and cannot prove live session ownership.

## D-007 — Preserve list order in canonical fingerprints

Decision: dictionary keys are canonicalized but list order is preserved.

Reason: list order can encode user priority or intended sequence. Treating lists as sets would silently alter meaning.
