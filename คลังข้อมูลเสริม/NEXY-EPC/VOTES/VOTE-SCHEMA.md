# EPC Vote Schema v1

Required fields:
VOTE_ID
CHAT_ID
ROUND = KEEP | CUT
TIMESTAMP
SPEC_ID
SPEC_HASH
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

## Invariants
1. One CHAT_ID may consume KEEP once and CUT once only.
2. Prior votes are append-only. Corrections use revisions/evidence attachments.
3. Spec + actual NEXY code + current AI-CONTEXT must be read before a binding vote.
4. UNKNOWN/WIP/DEFER cannot justify CUT.
5. Duplication requires semantic evidence at file/module/function/behavior level.
6. CUT implies archive/reject/supersede, never physical deletion.
7. Votes cannot override Canon/LAW/JUDGE or auto-promote.
8. Every negative claim must identify searched scope and evidence ref; absence of search evidence is UNKNOWN.
9. Evidence hashes/refs are mandatory for promotion-readiness claims.
10. Any contradiction between authoritative sources => FREEZE the affected verdict.
