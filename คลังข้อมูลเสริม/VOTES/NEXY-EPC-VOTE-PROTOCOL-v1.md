# NEXY Evolutionary Proposal Court (EPC) — Vote Protocol v1

STATUS: `Lo4 governance protocol / advisory / non-Canon`
DATE: `2026-10-05`

## Authority boundary
EPC vote artifacts are evidence/recommendations only. They cannot override Canon, User Law, NEXY::LAW, CORE/L1o, NEXY::JUDGE, or any release/deployment authority. SWARM/AI/Human auxiliary layers cannot use this protocol to bypass verification or mutate Core state.

## Lifetime vote rights per CHAT_ID
Each durable CHAT_ID has exactly:
- one KEEP round over its lifetime;
- one CUT round over its lifetime.

The following statuses consume neither right:
- `DEFER`
- `INSUFFICIENT_EVIDENCE`
- `WIP`

Historical KEEP/CUT results are immutable. New evidence may append a revision/evidence record, but cannot restore or create extra vote rights.

## Required fields for KEEP/CUT
Every formal vote must contain:

```text
VOTE_ID
CHAT_ID
ROUND = KEEP | CUT
TIMESTAMP

SPEC_ID / SPEC_HASH
NEXY_REPO
NEXY_BRANCH
NEXY_COMMIT_SHA
AI_CONTEXT_COMMIT_SHA

CANDIDATE_ID
CANDIDATE_PATH

STATUS_BEFORE
VERDICT

SPEC_EVIDENCE
CODE_EVIDENCE
AI_CONTEXT_EVIDENCE

ARCHITECTURE_FIT
CANON_COMPATIBILITY
NOVELTY
OVERLAP
IMPLEMENTATION_VALUE
VERIFICATION_VALUE
SECURITY_IMPACT
DETERMINISM_IMPACT
MAINTENANCE_COST

CONFLICTS
DUPLICATES
DEPENDENCIES

FACT
ASSUMPTION
UNKNOWN

REASON
COUNTERARGUMENT
FINAL_JUSTIFICATION
```

## Seven anti-random-vote locks
1. One CHAT_ID may use KEEP once and CUT once, total lifetime.
2. Never edit a historical vote result in place. Append new evidence/revision lineage instead; vote rights do not reset.
3. Read the governing Spec, real NEXY code at an exact commit, and current AI-CONTEXT before a formal vote.
4. UNKNOWN/WIP/INSUFFICIENT_EVIDENCE cannot be a sufficient reason for CUT.
5. Duplication must be proven semantically with cited files/functions/modules/Canon clauses and exact commits; similar names are insufficient.
6. CUT defaults to `ARCHIVE / REJECTED / SUPERSEDED`, never physical deletion.
7. Vote scores cannot override Canon/Law/JUDGE and cannot auto-promote a system into NEXY.AI.

## Evidence discipline
“KEEP because good” and “CUT because duplicate” are invalid. A duplicate claim must identify the exact target and semantic overlap. A Canon-conflict claim must cite the controlling clause/source and exact repository revision where relevant.

## Concurrency law
Each chat writes only its own vote receipt filename. Shared protocol revisions must be append-only versioned files, never silent rewrites. This prevents parallel chats from erasing one another's evidence.
