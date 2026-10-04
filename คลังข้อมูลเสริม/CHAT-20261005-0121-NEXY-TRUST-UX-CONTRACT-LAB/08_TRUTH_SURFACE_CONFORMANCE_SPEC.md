# Truth Surface Conformance Model Checker

**Classification:** AI-PROPOSED / advisory verification system.

## Objective

Provide a deterministic executable gate that can answer a narrow question:

> Given authoritative backend state and a machine-readable description of what the UI rendered, did the presentation preserve truth and authority boundaries?

This is verification, not rendering and not authorization.

## Inputs

### Backend truth
Required:
- `status`
- `state`
- `request_id`
- `trace_id`

Optional relevant fields:
- `data.accepted`
- `data.releaseable`
- `data.integrity_hash`
- `freeze.recoverable`

### Surface manifest
Required proposal fields:
- `displayed_status`
- `displayed_state`
- `headline`
- `summary`
- `result_visible`
- `result`
- `actions[]`
- `request_id`
- `trace_id`

Each action declares:
- `id`
- `kind` = `READ` or `MUTATION_REQUEST`
- `requires_backend_authorization`
- optional `requires_confirmation`

### Role
One of:
- OWNER
- OPERATOR
- AUDITOR
- SYSTEM
- PUBLIC_USER

## Core invariants

### TS-001 Status fidelity
Rendered status must equal authoritative backend status.

### TS-002 State fidelity
Rendered state must equal authoritative backend state.

### TS-003 Request identity binding
Rendered request ID must match backend request ID.

### TS-004 Trace identity binding
Rendered trace ID must match backend trace ID.

### TS-005 FREEZE result suppression
FREEZE must not expose stale/candidate/final result payloads.

### TS-006 FREEZE semantic honesty
FREEZE copy must not imply success/completion.

### TS-007 Recover visibility
Recover may be surfaced only for OWNER when authoritative freeze metadata says recoverable=true.

### TS-008 STOP mutation suppression
STOP must expose no ordinary mutation CTA.

### TS-009 STOP semantic honesty
STOP copy must not imply ordinary retry/recover behavior.

### TS-010 Pending result suppression
INIT/RUNNING/VERIFYING/CONSENSUS must not expose final result.

### TS-011 Pending semantic honesty
Pending states must not use success/completion copy.

### TS-012 Pending mutation suppression
Pending run surfaces must not expose a second mutation request through the same truth card.

### TS-013 Release-proof gate
STABLE alone is insufficient to display final result. The proposal checker requires accepted=true, releaseable=true and non-empty integrity_hash in the supplied backend envelope.

This is a presentation verification heuristic and does not replace full DOC-C release policy.

### TS-014 Read-only role boundary
AUDITOR/PUBLIC_USER must not receive a mutation CTA on READY from this truth surface.

### TS-015 Backend authorization annotation
Every mutation CTA must explicitly remain backend-authorized.

### TS-016 Recover confirmation
Recover CTA must require explicit confirmation in this proposal.

## Failure model

Malformed critical enums/fields do not become a warning. The checker raises `ConformanceInputError` and fails closed.

A valid but nonconformant surface yields deterministic violations rather than guessing a repair.

## Output

`AuditReport`:
- conformance boolean;
- exact violation list;
- authoritative IDs/status/state/role;
- SHA-256 certificate fingerprint.

The fingerprint binds the normalized report. It is not a cryptographic signature and proves no authenticity by itself.

## Determinism

The checker uses no clock, RNG, network, model call or external dependency. Same normalized backend + same surface + same role -> same report/fingerprint.

## Intended future use

Potential CI flow:

`backend contract fixture -> real renderer adapter -> surface manifest -> checker -> PASS/FAIL`

Promotion would require explicit mapping to the actual frontend component tree, current authorization contracts, accessibility surface and localization behavior.
