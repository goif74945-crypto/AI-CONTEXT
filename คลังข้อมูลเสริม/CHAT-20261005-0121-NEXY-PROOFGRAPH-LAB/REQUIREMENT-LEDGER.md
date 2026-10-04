# Requirement Ledger

> **AI-PROPOSED / EXPERIMENTAL / NOT CANON**

| ID | Requirement | Implementation | Evidence target |
|---|---|---|---|
| R1 | Store only under `AI-CONTEXT/คลังข้อมูลเสริม` | repository path boundary | post-write path audit |
| R2 | Do not modify NEXY.AI repository | no connector writes to that repository | mutation log + final audit |
| R3 | Mark AI ideas as proposals, not canon | README/DESIGN/concepts markers + PG005 | unit test + scan |
| R4 | Detect deprecated 215 current-truth misuse | PG002 | unit test |
| R5 | Detect current normalized-row drift | PG003 | unit test |
| R6 | Detect Current Build denominator drift | PG004 | unit test |
| R7 | Detect broken local context links | PG001 | unit/scan behavior |
| R8 | Detect candidate secrets without echoing them | PG007 fingerprint-only evidence | unit test |
| R9 | Compute change impact | graph reverse closure | unit test |
| R10 | Detect stale authority binding | truth lock | unit test |
| R11 | Avoid network/dependency requirement | Python stdlib only | pyproject inspection + tests |
| R12 | Produce reproducible CLI | scan/graph/impact/lock/verify-lock | CLI integration test |
