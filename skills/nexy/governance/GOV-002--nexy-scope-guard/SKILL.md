# NEXY Skill
## Identity
Skill ID: GOV-002
Skill name: nexy-scope-guard
Family: 00 GOVERNANCE
Wave: 1
Source: NEXY สกิว.pdf p5 s5
## Objective
Prevent work outside authorized scope.
## Authority
Primary: NEXY สกิว.pdf.
## Source of Truth
p5 s5; SHA-256 a2b07fcc9f792ac03331e60ffdfe1a87594788d7d65c75a361b463ea158e5a1c.
## Scope
### In Scope
Scope gate for requests.
### Out of Scope
Feature creep, out-of-scope refactor, rename, delete, architecture change, dependency addition.
## Inputs
### Required
task, authority, scope, repository, branch, head, source_of_truth, constraints, expected_output, validation_requirements
### Optional
UNKNOWN.
## Preconditions
Current scope is resolved.
## Outputs
Universal output contract.
## Workflow
### Phase 1 — Context
Load state.
### Phase 2 — Authority
Resolve authority.
### Phase 3 — Requirement
Check request scope.
### Phase 4 — Inspection
Inspect affected scope.
### Phase 5 — Execution
Continue only if in scope.
### Phase 6 — Validation
Validate scope gate.
### Phase 7 — Evidence
Record gate evidence.
## Required Behavior
Gate: REQUEST -> IN SCOPE? YES -> CONTINUE; NO -> STOP.
## Forbidden Behavior
Do not expand scope or change identity.
## Architecture Constraints
No architecture change without source authorization.
## Security Constraints
No bypass of control gates.
## Compatibility Constraints
Preserve contracts.
## Data Integrity
No destructive out-of-scope change.
## Failure Handling
Out-of-scope request stops.
## Freeze Conditions
Critical ambiguity/conflict or insufficient evidence.
## Validation
### Structural
Identity/source/template.
### Functional
Actual scope gate.
### Integration
No out-of-scope dependency.
### Regression
Affected surface.
### Evidence
WHAT/WHERE/HOW/RESULT/EVIDENCE.
## Completion Criteria
VERIFIED only with scope proof.
## Stop Conditions
STOP or BLOCKED when scope cannot be established.
## Checkpoint
expected, processed, verified, failed, skipped, blocked, remaining, current_item, resume_point, last_verified_source, last_verified_head.
## Resume
Revalidate scope and HEAD.
## Error Reporting
ERROR, LOCATION, IMPACT, ROOT_CAUSE if proven, RECOVERY, CURRENT_STATUS.
## Examples
UNKNOWN.
## Non-Goals
No out-of-scope work.
## Version
UNKNOWN.
