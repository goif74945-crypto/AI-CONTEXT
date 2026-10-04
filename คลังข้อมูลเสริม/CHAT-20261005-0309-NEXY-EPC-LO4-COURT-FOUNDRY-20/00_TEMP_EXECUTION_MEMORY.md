# EPC Lo4 Court Foundry 20 — Temporary Execution Memory

CHAT_ID: `CHAT-20261005-0309-NEXY-EPC-LO4-COURT-FOUNDRY-20`
PLATFORM_NATIVE_CHAT_ID: `UNKNOWN_NOT_EXPOSED_TO_AVAILABLE_TOOLS`
CREATED_LOCAL: `2026-10-05T03:09+07:00`
STATUS: `IN_PROGRESS`
AUTHORITY_CLASS: `Lo4_AI_PROPOSAL_ONLY / NON_CANONICAL / NON_GOVERNING`

## Immutable scope
- Writable repo: `goif74945-crypto/AI-CONTEXT` only.
- Protected repo: every repository whose name contains `NEXY.AI`; read-only inspection only.
- NEXY repository observed: `goif74945-crypto/NEXY.AI-`, branch `NEXY.ai`, commit `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`.
- AI-CONTEXT observed pre-work HEAD: `b76c4a2bae45b3e9fb2367cc467751df8a751d61`.
- Canon promotion: forbidden.
- CORE/JUDGE/LAW/SWARM state mutation: forbidden.
- Vote outputs are advisory evidence only.

## Governing inputs
1. Current user directive defining NEXY Evolutionary Proposal Court (EPC), KEEP/CUT rights, DEFER/WIP rules, required vote fields, and anti-random-vote constraints.
2. AI-CONTEXT `AI-EXECUTION-KERNEL.md`, `rules/GLOBAL.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`.
3. NEXY project context `projects/NEXY.AI/overview.md` and normalized 837-row matrix.
4. Read-only NEXY exact head stated above.
5. Existing supplemental implementations including NEXY Proposal Forge and Lo4 Promotion Gate, used as collision boundaries rather than copied functionality.

## Current architecture decision
Build one coherent standalone package: **EPC Court Foundry 20**.
All 20 court organs:
- use checked signed Q64.64 where numeric scoring exists;
- are deterministic;
- fail closed on malformed/insufficient critical evidence;
- cannot promote, mutate Canon, mutate NEXY runtime state, or delete candidates;
- emit advisory court records only.

## Collision exclusions already established
- Do not recreate Proposal Forge duplicate/evidence pre-screen.
- Do not recreate Lo4 Promotion Gate eligibility scoring.
- EPC owns vote-right enforcement, immutable ballot lineage, commit pinning, WIP/CUT law, court replay, disposition semantics, and evidence-bound adjudication.

## Vote budget
- KEEP round remaining: 1.
- CUT round remaining: 1.
- DEFER / INSUFFICIENT_EVIDENCE / WIP does not consume a round.
- Existing vote records must never be edited to change verdict; amendments are append-only evidence lineage.

## Resume rule
Refresh AI-CONTEXT HEAD, re-read this file, continue from latest verified local/package state, and never infer PASS without executable evidence.
