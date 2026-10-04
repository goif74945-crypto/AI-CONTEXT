# Proposed NEXY Integration Boundary

**STATUS: PROPOSAL ONLY. No current NEXY integration is claimed.**

## Compatibility principles

The five modules are designed to sit outside the Canon boundary and accept explicit immutable data from an authorized adapter.

### SQX
Candidate placement: verification/model-checking tooling before exhaustive state exploration. It may reduce redundant test states but must preserve a mapping back to every original state represented by a quotient bucket.

### CEFG
Candidate placement: between decision-trace generation and user-facing explanation rendering. NEXY authority must provide the actual causal trace; CEFG must never infer authority from prose.

### RSEK
Candidate placement: robotics planning/simulation preflight only. A dedicated independent safety controller remains authoritative for physical emergency behavior.

### FPSA
Candidate placement: admission analysis for periodic execution contracts, robotics loops, or deterministic worker budgets. Real deployment needs runtime timing evidence and a richer scheduling model where the platform requires it.

### OEWC
Candidate placement: shadow validation during provider/runtime/refactor substitution. The adapter must explicitly define observable fields; internal implementation equality is neither required nor assumed.

## Required adapter envelope

A future adapter should bind at least:
- adapter/version identity;
- exact NEXY revision;
- authority reference;
- input provenance;
- module/version digest;
- explicit contract version;
- evidence timestamp supplied by the outer system if time matters;
- result digest;
- evidence class.

The reference modules do not read the clock themselves.

## Promotion gate

Promotion from Lo4 proposal to Canon requires a separate authorized process that includes:
1. requirement mapping against the current governing source/spec;
2. threat/failure review;
3. exact-revision adapter implementation;
4. E1 static validation;
5. E2 focused behavior tests;
6. E3 integration tests;
7. E4/E5/E6/E7 evidence where the claimed behavior requires it;
8. rollback/rejection path;
9. explicit human/project authority approval.

Existence in AI-CONTEXT is not promotion.
