# Authority and Baseline

## Authority order used
1. Current user directive and EPC laws.
2. Canonical NEXY source/spec identity and current source snapshots.
3. Current NEXY implementation at the observed exact commit.
4. AI-CONTEXT execution/security/verification laws.
5. This Lo4 design.

## NEXY implementation baseline
- Repository: `goif74945-crypto/NEXY.AI-`
- Branch: `NEXY.ai`
- Observed commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- Read-only inspection: YES
- Mutation performed by this task: NO

Relevant implementation evidence inspected:
- `core-kernel/src/engine/fixed128_math.rs`: signed Q64.64 `Fixed128(i128)` and fail-closed checked arithmetic.
- `packages/intelligence/trinity.ts`: `publisher: EXTERNAL_JUDGE`, `implicitOverride: false`, `lo2MayOverrideCurrentDecision: false`, release is JUDGE-pending/freeze.
- `tests/contract/intelligence-layer-contract.test.ts`: tests authority separation and no pre-JUDGE release.
- `tests/contract/release-spine.test.ts`: current release-spine evidence binds final release to JUDGE verification and LAW acceptance.
- `scripts/check-six-system-matrix.ts`, `scripts/check-six-system-spec-lock.ts`, `evidence/six-system/spec-traceability-matrix.json`: bind the design source identity/hash.

## Design-source identity
SPEC_ID: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`  
SPEC_SHA256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`

The NEXY source corpus records this exact source identity/hash. Google Drive also exposes a text copy named `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.txt`, but its direct content fetch failed UTF-8 decoding through the available connector. Therefore the exact original DOCX body was not independently re-read byte-for-byte during this session. This limitation is why no KEEP/CUT vote is cast.

## Source-snapshot corroboration
`NEXY_AI.txt` and `NEXY_AI-1.txt` were read through the connected Drive search surface. They describe:
- event ownership split across CORE, SWARM and JUDGE;
- non-owning transitions rejected;
- LAW pre-release gate as mandatory;
- Q64.64 Fixed128 arithmetic with no floating-point in the kernel equation;
- immutable no-higher-layer override boundaries.

## AI-CONTEXT baseline law read
- `AI-EXECUTION-KERNEL.md`
- `rules/GLOBAL.md`
- `rules/SECURITY.md`
- `rules/VERIFICATION.md`

These require scope control, current-state inspection, evidence-class matching, negative-path tests, least authority, durable checkpoints, and no fake completion claims.
