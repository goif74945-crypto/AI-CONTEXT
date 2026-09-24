---
name: nexy-agent-failure
description: Handle timeout, error, invalid output, contradiction, and missing evidence.
---

# NEXY Skill

## Identity
- Formal ID: `AI-006`
- Name: `nexy-agent-failure`
- Family: AI / SWARM
- Version: `1.0.0`
- Status: `MATERIALIZED`


## Objective
Handle timeout, error, invalid output, contradiction, and missing evidence.

## Authority
Operate only within current authoritative source and task scope. This Skill cannot invent missing requirements, expand permissions, weaken gates, or promote inference into project truth.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Applicable current project source, pinned repository state, tests/evidence and control state.

## Scope
### In Scope
agent execution failure classes, timeout, schema/invalid output, contradiction, missing evidence, retry/freeze policy, audit/result propagation.
### Out of Scope
Converting failure to success, endless retry, accepting malformed output, hiding contradiction, or fabricating evidence.

## Inputs
Universal inputs plus the exact target/requirement/context needed by this Skill, authoritative constraints, dependencies and available evidence.

## Outputs
Universal outputs plus structured findings/result, proof refs, gaps/risks, validation state and next action.

## Workflow
Context → Agent Contract → Detect Failure Class → Validate Evidence/Schema → Apply Contract Failure/Retry/Freeze Rule → Propagate Result → Evidence.

## Required Behavior
Failure semantics are deterministic, bounded and traceable; unresolved critical output/evidence issues do not enter consensus as valid.

## Forbidden Behavior
Converting failure to success, endless retry, accepting malformed output, hiding contradiction, or fabricating evidence.

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
Critical failure rule unavailable, retry authority ambiguous, contradiction/evidence gap can contaminate release, or stale run state.

## Validation
Use structural, source/spec, functional, security, architecture, integration, regression and evidence validation as applicable.

## Completion Criteria
Agent failure is correctly classified, propagated and evidenced without false success or hidden invalid output.

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
