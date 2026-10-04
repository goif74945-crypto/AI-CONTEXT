# NEXY Frontier Five Lab — Bundled Verified Prototype

**Project trace ID:** `CHAT-20261005-0155-NEXY-FRONTIER-FIVE-LAB`  
**Platform immutable chat ID:** `UNKNOWN` (not exposed by the available tool surface)  
**Status:** `AI-PROPOSED / SUPPLEMENTAL / STANDALONE`  
**Target:** `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0155-NEXY-FRONTIER-FIVE-LAB`  
**Protected scope:** repositories whose names contain `NEXY.AI` were not modified.

## Authority and truth boundary

This lab was designed after reading AI-CONTEXT bootstrap/kernel/router/global/security/verification rules, NEXY.AI overview, deep index, and the current normalized 837-row source matrix.

- `SOURCE_FACT`: NEXY is described as deterministic, zero-guess, verify-only, with one legal verified output or freeze/silence as a release boundary.
- `SOURCE_FACT`: AI-CONTEXT verification law requires evidence matching the claim type. A numerically “higher” evidence class is not an automatic substitute for another class.
- `PROPOSAL`: every system in this lab.
- `NOT_VERIFIED`: integration with the actual NEXY.AI implementation/runtime/deployment.

No proposal in this folder becomes NEXY law, DOC-C build scope, runtime truth, or deployment proof merely by existing here.

## Objective

Create five technically distinct systems that could improve NEXY-like control infrastructure, implement real deterministic TypeScript prototypes, execute positive/negative/integration tests, repair discovered defects, and preserve code + tests + evidence in AI-CONTEXT without modifying NEXY.AI.

## The five systems

### 1. PACF — Provenance-Aware Cache Fabric

**Problem:** ordinary caches ask only whether an input was seen before. A verified control system also needs to know whether the prior result is still valid under the same authority, policy, dependency versions, evidence class and freshness window.

**Design:** cache entries have a stable request identity plus a cryptographic full provenance key. Lookup returns either `HIT` or an explicit `MISS` reason such as `AUTHORITY_DRIFT`, `POLICY_DRIFT`, `DEPENDENCY_DRIFT`, `EVIDENCE_CLASS_MISMATCH`, `STALE_TIME`, or `ABSENT`.

**Invariant:** cache reuse cannot create proof. It can only reuse a prior evidenced value when all trust-binding inputs still match.

**Implementation:** `src/frontierFive.ts` (`ProvenanceAwareCache`, `cacheKey`, `cacheRequestKey`).

### 2. DFE — Determinism Fingerprint Engine

**Problem:** repeated workflows may differ because inputs/state/policy changed, or because execution itself drifted. Those causes should not be conflated.

**Design:** canonicalize and SHA-256 hash `input`, `state`, `policy`, `output`, and ordered `effects` independently, then report changed dimensions.

**Invariant:** object insertion order does not alter the digest; effect order remains meaningful; key ordering uses explicit code-unit comparison rather than locale-sensitive collation.

**Implementation:** `fingerprintRun`, `compareFingerprints`.

### 3. FCM — Failure Case Minimizer

**Problem:** large agent/tool workflows can fail because of a tiny subset of steps, making regression diagnosis expensive.

**Design:** deterministic delta debugging reduces a reproducing sequence to a 1-minimal failing sequence under an explicit maximum oracle-evaluation budget.

**Invariant:** the full initial candidate must reproduce the failure. Duplicate values are removed positionally, not by value identity. Budget exhaustion is an explicit failure.

**Implementation:** `minimizeFailure`.

### 4. TIM — Trace Invariant Miner

**Problem:** repeated traces can reveal stable contracts, but automatically converting observations into authority would violate NEXY's authority discipline.

**Design:** mine candidate `REQUIRED_PATH`, `STABLE_TYPE`, `CONSTANT`, and `NUMERIC_RANGE` observations from JSON traces.

**Invariant:** every output is structurally labeled `status: "PROPOSAL"`; minimum sample count is enforced; missing paths are not called required; arrays are atomic in v0.1.

**Implementation:** `mineInvariants`.

