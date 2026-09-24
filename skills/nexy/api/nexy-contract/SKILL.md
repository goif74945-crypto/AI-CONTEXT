---
name: nexy-contract
description: Manage NEXY API and cross-module contracts by inspecting producers and consumers before any schema, error, version or compatibility change.
---

# NEXY Skill

## Identity
- Formal ID: `API-002`
- Name: `nexy-contract`
- Family: API
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Manage API contracts and inspect consumers before changing a contract.

## Authority
Contract changes require explicit requirement/scope authority; this Skill cannot silently redefine producer/consumer obligations.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Exact schema/producer/consumer implementation at pinned revision.

## Scope
### In Scope
Request/response/error/event/cross-module contract identity, version, required fields, producers, consumers, compatibility, tests/evidence.
### Out of Scope
Unrelated business logic, invented schema fields, consumer breakage hidden as implementation detail.

## Inputs
Universal inputs plus contract target and known producer/consumer set.

## Outputs
Universal outputs plus contract model, version, producer/consumer map, compatibility verdict, migration needs, tests/evidence.

## Workflow
Context → Authority → Requirement → Inspect Contract + All Relevant Consumers → Compare Change → Validate Compatibility → Evidence.

## Required Behavior
- Inspect consumers before change.
- Preserve required fields/version/error semantics unless authorized.
- Treat unknown consumer set as risk/UNKNOWN, not safe.
- Distinguish additive/compatible/breaking based on actual consumers/source.

## Forbidden Behavior
- No schema widening/narrowing by convenience.
- No version change without traceability.
- No treating compile success as consumer compatibility proof.
- No silent error-contract change.

## Architecture Constraints
Producer/consumer ownership and boundary must remain explicit.

## Security Constraints
Contracts must not expose secrets or unauthorized fields and must preserve auth/error disclosure policy.

## Compatibility Constraints
Breaking change requires explicit migration/version strategy and affected-consumer evidence.

## Data Integrity
Storage/event contract changes require persistence/migration impact analysis as applicable.

## Failure Handling
Unresolved consumer or version conflict => BLOCKED/PARTIAL.

## Freeze Conditions
Unknown critical consumer, security-sensitive contract ambiguity, destructive/breaking change without authority, stale revision.

## Validation
Schema/contract tests, producer/consumer integration, negative/error cases and regression.

## Completion Criteria
Contract is explicit, source-backed, consumer-aware and evidence-validated.

## Stop Conditions
Consumer set/source/version cannot be established or change requires unapproved migration.

## Checkpoint
Persist contract/version, producer/consumer map, compatibility result and evidence.

## Resume
Refresh all relevant consumers and contract revision.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Adding a required response field may be breaking if a strict consumer rejects unknown/changed shape; verify actual consumers.

## Non-Goals
This Skill does not independently implement every producer/consumer change.

## Version
1.0.0
