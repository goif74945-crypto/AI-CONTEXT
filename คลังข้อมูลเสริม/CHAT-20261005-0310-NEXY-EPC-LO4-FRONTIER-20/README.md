# NEXY Evolutionary Proposal Court (EPC) — Lo4 Frontier 20

**Status:** `IMPLEMENTED_SUPPLEMENTAL_TOOL / LO4_AI_PROPOSAL_ONLY / NON_AUTHORITATIVE`

**CHAT_ID:** `CHAT-20261005-0310-NEXY-EPC-LO4-FRONTIER-20`

This CHAT_ID is a project-scoped lineage identifier created for this work. It is not claimed to expose an internal ChatGPT platform conversation identifier.

## Purpose

EPC is a deterministic evidence court for AI-proposed NEXY supplements. It evaluates a candidate through twenty independent Q64.64 engines, applies non-compensatory authority/safety/determinism gates, protects WIP/UNKNOWN work from unjustified CUT, and renders auditable KEEP/CUT vote records without granting itself any Canon authority.

It is deliberately **not** a NEXY Core/JUDGE replacement. The strongest thing EPC can do is create an advisory artifact for authorized review.

## Why it exists

AI-CONTEXT already contains strong proposal, proof, reliability and Q64 labs. The missing control problem found during this campaign was a formalized **proposal court with per-chat KEEP/CUT rights, immutable vote lineage, WIP anti-purge law, semantic-evidence CUT requirements, and an explicit no-auto-promotion boundary**.

## Twenty implemented engines

E01 Canon Compatibility Lattice; E02 Authority Boundary Firewall; E03 Evidence Sufficiency Gate; E04 Evidence Freshness Clock; E05 Semantic Novelty Proof; E06 Overlap Burden Meter; E07 Dependency Integrity DAG Gate; E08 Conflict Isolation Chamber; E09 Determinism Impact Proof; E10 Security Impact Gate; E11 Implementation Value Engine; E12 Verification Value Engine; E13 Maintenance Cost Inverter; E14 Reversibility Proof; E15 Blast Radius Containment; E16 Supersession Lineage Graph; E17 Adversarial Counterargument Ledger; E18 Anti-Goodhart Robustness Gate; E19 Promotion Readiness Envelope; E20 Portfolio Orthogonality Engine.

See `03_CONCEPTS_20.md` for individual contracts.

## Runtime

Requirements: Node.js >= 22 and a TypeScript compiler (`tsc`) available for build.

```bash
npm run build
npm run test
npm run smoke
npm run verify
```

No runtime npm dependency is required. The library uses Node built-ins only.

CLI:

```bash
node bin/epc.mjs evaluate examples/candidate.json
node bin/epc.mjs vote examples/candidate.json KEEP CHAT_ID VOTE_ID 2026-10-05T03:10:00+07:00
```

## Verification snapshot

- First 40-test run exposed a real E07 aggregation defect: dependency cycles were detected by E07 but omitted from final hard-block selection.
- Production fix: added E07 to the non-compensatory hard-block set.
- 40/40 regression PASS.
- Test suite expanded with engine-level partial/negative and contract tests.
- Final local suite: **63/63 PASS**.
- Valid candidate smoke evaluation: 20 engines, `KEEP_CANDIDATE`, Q64 score `1.00000000`, no hard blocks.
- Smoke evaluation digest before exact-head re-anchor: `cc9961a1cff827b113746fbdc6a888dda2dd9705c854431b403b47ed0ce7d5da`.

Raw evidence is under `evidence/`.

## Authority boundary

EPC never claims:

- automatic promotion into NEXY Canon/DOC-B/C/D/E;
- permission to mutate NEXY Core state;
- permission to bypass JUDGE/LAW/verification;
- permission to physically delete a CUT candidate;
- production deployment proof;
- proof that it is globally superior to every concurrent chat artifact.

`goif74945-crypto/NEXY.AI-` was treated as read-only for this work.

## Evidence baseline

- Canonical NEXY-IGNIS content SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
- NEXY commit inspected: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43` on `NEXY.ai`.
- AI-CONTEXT pre-mutation baseline: `55469befc00844f14993c98c104a29c99dff7a0b`.
- Current normalized NEXY requirement denominator used for context: 837 rows; legacy 215 registry explicitly not used.

## Directory map

- `00_TEMP_MEMORY.md` — resumable execution state and real failure/repair history.
- `01_TASK_CONTRACT.md` — scope/acceptance/stop conditions.
- `02_ARCHITECTURE.md` — authority, Q64, evidence, recommendation and integration architecture.
- `03_CONCEPTS_20.md` — twenty implemented Lo4 concept engines.
- `04_NOVELTY_COLLISION_AUDIT.md` — targeted semantic collision analysis.
- `05_INTEGRATION_CONTRACT.md` — one-way read/advisory NEXY compatibility contract.
- `06_REQUIREMENT_LEDGER.md` — explicit user-requirement mapping.
- `07_THREAT_MODEL.md` — adversarial and failure model.
- `08_VOTE_PROTOCOL.md` — KEEP/CUT round law.
- `src/epc.ts` — implementation.
- `tests/epc.test.mjs` — unit/adversarial suite.
- `bin/epc.mjs` — CLI.
- `examples/candidate.json` — baseline fixture, not itself a Canon proof.
- `evidence/` — raw executed proof and hashes.
- `09_FINAL_AUDIT.md` — release audit for this supplemental artifact.
