# Requirement Ledger

| ID | Requirement | Implementation | Evidence | Status |
|---|---|---|---|---|
| R-001 | five new Lo4 proposals | UMC/DRC/VBR/RHL/EDB | design files + package | PASS |
| R-002 | remain non-Canon | labels + integration contract | repo artifacts | PASS |
| R-003 | Q64.64 quantitative logic | `qcp/fixed.py` + all engines | no-float AST, tests | PASS |
| R-004 | deterministic/fail-closed numeric core | checked 128-bit raw, ties-even, domain/overflow errors | unit tests | PASS |
| R-005 | code actually executes | `qcp/*` | 37/37 tests | PASS |
| R-006 | negative/adversarial paths | all engine tests | `FINAL_TESTS.txt` | PASS |
| R-007 | integration behavior | `qcp/pipeline.py` | pipeline integration tests | PASS, isolated E3 only |
| R-008 | stress/determinism | stress harness | 1,000 checks | PASS |
| R-009 | failure→fix→retest lineage | UMC correction + harness correction | failure/fix logs, RED/GREEN | PASS |
| R-010 | temporary memory for resumption | `00_TEMP_MEMORY.md` in AI-CONTEXT | GitHub commit 11599c5... | PASS presence; final update pending |
| R-011 | no NEXY.AI repository mutation | protected-scope lock | tool-action audit | PASS for this execution so far |
| R-012 | durable AI-CONTEXT publication/read-back | target folder | GitHub read-back | NOT_VERIFIED until publication step finishes |
| R-013 | production NEXY compatibility | proposed adapter contract | requires exact NEXY E3+ evidence | NOT_VERIFIED |
| R-014 | Canon promotion | formal future authority action | none | NOT_VERIFIED / intentionally absent |
