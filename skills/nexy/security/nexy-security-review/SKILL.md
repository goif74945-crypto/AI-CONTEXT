---
name: nexy-security-review
description: Review NEXY authentication, authorization, input, data, dependencies, secrets and logging for evidence-backed security defects and proof gaps.
---

# NEXY Skill

## Identity
- Formal ID: `SEC-005`
- Name: `nexy-security-review`
- Family: SECURITY
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Review authentication, authorization, input, data, dependencies, secrets and logging.

## Authority
Review is read/adversarial by default and cannot mutate or waive security requirements.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Exact target code/config/tests/evidence.

## Scope
### In Scope
Auth/session/RBAC, validation, data/tenant, dependency/supply-chain, secret/logging, abuse/injection/replay and audit controls.
### Out of Scope
Unsupported vulnerability claims, destructive exploitation, remediation mutation unless separately authorized.

## Inputs
Universal inputs plus review target, threat model and governing security requirements.

## Outputs
Universal outputs plus findings, severity, source/claim/proof, affected boundaries, test/evidence gaps and recommended action class.

## Workflow
Context → Authority → Threat/Requirement → Static/Behavioral Review → Adversarial Cases → Validate Findings → Evidence.

## Required Behavior
High-risk claims first; prove exploit/control gap where practical/safe; distinguish defect/risk/unknown.

## Forbidden Behavior
No secret copying, no exploit beyond authorized scope, no fake CVE/severity/proof.

## Architecture Constraints
Review actual trust boundaries and owners.

## Security Constraints
Review itself uses least privilege and safe/redacted evidence.

## Compatibility Constraints
Remediation recommendations identify compatibility impact.

## Data Integrity
Include unauthorized mutation, replay, corruption/isolation impact as applicable.

## Failure Handling
Missing behavioral proof keeps claim at appropriate static/risk level.

## Freeze Conditions
S5-like integrity/security defect requiring containment or unsafe review path.

## Validation
Reproducibility, negative tests, source proof and evidence freshness.

## Completion Criteria
Requested surface reviewed with traceable findings and explicit proof gaps.

## Stop Conditions
Unsafe/destructive test, secret exposure or insufficient target identity.

## Checkpoint
Persist sanitized finding/evidence records.

## Resume
Refresh target and re-test stale findings.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A plaintext one-time code written to stderr is a proven secret exposure when source and reachable configuration path are established.

## Non-Goals
This Skill does not self-approve fixes/releases.

## Version
1.0.0
