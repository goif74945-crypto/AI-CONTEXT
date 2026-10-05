# PAREX Metric Integrity Admission — Design

**Classification: AI-PROPOSED / EXPERIMENTAL / NOT CANON / NOT NEXY.AI IMPLEMENTATION**

## Verified gap

Fresh execution showed the original experimental `Plan` accepting both
`float("nan")` and `True` as a benefit metric. `ParetoPruner` returned `PASS`
for either value and produced the same result hash because its output does not
bind the compared metric bytes. Separately, candidates carry no versioned
definition, unit, bound, transformation digest, or per-axis evidence reference,
so values produced under incompatible metric profiles can be compared.

This continuation deepens PAREX; it does not add a sixth mission concept.

## Objective

Admit a plan to PAREX comparison only when:

1. the metric contract defines exactly PAREX's five axes and directions;
2. every axis has a non-empty unit and inclusive exact-integer bounds;
3. the contract binds a non-empty identifier and 64-hex transformation digest;
4. every plan declares the exact canonical profile hash;
5. every metric is an exact integer (never `bool`, float, NaN, or infinity);
6. every metric is within its declared bounds;
7. every axis has exactly one non-empty evidence reference; and
8. plan identifiers are non-empty and unique.

Malformed or incomparable input raises `FreezeError` before dominance. Valid
input is converted to the original `Plan` and delegated to the original
`ParetoPruner`; this admission layer does not choose a winner.

## Contracts

- `MetricAxis`: axis name, fixed direction, unit, and inclusive bounds.
- `ParexMetricContract`: exact five-axis profile plus transformation digest;
  its canonical profile hash changes when any semantic field changes.
- `AttestedPlan`: candidate values, declared profile hash, and exact per-axis
  evidence references.
- `MetricIntegrityPruner`: fail-closed admission adapter around original PAREX.

## Determinism and evidence binding

Contract axes, evidence references, plans, frontier IDs, and rejection details
are normalized into stable order. The returned record includes the canonical
metric profile hash and a digest of admitted candidate metrics/evidence, then
hashes the entire result. Equal normalized inputs therefore yield equal bytes.

## Non-duplication boundary

Repository-wide inspection found multiple Pareto filters, general numeric
integrity/provenance systems, and an explicit backlog item for metric
provenance. It did not find an implemented adapter that binds this mission's
PAREX axes to one canonical metric profile, rejects Python bool/non-finite
numeric confusion, requires per-axis evidence, and delegates admitted plans to
the original pruner. This artifact owns only that narrow pre-comparison
integrity boundary.

## Limits

- Evidence references and transformation digests are syntactically bound, not
  authenticated or independently retrieved.
- Bounds and units prevent incompatible comparison only when the trusted caller
  defines the contract correctly.
- The original PAREX algorithm is unchanged and still returns a frontier, not a
  winner or authorization decision.
- No canonical, production, deployment, or NEXY.AI implementation claim is
  made.
