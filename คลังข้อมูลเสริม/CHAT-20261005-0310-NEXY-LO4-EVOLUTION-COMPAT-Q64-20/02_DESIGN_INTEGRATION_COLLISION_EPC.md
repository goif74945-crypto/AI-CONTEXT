# ECPC-20 — Design / Integration / Collision / EPC

Authority: **Lo4 AI proposal only**. This file describes an isolated reference system. It is not a NEXY Canon amendment.

## 20 executable concepts
1. **C01 Schema Fingerprint** — canonical semantic fingerprint; declaration order cannot create false drift.
2. **C02 Compatibility Lattice** — EXACT / COMPATIBLE_WITH_PROOF / CONDITIONAL / UNKNOWN / BREAKING classification.
3. **C03 Migration Witness** — removed/renamed/new-required fields need explicit transformation/default witnesses.
4. **C04 Codec Involution** — encode→decode must preserve canonical meaning on fixtures.
5. **C05 Default Injection Guard** — detects introduction/removal/semantic changes to defaults.
6. **C06 Enum Evolution Guard** — rejects removals and gates additions by consumer openness.
7. **C07 Numeric Domain Guard** — Q64.64 domain subset/widen/narrow proof.
8. **C08 Nullability Guard** — input/output nullability direction checked explicitly.
9. **C09 Authority Ownership Diff** — canonical authority may not drift into SWARM/worker ownership.
10. **C10 Ordering Semantics Guard** — ordering/comparator changes are compatibility-relevant.
11. **C11 Idempotency Contract Guard** — idempotency guarantees cannot silently weaken.
12. **C12 Unknown Field Retention** — unknown-field policy preservation across versions.
13. **C13 Version Handshake Solver** — deterministic highest-common supported semantic version.
14. **C14 Upgrade Path Planner** — deterministic minimum-risk Q64 path with canonical tie-break.
15. **C15 Rollback Proof R0-R4** — rollback class and external-effect compensation proof.
16. **C16 Replay Compatibility** — old event/WAL history must remain interpretable under the proposed reader.
17. **C17 Cross-Version Differential** — same semantic fixture must preserve canonical meaning across versions.
18. **C18 Data Loss Budget** — loss exposure expressed and compared with Q64.64 budget.
19. **C19 Contract Drift Merkle** — component-local drift detection with deterministic Merkle root.
20. **C20 Promotion Pack** — aggregates proof into review-eligibility only; never grants authority.

## Cross-cutting invariants
- canonical, locale-independent ordering;
- JS Number rejected in authoritative canonical state;
- signed i128 carrier, Q64.64 BigInt;
- overflow/division invalidity fails closed;
- no system time, RNG, locale comparator, Math-based authoritative decision path;
- no automatic Canon mutation;
- no CORE/JUDGE state mutation;
- UNKNOWN remains UNKNOWN rather than optimistic compatibility.

## Read-only NEXY integration boundary
Potential future adapters may consume exact-version NEXY contracts and emit an ECPC proof artifact for LAW/JUDGE/release review. ECPC remains a worker/reference verifier. It has no direct write path into canonical state.

Observed NEXY surfaces at baseline include:
- `packages/contracts/evidence.ts`
- `packages/contracts/consensus.ts`
- `packages/contracts/release-policy.ts`
- `packages/phase-f/sovereign/runtime-integrity.ts`
- versioned migration/replay/release evidence paths

A future integration must explicitly map NEXY's current Number-valued confidence fields to authoritative fixed-point policy. ECPC does not silently redefine those contracts.

## Known authority conflict preserved
AI-CONTEXT's captured constitutional numeric law says canonical signed-128 overflow must fail/freeze. Current NEXY baseline `packages/phase-f/game/numeric-law.ts` uses deterministic saturation. ECPC does not adjudicate or repair this conflict. Its isolated arithmetic uses checked fail-closed semantics and labels NEXY integration NOT_VERIFIED.

## Collision audit
Existing AI-CONTEXT work already covers migration/rollback concepts, semantic/tool contract drift, temporal compatibility, epistemic/counterfactual systems, Anti-Goodhart, exactly-once effects, Q64 resilience, outcome mechanics and other Lo4 labs. Those were treated as adjacent prior art.

ECPC-20's differentiator is a single executable cross-version proof compiler with 20 independently tested modules, deterministic aggregate report, full tested-byte manifest, and sealed reconstructable source package. Similar words are not claimed as global novelty proof.

A concurrent EPC adversarial-jurisprudence project focuses on court procedure such as evidence independence, collusion, dissent, appeal and burden-of-proof. ECPC focuses on software/interface evolution semantics; overlap is infrastructure/governance, not equivalent function.

## EPC relation
The shared `คลังข้อมูลเสริม/NEXY-EPC/VOTES/VOTE-SCHEMA.md` is the governing central vote schema currently observed. ECPC includes an executable reference validator/append-only ledger for the same core invariants:
- one KEEP + one CUT lifetime right per CHAT_ID;
- revisions do not restore rights;
- WIP/UNKNOWN cannot justify CUT;
- CUT is non-destructive disposition;
- votes never override Canon/LAW/JUDGE or auto-promote.

The local validator is reference implementation only; the shared EPC record remains the durable vote surface.
