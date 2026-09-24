---
name: nexy-determinism
description: Verify NEXY deterministic execution against source-defined requirements and explicitly identify authorized nondeterministic exceptions.
---

# NEXY Skill

## Identity
- Formal ID: `CORE-005`
- Name: `nexy-determinism`
- Family: CORE
- Version: `1.0.0`
- Status: `MATERIALIZED`

## Objective
Verify deterministic execution according to requirements.

## Authority
Determinism requirements come from authoritative source; this Skill cannot invent universal determinism constraints or exceptions.

## Source of Truth
- `skills/nexy/MASTER-SPECIFICATION.md`
- `NEXY สกิว.pdf`
- `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Exact current source/runtime/test evidence.

## Scope
### In Scope
Time/randomness/order/concurrency/environment/float/fallback sources relevant to required deterministic paths; reproducibility and exception mapping.
### Out of Scope
Declaring all time/random use defective without source; inventing thresholds.

## Inputs
Universal inputs plus deterministic requirement, target path, allowed exceptions and execution evidence.

## Outputs
Universal outputs plus nondeterminism inventory, exception mapping, reproducibility result, risks, tests/evidence.

## Workflow
Context → Authority → Determinism Requirement → Source Scan/Runtime Repetition → Exception Check → Verdict → Evidence.

## Required Behavior
Distinguish required deterministic path from allowed nondeterministic rendering/telemetry or other source-defined exceptions.

## Forbidden Behavior
No unsupported “bit-exact” claims, no fake reproducibility, no treating unordered behavior as deterministic without proof.

## Architecture Constraints
Critical decision/state/release paths receive stricter analysis than non-authoritative presentation paths.

## Security Constraints
Randomness used for security is not replaced by deterministic values unless source explicitly requires another mechanism.

## Compatibility Constraints
Determinism fixes must preserve APIs/state semantics.

## Data Integrity
Ordering/idempotency/concurrency effects on authoritative state are in scope.

## Failure Handling
Unresolved nondeterminism in critical required path => FAIL/BLOCKED.

## Freeze Conditions
Critical release/state result depends on prohibited nondeterminism or cannot be reproduced with required confidence/evidence.

## Validation
Static search plus repeated/golden/race tests as applicable and source-defined exception evidence.

## Completion Criteria
All applicable nondeterminism sources are classified and required deterministic behavior is proven or explicitly not verified.

## Stop Conditions
Requirement/exception source missing or runtime proof unavailable for a required completion claim.

## Checkpoint
Persist target, sources, exceptions, tests and verdict.

## Resume
Refresh code/config/environment and rerun affected reproducibility evidence.

## Error Reporting
Return ERROR, LOCATION, IMPACT, proven ROOT_CAUSE when available, RECOVERY and CURRENT_STATUS.

## Examples
- Date.now in logging is not automatically a deterministic-core defect if source scopes determinism to decision outputs.

## Non-Goals
This Skill does not remove all randomness/time globally.

## Version
1.0.0
