# 05 — RDRC: Requirement Delta Revalidation Compiler

**Status:** AI-PROPOSED / Lo4 / NON-CANONICAL

## Objective
Turn requirement evolution into a deterministic revalidation plan so evidence is not silently reused after semantics change.

## Supported structured relations
Reference constraints support:
- allowed-value sets;
- numeric intervals;
- evidence class E0..E7.

A requirement delta is classified as:
- `ADDED`;
- `REMOVED`;
- `UNCHANGED`;
- `TIGHTENED`;
- `LOOSENED`;
- `MIXED`.

## Revalidation semantics
- Added: implementation + positive + negative + traceability proof at declared evidence class.
- Removed: traceability + orphan-reference audit.
- Tightened: positive + negative + regression + traceability at the stronger evidence demand.
- Loosened: policy review + negative + regression + traceability. Loosening is not assumed safer.
- Mixed: full combined gates.

## Immutable rules
- Evidence-class changes are semantic changes.
- No stale evidence auto-carries across a changed requirement.
- Loosening is explicitly reviewed because expanded behavior can increase risk.
- Removed requirements trigger orphan-reference checks instead of disappearing silently.

## NEXY fit
The current NEXY source-normalization matrix contains 837 normalized rows. Future revisions need a machine-checkable answer to “what changed and what proof became stale?” RDRC is a small reference kernel for that boundary.

## Failure behavior
Duplicate requirement IDs or invalid evidence classes are rejected. Unknown constraint kinds degrade to `MIXED` rather than pretending a tightening/loosening order is known.

## Acceptance evidence
E2 tests cover tightening, loosening, add/remove and interval narrowing. Stress compares 2,000 old/new requirements twice and verifies deterministic identical delta output.
