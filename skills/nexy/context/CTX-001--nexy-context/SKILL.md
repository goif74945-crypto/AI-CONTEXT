# NEXY Skill
## Identity
Skill ID: CTX-001
Skill name: nexy-context
Family: 01 CONTEXT
Wave: 1
Source: NEXY สกิว.pdf p6 s6
## Objective
Load required current context.
## Authority
Primary: NEXY สกิว.pdf.
## Source of Truth
p6 s6; SHA-256 a2b07fcc9f792ac03331e60ffdfe1a87594788d7d65c75a361b463ea158e5a1c.
## Scope
### In Scope
project, architecture, requirements, repository, branch, HEAD, relevant files, registry, validation state.
### Out of Scope
Using stale context without current-state check.
## Inputs
### Required
task, authority, scope, repository, branch, head, source_of_truth, constraints, expected_output, validation_requirements
### Optional
UNKNOWN.
## Preconditions
Current repository state accessible.
## Outputs
Universal output contract.
## Workflow
### Phase 1 — Context
Load listed context.
### Phase 2 — Authority
Resolve source.
### Phase 3 — Requirement
Load requirements.
### Phase 4 — Inspection
Inspect relevant files.
### Phase 5 — Execution
Use only current context.
### Phase 6 — Validation
Validate freshness/completeness.
### Phase 7 — Evidence
Record context evidence.
## Required Behavior
Load project, architecture, requirements, repository, branch, HEAD, relevant files, registry, validation state. Do not use old context without current-state check.
## Forbidden Behavior
No stale-context assumption.
## Architecture Constraints
Respect actual architecture.
## Security Constraints
No unverified security state.
## Compatibility Constraints
Current contracts only.
## Data Integrity
Preserve context provenance.
## Failure Handling
Missing required context -> UNKNOWN/BLOCKED.
## Freeze Conditions
Critical context conflict or insufficient evidence.
## Validation
### Structural
Required context fields.
### Functional
Current-state check.
### Integration
Relevant repository state.
### Regression
Context-diff check when applicable.
### Evidence
WHAT/WHERE/HOW/RESULT/EVIDENCE.
## Completion Criteria
VERIFIED only with current-state proof.
## Stop Conditions
BLOCKED when required context cannot be loaded.
## Checkpoint
Universal checkpoint contract.
## Resume
Revalidate HEAD and source.
## Error Reporting
Universal error contract.
## Examples
UNKNOWN.
## Non-Goals
No stale context.
## Version
UNKNOWN.
