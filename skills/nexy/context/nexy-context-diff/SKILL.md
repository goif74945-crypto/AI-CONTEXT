---
name: nexy-context-diff
description: Compare previous/current/expected state to prevent stale context.
---

# NEXY Skill

## Identity
- Formal ID: `CTX-004`
- Name: `nexy-context-diff`
- Family: CONTEXT
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Compare previous/current/expected state to prevent stale context.

## Authority
Operate only within current authoritative source and task scope. This Skill cannot invent missing requirements, expand permissions, weaken gates, or promote inference into project truth.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current project source, pinned repository state, tests/evidence and control state.

## Scope
### In Scope
previous checkpoint, current source/repo/control state, expected state, semantic differences, freshness and downstream impact.
### Out of Scope
Treating unchanged filenames as unchanged semantics, ignoring new authority, or carrying stale assumptions forward.

## Inputs
Universal inputs plus the exact target/requirement/context needed by this Skill, authoritative constraints, dependencies and available evidence.

## Outputs
Universal outputs plus structured findings/result, proof refs, gaps/risks, validation state and next action.

## Workflow
Load Previous → Load Current → Load Expected → Semantic Diff → Impact → Stale/Conflict Classification → Checkpoint.

## Required Behavior
Material drift is surfaced before action; stale claims are invalidated or re-proven.

## Forbidden Behavior
Treating unchanged filenames as unchanged semantics, ignoring new authority, or carrying stale assumptions forward.

## Architecture Constraints
Respect declared layers, contracts, state ownership, dependency direction and source authority; do not create hidden bypasses.

## Security Constraints
Validate applicable trust boundaries, permissions, secret handling and unsafe side effects; fail closed on critical uncertainty.

## Compatibility Constraints
Assess contract/version/consumer/data compatibility when the task can affect them.

## Data Integrity
Preserve authoritative data/state/provenance and do not mutate or reinterpret protected state without explicit authority.

## Failure Handling
Failure, unknown, conflict, missing proof or unavailable dependency remains explicit; no fabricated fallback success.

## Freeze Conditions
Diff source missing, authority changed ambiguously, or critical expected/current mismatch cannot be reconciled.

## Validation
Use structural, source/spec, functional, security, architecture, integration, regression and evidence validation as applicable.

## Completion Criteria
Relevant previous/current/expected state differences and their impact are explicitly recorded.

## Stop Conditions
Stale target, material authority/scope conflict, missing critical proof, unsafe mutation, required human gate or unresolved dependency that affects correctness.

## Checkpoint
Persist exact target/version, inputs, claims/proofs, decisions, validation state, unresolved gaps and resume point.

## Resume
Refresh source authority, target state and evidence freshness before continuing.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Presence or naming similarity alone is never sufficient proof of implementation or compliance.

## Non-Goals
This Skill does not self-approve unsupported completion.

## Version
1.0.0
