# NEXY Skill
## Identity
Skill ID: CTX-003
Skill name: nexy-source-inspector
Family: 01 CONTEXT
Wave: 1
Source: NEXY สกิว.pdf p7 s6
## Objective
Inspect actual source before deciding.
## Authority
Primary: NEXY สกิว.pdf.
## Source of Truth
p7 s6; SHA-256 a2b07fcc9f792ac03331e60ffdfe1a87594788d7d65c75a361b463ea158e5a1c.
## Scope
### In Scope
Source inspection and relationship identification.
### Out of Scope
Invented source relationships.
## Inputs
### Required
Universal input contract.
### Optional
UNKNOWN.
## Preconditions
Actual source available.
## Outputs
Universal output contract.
## Workflow
### Phase 1 — Context
Load current source context.
### Phase 2 — Authority
Resolve authority.
### Phase 3 — Requirement
Identify inspection requirement.
### Phase 4 — Inspection
Inspect file and relationships.
### Phase 5 — Execution
Record only observed facts.
### Phase 6 — Validation
Validate source findings.
### Phase 7 — Evidence
Record source evidence.
## Required Behavior
Must identify FILE, PATH, TYPE, DEPENDENCIES, CALLERS, CALLEES, CONTRACTS, TESTS.
## Forbidden Behavior
No guessed dependencies/callers/callees/contracts/tests.
## Architecture Constraints
Preserve observed boundaries.
## Security Constraints
Do not invent security relationships.
## Compatibility Constraints
Record actual contracts.
## Data Integrity
Preserve source content and provenance.
## Failure Handling
Missing source -> BLOCKED.
## Freeze Conditions
Critical uncertainty or conflict.
## Validation
### Structural
Inspection fields present.
### Functional
Observed source facts.
### Integration
Observed relationships.
### Regression
Relevant tests identified.
### Evidence
Concrete source refs.
## Completion Criteria
VERIFIED only with evidence for required inspection facts.
## Stop Conditions
BLOCKED when source cannot be inspected.
## Checkpoint
Universal checkpoint contract.
## Resume
Revalidate source and HEAD.
## Error Reporting
Universal error contract.
## Examples
UNKNOWN.
## Non-Goals
No synthetic source facts.
## Version
UNKNOWN.