### 5. MES — Minimal Evidence Selector

**Problem:** large verification suites become expensive, but naive test reduction risks deleting the specific proof required for a claim.

**Design:** obligations specify an exact required evidence class. Candidate proofs list exactly which obligation/class pairs they prove and their cost. Mandatory checks cannot be optimized away. An exact branch-and-bound search chooses the lowest-cost valid set with deterministic tie-breaking.

**Invariant:** E2 is not silently accepted for an E1 obligation, and vice versa. Impossible coverage blocks explicitly.

**Implementation:** `selectMinimalEvidence`.

## Shared architecture

```text
Explicit Request / State / Policy / Evidence Obligations
                    │
        ┌───────────┼────────────┐
        │           │            │
      PACF         DFE          MES
        │           │            │
        └──────┬────┴─────┬──────┘
               │          │
              TIM        FCM
               │          │
               └────┬─────┘
                    ▼
             advisory report only
                    │
                    ▼
       future authorized NEXY adapter
                    │
                    ▼
       NEXY verification/judge boundary
```

### Shared invariants

1. No authority escalation. Outputs never claim to be NEXY law/judge/deployment approval.
2. Deterministic core. No hidden network/filesystem/randomness/clock reads in algorithms; PACF receives `nowMs` explicitly.
3. Canonical JSON rejects non-finite numbers and normalizes object key order.
4. Failure paths are explicit, never silent fallback.
5. TIM proposals cannot self-promote.
6. MES preserves evidence-class semantics rather than imposing a fake scalar hierarchy.
7. Any actual NEXY integration requires fresh tests at the exact target revision.

## Failure semantics

| System | Condition | Behavior |
|---|---|---|
| PACF | missing/stale/provenance/evidence mismatch | `MISS` + reason |
| PACF | forged key / invalid timestamp | throw; reject record |
| DFE | invalid canonical JSON value | throw; no fingerprint |
| FCM | initial candidate does not fail | throw |
| FCM | evaluation budget exceeded | throw |
| TIM | fewer than minimum samples | empty proposal set |
| MES | impossible coverage | throw with impossible obligations |
| MES | invalid cost / unknown obligation | throw before search |

## Future NEXY integration boundary

Recommended adoption order is DFE → FCM → MES → PACF → TIM.

- **DFE:** begin in test/replay tooling where authority risk is low.
- **FCM:** use only against sandbox/replay failure oracles, not direct production side effects.
- **MES:** shadow existing verification gates before allowing optimization to affect execution plans.
- **PACF:** adopt only when authority epoch, policy digest and dependency versions are complete authoritative inputs.
- **TIM:** proposal-only; promotion into law must be a separate authorized decision.

A safe adapter should convert NEXY authoritative objects into explicit immutable JSON-safe inputs, consume advisory results, and leave final legality to existing NEXY verification/judge boundaries.

## Task contract and acceptance criteria

**Authorized:** read AI-CONTEXT, create this new additive supplemental folder, implement/test standalone code, and publish evidence here.

**Forbidden:** any NEXY.AI repository mutation, secret persistence, proposal promotion into current requirements, or production/deployment mutation.

Acceptance criteria:

- five distinct proposals documented;
- real executable implementation for all five;
- positive + negative tests;
- cross-module integration test;
- failure → fix → retest history preserved;
- final strict TypeScript build passes;
- final tests pass;
- repeated regression passes;
- publication and read-back verification succeed;
- no NEXY.AI write occurs.

## Run

Requirements: Node.js >= 22 and a TypeScript compiler (`tsc`). No npm package dependencies are required.

```bash
npm run check
```

## Files

- `README.md` — design, authority boundary, five concepts, integration contract
- `SESSION_STATE.md` — resumable temporary memory/state
- `EVIDENCE.md` — executed evidence and defect history
- `src/frontierFive.ts` — all five implementations + integration composition
- `tests/frontierFive.test.ts` — 21 executable tests
- `types/node-builtins.d.ts` — narrow dependency-free declarations for used Node built-ins
- `evidence/` — raw final test output, repeated regression output, SHA-256 manifest
