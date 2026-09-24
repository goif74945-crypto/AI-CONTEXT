---
name: nexy-agent-adapter
description: Connect an AI provider or model to the canonical NEXY agent interface while preserving schema, timeout, error, provenance, security and provider-isolation boundaries.
---

# NEXY Skill

## Identity
- Formal ID: `AI-002`
- Name: `nexy-agent-adapter`
- Family: AI / SWARM
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Connect an agent to the canonical interface.

## Authority
Adapter code translates provider behavior; it cannot grant provider-specific authority or redefine canonical contracts.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Exact provider adapter and canonical interface at pinned HEAD.

## Scope
### In Scope
Request translation, response normalization, provider errors/timeouts, provenance, capability limits, tests/evidence.
### Out of Scope
Provider selection without authority, secret disclosure, canonical contract widening by convenience.

## Inputs
Universal inputs plus canonical agent contract, provider/model config, tool/capability policy and secret-reference mechanism.

## Outputs
Universal outputs plus normalized request/response mapping, provider error map, provenance and tests/evidence.

## Workflow
Context → Authority → Canonical Contract → Inspect Provider Adapter → Map/Validate → Negative/Timeout Tests → Evidence.

## Required Behavior
Provider-specific details stay behind adapter; canonical output is validated before entering SWARM.

## Forbidden Behavior
No raw secrets in logs; no provider-specific fields smuggled into authoritative contract; no fallback provider invention.

## Architecture Constraints
Adapter boundary isolates provider from Core/Law/state.

## Security Constraints
Server-side secret handling, tool permission limits and untrusted output validation.

## Compatibility Constraints
Provider changes must preserve canonical agent interface.

## Data Integrity
Provider metadata is provenance, not authoritative data unless explicitly governed.

## Failure Handling
Provider timeout/error/schema mismatch becomes explicit agent failure.

## Freeze Conditions
Secret exposure, capability/permission escalation, incompatible canonical mapping, unknown critical provider behavior.

## Validation
Schema mapping, timeout/error, secret/logging negative tests, integration with agent/swarm and regression.

## Completion Criteria
Adapter conforms to canonical interface with proven failure/security behavior.

## Stop Conditions
Missing canonical contract, unavailable provider mechanism, security unknown or unauthorized provider.

## Checkpoint
Persist adapter/provider identity, contract version, capability/security mapping and evidence.

## Resume
Refresh provider/canonical versions before reuse.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Provider-specific confidence cannot become canonical trust score unless the contract explicitly defines that mapping.

## Non-Goals
This Skill does not choose final result or release.

## Version
1.0.0
