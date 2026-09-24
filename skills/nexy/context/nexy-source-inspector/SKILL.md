---
name: nexy-source-inspector
description: Inspect real NEXY source at the exact target revision and map file, path, type, dependencies, callers, callees, contracts and tests without treating presence as correctness.
---

# NEXY Skill

## Identity
- Formal ID: `CTX-003`
- Name: `nexy-source-inspector`
- Family: CONTEXT
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Inspect real source and identify file, path, type, dependencies, callers, callees, contracts, and tests at the exact observed revision.

## Authority
Source inspection establishes repository facts, not normative authority and not behavioral verification by itself.

## Source of Truth
- Primary skill specification: `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source named by that specification: `NEXY สกิว.pdf`
- Secondary project context named by that specification: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current repository/runtime evidence is required for implementation-state claims.

## Scope
### In Scope
- inspect exact repository files/symbols at a pinned revision;
- identify imports/dependencies, direct callers/callees when evidence permits;
- locate contracts, tests and state/security touchpoints;
- distinguish exact, candidate and unknown mappings.

### Out of Scope
- modifying files;
- claiming behavior works from source presence;
- inventing missing symbols/dependencies;
- replacing runtime evidence.

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
- target_files_or_symbols

### Optional
- implementation map
- dependency graph
- requirement IDs
- contract/invariant IDs

## Preconditions
- exact target repository, branch and HEAD are established by `nexy-context`;
- access is read-only unless another Skill/task separately authorizes mutation.

## Outputs
- status
- inspected_revision
- files
- symbols
- dependencies
- callers
- callees
- contracts
- tests
- state_security_touchpoints
- mapping_certainty
- evidence
- unknowns
- next_action

## Workflow
### Phase 1 — Context
Pin repository, branch and HEAD.

### Phase 2 — Authority
Load only authority needed to know what source area is relevant; do not infer normative meaning from code.

### Phase 3 — Requirement
Resolve requirement/contract/invariant anchors relevant to inspection.

### Phase 4 — Inspection
Read exact files/symbols and traverse only necessary dependency/caller/callee edges.

### Phase 5 — Execution
Produce a source map with certainty labels.

### Phase 6 — Validation
Confirm every exact mapping is evidenced at the pinned HEAD and candidates remain candidates.

### Phase 7 — Evidence
Record repository paths, symbols and revision references.

## Required Behavior
- Pin exact HEAD.
- Separate exact evidence from candidate inference.
- Locate tests/contracts when relevant to downstream modification or audit.

## Forbidden Behavior
- Do not mark code as correct because it exists.
- Do not treat candidate mapping as exact.
- Do not inspect one search result and conclude an entity is missing.
- Do not mutate source.

## Architecture Constraints
Preserve module/contract boundaries and report cross-boundary dependencies for downstream analysis.

## Security Constraints
Do not expose secrets encountered during inspection; redact and stop unsafe propagation.

## Compatibility Constraints
Preserve exact path/symbol identity and distinguish renamed/moved targets.

## Data Integrity
Repository facts must be bound to the exact inspected revision.

## Failure Handling
Return UNKNOWN/PARTIAL when callers/callees/contracts/tests cannot be established from available evidence.

## Freeze Conditions
Wrong/unknown target revision when the inspection will drive mutation; inaccessible critical source; integrity mismatch.

## Validation
### Structural
Output contains revision and source references.

### Functional
Exact mapping claims resolve to real files/symbols at the pinned revision.

### Integration
Output feeds architecture-impact, debug, modify, code-review and audit workflows.

### Regression
HEAD changes invalidate revision-sensitive source facts until refreshed.

### Evidence
Every exact source fact includes path/symbol/revision evidence.

## Completion Criteria
Complete when the requested source surface is inspected sufficiently for the downstream task and unresolved mappings are explicit.

## Stop Conditions
Target identity/HEAD unknown, required source inaccessible, critical integrity mismatch.

## Checkpoint
Persist inspected revision, exact/candidate mappings, unresolved symbols and next source edge.

## Resume
Refresh HEAD; if changed, revalidate revision-sensitive mappings.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Before modifying an API route, identify route file, schema/auth/core calls, contract consumers and related tests at the exact HEAD.

## Non-Goals
This Skill does not prove runtime behavior and does not modify code.

## Version
1.0.0
