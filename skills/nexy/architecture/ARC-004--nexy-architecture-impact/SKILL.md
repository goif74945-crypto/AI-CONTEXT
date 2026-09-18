# NEXY Skill
## Identity
Skill ID: ARC-004 | Name: nexy-architecture-impact | Family: 03 ARCHITECTURE | Wave: 1 | Source: NEXY สกิว.pdf p10 s8
## Objective
Determine what an architectural change affects.
## Authority
NEXY สกิว.pdf.
## Source of Truth
p10 s8; SHA-256 a2b07fcc9f792ac03331e60ffdfe1a87594788d7d65c75a361b463ea158e5a1c.
## Scope
### In Scope
Affected modules, contracts, state, tests, security, release.
### Out of Scope
Unproven impact.
## Inputs
### Required
Universal input contract.
### Optional
UNKNOWN.
## Preconditions
Current architecture and change are known.
## Outputs
Universal output contract plus AFFECTED_MODULES, AFFECTED_CONTRACTS, AFFECTED_STATE, AFFECTED_TESTS, AFFECTED_SECURITY, AFFECTED_RELEASE.
## Workflow
### Phase 1 — Context
Load architecture/current change.
### Phase 2 — Authority
Resolve source.
### Phase 3 — Requirement
Identify affected dimensions.
### Phase 4 — Inspection
Inspect actual dependencies/contracts/state/tests/security/release.
### Phase 5 — Execution
Produce impact record.
### Phase 6 — Validation
Validate each impact item.
### Phase 7 — Evidence
Record concrete impact evidence.
## Required Behavior
Answer: what does this change affect? Output all six affected fields.
## Forbidden Behavior
No guessed impact.
## Architecture Constraints
Preserve architectural boundaries.
## Security Constraints
Security impact cannot be omitted.
## Compatibility Constraints
Contract impact cannot be omitted.
## Data Integrity
State/data impact must be evidenced.
## Failure Handling
Missing critical impact evidence -> BLOCKED.
## Freeze Conditions
Critical impact unknown.
## Validation
### Structural
Six impact outputs.
### Functional
Observed impact.
### Integration
Boundary/contract impact.
### Regression
Test/release impact.
### Evidence
Source/tree/diff/test evidence.
## Completion Criteria
VERIFIED only with evidenced impact analysis.
## Stop Conditions
BLOCKED on critical unknown impact.
## Checkpoint
Universal checkpoint fields.
## Resume
Revalidate source, change, HEAD.
## Error Reporting
Universal error contract.
## Examples
UNKNOWN.
## Non-Goals
No architectural redesign.
## Version
UNKNOWN.
