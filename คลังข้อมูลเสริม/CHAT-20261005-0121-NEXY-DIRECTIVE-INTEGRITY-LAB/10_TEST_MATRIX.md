# Test Matrix

Status: EXECUTED FOR STANDALONE REFERENCE MODEL

| ID | Property | Evidence | Expected |
|---|---|---|---|
| T01 | canonical set order independence | unit | equal digest |
| T02 | identical transition | unit | PASS |
| T03 | scope narrowing | unit | PASS |
| T04 | scope broadening | unit | FREEZE |
| T05 | explicit scope re-authorization | unit | PASS |
| T06 | constraint drop | unit | FREEZE |
| T07 | exclusion removal | unit | FREEZE |
| T08 | side-effect addition | unit | FREEZE |
| T09 | action drift | unit | FREEZE |
| T10 | target drift | unit | FREEZE |
| T11 | mutation escalation | unit | FREEZE |
| T12 | impact downgrade without evidence | unit | FREEZE |
| T13 | impact downgrade with evidence | unit | PASS |
| T14 | ambiguity close without clarification | unit | FREEZE |
| T15 | ambiguity close with clarification | unit | PASS |
| T16 | authority removal | unit | FREEZE |
| T17 | parent digest mismatch | unit | FREEZE |
| T18 | duplicate grant path | unit | exception/reject |
| T19 | operator explanation excludes COT field | unit | PASS |
| T20 | mapping round-trip | unit | stable |
| T21 | blank set item | unit | reject |
| T22 | CLI exit codes | unit | PASS=0, FREEZE=2 |

Additional static gates: Python bytecode compile, JSON parse, JSON Schema validation of fixture snapshots. CLI fixture gates: safe transition exits 0; broadened transition exits 2.
