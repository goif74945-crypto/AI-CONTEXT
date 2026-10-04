# NEXY::PRISM Integration Boundary

Status: future integration proposal only. No production integration has been performed.

## Recommended future placement
If explicitly promoted by a NEXY spec extension, PRISM should sit after backend truth is computed and before renderer controls are produced.

PRISM may consume a normalized read-only projection of SystemEnvelope state, backend authorization, release-policy result, evidence status, FreezeIncident data, and explicitly supplied risk/irreversibility metadata.

## Forbidden dependency direction
- PRISM -> CORE mutation
- PRISM -> LAW mutation
- PRISM -> JUDGE decision
- PRISM -> AUTH grant
- PRISM -> VAULT commit/delete
- PRISM -> queue execution
- PRISM -> release token creation

## Promotion gate
1. explicit spec promotion/version bump;
2. mapping review against current DOC-C schemas;
3. frontend contract review;
4. API/RBAC abuse tests;
5. E2E frozen-state tests;
6. accessibility/usability tests;
7. rollback path;
8. deployment evidence at exact commit.

Until then, this package proves only the standalone reference algorithm.
