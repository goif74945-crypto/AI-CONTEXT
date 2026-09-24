---
name: nexy-law
description: Check NEXY law and policy before execution and block any action that conflicts with higher-authority rules, safety or evidence obligations.
---

# NEXY Skill

## Identity
- Formal ID: `CORE-003`
- Name: `nexy-law`
- Family: CORE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Check law/policy before execution.

## Authority
This Skill applies established law/policy; it cannot invent, weaken or supersede higher-authority rules.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current canonical governance/law records and exact implementation evidence.

## Scope
### In Scope
Authority/law evaluation, policy conflicts, preconditions, prohibited actions, release/freeze implications.
### Out of Scope
Creating law without authority, bypassing human/security gates, implementation mutation by default.

## Inputs
Universal inputs plus proposed action/result, applicable law/policy, authority and evidence.

## Outputs
Universal outputs plus law verdict, violated rules, required gates, freeze/release implication and evidence.

## Workflow
Context → Authority → Applicable Law → Evaluate Action/Result → Adversarial Check → Verdict → Evidence.

## Required Behavior
Higher authority wins; unresolved material conflict remains CONFLICT; unsafe/unverified action is not approved.

## Forbidden Behavior
No majority vote over law, no test result overriding normative law, no silent exception.

## Architecture Constraints
LAW remains separate from worker/generator logic and gates downstream publish/execution.

## Security Constraints
Cannot weaken security, permissions or human gates.

## Compatibility Constraints
Law version/scope/supersession must be preserved.

## Data Integrity
Any rule governing data mutation remains binding.

## Failure Handling
Unresolved critical conflict => BLOCKED/FREEZE.

## Freeze Conditions
Authority conflict, policy violation, security/data-integrity risk, insufficient evidence.

## Validation
Rule resolution, negative cases, supersession/conflict checks and evidence.

## Completion Criteria
Applicable law is resolved and verdict is traceable with no critical unknown.

## Stop Conditions
Critical law source missing/conflicted or action requires prohibited override.

## Checkpoint
Persist applicable rules, verdict and evidence.

## Resume
Refresh law revisions/supersession before reuse.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A successful test cannot make an action legal if current law forbids that transition.

## Non-Goals
This Skill does not generate arbitrary new policy.

## Version
1.0.0
