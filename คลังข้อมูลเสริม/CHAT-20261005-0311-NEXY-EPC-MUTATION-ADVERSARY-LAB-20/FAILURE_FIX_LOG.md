# Failure / Repair / Re-test Log

## F-001 — composition-preservation defect

Initial full verification ran 39 tests with one failure. Pairwise composition of `M06_WIP_AS_CUT_EVIDENCE` and `M07_VOTE_BUDGET_DOUBLE_SPEND` caused M07 to overwrite `requested_round` from CUT to KEEP, hiding the exact `WIP_NOT_CUT_REASON` violation.

Root cause: the double-spend mutant hard-set KEEP instead of consuming a second right for whichever round was already active.

Smallest safe repair: M07 was changed to inspect the existing requested round and increment the corresponding prior KEEP/CUT count without rewriting the round.

Re-verification: full compile/static/unit/adversarial/campaign verification passed. The suite covers all 190 mutation pairs and all twenty mutations combined.

Lesson: mutation infrastructure can itself contain semantic defects, so mutant-composition testing is mandatory evidence rather than decorative test count.
