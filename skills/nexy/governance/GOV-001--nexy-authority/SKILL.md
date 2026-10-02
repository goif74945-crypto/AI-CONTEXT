# NEXY Skill
## Identity
Skill ID: GOV-001
Skill name: nexy-authority
Family: 00 GOVERNANCE
Wave: 1
Source: NEXY สกิว.pdf p4 s5
## Objective
Identify which Source has authority over a decision.
## Authority
Primary: NEXY สกิว.pdf. No override.
## Source of Truth
NEXY สกิว.pdf SHA-256 a2b07fcc9f792ac03331e60ffdfe1a87594788d7d65c75a361b463ea158e5a1c; p4; s5.
## Scope
### In Scope
Authority classification for the decision.
### Out of Scope
Unsupported mechanism or semantic.
## Inputs
### Required
 task, authority, scope, repository, branch, head, source_of_truth, constraints, expected_output, validation_requirements
### Optional
UNKNOWN.
## Preconditions
Current authority/context available.
## Outputs
status, objective, scope, inputs, actions, changed_files, unchanged_files, validation, evidence, errors, unknowns, remaining, next_action.
## Workflow
### Phase 1 — Context
Load current state.
### Phase 2 — Authority
Resolve authoritative source.
### Phase 3 — Requirement
Apply source requirement.
### Phase 4 — Inspection
Inspect actual source/state.
### Phase 5 — Execution
Perform only source-defined work.
### Phase 6 — Validation
Validate identity, scope, behavior, constraints.
### Phase 7 — Evidence
Record WHAT, WHERE, HOW, RESULT, EVIDENCE.
## Required Behavior
Input: requirement, specification, repository state, existing implementation, validation result. Output: AUTHORITY_RESULT, SOURCE, CONFIDENCE, CONFLICTS, DECISION. Classify AUTHORITATIVE/SUPPORTING/HISTORICAL/UNKNOWN. Unresolvable authoritative conflict -> BLOCKED.
## Forbidden Behavior
Guessing, inventing, fabricating evidence, scope expansion, rename, merge, split, silent conflict reconciliation.
## Architecture Constraints
No new architecture/dependency.
## Security Constraints
No unverified security claim.
## Compatibility Constraints
Preserve contracts.
## Data Integrity
Preserve source/evidence integrity.
## Failure Handling
Follow source; unresolved authority conflict is BLOCKED.
## Freeze Conditions
Authority/architecture conflict, security uncertainty, data risk, contract mismatch, critical failure, insufficient evidence, release gate failure.
## Validation
### Structural
Identity/template/source.
### Functional
Authority classification with evidence.
### Integration
Affected authority boundary.
### Regression
Affected regression surface.
### Evidence
WHAT/WHERE/HOW/RESULT/EVIDENCE.
## Completion Criteria
VERIFIED only with all required proof and evidence.
## Stop Conditions
BLOCKED when authority cannot be proven.
## Checkpoint
expected, processed, verified, failed, skipped, blocked, remaining, current_item, resume_point, last_verified_source, last_verified_head.
## Resume
Resume only after checkpoint and HEAD revalidation.
## Error Reporting
ERROR, LOCATION, IMPACT, ROOT_CAUSE only if proven, RECOVERY, CURRENT_STATUS.
## Examples
UNKNOWN.
## Non-Goals
No capability beyond source.
## Version
UNKNOWN.
