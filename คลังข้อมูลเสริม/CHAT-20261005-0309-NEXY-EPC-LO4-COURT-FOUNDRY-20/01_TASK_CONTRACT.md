# Task Contract

## OBJECTIVE
Create exactly 20 implemented, deterministic Q64.64 mechanisms that materially improve the proposed NEXY Evolutionary Proposal Court while remaining Lo4 proposal-only and unable to alter NEXY Canon or runtime authority.

## PRIMARY DELIVERABLE
`EPC CourtScript-Q64`: a bounded typed policy compiler + VM whose 20 mechanisms make EPC policy executable as evidence rather than implicit prose.

## INPUTS / AUTHORITY
1. User EPC law in the current conversation.
2. Canonical NEXY source identity recorded in AI-CONTEXT: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`.
3. AI-CONTEXT current NEXY authority notes and 837-row normalized requirement matrix.
4. Read-only NEXY implementation at `goif74945-crypto/NEXY.AI-`, branch `NEXY.ai`, head `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
5. Existing EPC / supplemental candidate corpus, including the shared EPC proposal list and NX language prototype.

## IMMUTABLE CONSTRAINTS
- Never write to any repository whose name contains `NEXY.AI`.
- CourtScript is not Canon and cannot make itself Canon.
- SWARM/AI/EPC cannot mutate authoritative state.
- All authoritative numeric policy math inside this prototype is checked signed Q64.64 backed by bigint.
- No IEEE-754 decimal decision constants.
- Same source + same context must produce the same structural result and trace digest.
- Missing/UNKNOWN facts never become positive evidence.
- WIP / UNKNOWN / INSUFFICIENT_EVIDENCE cannot justify CUT.
- CUT means archival/rejected/superseded semantics, never physical deletion.
- One chat KEEP/CUT entitlement remains external EPC law; the compiler only emits review eligibility.

## OUT OF SCOPE
- NEXY.AI integration mutation.
- Production deployment.
- Replacing NX v0.1.
- Automatic semantic duplicate discovery from natural language.
- Human/CORE/JUDGE approval.
- Network or persistent storage adapters.

## ACCEPTANCE CRITERIA
- 20 mechanisms exist in source and are exercised by tests.
- strict TypeScript compile passes.
- negative tests cover authority escalation, WIP CUT, missing pins/proofs, UNKNOWN, numeric bounds and policy loosening.
- clean-archive re-execution passes.
- source bundle is hash-addressed and reconstructable.
- current corpus collision audit distinguishes the primary candidate from overlapping deferred baseline work.
