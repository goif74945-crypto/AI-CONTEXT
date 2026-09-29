# NEXY.AI — Current Full System / Feature Build Matrix

## Status
**CURRENT NORMALIZED SOURCE MATRIX — SOURCE-GROUNDED / IMPLEMENTATION NOT VERIFIED**

This record is the current normalization reference for enumerating NEXY-IGNIS systems, features, requirements, scope and authority. It supersedes the legacy 215-entry registry for counting, audit denominators, build-scope enumeration and completeness claims.

## Provenance
- Matrix file: `NEXY_IGNIS_FULL_SYSTEM_FEATURE_BUILD_MATRIX.xlsx`
- Matrix SHA-256: `7685d962f0f3cd3453faba7853eb571c0e265177f8825d83f4f01a0672657622`
- Matrix byte size: `176681`
- Source document: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
- Source document SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
- Source non-empty paragraphs: `10,979`
- Normalized requirement rows: **837**
- Implementation audit in this matrix: **NOT PERFORMED**
- Default implementation status in this matrix: **NOT_VERIFIED**

## Workbook structure
- `Build Matrix`: 837 normalized requirement rows + header.
- `Current Build`: 773 current non-excluded/deferred rows + header.
- `Excluded Deferred`: 12 rows + header.
- `Deployment Evidence`: 52 rows + header.
- `Future Domains`: 10 named future/conceptual architecture domains + header.
- `Source Coverage`: source-range classification map.
- `Summary`: provenance, scope counts and authority rules.

## Scope denominator
| Build scope | Rows | Meaning |
|---|---:|---|
| CURRENT_GOVERNING_LAW | 12 | Current governing law |
| CURRENT_BUILD | 547 | Direct DOC-C build obligation |
| CURRENT_BUILD_SUPPLEMENT | 127 | Storage/Auth hardening build supplement |
| SUPPORTED_PRODUCT_DESIGN | 87 | DOC-D product/UI requirement where DOC-C supports it |
| DEPLOYMENT_EVIDENCE | 52 | DOC-E proof required for deploy approval |
| EXCLUDED_CURRENT | 8 | Explicitly outside current vNEXT |
| DEFERRED_FUTURE | 4 | Explicitly deferred to a future version |
| **TOTAL** | **837** | Normalized source requirements/features |

The 773-row `Current Build` worksheet consists of:
`12 + 547 + 127 + 87 = 773`.

DOC-E's 52 evidence rows are deployment-proof obligations, not substitutes for implementation. Excluded and deferred rows remain traceable but are not current implementation defects.

## Authority rules
1. **DOC-B** governs current system law.
2. **DOC-C** is the current build authority.
3. **DOC-D** is product/UI authority only where supported by DOC-C.
4. **DOC-E** controls deployment evidence/approval; it is not implementation proof.
5. Future Sovereign/Game/NCF/Trinity/Robotics/Final-Architecture material does not become current vNEXT build scope unless explicitly promoted.
6. Design, implementation, runtime behavior and deployment evidence remain separate truth domains.

## Future / conceptual domains preserved by the matrix
1. Sovereign / Universe / Host Recovery
2. Creator Fabric / Constitutional Layers
3. AAAA Game Fabric
4. NCF Creative Fabric
5. Capability Registry / Admission / Chaos
6. L1o Intelligence Layer
7. Lo3 Swarm Governor
8. Lo2 Synthesis / Evolution
9. RCL / Robotics
10. Final 10-Layer Architecture

## Legacy 215-entry registry policy
**STATUS: DEPRECATED_UNRELIABLE_DO_NOT_USE**

The historical 215-entry registry must **not** be used as:
- the current NEXY system count;
- an atomic-system count;
- an audit denominator;
- a build denominator;
- a completeness denominator;
- a requirement denominator;
- a source-of-truth inventory;
- a basis for creating or deleting systems.

Reason:
- it was a historical tracking inventory rather than a fresh, exhaustive normalization of the full source;
- its counting unit was inconsistent and compressed systems, engines, laws, protocols, FSMs, contracts and other objects into mixed entries;
- it can omit or duplicate lower-level requirements/mechanisms;
- the current matrix provides a source-anchored, authority/scope-classified denominator of 837 normalized requirement rows.

Historical 215 records may remain in `TASKS/`, `CASES/`, `FAILURES/` and `LEDGER/` **for provenance only**. They are not current authority and must not be used to answer current NEXY inventory/count questions.

## Relationship to older AI-CONTEXT registries
- The **262-entry Requirement Registry** is a prior partial/source-derived registry. Its internal structural validation may remain valid, but **262 is not the current exhaustive source denominator**.
- The **518-entity Ontology v1** is a typed architecture-object registry under its own ontology rules. It is **not a count of NEXY systems** and is not interchangeable with the 837 normalized requirement rows.
- Neither 262 nor 518 should be silently substituted for the current matrix denominator when the task asks for exhaustive requirements/features.

## Current counting rule
For current source enumeration, use:
**837 normalized requirement rows + explicit scope/authority classification.**

Do not publish a single “total systems” number unless the counting ontology is explicitly defined for that task.

## Verification boundary
This matrix is a source-normalization artifact. It does not prove:
- code implementation;
- test pass;
- runtime correctness;
- deployment readiness;
- physical robotics behavior.

Those claims require repository/runtime/DOC-E evidence at the exact revision being claimed.
