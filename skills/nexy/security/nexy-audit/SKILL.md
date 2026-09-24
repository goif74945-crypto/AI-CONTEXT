---
name: nexy-audit
description: Create and verify NEXY audit events so critical actions, state changes, security decisions and failures are traceable without secrets or fabricated records.
---

# NEXY Skill

## Identity
- Formal ID: `SEC-006`
- Name: `nexy-audit`
- Family: SECURITY
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Create/verify audit events.

## Authority
Audit records describe actions/results; they cannot retroactively legalize an unauthorized action or fabricate proof.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Current audit/event/storage contract at pinned HEAD.

## Scope
### In Scope
Required event fields, actor/action/resource/result, state/security/freeze/recovery events, persistence/integrity/access and tests.
### Out of Scope
Plaintext secrets/PII beyond need, mutable/fake historical records, optional telemetry substitution for mandatory audit.

## Inputs
Universal inputs plus auditable action/event, actor/context/result and audit contract.

## Outputs
Universal outputs plus audit_record/reference, persistence status, integrity/access status and evidence.

## Workflow
Context → Authority → Audit Obligation → Validate Event → Persist Through Owner → Verify → Evidence.

## Required Behavior
Mandatory audit failure remains visible; records are traceable and sanitized.

## Forbidden Behavior
No fabricated record, no secret logging, no warning-only downgrade of mandatory audit.

## Architecture Constraints
Use canonical audit/event persistence owner.

## Security Constraints
Audit access/integrity and sensitive-field minimization.

## Compatibility Constraints
Event schema/version consumers preserved.

## Data Integrity
Immutability/append-only semantics honored when required.

## Failure Handling
Mandatory audit persistence failure blocks/fails the associated legal operation as required.

## Freeze Conditions
Critical action lacks mandatory audit evidence or audit integrity is compromised.

## Validation
Schema, persistence, negative secret leakage, required event ordering/integration and regression.

## Completion Criteria
Required audit event exists durably as applicable and is verified without sensitive leakage.

## Stop Conditions
Audit contract/owner unknown or unsafe sensitive recording.

## Checkpoint
Persist event ID/schema/version/status/evidence.

## Resume
Re-read durable audit state.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- A FREEZE transition that requires incident + audit cannot be called complete if audit persistence failed.

## Non-Goals
This Skill does not replace observability telemetry.

## Version
1.0.0
