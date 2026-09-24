---
name: nexy-repository-context
description: Inspect repository, branch, HEAD, working state, and relevant tree before code changes.
---

# NEXY Skill

## Identity
- Formal ID: `CTX-002`
- Name: `nexy-repository-context`
- Family: CONTEXT
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Inspect repository, branch, HEAD, working state, and relevant tree before code changes.

## Authority
Operate only within current authoritative source and task scope. This Skill cannot invent missing requirements, expand permissions, weaken gates, or promote inference into project truth.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current project source, pinned repository state, tests/evidence and control state.

## Scope
### In Scope
repository identity, branch/ref, exact HEAD, relevant paths/tree, working state where accessible, diff/base relationships and freshness.
### Out of Scope
Assuming a branch, auditing a moving target without pinning, inventing working-tree state, or using stale repository context.

## Inputs
Universal inputs plus the exact target/requirement/context needed by this Skill, authoritative constraints, dependencies and available evidence.

## Outputs
Universal outputs plus structured findings/result, proof refs, gaps/risks, validation state and next action.

## Workflow
Resolve Repo → Discover Branch/Ref → Pin HEAD → Inspect Relevant Tree/History → Record Context/Freshness.

## Required Behavior
Current-state claims must bind to exact repository/ref/HEAD; unavailable working state is reported UNKNOWN rather than guessed.

## Forbidden Behavior
Assuming a branch, auditing a moving target without pinning, inventing working-tree state, or using stale repository context.

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
Repository/ref unavailable, HEAD cannot be established, or stale context materially affects the requested action.

## Validation
Use structural, source/spec, functional, security, architecture, integration, regression and evidence validation as applicable.

## Completion Criteria
Repository context is pinned, traceable and sufficient for the next authorized operation.

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
