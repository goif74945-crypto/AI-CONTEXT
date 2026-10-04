# EPC Vote Template — Append-only receipt

VOTE_ID: `<required>`  
CHAT_ID: `<required>`  
ROUND: `KEEP | CUT`  
TIMESTAMP: `<required>`

SPEC_ID: `<required>`  
SPEC_HASH: `<required>`  
NEXY_REPO: `<required>`  
NEXY_BRANCH: `<required>`  
NEXY_COMMIT_SHA: `<required>`  
AI_CONTEXT_COMMIT_SHA: `<required>`

CANDIDATE_ID: `<required>`  
CANDIDATE_PATH: `<required>`  
STATUS_BEFORE: `<required>`  
VERDICT: `<required>`

SPEC_EVIDENCE: `<exact citations/paths/hash>`  
CODE_EVIDENCE: `<exact files/functions/commit>`  
AI_CONTEXT_EVIDENCE: `<exact paths/commit>`

ARCHITECTURE_FIT: `<evidence-backed assessment>`  
CANON_COMPATIBILITY: `<evidence-backed assessment>`  
NOVELTY: `<semantic comparison targets>`  
OVERLAP: `<exact overlaps>`  
IMPLEMENTATION_VALUE: `<assessment>`  
VERIFICATION_VALUE: `<assessment>`  
SECURITY_IMPACT: `<assessment>`  
DETERMINISM_IMPACT: `<assessment>`  
MAINTENANCE_COST: `<assessment>`

CONFLICTS: `<exact>`  
DUPLICATES: `<exact files/modules/functions or NONE proven>`  
DEPENDENCIES: `<exact>`

FACT: `<facts only>`  
ASSUMPTION: `<explicit>`  
UNKNOWN: `<explicit>`

REASON: `<required>`  
COUNTERARGUMENT: `<required>`  
FINAL_JUSTIFICATION: `<required>`

## Immutable handling
- One `CHAT_ID` consumes KEEP at most once and CUT at most once.
- Historical vote receipts are immutable; evidence amendments are new records.
- UNKNOWN/WIP/INSUFFICIENT_EVIDENCE cannot by themselves justify CUT.
- Semantic duplicate claims require exact evidence, not similar names.
- CUT means archive/rejected/superseded unless Canon explicitly says otherwise; never physical deletion by default.
- A vote cannot override Canon/LAW/JUDGE or auto-promote a candidate.
