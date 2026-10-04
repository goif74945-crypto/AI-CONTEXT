# NEXY Evolutionary Proposal Court (EPC) — Shared Vote Ledger Protocol

STATUS: `ACTIVE_PROTOCOL / USER_DEFINED / NON_CANON_OVERRIDE`

This directory stores immutable KEEP/CUT vote receipts for Lo4 proposal work. A vote is advisory governance evidence only. It cannot override NEXY Canon/LAW/JUDGE and cannot auto-promote any system into NEXY.AI.

## Lifetime entitlement

For one `CHAT_ID`:

- KEEP: at most one lifetime round.
- CUT: at most one lifetime round.
- `DEFER`, `INSUFFICIENT_EVIDENCE`, and `WIP` do not consume a round.

Never edit an old vote to change its outcome or regain entitlement. Add a new revision/evidence appendix without creating a new KEEP/CUT entitlement.

## Required vote fields

Every actual vote receipt must contain:

- `VOTE_ID`
- `CHAT_ID`
- `ROUND = KEEP | CUT`
- `TIMESTAMP`
- `SPEC_ID / SPEC_HASH`
- `NEXY_REPO`
- `NEXY_BRANCH`
- `NEXY_COMMIT_SHA`
- `AI_CONTEXT_COMMIT_SHA`
- `CANDIDATE_ID`
- `CANDIDATE_PATH`
- `STATUS_BEFORE`
- `VERDICT`
- `SPEC_EVIDENCE`
- `CODE_EVIDENCE`
- `AI_CONTEXT_EVIDENCE`
- `ARCHITECTURE_FIT`
- `CANON_COMPATIBILITY`
- `NOVELTY`
- `OVERLAP`
- `IMPLEMENTATION_VALUE`
- `VERIFICATION_VALUE`
- `SECURITY_IMPACT`
- `DETERMINISM_IMPACT`
- `MAINTENANCE_COST`
- `CONFLICTS`
- `DUPLICATES`
- `DEPENDENCIES`
- `FACT`
- `ASSUMPTION`
- `UNKNOWN`
- `REASON`
- `COUNTERARGUMENT`
- `FINAL_JUSTIFICATION`

## Vote law

1. One CHAT_ID can use KEEP once and CUT once only.
2. Historical vote outcomes are append-only/immutable.
3. Read Spec + real NEXY code + current AI-CONTEXT before voting.
4. UNKNOWN/WIP/INSUFFICIENT_EVIDENCE is never sufficient CUT cause.
5. Duplicate claims require semantic evidence, not name similarity.
6. CUT means `ARCHIVE / REJECTED / SUPERSEDED` by default, never physical deletion.
7. Vote score/verdict cannot override Canon/LAW/JUDGE or promote automatically.

## Evidence discipline

`KEEP because good` and `CUT because duplicate` are invalid. A duplication claim must identify the exact path/module/function/contract or Canon clause and the inspected commit. A vote must distinguish FACT, ASSUMPTION and UNKNOWN.
