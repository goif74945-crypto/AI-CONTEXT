# Durable Memory / Continuation Checkpoint

## Current state
A standalone canonical provider wire contract lab has been designed and implemented locally for later write-back into AI-CONTEXT.

## Why this project is distinct
Existing supplemental work covers capability negotiation, provider substitution safety, capability health routing, verification, semantics, and reliability. This lab isolates the lower-level streaming/tool-call/error wire contract that those higher layers depend on.

## Protected boundary
Do not write to any repository whose name contains `NEXY.AI`. Integration is documentation/interface-only unless the user later gives an explicit separate authorization.

## Resume sequence
1. Read `TASK_CONTRACT.md` and `DESIGN.md`.
2. Run `PYTHONPATH=src python -m unittest discover -s tests -v`.
3. If failing: fix smallest root cause, rerun full tests.
4. Update `EVIDENCE.md` and `REQUIREMENT_LEDGER.md` from actual results only.
5. Write all project files into a unique folder under `AI-CONTEXT/คลังข้อมูลเสริม/`.
6. Re-read repository paths and record commit SHAs.

## Remaining future work (not current completion requirement)
- official provider adapters using current provider documentation;
- captured real SDK/API fixtures;
- integration with NEXY runtime behind explicit authorization;
- performance/load characterization.
