# Requirement / Evidence Ledger

| ID | Requirement | Implementation | Evidence | Status |
|---|---|---|---|---|
| R1 | Five distinct Lo4 systems | DESIGN + five audit modules | E0/E1/E2 | PASS locally |
| R2 | Q64.64 numeric semantics | `src/q64.mjs` + all audit calculations | E1/E2 | PASS locally |
| R3 | No binary float input at Q64 boundary | Q64 constructors | negative tests | PASS locally |
| R4 | Fail closed on bad counts/samples | common validators + modules | negative tests | PASS locally |
| R5 | No sensitive cohort inference | aggregate-only API | integration/API inspection | PASS for reference API |
| R6 | No Canon/release authority | pipeline contract | E1/E2 | PASS locally |
| R7 | Five-system integrated execution | `auditEquitableControlPack` | E3 integration tests | PASS locally |
| R8 | Deterministic stress behavior | `verify.mjs` | 56,448 checks / 20,000 packs | PASS locally |
| R9 | Durable AI-CONTEXT persistence | unique supplemental folder | GitHub atomic write/readback | NOT_VERIFIED until publish |
| R10 | NEXY.AI runtime integration | future adapters | runtime evidence | NOT_VERIFIED |
| R11 | Legal/statistical fairness validity | outside reference-code scope | domain study required | NOT_VERIFIED |
