# NEXY Skill
## Identity
Skill ID: REQ-001
Skill name: nexy-requirement
Family: 02 REQUIREMENT
Wave: 1
Source: NEXY สกิว.pdf p7 s7
## Objective
Translate a command into an explicit requirement contract.
## Authority
Primary: NEXY สกิว.pdf.
## Source of Truth
p7 s7; SHA-256 a2b07fcc9f792ac03331e60ffdfe1a87594788d7d65c75a361b463ea158e5a1c.
## Scope
### In Scope
OBJECTIVE, IN_SCOPE, OUT_SCOPE, INPUT, OUTPUT, CONSTRAINT, ACCEPTANCE, VALIDATION.
### Out of Scope
Invented requirements.
## Inputs
### Required
Universal input contract.
### Optional
UNKNOWN.
## Preconditions
Command and authority available.
## Outputs
Universal output contract plus requirement fields.
## Workflow
### Phase 1 — Context
Load current context.
### Phase 2 — Authority
Resolve source.
### Phase 3 — Requirement
Translate command.
### Phase 4 — Inspection
Check source evidence.
### Phase 5 — Execution
Produce explicit requirement contract.
### Phase 6 — Validation
Validate completeness against source.
### Phase 7 — Evidence
Record traceable requirement evidence.
## Required Behavior
Convert command to OBJECTIVE, IN_SCOPE, OUT_SCOPE, INPUT, OUTPUT, CONSTRAINT, ACCEPTANCE, VALIDATION.
## Forbidden Behavior
No guessed requirement.
## Architecture Constraints
Do not add architecture requirements not sourced.
## Security Constraints
Security requirements only when sourced.
## Compatibility Constraints
Preserve source contracts.
## Data Integrity
Preserve requirement provenance.
## Failure Handling
Missing authoritative detail -> UNKNOWN/BLOCKED.
## Freeze Conditions
Requirement conflict or insufficient authority.
## Validation
### Structural
All requirement fields.
### Functional
Source alignment.
### Integration
Affected contracts.
### Regression
Requirement traceability.
### Evidence
PDF/source evidence.
## Completion Criteria
VERIFIED only with complete source-backed contract.
## Stop Conditions
BLOCKED on unresolved authoritative ambiguity.
## Checkpoint
Universal checkpoint contract.
## Resume
Revalidate source and HEAD.
## Error Reporting
Universal error contract.
## Examples
UNKNOWN.
## Non-Goals
No additional requirement.
## Version
UNKNOWN.
