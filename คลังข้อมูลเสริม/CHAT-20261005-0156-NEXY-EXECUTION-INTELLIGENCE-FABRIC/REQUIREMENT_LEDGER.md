# Requirement Ledger

| ID | Requirement | Implementation | Evidence target | Status before persistence |
|---|---|---|---|---|
| R1 | Five distinct AI-proposed concepts | `concepts/*` | File inventory | PASS locally |
| R2 | Explicit non-canon labeling | README + all DESIGN docs | Presence/read-back | PASS locally |
| R3 | Deterministic normalized outputs | stable hashes + sorted set-like inputs | unit + fuzz | PASS locally |
| R4 | Fail closed on unsafe/malformed state | all five engines + CLI | negative tests | PASS locally |
| R5 | Goal completion predicate executable | GSC | unit tests | PASS locally |
| R6 | Minimum blocking question/probe set | UCP exact search | unit + fuzz | PASS locally |
| R7 | Minimum sufficient assurance with independence | ABP exact search | unit + fuzz | PASS locally |
| R8 | Rollback legality computed before mutation | RE | unit tests | PASS locally |
| R9 | Negative vectors generated from contract | CES | unit tests | PASS locally |
| R10 | Five engines compose without NEXY.AI imports | integration fabric | integration tests | PASS locally |
| R11 | CLI exposes READY/ASK/FREEZE contract | `cli.py` | subprocess tests | PASS locally |
| R12 | No protected repository mutation | execution boundary | GitHub mutation audit | NOT_VERIFIED until persistence audit |
| R13 | Persisted bytes equal tested bytes | integrity manifest | GitHub read-back hashes | NOT_VERIFIED until persistence |
