---
name: nexy-consensus
description: Evaluate NEXY consensus from explicit agent evidence, contradictions and source-defined quorum/trust rules without inventing agreement metrics.
---

# NEXY Skill

## Identity
- Formal ID: `AI-004`
- Name: `nexy-consensus`
- Family: AI / SWARM
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Evaluate consensus.

## Authority
Consensus is a candidate-evaluation stage and does not supersede JUDGE/LAW.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current consensus/quorum contracts/config at pinned HEAD.

## Scope
### In Scope
Agreement/contradiction evidence, source-defined quorum/trust thresholds, critical-agent failures, consensus hash/result structure.
### Out of Scope
Invented thresholds, majority-vote truth by default, release approval.

## Inputs
Universal inputs plus agent results, adversarial/cross-verification output, consensus policy and evidence.

## Outputs
Universal outputs plus consensus_status, supporting/opposing evidence, quorum status, critical failures, candidate and unknowns.

## Workflow
Context → Authority → Consensus Policy → Normalize Agent Evidence → Evaluate Agreement/Contradiction/Quorum → Candidate Verdict → Evidence.

## Required Behavior
Use only source-defined metrics/thresholds; unresolved contradiction remains visible.

## Forbidden Behavior
No fabricated consensus score/hash/quorum; no dropping dissenting evidence to pass.

## Architecture Constraints
Consensus output remains input to downstream judge/law.

## Security Constraints
Untrusted/model-derived claims cannot bypass evidence/security gates through consensus.

## Compatibility Constraints
Consensus result must satisfy canonical contract version.

## Data Integrity
Any persisted consensus artifact preserves provenance and participant results.

## Failure Handling
Quorum not met, contradiction or critical failure remains explicit.

## Freeze Conditions
Consensus failure where policy requires FREEZE, critical evidence conflict or unknown mandatory threshold.

## Validation
Golden disagreement/agreement, missing quorum, critical-agent failure and regression cases.

## Completion Criteria
Consensus evaluation is complete when policy result and all material support/opposition are traceable.

## Stop Conditions
Consensus policy missing/ambiguous or evidence set incomplete in a critical way.

## Checkpoint
Persist policy version, participants, evidence, contradictions and result.

## Resume
Refresh participant results/policy before recomputation.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- “3 of 5 agree” is not sufficient unless source defines that as legal quorum/consensus.

## Non-Goals
This Skill does not release output.

## Version
1.0.0
