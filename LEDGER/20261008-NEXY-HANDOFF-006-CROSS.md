# LEDGER — handoff 006 CROSS
| Finding | Provenance | Current claim | Disposition |
| --- | --- | --- | --- |
| AUTH-01 | locally hashed uploaded DOCX | SPEC SOURCE SHA256 MATCH | VERIFIED SOURCE only |
| AUTH-02 | P09837-P09845 in direct DOCX | DOC-C build vs DOC-E deploy distinction | VERIFIED SOURCE only |
| AUTH-03 | P09930-P09938 + packages/api/vnext-config.ts blob a3141a649be7e40ec79f417f53bba9b73081232b | canonical values match static config | SOURCE VERIFIED WITH LIMITS |
| QUEUE-02 | dispatch.ts blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29 | potential terminal-status overwrite on await boundary | SOURCE-REACHABLE RISK, no DB test |
| QUEUE-04 | P09945-P09948 + config blob a3141a649be7e40ec79f417f53bba9b73081232b | TTL=900000 concurrency=10 | SOURCE VERIFIED WITH LIMITS |
| QUEUE-06 | tick.ts 517614809c8cefa3e516348b1268f6dca4a744e5; dispatch.ts 002eef... | fails closed without injected TSA time | current-head SOURCE VERIFIED, browser NOT_RUN |
| EXP-05 | cage.ts blob 5afd464ed39470381ef1df643a630e1f431817dc | bwrap-false Linux direct spawn path; seccomp not applied in examined code | SECURITY REVIEW REQUIRED |
| GATE-03 | current-head GitHub API statuses=[]; workflow-runs=[] PR-only; dispatch rejected 403 | actual CI unknown | NOT_VERIFIED / DISPATCH_BLOCKED |
| GATE-06 | DOC-E P10977-P10982 | signoffs rollback monitoring not provided | NOT_VERIFIED |
No 98-row baseline TSV records were mass-promoted. Historical 39/98 substantive audit coverage belongs to 8b406a63, not current-head coverage. Assessed completion for this chat is NOT_COMPUTABLE.
