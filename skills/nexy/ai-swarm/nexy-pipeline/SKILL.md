---
name: nexy-pipeline
description: Control the end-to-end NEXY execution pipeline while obeying source-defined timeouts, state, authority, agent, evidence, consensus, judge, law and freeze requirements.
---

# NEXY Skill

## Identity
- Formal ID: `AI-007`
- Name: `nexy-pipeline`
- Family: AI / SWARM
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Control end-to-end execution and obey specification-defined timeouts.

## Authority
Pipeline orchestration cannot bypass authority, state, JUDGE, LAW, security or release gates.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current pipeline/FSM/config/contracts at pinned HEAD.

## Scope
### In Scope
Stage ordering, state transitions, timeout/failure policy, agent/swarm invocation, verification/consensus handoff, judge/law handoff, evidence and terminal status.
### Out of Scope
Invented timeout values, bypassing stages, final release without gate.

## Inputs
Universal inputs plus directive/task, pipeline state, config/timeouts, agent/swarm policy, verification/judge/law contracts.

## Outputs
Universal outputs plus stage states, timings/timeout results where applicable, candidate/evidence, failure/freeze state and downstream handoff.

## Workflow
Context → Authority → Pipeline Contract → State/Stage Execution → Agent/SWARM → Verify/Consensus → JUDGE/LAW Handoff → Terminal State/Evidence.

## Required Behavior
Obey source-defined stage order and timeouts; no stage success without required predecessor evidence.

## Forbidden Behavior
No hidden retries, invented timeout, state skipping, fake progress or direct final output from worker/model.

## Architecture Constraints
Pipeline coordinates boundaries but does not absorb their authority.

## Security Constraints
Every tool/agent/API boundary remains zero-trust and permission-scoped.

## Compatibility Constraints
Stage contracts/state/event versions remain compatible.

## Data Integrity
Pipeline state must persist/recover according to authoritative ownership; restart is not continue.

## Failure Handling
Stage timeout/error/invalid evidence/consensus/law failure routes to explicit failure/FREEZE/recovery policy.

## Freeze Conditions
Critical agent failure, consensus failure, policy/security violation, insufficient evidence, invalid state or timeout when source requires freeze.

## Validation
Stage-order, timeout, failure, replay/idempotency, restart/recovery, integration and regression tests.

## Completion Criteria
Pipeline run is complete only at a legal terminal state with required evidence; successful SWARM alone is not completion.

## Stop Conditions
Unknown required timeout/stage contract, illegal state, missing authority or critical dependency.

## Checkpoint
Persist pipeline/run IDs, state, stage evidence, failures and next legal action.

## Resume
Reload authoritative persisted pipeline state and verify recovery gate.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A worker restart does not justify continuing from an in-memory “VERIFYING” stage without persisted authoritative state.

## Non-Goals
This Skill does not self-approve release.

## Version
1.0.0
