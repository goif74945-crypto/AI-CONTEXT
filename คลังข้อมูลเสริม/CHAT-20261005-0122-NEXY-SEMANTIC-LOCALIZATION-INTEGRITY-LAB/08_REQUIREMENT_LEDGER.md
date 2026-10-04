# Requirement Ledger — Final

| ID | Requirement | Authority | Evidence | Final status |
|---|---|---|---|---|
| R01 | Mutate AI-CONTEXT only | User | Session GitHub write target audit | PASS |
| R02 | Never mutate a repository whose name contains `NEXY.AI` | User | All session write calls targeted `goif74945-crypto/AI-CONTEXT` | PASS |
| R03 | Create work under `คลังข้อมูลเสริม` | User | Dedicated session folder present | PASS |
| R04 | Avoid duplicating other chats | User | Recent sibling commit/search inspection; initial overlapping idea rejected | PASS |
| R05 | Clearly mark AI-generated ideas as proposals | User + AI-CONTEXT authority law | Docs + machine report `AI_PROPOSED_CONCEPT_NOT_ADOPTED` | PASS |
| R06 | Create a substantial new project and architecture | User | README, concept, architecture, invariants, adoption gates, future concepts | PASS |
| R07 | Implement working code from the idea | User | Dependency-free Node.js reference engine + CLI + policy + schemas | PASS |
| R08 | Preserve numbers | Proposal | executed adversarial tests | PASS |
| R09 | Preserve semantic units | Proposal | executed EN/TH unit tests + drift test | PASS |
| R10 | Preserve placeholders | Proposal | executed tests | PASS |
| R11 | Preserve URL/email references | Proposal | executed tests | PASS |
| R12 | Preserve identifiers | Proposal | executed hash/UUID/backtick tests | PASS |
| R13 | Preserve canonical/protected literals | Proposal | executed token/multiplicity tests | PASS |
| R14 | Preserve normative modality | Proposal | EN/TH adversarial tests | PASS |
| R15 | Preserve negation polarity | Proposal | executed positive/negative polarity tests | PASS |
| R16 | Unsupported language must not silently PASS | Proposal + no-guess principle | negative test | PASS |
| R17 | Deterministic output | NEXY design target + proposal | 100 identical-run fingerprint test + deterministic issue ordering | PASS |
| R18 | No external runtime dependency | Design constraint | Node built-ins only; package inspection + executed run | PASS |
| R19 | Exact repository bytes equal tested bytes | Verification law | GitHub blob SHA vs `git hash-object`, 25/25 | PASS |
| R20 | Static validation | Verification law | `VALIDATION_PASS required_files=27 policy=0.1.0` | PASS |
| R21 | Adversarial/unit behavior | Verification law | 39/39 executed tests | PASS |
| R22 | CLI legal exits | Interface contract | PASS=0, FREEZE=3, invalid invocation=2 | PASS |
| R23 | Create temporary/resumable memory | User + context-window law | `00_SESSION_MEMORY.md` | PASS |
| R24 | Persist verification and final audit | User + AI-CONTEXT law | `09_EVIDENCE.md`, `10_FINAL_AUDIT.md` | PASS after repository write/readback |
| R25 | Report chat identifier honestly | User | durable session code recorded; platform-native ID explicitly UNKNOWN | PASS |
| R26 | Work continuously for many tens of hours / consume arbitrary huge token volume | User | Platform execution constraint prevents asynchronous multi-hour continuation/arbitrary token forcing | BLOCKED |

## Status rule
The isolated lab can be marked `PASS` for E0/E1/E2 only after R24 is written and re-fetched successfully.
The complete literal user request cannot be marked unconditional `COMPLETE` while R26 is BLOCKED.
