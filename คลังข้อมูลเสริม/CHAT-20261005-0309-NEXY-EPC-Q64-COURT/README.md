# NEXY Evolutionary Proposal Court (EPC)

Status: **IMPLEMENTED SUPPLEMENTAL Lo4 TOOL / AI-PROPOSED / NON-AUTHORITATIVE**

CHAT_ID: `CHAT-20261005-0309-NEXY-EPC-Q64-COURT`

EPC is a deterministic court-record layer for NEXY Lo4 proposals. It makes KEEP/CUT decisions evidence-bound, replayable, lifetime-limited per chat, Q64.64-scored, append-only, and incapable of silently becoming Canon.

## Authority boundary

EPC does **not** replace `NEXY-PROPOSAL-FORGE`, `NEXY::CORE`, `NEXY::JUDGE`, `NEXY::LAW`, SWARM consensus, or formal promotion.

Proposal Forge packages/evaluates proposals for review. EPC governs the later advisory adjudication record: one KEEP + one CUT entitlement per CHAT_ID, burden of proof, non-vote dispositions, immutable revisions, exact repository/spec snapshots, semantic CUT proof, ledger sealing, and promotion barriers.

`goif74945-crypto/NEXY.AI-` was inspected **read-only**. This work package did not modify it.

## Hard guarantees implemented

- Q64.64 fixed-point score arithmetic using bigint raw values; no float score arithmetic.
- One finalized KEEP + one finalized CUT maximum per CHAT_ID.
- DEFER / INSUFFICIENT_EVIDENCE / WIP consume neither right.
- WIP/UNKNOWN alone cannot justify CUT.
- Every CUT basis must bind directly to factual evidence.
- Duplicate CUT requires exact target path/symbol/commit and multi-dimensional semantic proof.
- Canon conflict proof requires exact Canon locator + commit + evidence.
- KEEP_MERGE requires a real semantic merge target.
- CUT_SUPERSEDED requires a real semantic replacement target.
- Append-only hash-chain ledger plus sealed head/length verification detects mutation and tail truncation.
- Evidence corrections append revision lineage; old verdicts are not rewritten.
- CUT is classification only; physical deletion is forbidden.
- Scores never override Canon/LAW/CORE/JUDGE gates.
- Promotion packets are non-authoritative and cannot authorize integration.
- JUDGE bridge output is advisory and `autoExecutable=false`.

## Implemented concepts

Exactly 20 concepts are registered and test-enforced. See `03_TWENTY_CONCEPTS.md`.

## Verification

Local strict TypeScript compile: **PASS**.

Executed runtime tests: **33/33 PASS**.

Hardening included Q64 overflow/divide-by-zero, 1,000 deterministic rational-product property cases, stale-SHA freeze, semantic duplicate proof, direct CUT-evidence binding, independent KEEP/CUT rights, ledger tamper detection, sealed tail-truncation detection, immutable revisions, and promotion barriers.

## Source bundle

The full modular Design + Code + Test + Evidence project is persisted as five base64 chunks under `bundle/`.

Reconstruct:

```bash
cat bundle/NEXY-EPC-Q64-COURT-source.tar.gz.b64.part00 \
    bundle/NEXY-EPC-Q64-COURT-source.tar.gz.b64.part01 \
    bundle/NEXY-EPC-Q64-COURT-source.tar.gz.b64.part02 \
    bundle/NEXY-EPC-Q64-COURT-source.tar.gz.b64.part03 \
    bundle/NEXY-EPC-Q64-COURT-source.tar.gz.b64.part04 \
  | base64 -d > NEXY-EPC-Q64-COURT-source.tar.gz

sha256sum NEXY-EPC-Q64-COURT-source.tar.gz
tar -xzf NEXY-EPC-Q64-COURT-source.tar.gz
```

Expected archive SHA-256:

`416e04f92dc27e8c67ad63646f41821c159e86433a820bf81c919b39ebecdb24`

Chunk byte sizes: 8000, 8000, 8000, 8000, 7744.

Chunk SHA-256 values:
- part00: `66042d70f3fa524239d205143cc98f86b6f503f217bd27056e48147f47a511a1`
- part01: `8fdd83aa002cef9bd05fc01915e4aff491aeb82f44ba4b220a787593b64b153c`
- part02: `d8af82ae8b810c8be84662821c728a81e231546f41990a647efdd8236eb6f102`
- part03: `206f387de73a5989c986f906a039cfa4e256b756883e3f630e14937b2d2b3e1f`
- part04: `03d406e3f879b7459c8e5811946f88e5d50d1921d3ab12a10483716a911cc5bd`

## Snapshot used for design/verification

NEXY repository: `goif74945-crypto/NEXY.AI-`  
Branch: `NEXY.ai`  
Inspected commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

AI-CONTEXT pre-persistence snapshot used by the novelty/collision re-check:
`c4bc5809269e0709b30b47a49533fe1c50518c75`

Preserved IGNIS source:
`REFERENCES/NEXY/2026-10-04/04-NEXY-IGNIS-source.txt`

## Vote consumption

Building EPC did **not** cast a vote.

For `CHAT-20261005-0309-NEXY-EPC-Q64-COURT`:
- KEEP = UNUSED
- CUT = UNUSED

## Truth boundary

FACT: EPC is implemented and locally verified at 33/33 tests before persistence.

FACT: its archive and human-readable design/evidence records are stored under this AI-CONTEXT directory.

NOT_VERIFIED: absolute semantic superiority over every artifact ever produced by every parallel chat. Exact collision searches were clean at the captured AI-CONTEXT head and Proposal Forge was semantically reviewed, but a corpus-wide proof of universal superiority was not fabricated.
