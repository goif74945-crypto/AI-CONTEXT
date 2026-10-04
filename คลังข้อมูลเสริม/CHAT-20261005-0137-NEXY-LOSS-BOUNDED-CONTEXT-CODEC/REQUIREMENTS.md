# LBCC Requirement Ledger

Status labels follow AI-CONTEXT verification law.

| ID | Requirement | Authority | Implementation | Required evidence |
|---|---|---|---|---|
| R1 | Deterministic output for identical input + policy | NEXY deterministic direction + project design | canonical JSON, stable sort, integer scoring | E2 |
| R2 | Never silently drop immutable records | project design + zero-guess/freeze principles | protected set + FREEZE | E2 negative |
| R3 | Preserve `UNKNOWN` and `CONFLICT` by default | AI-CONTEXT truth model | protected truth classes | E2 negative |
| R4 | Preserve provenance/evidence for retained atoms | memory/provenance rules | atom schema | E2 |
| R5 | Quantify loss without floating-point nondeterminism | project design | integer importance + ppm | E2 |
| R6 | Enforce canonical capsule byte budget | project design | canonical UTF-8 byte length | E2 |
| R7 | Freeze when loss budget cannot be met | NEXY freeze direction | policy gate | E2 negative |
| R8 | Detect source/result tampering | evidence integrity design | SHA-256 commitments + verifier | E2 |
| R9 | Refuse likely secrets by default | security rule | sensitive scanner | E2 negative |
| R10 | No runtime dependency on an LLM/provider | model independence | stdlib-only core | E1 inspection/compile |
| R11 | Provide machine-readable integration contract | user objective | JSON schemas documented in contract | E0 + E2 CLI |
| R12 | CLI compact/verify path works end-to-end | user objective | `lbcc.cli` | E3 subprocess |
| R13 | Invalid/duplicate atom IDs fail closed | integrity requirement | validation | E2 negative |
| R14 | Full source can be rehydrated only with matching ledger/store | audit/replay requirement | `rehydrate` | E2 |
| R15 | No mutation of any repository named NEXY.AI | explicit user scope | operational boundary | repository evidence |
