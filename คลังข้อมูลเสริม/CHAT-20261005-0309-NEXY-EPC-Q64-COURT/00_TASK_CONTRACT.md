# NEXY Evolutionary Proposal Court (EPC) — Task Contract

Status: AI_PROPOSED_CONCEPT + IMPLEMENTED_SUPPLEMENTAL_TOOL + NON_AUTHORITATIVE
CHAT_ID: `CHAT-20261005-0309-NEXY-EPC-Q64-COURT`

## Objective
Build a deterministic Q64.64 adjudication layer for Lo4 proposals that can record one KEEP and one CUT round per CHAT_ID, preserve WIP/DEFER/INSUFFICIENT_EVIDENCE without consuming rights, bind every final vote to exact Spec/NEXY/AI-CONTEXT evidence, and produce an advisory review packet without changing NEXY Canon or Core state.

## In scope
- New files only under this project directory in `AI-CONTEXT/คลังข้อมูลเสริม/`.
- Read-only inspection of `goif74945-crypto/NEXY.AI-` and preserved NEXY IGNIS source.
- Q64.64 deterministic scoring.
- Append-only vote/revision ledger semantics.
- 20 court-specific innovations with implementation/test mapping.
- Tests, evidence, integration contract, and vote format.

## Protected scope
- **NO MUTATION** to `goif74945-crypto/NEXY.AI-`.
- No automatic Canon/LAW/Core/JUDGE state mutation.
- No automatic promotion.
- No physical deletion for CUT.
- No retroactive rewrite of prior vote verdicts.

## Authority
1. Current explicit user directive.
2. Preserved NEXY IGNIS source / locked authority rules.
3. Current NEXY.AI- source at inspected commit.
4. AI-CONTEXT execution kernel and current supplemental context.
5. EPC design in this folder, explicitly advisory.

## Success invariants
- Exactly 20 distinct concepts in registry.
- One KEEP + one CUT max per CHAT_ID.
- DEFER/INSUFFICIENT_EVIDENCE/WIP consumes neither round.
- UNKNOWN/WIP cannot serve as affirmative CUT proof.
- Semantic duplicate proof cites exact target path/symbol/commit and >=2 semantic dimensions.
- Q64.64 score math contains no floating-point operations.
- Score cannot override Canon/LAW.
- Promotion packet remains `authoritative=false`, `promotionAuthorized=false`, and requires JUDGE/Core/Law review.
- Hash-chain tampering is detected.
- Test suite passes before persistence claims are marked verified.

## Stop conditions
Freeze a final vote when the inspected snapshot is stale, evidence identity is invalid, a final vote round was already spent, or a request attempts authority escalation.
