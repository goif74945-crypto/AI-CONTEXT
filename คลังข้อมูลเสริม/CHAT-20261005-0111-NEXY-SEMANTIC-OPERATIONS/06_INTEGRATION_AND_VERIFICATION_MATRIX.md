# Integration and Verification Matrix
| Concern | Artifact | Static evidence | Runtime evidence | Failure |
|---|---|---|---|---|
| semantics | versioned contract | schema + semantic review | conformance tests | semantic drift |
| provenance | claim graph | referential integrity | lineage query | unverifiable claims |
| authority | authority metadata | policy validation | denied unauthorized mutation | privilege ambiguity |
| freshness | observation/expiry | schema checks | stale-path test | stale truth |
| unknowns | state lattice | exhaustive handling | UNKNOWN/CONFLICT tests | fabricated certainty |
| capabilities | handshake | compatibility fixtures | negotiation tests | silent downgrade |
| replay | replay capsule | required fields | seeded replay | non-reproducible failure |
| mutation | receipt | revision fields | before/after verification | unauditable side effects |

## Cross-cutting tests
1. unit mismatch rejected;
2. stale cache cannot override fresher authoritative observation;
3. contradictory authoritative claims yield CONFLICT;
4. derived claims dirty after source invalidation;
5. missing required capability blocks;
6. missing optional capability only follows declared downgrade;
7. replay uses recorded observations, not live state;
8. durable write emits mutation receipt;
9. changed evidence revision invalidates stale reference;
10. unsupported semantic state fails closed.

## Adoption sequence
A inventory contracts/state words.
B define state lattice and authority classes.
C add provenance/correlation/causation IDs.
D negotiate capabilities at volatile boundaries.
E add mutation receipts/replay capsules.
F execute adversarial compatibility/evidence tests.
G migrate incrementally with telemetry.

PASS requires executed evidence for the relevant layer. Documentation alone is NOT_VERIFIED runtime behavior.
