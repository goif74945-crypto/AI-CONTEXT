# LEDGER Execution 008
TASK_ID: 20261008-NEXY-NORMAL-CHAT-EXECUTION-008-CROSS
PRODUCT HEAD: 44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL MAIN PREWRITE: 8e787a81e11fc00f2bd7d5ca68474f0b774085c1
SPEC SHA-256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7 (recomputed from mounted DOCX 2026-10-08)
SOURCE BLOBS: dispatch.ts 002eef253ce836e2cd0e200f5d15cb5042cdeb29; cage.ts 5afd464ed39470381ef1df643a630e1f431817dc; vnext-config.ts a3141a649be7e40ec79f417f53bba9b73081232b; matrix historical f18b4874b875ca713dd007c7feddffba13d0f380

| Evidence | Status | Source |
|---|---|---|
| Canonical DOCX | VERIFIED BY HASH | mounted DOCX 12,537 paragraphs; P04137-49 isolation, P09945-48 Queue |
| Queue ID-only success/failure | VERIFIED SOURCE DEFECT | dispatch blob 002eef253ce836e2cd0e200f5d15cb5042cdeb29 |
| Product integrated regression authored | FILE_CREATED_NOT_RUN | PATCHES/008/queue-cancel-race-008.spec.ts |
| CAS queue full-source candidate | FILE_CREATED_NOT_APPLIED | PATCHES/008/queue-dispatch-cas.patch and queue-dispatch-cas-candidate.ts |
| Cage fallback exposure | VERIFIED SOURCE RISK | cage blob 5afd464ed39470381ef1df643a630e1f431817dc |
| Cage fail-closed candidate | FILE_CREATED_NOT_APPLIED | PATCHES/008/cage-bwrap-fail-closed.patch |
| GitHub Actions E7 rerun | ACCEPTED, RESULT_UNKNOWN | job 113193487979, initial run 37741650376 |
| CI root cause | UNKNOWN | job steps empty; log fetch 404 |
| 98 row inventory | HISTORICAL IDS ONLY, SOURCE TRIAGE 13 | EVIDENCE/...008-98-current-head.tsv |
| AUTH-01 | DOCUMENT MATCH | SHA256 equals locked hash |
| DOC-E | NOT_AUTHORIZED | human signoffs/rollback/incident evidence absent |
AUDIT INVENTORY=98/98; SOURCE_TRIAGE=13/98; FULL SUBSTANTIVE AUDIT COVERAGE=NOT_COMPUTABLE (separate from inventory); ASSESSED COMPLETION=NOT_COMPUTABLE.
No mass status promotion; do not call source risk verified exploit.
