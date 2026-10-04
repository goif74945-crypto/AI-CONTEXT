# NEXY Integration Contract Proposal

Status: **AI-PROPOSED Lo4 / NOT CANON / NOT INTEGRATED**

## Input
- `concept_id`: one registered `L4Q64-01..20` identifier.
- values: exact mapping of required field names to Q64 raw values in `[0, 2^64]`.
- adapters from JSON/network types must validate and convert explicitly before evaluation.

## Output
- readiness raw Q64 and decimal rendering;
- confidence raw Q64 and decimal rendering;
- candidate decision (`ACT|HOLD|ESCALATE|FREEZE`);
- stable rationale codes.

## Authority
The candidate decision MUST NOT directly trigger side effects. NEXY policy, evidence checks, current state and NEXY::JUDGE remain downstream gates.

## Failure semantics
Unknown concept, shape mismatch, out-of-domain input, overflow or divide-by-zero are explicit errors. Integration adapters should map these to NEXY freeze semantics, not fallback guesses.
