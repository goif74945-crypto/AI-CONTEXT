# Requirements Ledger

| ID | Requirement | Authority | Implementation | Evidence | Status |
|---|---|---|---|---|---|
| R01 | Store work only in unique supplemental AI-CONTEXT folder | User | this project folder | remote path verification | PASS after durable write |
| R02 | Never mutate NEXY.AI repo | User + AI-CONTEXT security | no NEXY write operations in workflow | tool history + source-observation record | PASS |
| R03 | Build a genuinely distinct useful project | User | cross-runtime contract forge | supplemental index review + design | PASS |
| R04 | Preserve design, code, tests and evidence | User | `docs/`, `src/`, `tests/`, `evidence/`, `generated/` | file inventory | PASS |
| R05 | Keep temporary resumable memory | User + execution kernel | `memory/TEMPORARY_SESSION_MEMORY.md` | file presence/content | PASS |
| R06 | Strict manifest schema and unknown-key rejection | Design | validator | unit tests | PASS |
| R07 | Reject prototype pollution/dangerous JSON keys | Design/security | canonicalizer + validator | negative unit test | PASS |
| R08 | Reject code-injection-shaped wire values | Design/security | regex validation | negative unit test | PASS |
| R09 | Bound input/resource consumption | Design/security | validator limits | code inspection + tests around validator behavior | PASS for implemented bounds |
| R10 | Actor-aware transition determinism | Design | semantic key validator | duplicate/nondeterminism unit tests | PASS |
| R11 | Terminal state cannot have outbound transition | Design | validator | negative unit test | PASS |
| R12 | Stable semantic/full fingerprints | Design | canonicalizer + validator | unit tests + generated evidence | PASS |
| R13 | Reordered set-like input retains semantic fingerprint | Design | normalizer | unit test | PASS |
| R14 | Repeated compile is byte-deterministic | Design | compiler | independent A/B compile + recursive diff | PASS |
| R15 | Generate TypeScript from same normalized IR | Design | compiler | output + strict TypeScript compile | PASS |
| R16 | Generate no_std Rust from same normalized IR | Design | compiler | output + static tests | PARTIAL: generation PASS, rustc NOT_VERIFIED |
| R17 | Emit expected runtime snapshot + fixtures | Design | compiler | generated artifacts | PASS |
| R18 | Self-audit expected snapshot | Design | auditor | CLI audit | PASS |
| R19 | Fail closed on injected drift | Design | auditor/CLI | real modified snapshot, exit 2 + diffs | PASS |
| R20 | Preserve observed NEXY provenance without promoting it to authority | User/project rules | example manifest + docs | provenance fields and labels | PASS |
| R21 | Do not claim production/runtime NEXY integration | Project rules | scope/status language | docs + final report | PASS |
| R22 | Capture discovered failure and regression repair | Execution kernel | evidence record | initial TS compile failure, root fix, new tsc regression test | PASS |

## Acceptance interpretation

R16 is intentionally not upgraded to full PASS because no Rust compiler exists in the current sandbox. This does not block completion of the standalone supplemental tool, but it blocks any claim that the generated Rust artifact has been compiler-verified.
