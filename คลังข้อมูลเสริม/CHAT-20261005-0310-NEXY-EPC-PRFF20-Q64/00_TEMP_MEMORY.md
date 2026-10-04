# Durable Temporary Execution Memory

WORK_CHAT_ID: `CHAT-20261005-0310-NEXY-EPC-PRFF20-Q64`
PLATFORM_NATIVE_CHAT_ID: `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`
PROJECT: `NEXY EPC Proof Resilience Fracture Fabric 20 (PRFF20)`
CLASSIFICATION: `Lo4 / AI-PROPOSED / NON-CANONICAL / STANDALONE REFERENCE LAB`
STATUS: `IMPLEMENTATION_VERIFIED / PUBLICATION_PENDING`

## Objective
Build twenty executable Q64.64 mechanisms that add a new verification dimension for NEXY/EPC without editing any repository whose name contains `NEXY.AI`: proof-topology resilience under root, evidence-node and support-edge failure.

## Authority pins inspected
- Authoritative source document identity recorded by AI-CONTEXT ingestion: `แอป [NEXY-IGNIS] ที่กำลังพัฒนา(20260929-184432).docx`.
- Source SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
- Parsed accelerator: `REFERENCES/NEXY/2026-10-04/04-NEXY-IGNIS-source.txt`, blob `30b0c179670a836af61923b4b85ae89f3a40d8dc` as inspected.
- NEXY repository: `goif74945-crypto/NEXY.AI-`, branch `NEXY.ai`, read-only pin `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
- AI-CONTEXT collision-audit pin before publication: `7b3e350e84bb2997c6a8c0c9685a66b6019ebdb1`.

## Pivot history
The first local direction was an Evidence Causality & Independence Fabric. It was explicitly frozen as WIP after semantic collision discovery, not CUT:
- NEIK evidence-independence kernel: `267b67740f26dfa9544af8ce54a47abee520ea4b` / source commit `033a1cd9ff43d71bdc8636891f7d34c7b47f0e51`.
- Epistemic control proposals already cover counterfactual verification and correlated failure.
- A correlation-consensus guard already exists.

The project therefore pivoted to graph-theoretic proof resilience: minimum vertex/edge cuts, disjoint support channels, dominators, bridges, exact bounded ablation and cross-claim fracture topology.

## Verified implementation state
- C++20 source + tests: 1,680 lines before documentation.
- Exactly 20 PRFF mechanisms C01..C20.
- GCC 14.2 Release: 3/3 CTest PASS.
- GCC strict extra-warning gate: 3/3 PASS with `-Werror` retained.
- Clang 17 Release: 3/3 PASS.
- Property suite: 14,207 checks PASS, including 200 random-DAG brute-force min-cut oracles.
- UBSan full unit/property/stress: PASS.
- ASan unit + 200-case stress + integration example: PASS.
- Full 14,207-property suite under ASan: NOT_VERIFIED_BY_THIS_GATE because prior full-instrumented attempts exceeded command budget; no PASS claim is made for that surface.
- Authoritative binary-float ingress scan: PASS.
- Example deterministic replay: 10/10 byte streams produce SHA-256 `e52f6fa0ace6819816d2f7c5ecb7b0fb21acfa8f1aaf3fe7a02cf474fc362ff8`.

## Failure / repair ledger
1. Initial ECIF idea collided semantically with NEIK and related epistemic/correlation work -> FREEZE WIP and pivot; no CUT vote consumed.
2. First PRFF C++20 build used reserved identifier `concept` and had an unused helper -> compile FAIL under `-Werror`; renamed/removed, rebuilt.
3. Unit helper repeated reserved `concept` identifier -> compile FAIL; renamed to `findConcept`.
4. Root-channel semantics were re-audited: root count duplicated C03 when support edges were infinite capacity -> changed C04 to root-and-edge-disjoint channels; one stale function call then failed compile and was repaired.
5. Property iteration label said 14,014 while actual count was 14,007 at that stage -> evidence label corrected before publication; later random-DAG oracle added, final count 14,207.
6. ASan full property attempts exceeded command budget -> preserved as NOT_VERIFIED, not converted to PASS.
7. Sanitizer stress oracle incorrectly assumed one edge removal must fail graphs with 4–6 channels -> test FAIL; corrected the oracle to remove enough channels to leave exactly two, without weakening product policy.

## Resume law
Never mutate NEXY.AI from this project. Before semantic changes, rerun GCC Release, strict warnings, Clang, UBSan, bounded ASan, float scan and deterministic replay. Any proposed NEXY integration remains a separate authorization and promotion process.
