# Multichannel Truth Equivalence

**Classification:** AI-PROPOSED / advisory verification extension.

## Problem

A product can preserve truth in the primary visual component while silently diverging elsewhere:
- screen-reader/ARIA text;
- mobile condensed cards;
- print/export views;
- alternative dashboards;
- notification summaries.

That creates a semantic split-brain UI. For a system whose identity depends on truthful state exposure, this is an integrity defect rather than a cosmetic inconsistency.

## Contract

Given one authoritative backend envelope and one role, every declared presentation channel should preserve equivalent values for:
- displayed status;
- displayed state;
- result visibility;
- request identity;
- trace identity;
- action identity/kind set.

Each channel must also pass the single-surface Truth Surface Checker independently.

## Reference channels

The bounded model-check suite uses:
- `visual`
- `aria`
- `mobile`
- `export`

These names are proposals, not a claim about current NEXY implementation.

## Why action order is ignored

Different channels may reorder equivalent actions for layout/accessibility reasons. The equivalence checker compares normalized `(action id, kind)` sets rather than presentation order.

## What is not normalized away

The checker does not normalize away:
- a missing action;
- a different mutation/read kind;
- a different state/status;
- a different request/trace identity;
- result visibility differences.

Those are semantic differences.

## Failure model

A multichannel report fails when:
1. any individual channel violates a truth-surface invariant; or
2. channels disagree on a locked semantic field.

## Local evidence

Unit suite:
- 47 total tests in `conformance_tests` after adding multichannel tests;
- 47 PASS.

Bounded multichannel fault matrix:
- 45 clean cross-channel cases PASS;
- 135 injected cross-channel defects;
- 135/135 detected;
- 0 failures.

The matrix covers 9 state/status scenarios × 5 roles × 4 channels. It is exhaustive over that generated bounded matrix only.

## Future extension

A production adapter could capture:
- DOM-visible state;
- accessibility tree semantic state;
- mobile renderer snapshot metadata;
- export serializer metadata;

and normalize all four into the manifest contract. This lab does not implement browser capture or claim E4 evidence.
