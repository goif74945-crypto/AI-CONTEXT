# PRFF20 Task Contract

## OBJECTIVE
Create exactly twenty implemented mechanisms that measure whether a proposal/evidence proof graph is structurally resilient enough to be reviewed, while preserving NEXY Canon, LAW and JUDGE authority.

## REQUIRED OUTPUT
A standalone C++20 library, tests, example, architecture, collision audit, failure history, reproducible evidence and an EPC-compatible non-authoritative receipt proposal, stored only in AI-CONTEXT supplemental space.

## INPUTS / AUTHORITY
1. User EPC rules in the initiating conversation.
2. Authoritative NEXY-IGNIS DOCX identity: SHA-256 `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
3. Read-only NEXY code at `goif74945-crypto/NEXY.AI-@9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
4. Current AI-CONTEXT candidate corpus and EPC vote schema.
5. EPC Vote Schema v1 at `คลังข้อมูลเสริม/NEXY-EPC/VOTES/VOTE-SCHEMA.md`.

## IMMUTABLE REQUIREMENTS
- No mutation to any repository whose name contains `NEXY.AI`.
- PRFF is Lo4 proposal-only and cannot become Canon by self-assertion.
- SWARM/AI/EPC/Human auxiliary layers cannot change Core/JUDGE state through PRFF.
- C20 means only `READY_FOR_JUDGE_LAW_REVIEW_ONLY`; it does not mean KEEP, ACCEPT, PROMOTE, STABLE or FINAL.
- Authoritative numeric scoring uses checked signed Q64.64; no binary floating-point decision path.
- Exact combinatorial search is bounded; budget exhaustion fails review readiness rather than approximating.
- Same normalized graph + same policy -> byte-identical canonical report.
- UNKNOWN/WIP/INSUFFICIENT_EVIDENCE cannot justify EPC CUT.
- CUT never means physical deletion.
- A PRFF result cannot consume EPC KEEP/CUT rights.

## IN SCOPE
- strict proof-DAG contract;
- root/evidence/edge connectivity;
- deterministic max-flow/min-cut certificates;
- exact bounded evidence ablation;
- minimum-cut family enumeration;
- shared multi-claim bottleneck analysis;
- advisory repair ranking;
- tests, sanitizers and replay evidence;
- read-only NEXY/EPC integration contract.

## OUT OF SCOPE
- truth/authenticity of supplied evidence metadata;
- cryptographic provenance attestation;
- production deployment;
- NEXY runtime integration;
- automatic Canon promotion;
- automatic KEEP/CUT verdicts;
- natural-language semantic duplicate discovery;
- claiming universal superiority over every possible future system.

## ACCEPTANCE CRITERIA
- exactly 20 implemented mechanisms C01..C20;
- Q64.64 implementation has checked arithmetic and float-ingress scan passes;
- Release build/test passes under GCC and Clang;
- strict warning build passes without lowering `-Werror`;
- randomized small-graph min-cut results match brute-force exhaustive oracle;
- exact-search budget exhaustion is fail-closed;
- deterministic replay is byte-identical;
- known limitations are explicit;
- artifact is persisted and fetched back from AI-CONTEXT before a KEEP vote is considered.
