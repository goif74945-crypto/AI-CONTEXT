# Non-Governing Integration Proposal

## Status
AI-PROPOSED ONLY. This file does not add current NEXY build scope.

## Candidate placement
If promoted by future authority, an Evidence Capsule service could sit beside evidence/audit/Vault read paths. It should never become a source of canonical truth. Canonical evidence remains in the authoritative store; the capsule service only creates verifiable derived disclosure views.

## Suggested flow
1. Authoritative evidence record is committed normally.
2. A trusted adapter selects a disclosure schema/version.
3. Field commitments are produced from the immutable record.
4. A protected signer authenticates capsule metadata.
5. Requesting actor is authorized by current server-side RBAC/policy.
6. A presentation is generated for explicit purpose and audience.
7. Consumer verifies signature, policy-independent integrity proof, freshness and replay status.
8. Audit records link capsule/presentation IDs back to authoritative evidence lineage.

## Boundaries
- UI never decides authorization.
- Model output never grants disclosure rights.
- Presentation generation never mutates the source audit row.
- Hash proof does not substitute for issuer authentication.
- Issuer authentication does not substitute for access control.
- Access control does not substitute for freshness/replay checks.
- A valid capsule does not prove the underlying NEXY claim itself is true; it proves integrity/authenticity of what was committed.

## Adoption gates
Before any production merge:
1. explicit product/security requirement and authority approval;
2. asymmetric signing algorithm and protected signer;
3. versioned canonicalization with cross-language test vectors;
4. key lifecycle, revocation and rotation;
5. durable replay/freshness state;
6. privacy review for metadata leakage;
7. abuse tests and fuzzing;
8. integration tests against real evidence/Vault/Audit contracts;
9. E2E tests for role/purpose/audience disclosure;
10. operational evidence for rotation, signer outage and recovery.

## Rollback
Because capsules are derived views, integration should be feature-gated and removable without rewriting canonical evidence history. Previously issued capsules need an explicit verification/version policy rather than silent invalidation.