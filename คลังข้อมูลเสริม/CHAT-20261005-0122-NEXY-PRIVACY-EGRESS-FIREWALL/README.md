# NEXY Purpose-Bound Privacy & Context Egress Firewall Lab (NPCEF)

**Status:** AI-PROPOSED / NON-GOVERNING / REFERENCE PROTOTYPE

NPCEF explores a deterministic boundary between trusted NEXY/Vault context and any outbound recipient such as an external model, connector, export surface, or a trusted local component. Its job is not to decide whether a task is useful. Its job is narrower: compile the smallest context payload that is permitted for a declared purpose and recipient, or fail closed with a machine-readable decision.

## Why this exists

Agentic systems can have perfect task routing and still leak too much context. A generic “connector allowed” bit is not enough because the same datum may be appropriate for one purpose, recipient, and time window but forbidden for another. NPCEF therefore makes egress authority explicit at datum and field granularity.

## Core decision states

- `ALLOW` — every included datum is currently permitted and no minimization changed the payload.
- `REDACT` — optional data or fields were removed; the reduced payload may proceed.
- `ASK` — a required datum needs an explicit, purpose/recipient-bound consent grant.
- `BLOCK` — a required datum cannot legally satisfy the request under the active policy.
- `FREEZE` — request/policy metadata is malformed or contradictory enough that evaluation cannot safely continue.

## Reference invariants

1. Same normalized request + same policy => same action, payload structure, and receipt digest.
2. Data not needed for the declared purpose is excluded.
3. Sensitive+ data requires explicit recipient binding by default.
4. Sensitive+ external egress requires a valid purpose/recipient/item/time-bound grant by default.
5. Secret data never leaves to a non-local recipient under the default policy.
6. Terminal states `ASK`, `BLOCK`, and `FREEZE` release no payload.
7. Audit receipts contain IDs/reason metadata, never raw values.
8. Malformed policy metadata fails closed.

## What this prototype is not

It is not a legal-compliance engine, a DLP replacement, a secrets scanner, a complete consent-management platform, or proof that NEXY.AI currently implements these controls. The word `consent` here means an application-level release grant. Production adoption would require legal-basis mapping, identity/authentication, policy administration, storage semantics, connector attestations, revocation propagation, nested/streaming data handling, runtime telemetry, and independent security review.

## Verification scope

The lab targets E0/E1/E2 evidence for the reference code only: repository presence/read-back, static compilation/JSON parsing, unit/adversarial tests, and a bounded deterministic property audit. No E3-E6 NEXY runtime/deployment claim is made.

Start with `01_TASK_CONTRACT.md`, then `03_ARCHITECTURE.md`, `04_REQUIREMENT_LEDGER.md`, and `05_POLICY_AND_STATE_MODEL.md`.
