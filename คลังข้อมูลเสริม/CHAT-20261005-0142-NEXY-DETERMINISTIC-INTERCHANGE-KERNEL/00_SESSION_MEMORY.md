# Temporary / Resumable Session Memory

## Work ID
`CHAT-20261005-0142-NEXY-DETERMINISTIC-INTERCHANGE-KERNEL`

This is an **AI-CONTEXT work identifier derived from the local session timestamp**, not a claim that the ChatGPT platform exposed an internal conversation ID.

## Objective
Create a new, non-duplicative, useful-for-NEXY standalone engineering project under `AI-CONTEXT/คลังข้อมูลเสริม/` without modifying any repository whose name contains `NEXY.AI`.

## Protected scope
- Any repository with `NEXY.AI` in its name: read-only unless explicitly authorized by the user.
- Existing sibling projects in `คลังข้อมูลเสริม/`: do not modify.

## Selected concept
NEXY Deterministic Interchange Kernel (NDIK): deterministic canonical serialization + proof-carrying envelope reference implementation.

## Why selected
The existing supplemental catalog already includes formal assurance, truth/evidence compilers, counterfactual systems, context/privacy firewalls, resource governance, tool-contract drift, concurrency, side-effect transactions, numeric integrity, and model substitution. NDIK targets a lower-level interchange invariant: identical logical data must have stable bytes and identity across reordering and benign Unicode representation differences, while ambiguous numeric/data shapes fail closed.

## Current state
- design drafted;
- Python reference implementation created;
- deterministic and negative tests created;
- local verification required before repository publication.

## Resume rule
Do not claim completion from file existence. Re-run the recorded verification commands and compare hashes if implementation changes.

## Verification checkpoint
- compile: PASS;
- pytest: 33/33 PASS;
- demo: PASS;
- deterministic property grid: PASS;
- conformance vectors: PASS;
- benchmark observation captured;
- cross-language equivalence: NOT VERIFIED;
- NEXY production integration: NOT PERFORMED / OUT OF SCOPE.
