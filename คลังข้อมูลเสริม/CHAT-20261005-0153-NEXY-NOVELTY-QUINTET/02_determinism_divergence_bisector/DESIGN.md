# Design — Determinism Divergence Bisector (DDB)

**Classification:** AI-PROPOSED CONCEPT / ADVISORY ONLY

## Objective
Localize the first meaningful divergence between two ordered execution traces without treating known volatile metadata as semantic output.

## NEXY value
When two supposedly equivalent runs disagree, a giant final diff answers too late. DDB builds chained prefix hashes, then binary-searches the first mismatching prefix. This turns "the runs differ" into "the earliest proven divergence is step i, with dependency frontier X".

## Core contract
- Input: ordered trace steps with optional `id`, `deps`, arbitrary structured content.
- Volatile fields ignored by default: `timestamp`, `trace_id`, `span_id`, `duration_ms`.
- Canonical structured serialization is hashed with SHA-256.
- Prefix hashes are chained so once semantic divergence occurs, later prefix equality cannot falsely recover.
- Different common-prefix content -> `DIVERGED` with first index and hashes.
- Equal common prefix but different lengths -> `TRACE_LENGTH` divergence.
- Exact equality -> `EQUIVALENT`.

## Failure / risk semantics
Ignoring a field that actually carries authority would be unsafe. Therefore the volatile-key set must be treated as an integration contract, not casually expanded. DDB proves trace equivalence only under the declared canonicalization policy.

## Complexity
Step canonicalization is O(total serialized trace size). Divergence localization over precomputed prefix chains is O(log n).
