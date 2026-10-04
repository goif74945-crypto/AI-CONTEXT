# Read-Only NEXY.AI Compatibility Audit

Status: `PARTIAL / REFERENCE-LAB COMPATIBILITY ONLY`

This audit used read-only GitHub inspection of `goif74945-crypto/NEXY.AI-`. No mutation was performed.

## Observed repository facts
1. `README.md` describes NEXY as deterministic, fail-closed, and governed by an authority hierarchy. It documents canonical V-NEXT states and explicitly warns that descriptive README content is non-authoritative unless backed by higher authority.
2. `packages/contracts/evidence.ts` defines a strict Evidence item with source type, SHA-like hash, confidence, verification status, anchors, contradiction flag, and normalization version.
3. `packages/intelligence/rsel.ts` keeps risk/intelligence state distinct from execution state and fails closed when threshold authority or valid inputs are missing.
4. `apps/web/app/dialog/page.tsx` stores up to 32 browser-session context items and marks dialog output as presentation-only/request-only; explicit TASK intent hands off to CORE.
5. Repository search and README material show canonical hash-chained state/ledger behavior and canonical FSM already exist. NCAF REJ therefore must never be presented as replacement canonical state.

## Compatibility mapping
| NCAF | Candidate integration boundary | Must not do |
|---|---|---|
| CBA | browser/session or offline context preparation | infer canonical intent, mutate CORE, override CIRL |
| ECR | pre-canonical external evidence contradiction flagging | replace Lo3/Lo2 consensus/conflict law, authorize release |
| PRP | non-authoritative equivalent-provider scheduling | select truth winner, relax risk/safety constraints |
| REJ | external job checkpoint/resume metadata | become USL/FSM truth, assert canonical transition |
| FCE | retry-permitted external dependency isolation | intercept Safety Kernel/CORE freeze, retry no-retry components |

## Compatibility laws derived from observed state
- All NCAF outputs remain advisory until an authoritative NEXY spec explicitly adopts an interface.
- NCAF must never mint `STABLE`, `FREEZE`, `READY`, or other canonical FSM transitions.
- NCAF must not claim evidence minimum/release approval.
- Any future TypeScript/Rust adapter must validate against canonical NEXY contracts at the exact target revision.
- Any future runtime integration requires E3+ evidence and must be re-audited against the target NEXY commit.

## NOT VERIFIED
- No NEXY.AI code was modified or executed as part of this task.
- No NCAF ↔ NEXY runtime integration was executed.
- No performance/load benchmark was run in NEXY target runtime.
- Therefore “works inside NEXY.AI production” is explicitly NOT_VERIFIED.
