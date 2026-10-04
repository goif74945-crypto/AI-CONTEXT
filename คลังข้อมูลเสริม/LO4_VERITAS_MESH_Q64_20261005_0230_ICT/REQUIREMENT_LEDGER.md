# Requirement Ledger

| Requirement | Implementation/evidence | Status |
|---|---|---|
| Work useful to NEXY.AI | Lo4 promotion laboratory + NEXY compatibility audit | PASS (design relevance) |
| Do not mutate NEXY.AI | only read NEXY files; no NEXY write calls executed | PASS |
| Store under AI-CONTEXT/คลังข้อมูลเสริม | unique additive work folder | PASS after remote write verification |
| 20 concepts | `src/models.ts` + `CONCEPTS.md` | PASS E0/E2 |
| Q64.64 | `src/q64.ts`, raw bigint Q64.64, UnitQ64 | PASS E1/E2 standalone |
| Run real tests | `npm test` | PASS E2, 17/17 |
| Fix failures and rerun | first run had 2 failures, second 1, final 17/17 | PASS, evidence retained in execution memory |
| Stress test | 2000 deterministic SignalFrames × 20 concepts | PASS E2 |
| Static type safety | `tsc -p tsconfig.json --pretty false` | PASS E1 |
| Runtime benchmark | 10,000 decisions | PASS local runtime observation only; not production proof |
| Design + Code + Test + Evidence together | project folder structure | PASS |
| Lo4 cannot override Canon | authority field + no PROMOTED state + hard false flag | PASS E1/E2 |
| Temporary memory/checkpoint | `TEMP_EXECUTION_MEMORY.md` | PASS |
| No duplication with previous chats | compared against known six existing knowledge packs | PARTIAL: global uniqueness across all unseen chat work cannot be proven from available index/search |
| Better than all previous chat systems | no objective global benchmark exists | UNKNOWN; no fabricated superiority claim |
| Internal ChatGPT chat ID | runtime does not expose an internal conversation ID | UNKNOWN; Work ID used instead |
