# NEXY EPC Constitutional Jurisprudence & Precedent Engine 20

CHAT_ID: CHAT-20261005-0312-GPT56SOL-NEXY-EPC-JURISPRUDENCE-20
PLATFORM_NATIVE_CHAT_ID: UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS
CANDIDATE_ID: EPC-JURISPRUDENCE-20
STATUS: Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING

## Objective
Create 20 deterministic jurisprudence and precedent-analysis systems for the proposed NEXY Evolutionary Proposal Court (EPC), implemented and tested outside NEXY.AI. The output is advisory only and has no authority to promote, release, mutate Canon/LAW/CORE/JUDGE state, or physically delete a candidate.

## 20 systems
1. Precedent Applicability Matcher
2. Precedent Weight Calibrator
3. Precedent Conflict Cartographer
4. Precedent Supersession Resolver
5. Doctrine Drift Detector
6. Doctrine Scope Extractor
7. Standard-of-Review Selector
8. Burden-of-Proof Allocator
9. Evidentiary Burden Satisfaction Matrix
10. Argument Completeness Auditor
11. Counterargument Strength Evaluator
12. Dissent Preservation Compiler
13. Dissent-to-Test Generator
14. Recusal / Conflict-of-Interest Detector
15. Independent Panel Composition Planner
16. Reason-Code Canonicalizer
17. Holding-vs-Dicta Separator
18. Remedy Proportionality Advisor
19. Cross-Case Consistency Auditor
20. Jurisprudence Query Engine

## Authority evidence
SPEC_ID: แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx
SPEC_SHA256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

The Drive source was materialized as exact raw bytes, identified as Microsoft Word 2007+ OOXML, and its SHA-256 matched the AI-CONTEXT provenance exactly before direct word/document.xml inspection. Relevant source rules establish:
- Human/auxiliary layers cannot mutate Core state, override Core decisions, bypass verification, or lower correctness.
- AGENT proposes, SWARM debates, VERIFY validates evidence, CORE decides.
- JUDGE -> CORE dependency is forbidden.
- new functionality outside the version scope requires explicit spec extension, dependency review, test-gate impact review, and version bump.
- authoritative arithmetic is deterministic signed 128-bit fixed-point / Q64.64, with overflow fail-closed and no authoritative floating-point.

NEXY_REPO: goif74945-crypto/NEXY.AI-
NEXY_BRANCH: NEXY.ai
NEXY_INSPECTED_COMMIT: 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43

Exact read-only code evidence included:
- packages/core/vnext-state-matrix.ts
- packages/intelligence/dsl.ts
- packages/phase-f/lo3/governor.ts
- packages/judge/consensus.ts
- README.md / contract-test authority surfaces

No mutation command was sent to NEXY.AI-.

## Implementation
Runtime/toolchain used for local execution:
- Node 22.16.0
- npm 10.9.2
- TypeScript 5.8.3
- strict TypeScript
- BigInt signed Q64.64 with conceptual signed-i128 range checks

Determinism hardening:
- no Math.random
- no Date.now / performance.now / new Date
- no localeCompare / Intl ordering
- no parseFloat / toFixed
- no authoritative decimal floating literals
- no bare sort() in deterministic source
- checked overflow and divide-by-zero
- advisory authority hard-lock: mayPromote=false, mayMutateCoreState=false

## Verification
Final command: npm run verify
Final exit code: 0
Tests: 29
PASS: 29
FAIL: 0
SKIP: 0

Evidence classes:
- E1 static/type/source invariants: PASS
- E2 unit/negative/property: PASS
- E3 local multi-module/replay: PASS
- E4 NEXY end-to-end integration: NOT_VERIFIED
- E5 NEXY runtime: NOT_VERIFIED
- E6 deployment: NOT_VERIFIED

## Exact tested artifact
The complete Design + Code + Tests + Evidence snapshot is stored at:
artifacts/epc-jurisprudence20.tar.gz.b64

Base64-text bytes:
SHA256: 946af23416682cecb0a543b47db75d30aa66bc64ff4fe66d9212730d621f8dc2
SIZE: 36929 bytes including final newline
PUBLISH_COMMIT: 1a93d81133448bec9edbe5af8d122c98bb5da741

Decode:
```bash
base64 -d epc-jurisprudence20.tar.gz.b64 > epc-jurisprudence20.tar.gz
sha256sum epc-jurisprudence20.tar.gz
# expected:
# b71547f52482c8d633a2b953b70124ee8e33e425f9ab134a1d7561d03a070440
tar -xzf epc-jurisprudence20.tar.gz
cd epc-jurisprudence20
npm run verify
```

Archive SHA256: b71547f52482c8d633a2b953b70124ee8e33e425f9ab134a1d7561d03a070440
Candidate tested-bytes digest: b21bbae4f08fc2e0a595ab1e7ac4554a55539c912af4b16746cce52863d320a9
Artifact manifest SHA256: 9f07fce0668cfb26c3cacee8d067ffe3339f87adf68d922382d563dbdde0ca6e

## Collision boundary
This project intentionally excludes active EPC work on immutable vote rights, WIP/CUT law, evidence freshness, promotion readiness, semantic duplicate proof, proposal generation, integration ecology, blast radius, Anti-Goodhart, economic integrity, and generic deterministic optimization.

Initial AI-CONTEXT semantic scan found no direct supplemental implementation for precedent, jurisprudence, burden of proof, dissent, recusal, standard of review, or stare decisis. This is novelty evidence at the inspected state, not an eternal uniqueness claim.

## Promotion boundary
Local PASS does not promote this project. Promotion would require the authoritative NEXY process, formal scope/spec change where applicable, NEXY integration evidence, and higher evidence classes. Until then this artifact remains Lo4 experimental.
