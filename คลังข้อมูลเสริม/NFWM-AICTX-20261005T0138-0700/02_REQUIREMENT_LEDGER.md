# NFWM Requirement Ledger

| ID | Requirement | Authority | Implementation | Evidence | Status |
|---|---|---|---|---|---|
| R-001 | Work only in AI-CONTEXT isolated supplemental area | User | repository destination | GitHub read/write verification | PENDING_REMOTE |
| R-002 | Never mutate repo containing `NEXY.AI` | User | no connector write targets that repo | tool-call audit + final report | PASS_LOCAL_PROCESS |
| R-003 | Label concept as AI-proposed | User + AI-CONTEXT truth-class law | README/docs/profile status | static inspection | PASS |
| R-004 | Strictly parse trace input | AI-CONTEXT no-guess law | `model.py` | unit tests | PASS |
| R-005 | Deterministic invariant analysis | design | `analyzer.py` | unit tests | PASS |
| R-006 | Detect illegal FSM transition | DOC-C-derived external profile | `analyzer.py` | unit test | PASS |
| R-007 | Detect missing FREEZE incident link | DOC-C-derived external profile | `analyzer.py` | unit test | PASS |
| R-008 | Detect release after FREEZE in same run scope | DOC-C-derived external profile | `analyzer.py` | fixture + unit/CLI test | PASS |
| R-009 | Detect idempotency key starting different runs | DOC-C-derived external profile | `analyzer.py` | fixture + unit test | PASS |
| R-010 | Detect non-increasing sequence | proposed trace integrity rule | `analyzer.py` | unit test | PASS |
| R-011 | Produce deterministic 1-minimal witness | user objective + design | `minimize.py` | unit tests | PASS |
| R-012 | Canonical SHA-256 witness identity | evidence/replay design | `canonical.py` | hash determinism test | PASS |
| R-013 | Detect witness hash tampering | evidence integrity design | CLI verifier | negative CLI test | PASS |
| R-014 | Use no runtime third-party dependency | portability constraint | stdlib-only code | `pyproject.toml` + imports | PASS |
| R-015 | Preserve resumable execution state | user + AI-CONTEXT long-work law | `CHECKPOINT.md` | file presence/readback | PENDING_REMOTE |
| R-016 | Store executed test evidence | user + verification law | `evidence/` | commands + outputs + hashes | PASS_LOCAL |
| R-017 | Do not claim NEXY runtime/deployment verification | verification law | explicit docs/profile status | final audit | PASS |

## Acceptance rule

Remote project status may become `COMPLETE` only after all `PENDING_REMOTE` rows are written to AI-CONTEXT and read back successfully.
