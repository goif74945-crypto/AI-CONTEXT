---
name: nexy-conflict-resolution
description: Detect requirement conflict and resolve only through authoritative source; unresolved conflict is BLOCKED.
---

# NEXY Skill

## Identity
- Formal ID: `REQ-004`
- Name: `nexy-conflict-resolution`
- Family: REQUIREMENTS
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Detect requirement conflict and resolve only through authoritative source; unresolved conflict is BLOCKED.

## Authority
Operate only within current authoritative source and task scope. This Skill cannot invent missing requirements, expand permissions, weaken gates, or promote inference into project truth.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current project source, pinned repository state, tests/evidence and control state.

## Scope
### In Scope
conflicting claims, source authority/domain/scope, supersession edges, affected systems and possible resolutions.
### Out of Scope
Resolving by model preference, recency alone, implementation convenience, or silently merging incompatible claims.

## Inputs
Universal inputs plus the exact target/requirement/context needed by this Skill, authoritative constraints, dependencies and available evidence.

## Outputs
Universal outputs plus structured findings/result, proof refs, gaps/risks, validation state and next action.

## Workflow
Detect Conflict → Classify Domain/Scope → Authority/Supersession → Evidence → Resolution or BLOCKED → Record.

## Required Behavior
Only authoritative source/supersession may resolve normative conflict; distinctions are not mislabeled conflicts.

## Forbidden Behavior
Resolving by model preference, recency alone, implementation convenience, or silently merging incompatible claims.

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
Material authority conflict remains unresolved or resolution would require inventing source intent.

## Validation
Use structural, source/spec, functional, security, architecture, integration, regression and evidence validation as applicable.

## Completion Criteria
Conflict is resolved with traceable authority or remains explicitly BLOCKED with affected paths frozen.

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
