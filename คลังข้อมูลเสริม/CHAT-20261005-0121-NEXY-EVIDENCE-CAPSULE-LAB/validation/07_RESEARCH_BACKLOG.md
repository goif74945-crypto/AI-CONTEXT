# Research / Adoption Backlog

## P0 before production consideration
1. Replace HMAC with an asymmetric signature scheme selected by security review.
2. Define key registry, rotation, revocation and compromise recovery.
3. Bind canonicalization version and disclosure schema digest into the signed contract.
4. Publish cross-language deterministic test vectors.
5. Design durable replay storage with TTL, sharding and failure semantics.
6. Define trusted time authority/skew behavior.
7. Threat-model metadata leakage and traffic correlation.
8. Fuzz parser, canonicalization, proof and bundle-shape boundaries.
9. Define relationship to canonical NEXY Evidence, AuditLog, EventLog, FreezeIncident and Vault objects.
10. Add policy-version digest so historical disclosure can be interpreted against the exact policy snapshot.

## P1 privacy and reliability
- blinded/selective commitments for highly sensitive fields;
- optional encrypted disclosures for named recipients;
- batch/multi-proof optimization;
- proof-size/latency benchmarks;
- malformed proof depth limits;
- record-size and field-count limits;
- salt custody/retention policy;
- signer outage/degraded mode;
- verifier cache rules;
- deterministic error taxonomy;
- negative conformance corpus shared across languages.

## P2 advanced research
- zero-knowledge predicates such as “threshold satisfied” without revealing raw value;
- anonymous/selective credentials where identity minimization is useful;
- hardware-backed signing/attestation;
- transparency log for issuer key events;
- policy proofs that show why a disclosure was permitted without leaking unrelated policy.

## Kill criteria
Do not adopt if the mechanism adds complexity without measurable disclosure reduction, if policy/version semantics remain ambiguous, if cross-language canonicalization cannot be made deterministic, or if verification cannot remain independent from the generator.