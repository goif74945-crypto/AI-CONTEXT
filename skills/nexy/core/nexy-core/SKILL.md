---
name: nexy-core
description: Work with NEXY core-kernel while preserving core law, authority, state ownership, contracts, determinism and evidence requirements.
---

# NEXY Skill

## Identity
- Formal ID: `CORE-001`
- Name: `nexy-core`
- Family: CORE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Work with the core-kernel without bypassing core law, authority, state, contracts or verification.

## Authority
Core work is subordinate to current authority/law and protected mutation gates. This Skill cannot redefine system law or approve release.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- Primary underlying source: `NEXY สกิว.pdf`
- Secondary project context: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current core implementation/state requires exact repository/branch/HEAD evidence.

## Scope
### In Scope
Core logic, legal execution boundaries, state transition integration, contract enforcement, determinism, error/freeze behavior, tests/evidence.
### Out of Scope
UI concerns, unauthorized state bypass, hidden persistence, unapproved law changes, release approval.

## Inputs
Universal inputs plus core requirement, state/FSM, contracts, law/policy, architecture and evidence.

## Outputs
Universal outputs plus core boundary map, authority checks, state/contract impacts, tests/evidence.

## Workflow
Context → Authority/Law → Requirement → Core/State/Contract Inspection → Authorized Change/Analysis → Validation → Evidence.

## Required Behavior
Preserve legal execution order, explicit errors, state ownership, deterministic requirements and auditability.

## Forbidden Behavior
No bypass of LAW/JUDGE/state guards, no hidden fallback, no fake success, no silent persistence.

## Architecture Constraints
Core remains within canonical ownership boundaries and does not absorb unrelated UI/API authority.

## Security Constraints
Input trust, authz, secret handling, audit and protected actions remain enforced.

## Compatibility Constraints
Preserve public/internal core contracts and state semantics unless explicitly authorized.

## Data Integrity
Authoritative state writes require declared owner and durable/transactional behavior as applicable.

## Failure Handling
Fail closed on critical contract/state/law violation; propagate explicit governed error/FREEZE.

## Freeze Conditions
Authority/law conflict, illegal state transition, security/data-integrity risk, insufficient evidence or stale target.

## Validation
Core unit/contract/state/security/integration/regression evidence as applicable.

## Completion Criteria
Core work is complete only when law/state/contracts and required evidence all hold.

## Stop Conditions
Unknown critical law/state/contract, forbidden path, human gate or stale HEAD.

## Checkpoint
Persist target revision, state/law/contract context, actions, validation and evidence.

## Resume
Refresh current law/state/contracts/HEAD.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A core helper cannot directly force STABLE if the state machine requires JUDGE/LAW gates.

## Non-Goals
This Skill does not approve release or bypass governing layers.

## Version
1.0.0
