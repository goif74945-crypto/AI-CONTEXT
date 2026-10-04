# Task Contract

Status: LOCKED FOR THIS LAB

## Objective
Design, implement, and verify an additive advisory system that detects semantic drift between adjacent representations of an authorized directive.

## Target
`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-DIRECTIVE-INTEGRITY-LAB`

## Authority sources
1. Explicit current user directive.
2. AI-CONTEXT `AI-EXECUTION-KERNEL.md` and global rules.
3. NEXY project authority hierarchy in `projects/NEXY.AI/*`.
4. Read-only NEXY repository observations for implementation-adjacent facts.
5. This lab's own AI proposals, which remain EXPERIMENTAL.

## Authorized scope
Add new files only in this lab folder; run standalone tests; inspect NEXY sources read-only.

## Protected scope
Every repository whose name contains `NEXY.AI`; all existing AI-CONTEXT content outside this unique folder; credentials/secrets; canonical project law.

## Success invariants
1. No protected repository mutation occurs.
2. Proposal is clearly labeled non-authoritative.
3. Reference engine is deterministic for equivalent set-like fields.
4. Material unauthorized semantic deltas cause FREEZE.
5. Explicit evidence-backed path authorization can admit a deliberate delta.
6. Negative paths are tested, not merely described.
7. Operator output contains concise facts/blockers rather than hidden reasoning.
8. Repository publication is fetch-verified and, where possible, exact-copy tested.

## Required evidence
E0 presence: repository listing/fetch.  
E1 static: Python compile and JSON Schema validation.  
E2 behavior: executed unit tests and CLI positive/negative fixtures.

No E3/E4/E5/E6 claim is permitted for this standalone lab.

## Stop conditions
FREEZE mutation if target repo changes, protected scope would be touched, path collision indicates another writer owns this exact folder, or authoritative rules conflict materially.

## Deliverables
Architecture/spec, schema, reference implementation, fixtures, tests, test matrix, adoption map, future ideas, validation evidence, final audit, temporary execution memory, and machine-readable manifest.
