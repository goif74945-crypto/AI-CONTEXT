# TEMP EXECUTION MEMORY — NEXY EPC Adoption Provenance & Supply-Chain Court 20

CHAT_ID: `CHAT-20261005-0311-GPT56SOL-NEXY-EPC-APSC20`
PLATFORM_NATIVE_CHAT_ID: `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`
STATUS: `IN_PROGRESS`
AUTHORITY_CLASS: `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL / NON_GOVERNING`
CREATED_LOCAL_CONTEXT: `2026-10-05 Asia/Bangkok`

## Objective
Design, implement, execute, repair, re-test, and preserve exactly 20 deterministic Q64.64 mechanisms that help the proposed NEXY Evolutionary Proposal Court decide whether a Lo4 candidate is sufficiently supply-chain/provenance-ready to be handed to the existing JUDGE/human authority for adoption consideration.

This is not a legal-opinion engine and does not decide Canon. It checks engineering evidence about artifact identity, dependency/license metadata, source origin, lock integrity, install scripts, native binaries, hermetic build inputs, reproducibility, attestations, drift, and adoption risk.

## Scope lock
WRITABLE:
- `goif74945-crypto/AI-CONTEXT` branch `main`
- only `คลังข้อมูลเสริม/CHAT-20261005-0311-GPT56SOL-NEXY-EPC-APSC20/**`
- one append-only KEEP vote under `คลังข้อมูลเสริม/VOTES/**` only if final evidence is sufficient.

READ-ONLY / PROTECTED:
- every repository whose name contains `NEXY.AI`
- observed implementation repository: `goif74945-crypto/NEXY.AI-`
- branch: `NEXY.ai`
- inspected commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

FORBIDDEN:
- any mutation to NEXY.AI-
- Canon/LAW/CORE/JUDGE/SWARM state mutation or bypass
- automatic promotion
- physical deletion for CUT
- hidden wall-clock/random/network decisions
- authoritative IEEE-754 scoring
- legal conclusions inferred from incomplete license metadata
- claiming NEXY runtime integration from standalone tests

## Authority pins
SPEC_ID: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx`
SPEC_SHA256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
NORMALIZED_REQUIREMENT_ROWS: `837`
NEXY_REPO: `goif74945-crypto/NEXY.AI-`
NEXY_BRANCH: `NEXY.ai`
NEXY_COMMIT_SHA: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
AI_CONTEXT_BASELINE: `c4bc5809269e0709b30b47a49533fe1c50518c75`

## Direct compatibility observations
- NEXY package.json declares package license ISC and has Node dependencies.
- NEXY package-lock carries per-package license metadata and integrity digests.
- NEXY Dockerfile pins the base image by sha256, uses npm ci, pins Rust 1.98.1, and binds source/test identities.
- NEXY core-kernel/build.rs hashes compiler/target/flags/normalized environment for build provenance and explicitly says external Layer-8 verification owns broader provenance.
- NEXY already has runtime/evidence attestations; APSC-20 is therefore an upstream Lo4 adoption-evidence proposal, not a replacement for those Canon/runtime mechanisms.

## Collision boundary
Current/concurrent supplemental work already covers generic EPC voting/adjudication, causal proof, evidence acquisition, scientific trials/replication, strategic integrity, due process, human deliberation, temporal proof, atomic ballot publication, proposal fingerprint/overlap, integration compatibility/ecology, cross-runtime contract drift, privacy egress/selective disclosure, Anti-Goodhart, and economic integrity.

Repository-wide commit searches returned no dedicated current supplemental project for:
- SPDX/license metadata policy;
- SBOM-like adoption manifests;
- transitive dependency/license evidence;
- lockfile integrity coverage;
- vendored artifact origin;
- registry origin pinning;
- install-script/native-binary provenance;
- hermetic build closure;
- reproducible-build consensus specifically as an EPC adoption gate.

This is bounded repository evidence, not universal novelty proof.

## Frozen 20-system surface
1. SAIG — Source Artifact Identity Gate
2. LICA — Lockfile Integrity Coverage Auditor
3. SEPG — SPDX Expression Policy Gate
4. LECM — License Evidence Completeness Meter
5. TOSM — Transitive Obligation Surface Mapper
6. ANCG — Attribution/Notice Completeness Gate
7. VAFB — Vendored Artifact Fingerprint Binder
8. ROPG — Registry Origin Pin Gate
9. SERG — Script Execution Risk Gate
10. NBPG — Native Binary Provenance Gate
11. DSD — Dependency Substitution Detector
12. DGCRA — Dependency Graph Closure/Reachability Auditor
13. MPICM — Maintainer/Publisher Identity Continuity Meter
14. BICC — Build Input Closure Compiler
15. HBBA — Hermetic Build Boundary Auditor
16. RAC — Reproducible Artifact Consensus
17. PATG — Provenance Attestation Threshold Gate
18. SCDDA — Supply-Chain Drift Delta Auditor
19. ARBL — Adoption Risk Budget Ledger
20. APCC — Adoption Provenance Capsule Compiler

## Numeric law
- all quantitative advisory metrics use checked signed Q64.64 carried by BigInt in signed-i128 raw bounds;
- no binary floating-point decision authority;
- overflow/divide-by-zero/range violations fail closed;
- hard provenance/policy gates are non-compensatory;
- scores never grant adoption/promotion authority.

## Vote budget
KEEP remaining: 1
CUT remaining: 1
DEFER / INSUFFICIENT_EVIDENCE / WIP consume neither.
Historical votes are immutable; evidence revisions never restore rights.

## Execution state
COMPLETED:
- AI-CONTEXT boot/kernel/security/verification/project context inspected.
- current NEXY exact-head Q64/authority/build-provenance surfaces inspected read-only.
- broad collision scan performed.
- first local EPC candidate was discarded after semantic collision with NEXY-PROPOSAL-FORGE; it will not be published.
- APSC-20 unique axis frozen.

IN_PROGRESS:
- standalone TypeScript Q64.64 implementation and tests.

NEXT:
- implement all 20 systems;
- run E1/E2/E3 and property/negative/determinism checks;
- repair failures and rerun;
- hash exact tested bytes;
- publish design/code/tests/evidence;
- GitHub read-back;
- refresh both repository heads;
- cast at most one KEEP vote only if all user vote fields can be evidenced.

## Resume rule
Refresh AI-CONTEXT HEAD and protected NEXY HEAD first, re-read this file, re-run collision checks for newly-landed work, and continue only from exact verified artifacts.