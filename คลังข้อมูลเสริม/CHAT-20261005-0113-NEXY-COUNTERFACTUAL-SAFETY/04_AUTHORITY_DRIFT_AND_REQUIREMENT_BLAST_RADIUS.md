# Authority Drift and Requirement Blast Radius

Status: AI-PROPOSED CONCEPT — NOT CURRENT NEXY REQUIREMENT

## Authority drift
Authority drift occurs when a downstream artifact continues using a rule that has been superseded, narrowed, deferred, excluded, or reclassified.

## Detector inputs
- canonical authority hierarchy
- requirement stable IDs
- source anchors
- scope class
- supersession links
- consuming artifacts
- last-resolved authority hash

## Drift classes
AD0 ALIGNED
AD1 SOURCE_MOVED
AD2 SCOPE_RECLASSIFIED
AD3 SEMANTIC_CHANGED
AD4 CONFLICTING_AUTHORITY
AD5 ORPHANED_DERIVATION
AD6 UNKNOWN_PROVENANCE

AD4-AD6 MUST freeze automatic promotion.

## Blast radius dimensions
Do not reduce impact to a single number. Emit vector:
B = {
 law,
 requirements,
 interfaces,
 data,
 security,
 runtime,
 ux,
 deployment,
 evidence,
 migration
}

Each dimension contains affected IDs and confidence/proof, not merely a score.

## Requirement impact states
UNCHANGED
TEXT_ONLY
SEMANTIC_COMPATIBLE
SEMANTIC_BREAKING
REMOVED
NEW
SCOPE_CHANGED
AUTHORITY_CHANGED
UNKNOWN

## Critical rule
A wording diff is not a semantic diff. Conversely, unchanged wording does not prove unchanged semantics if referenced definitions or authorities changed.

## 837-matrix compatibility
The current matrix may act as source enumeration input, but this concept MUST NOT reinterpret all 837 rows as atomic systems. It operates on stable requirement identities and typed relationships.
