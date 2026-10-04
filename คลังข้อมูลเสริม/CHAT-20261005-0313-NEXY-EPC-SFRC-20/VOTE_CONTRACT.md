# EPC Vote Contract — SFRC Chat

CHAT_ID: `CHAT-20261005-0313-NEXY-EPC-SFRC-20`

## Lifetime entitlement
- KEEP: maximum 1 consumed round.
- CUT: maximum 1 consumed round.
- DEFER / INSUFFICIENT_EVIDENCE / WIP: does not consume either round.

A historical vote verdict is immutable. New evidence creates a new evidence/amendment record, not a rewritten verdict and not new vote entitlement.

## Mandatory fields

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

## Hard vote law
1. One CHAT_ID can consume KEEP once and CUT once only.
2. Prior verdicts cannot be edited; append evidence revisions instead.
3. A vote requires current Spec + real NEXY code + current AI-CONTEXT + candidate evidence.
4. UNKNOWN/WIP/INSUFFICIENT_EVIDENCE alone cannot justify CUT.
5. Duplicate claims require semantic evidence naming the overlapping artifact/function/module and inspected commit; name similarity is insufficient.
6. CUT means ARCHIVE/REJECTED/SUPERSEDED by default, never physical deletion.
7. Vote/score never overrides Canon, LAW, CORE, JUDGE or verification and never auto-promotes.
