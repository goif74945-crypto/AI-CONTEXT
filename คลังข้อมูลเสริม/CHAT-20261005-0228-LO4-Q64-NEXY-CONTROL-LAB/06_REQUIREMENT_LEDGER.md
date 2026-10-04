# Requirement Ledger

| Requirement | Implementation | Evidence | Status |
|---|---|---|---|
| 20 distinct Lo4 ideas | 20 numbered concept folders | E0 + concept index | PASS |
| Q64.64 decision math | shared checked signed Q64.64 + 20 modules | E1 scan + E2 arithmetic tests | PASS |
| No hidden float decision primitives | strict scanner | E1 policy scan | PASS |
| Checked overflow / explicit failure | Q64 kernel + adversarial tests | E2 | PASS |
| Deterministic allocation totals | residual-safe budget/duty allocation | E2 deterministic tests | PASS |
| Stable IDs / tie behavior | lexical ordering + duplicate rejection | E2 | PASS |
| 20 modules compose | all-system integration test | E3 local | PASS |
| Source and compiled output agree | deterministic probe hash | source-vs-dist SHA-256 | PASS |
| NEXY-compatible adapter boundary | pure TS modules + integration contract | design/static only | NOT_VERIFIED in NEXY runtime |
| No NEXY.AI repository mutation | protected scope + write target limited to AI-CONTEXT folder | action-scope audit | PASS for this execution |
| Lo4 remains non-Canon | docs + promotion gate status wording | static review | PASS |
| NEXY E2E/runtime/deploy | intentionally outside authorized mutation scope | requires exact NEXY revision evidence | NOT_VERIFIED |
