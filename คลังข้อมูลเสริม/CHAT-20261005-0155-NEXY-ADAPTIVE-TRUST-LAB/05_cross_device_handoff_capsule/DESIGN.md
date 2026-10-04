# CDHC — Cross-Device Minimal Handoff Capsule

**Status:** AI_PROPOSAL / NON_GOVERNING

## Objective
Allow a verified NEXY task to move between devices/agents without shipping the whole conversation or relying on vague memory. The capsule carries only resumability-critical fields, expires, binds to a target identity string, and detects tampering using HMAC-SHA256.

## Separation from generic handoff protocol
The existing protocol defines *what a good handoff must contain*. CDHC is a concrete minimal authenticated envelope for transport. It intentionally does not solve device attestation, shared-secret distribution, or production key rotation.

## Allowed payload
`objective`, `authority_sources`, `verified_state`, `completed`, `unknowns`, `next_action`, `evidence_refs`, `rollback_data`.

Keys suggesting secrets (`password`, `token`, `cookie`, `secret`, `api_key`, `private_key`, etc.) are recursively removed from payload values before signing.

## Invariants
- secret key is caller-supplied and never serialized;
- capsule has version, issue/expiry time, target hash, payload, signature;
- canonical JSON is signed excluding signature field;
- target mismatch, expiry, unsupported version, or tampering causes `FREEZE`;
- omitted fields are not inferred during verification.

## Security limits
HMAC gives integrity/authenticity only to parties already sharing the secret. It does not provide confidentiality. Production adoption would require authenticated encryption, secure key management, replay controls, and real device identity/attestation as appropriate.
