# Proposed NEXY Integration Contract

Status: `Lo4_AI_PROPOSAL_ONLY` / `NOT_VERIFIED` against NEXY runtime.

## Adapter boundary
A future NEXY adapter could map existing internal objects into these neutral contracts:

- authority claims -> `AuthorityClaim`
- claim dependency/status graph -> `ClaimNode`
- evidence obligations -> `ClaimRequirement`
- executable check catalog -> `Probe`
- normalized requirement rows -> `RequirementSpec`
- release candidate claims -> `ClaimArtifact`

## Required integration guarantees
1. NEXY remains the authority; these modules never self-promote.
2. Promotion receipts must originate from an authorized governance path, not from model text.
3. Evidence class mappings must follow project verification law.
4. Probe `cost` is scheduling metadata only and cannot lower proof requirements.
5. RBWE receives normalized explicit requirements; it must not invent missing semantics.
6. PCOC sits at a release boundary and must fail closed on missing proof.
7. PCOC trusted seal digests must come from the protected APS/governance path, never directly from model/user payload fields.
8. Evidence records must be bound to the same claim ID and exact target version before release.
9. All integration data keeps provenance IDs traceable back to NEXY sources/evidence.

## Forbidden shortcut
Do not treat a passing isolated test suite here as proof that NEXY.AI has adopted, integrated, deployed, or safely operates these systems.
