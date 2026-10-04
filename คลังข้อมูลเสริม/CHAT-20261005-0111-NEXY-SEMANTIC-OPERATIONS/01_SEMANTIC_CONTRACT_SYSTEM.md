# Semantic Contract System for Long-Lived AI Platforms
## Purpose
Prevent independently evolving components from agreeing on shape while disagreeing on meaning.
## Contract dimensions
identity; semantics; authority; freshness; evidence.
A schema validates shape, not meaning.
## Portable envelope
contract_id, contract_version, producer_id, producer_capabilities, subject_id, assertion_time, observation_time, expiry_policy, authority_class, confidence_class, provenance_refs, payload_schema_ref, payload, invariants, compatibility_range, idempotency_key, correlation_id, causation_id.
## State lattice
KNOWN_VALID, KNOWN_STALE, UNKNOWN, UNAVAILABLE, UNSUPPORTED, REDACTED, CONFLICT, INVALID, PENDING_VERIFICATION.
Absence/null/redacted/unsupported/stale/not-yet-computed must not collapse into one state.
## Invariants
Identity is never inferred from display text. Observation and assertion time are distinct. UNKNOWN remains representable. Producers cannot self-grant authority. Derived facts retain lineage. Required compatibility is explicit.
## Change protocol
Version semantic changes; classify additive/narrowing/widening/reinterpretation/breaking; publish compatibility range; add conformance fixtures; migrate via dual-read/write when needed; measure population; retire legacy only with evidence.
## Failure examples
Unit mismatch; lifecycle-word mismatch; clock/timezone mismatch; incomparable confidence scores; tool success meaning accepted rather than completed; cached value treated as current truth.
## Acceptance evidence
Machine schema + human semantics + negative fixtures + executed compatibility tests + traceable provenance + tested unknown/conflict/stale paths.
