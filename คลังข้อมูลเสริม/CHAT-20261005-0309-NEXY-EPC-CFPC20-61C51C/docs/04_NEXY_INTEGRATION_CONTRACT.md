# Read-only NEXY Integration Contract

## Input adapter may provide
- proposal_id
- exact canonical spec SHA-256
- exact proposal/code SHA-256
- policy-selected worst-case workload dimensions
- ten resource-bound expressions + budgets
- required/provided verification-step IDs
- fail-closed degradation declaration

## CFPC output
- PASS or FREEZE for the standalone feasibility model
- per-mechanism checks/reasons
- evaluated Q64.64 bounds
- deterministic canonical record
- SHA-256 certificate

## Authority prohibition
CFPC MUST NOT:
- mutate NEXY state;
- emit a NEXY release authorization;
- modify Canon/Law/JUDGE rules;
- treat PASS as promotion;
- call providers or execute a proposal;
- convert runtime measurements into canonical policy by itself.

## Evidence boundary
Standalone E1/E2/E3 evidence proves only the reference CFPC implementation. It does not prove NEXY runtime integration, production performance, deployment, or the truth of a proposal's declared symbolic bound. A future adoption path must independently establish that the bound model accurately describes the target implementation.
