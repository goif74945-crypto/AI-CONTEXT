# Requirement Ledger

| ID | Requirement | Implementation | Evidence | Status |
|---|---|---|---|---|
| L5-01 | five distinct Lo4 proposals | README + five subfolders | E0 local + design review | PASS |
| L5-02 | non-canonical labeling | README, designs, state | static inspection | PASS |
| L5-03 | no NEXY.AI mutation | task contract / publish scope | repository target restriction | PASS so far |
| L5-04 | executable code for every concept | five Python modules | compileall | PASS |
| L5-05 | real tests | five test modules | 20 executed tests | PASS |
| L5-06 | negative/failure paths | tests per module | executed unit output | PASS |
| L5-07 | deterministic behavior | engines + stress checks | seeded/repeat comparison | PASS |
| L5-08 | fail closed on unsafe verification size | RUC max assignment guard | unit test | PASS |
| L5-09 | absence not inferred from incomplete search | AEP | unit tests | PASS |
| L5-10 | semantic collisions explicit | SNCG | unit tests | PASS |
| L5-11 | mined invariants never canonized | TICM statuses | unit tests | PASS |
| L5-12 | requirement changes map to revalidation | RDRC | unit tests | PASS |
| L5-13 | final files published under AI-CONTEXT only | pending publish | Git tree re-read | PENDING |
| L5-14 | NEXY runtime compatibility | intentionally not integrated | none | NOT_VERIFIED |
