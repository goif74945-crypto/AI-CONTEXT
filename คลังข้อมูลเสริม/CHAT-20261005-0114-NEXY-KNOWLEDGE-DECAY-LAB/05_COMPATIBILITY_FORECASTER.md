# Compatibility Forecaster
**AI-PROPOSED CONCEPT — NOT AUTHORITATIVE — NOT IMPLEMENTED — NOT VERIFIED**

## Purpose
Forecast what a proposed change could invalidate before mutation. It generates proof obligations; it is not an oracle.

## Inputs
proposed semantic change; contracts; requirement/dependency graphs; evidence bindings; failure fossils; environment/provider constraints; protected invariants.

## Compatibility Envelope
Assess DIRECT_BREAK, TRANSITIVE_BREAK, EVIDENCE_INVALIDATION, DATA_MIGRATION, ROLLBACK, SECURITY_BOUNDARY, DETERMINISM, UX_CONTRACT and UNKNOWN_DEPENDENCY risks. Every assessment carries evidence class.

## Shadow contracts
Systems often depend on undeclared behavior: ordering, latency, error shape, retry timing, casing, null semantics, idempotency and side effects. Observed shadow contracts are descriptive, not automatically authoritative.

## Change radius
R0 local/internal; R1 module contract; R2 service/domain; R3 cross-domain; R4 authority/evidence model; R5 irreversible/external ecosystem. Higher radius demands stronger discovery, proof and rollback design.

## Proof obligation generation
Examples: schema compatibility; deterministic replay equivalence; migration reversibility; provider receipt identity; security boundary preservation; stale-evidence rejection; rollback restoration.

## Unknown-edge rule
Absence of a known dependency is not proof of no dependency. High-radius UNKNOWN edges increase required discovery.

## Failure semantics
Insufficient graph coverage -> PARTIAL/UNKNOWN. Never emit a “safe change” claim from incomplete dependency evidence.
