---
name: nexy-adversarial
description: Challenge NEXY candidate outputs with counter-evidence, contradiction, edge cases and attack hypotheses before consensus or verification.
---

# NEXY Skill

## Identity
- Formal ID: `AI-005`
- Name: `nexy-adversarial`
- Family: AI / SWARM
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Check counter-evidence and contradiction.

## Authority
Adversarial review challenges claims but cannot invent facts, change requirements or self-authorize mutation.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Candidate/evidence/current source state.

## Scope
### In Scope
Counterexamples, contradiction search, negative cases, assumption attack, evidence-quality challenge, failure-mode probing.
### Out of Scope
Fabricated attacks/evidence, denial-of-service style uncontrolled testing, mutation without authority.

## Inputs
Universal inputs plus candidate, claims, evidence, constraints and threat/failure context.

## Outputs
Universal outputs plus challenged_claims, counter_evidence, contradictions, surviving_claims, unresolved risks and next verification.

## Workflow
Context → Authority → Claim Decomposition → Counter-Evidence Search → Negative/Edge Attack → Reconcile → Evidence.

## Required Behavior
Attack high-risk claims first; distinguish disproven, weakened, surviving and unknown claims.

## Forbidden Behavior
No manufactured contradiction; no changing acceptance criteria; no hiding surviving counter-evidence.

## Architecture Constraints
Cross-system claims are attacked at their actual boundaries/contracts.

## Security Constraints
Security claims receive abuse/privilege/injection/secret/tenant attack consideration as applicable.

## Compatibility Constraints
Attack semantic regressions, not only syntax.

## Data Integrity
Include replay/race/rollback/corruption hypotheses where data/state is affected.

## Failure Handling
If evidence cannot settle contradiction, output UNKNOWN/CONFLICT.

## Freeze Conditions
Critical contradiction, security/data-integrity risk or unsupported completion claim.

## Validation
Known-good/known-bad examples, reproducible counterexample checks and integration with consensus/verify.

## Completion Criteria
Material claims have been challenged and unresolved critical contradictions are explicit.

## Stop Conditions
Evidence source unavailable or attack requires unsafe/destructive operation without authority.

## Checkpoint
Persist claims, attacks, counter-evidence and unresolved items.

## Resume
Refresh candidate/evidence before reuse.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A passing happy-path test is challenged with unauthorized, malformed, replay and failure-path cases when applicable.

## Non-Goals
This Skill does not decide final release.

## Version
1.0.0
