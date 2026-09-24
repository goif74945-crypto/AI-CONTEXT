---
name: nexy-requirement
description: Convert an authorized NEXY command into an explicit objective, scope, inputs, outputs, constraints, acceptance and validation contract without adding requirements.
---

# NEXY Skill

## Identity
- Formal ID: `REQ-001`
- Name: `nexy-requirement`
- Family: REQUIREMENT
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Convert a NEXY command into objective, in-scope, out-of-scope, input, output, constraints, acceptance, and validation requirements.

## Authority
This Skill normalizes requirements from authoritative inputs. It cannot add, remove, weaken or reinterpret requirements beyond established authority.

## Source of Truth
- Primary skill specification: `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source named by that specification: `NEXY สกิว.pdf`
- Secondary project context named by that specification: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current repository/runtime evidence is required for implementation-state claims.

## Scope
### In Scope
- normalize objective, scope, inputs/outputs, constraints and acceptance;
- identify validation/evidence obligations;
- preserve explicit non-goals and forbidden behavior;
- surface missing/contradictory requirements.

### Out of Scope
- design invention;
- scope expansion;
- implementation changes;
- resolving authority conflicts without `nexy-authority`.

## Inputs
### Required
- task
- authority
- scope
- repository
- branch
- head
- source_of_truth
- constraints
- expected_output
- validation_requirements
- authorized_command_or_request

### Optional
- requirement IDs
- contract IDs
- invariant IDs
- acceptance matrix

## Preconditions
- `nexy-context` has loaded relevant context;
- `nexy-authority` has resolved material authority questions.

## Outputs
- status
- objective
- in_scope
- out_of_scope
- inputs
- outputs
- constraints
- immutable_rules
- acceptance
- validation_requirements
- evidence_requirements
- unknowns
- conflicts
- next_action

## Workflow
### Phase 1 — Context
Read the authorized command/request and related current context.

### Phase 2 — Authority
Bind each requirement to the applicable authoritative source.

### Phase 3 — Requirement
Normalize the complete task contract without adding new behavior.

### Phase 4 — Inspection
Check requirement IDs, contracts, invariants and acceptance dependencies.

### Phase 5 — Execution
Emit a deterministic requirement package.

### Phase 6 — Validation
Check completeness, contradictions, scope boundaries and evidence-class requirements.

### Phase 7 — Evidence
Record source references for each material requirement.

## Required Behavior
- Preserve explicit non-goals and forbidden actions.
- Separate FACT, UNKNOWN and CONFLICT.
- Make completion criteria testable where the source supports them.

## Forbidden Behavior
- Do not invent acceptance criteria.
- Do not weaken tests or security requirements to make implementation pass.
- Do not convert ambiguity into an implementation choice when correctness depends on it.

## Architecture Constraints
Requirement normalization must precede architecture-impact or mutation planning.

## Security Constraints
Security and human-gate requirements remain mandatory even when omitted from an implementation convenience path.

## Compatibility Constraints
Preserve requirement IDs, contract semantics and supersession.

## Data Integrity
Keep source mapping for each material requirement.

## Failure Handling
Return BLOCKED/CONFLICT when a critical requirement cannot be established.

## Freeze Conditions
Critical unresolved requirement conflict, authority conflict, scope ambiguity affecting architecture/data/security.

## Validation
### Structural
All required task-contract fields are present.

### Functional
No source requirement is silently dropped or added.

### Integration
Output is consumable by scope, architecture, build, test and verification Skills.

### Regression
Later normalization changes must preserve previously authoritative requirements unless superseded.

### Evidence
Each material requirement links to an authority/source reference.

## Completion Criteria
Complete when the task contract is explicit, scoped, source-backed and validation-ready.

## Stop Conditions
Critical conflict, missing authoritative requirement, ambiguous scope that changes architecture/security/data.

## Checkpoint
Persist the normalized task contract and unresolved items.

## Resume
Revalidate source revisions and supersession before reuse.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A repair command becomes exact target, allowed surface, forbidden surface, acceptance, tests, rollback and evidence obligations.

## Non-Goals
This Skill does not decide architecture or modify code.

## Version
1.0.0
