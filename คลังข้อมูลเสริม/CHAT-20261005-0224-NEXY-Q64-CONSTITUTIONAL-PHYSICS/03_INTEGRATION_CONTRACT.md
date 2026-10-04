# Proposed NEXY Integration Contract

**Status:** proposal only; no NEXY integration performed.

## Placement
These engines are candidate advisory gates between normalized planning/evidence state and authoritative execution adjudication. They must not replace NEXY::LAW or NEXY::JUDGE.

## Adapter input law
A future adapter must:
1. map authoritative typed values to Q64.64 without float intermediates;
2. attach provenance for every derived quantity;
3. version the quantitative policy/threshold set;
4. reject missing units/dimensions/identities;
5. translate Q64 overflow/domain exceptions to fail-closed NEXY states;
6. never treat a local PASS as execution permission.

## Suggested output envelope
- engine ID + engine version;
- policy version/digest;
- status/reason;
- Q64 raw values needed to reproduce the decision;
- source/evidence references;
- deterministic input digest;
- target task/plan identity.

## Composition law
Any `FREEZE` dominates. `CERTIFY_DENY` is a robust negative certificate and should be routed to authoritative adjudication, not converted to a system failure. PASS from all five means only that these five advisory contracts were satisfied.

## Required promotion gates
Before any real integration:
- owner mapping against current NEXY Canon;
- schema/version review;
- independent Q64 arithmetic cross-implementation tests;
- exact threshold/rounding authority approval;
- transaction/concurrency design for VBR;
- real evidence model for UMC receipts and RHL parameters;
- integration E3 tests at exact NEXY revision;
- E4 user-flow tests for preview fidelity;
- E5 load/fault/recovery tests where operational claims are made;
- security review and rollback plan;
- formal promotion record. Until then status remains NON_GOVERNING.
