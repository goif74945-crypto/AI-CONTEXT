# EVIDENCE LEDGER — NEXY Next Command 004

TASK_ID: 20261008-NEXY-CODEX-NEXT-COMMAND-004
MODE: CROSS / AUDIT
STATUS: VERIFIED_WITH_LIMITS
SOURCE_HEAD_PRODUCT_OBSERVED: 8b406a63f10aa1424225a80453393af2e4cb78b5
SOURCE_HEAD_AI_CONTEXT_ORIGIN: 2e27e349e8dd3f6ae3c250588f11d8d31b9fd8da
VERSION: 1

| ID | Source | Claim | Proof / locator | Dependency | Risk / limit | Verdict |
|---|---|---|---|---|---|---|
| L01 | GitHub branch API | NEXY.ai current observed HEAD is 8b406a63... | branch NEXY.ai live observation | branch may drift | observation time only | VERIFIED_AT_OBSERVATION |
| L02 | GitHub branch API | AI-CONTEXT prior head was 2e27e349... | branch main live observation | concurrent writers | not a persistent guarantee | VERIFIED_AT_OBSERVATION |
| L03 | Uploaded DOCX bytes | SHA equals required b35ee1bf...61d26b7 | SHA256 of /mnt/data/แอป [NEXY-IGNIS] ที่กำลังพัฒนา.docx | available original attachment | original may not be mounted in Codex | VERIFIED |
| L04 | Hash-verified DOCX | DOC-C controls build; DOC-E controls deploy signoff | P9837-P9845, EVIDENCE/20261008-NEXY-SPEC-AUTHORITY-RESOLUTION-004.md | authority evidence | must not confuse broader TSA law with DOC-C build obligation | VERIFIED_SOURCE |
| L05 | Hash-verified DOCX | DOC-C canonical OTAC TTL 300000ms; session 21600000ms | P9910-P9938 | compare current source | historical prose conflict must remain visible | VERIFIED_SOURCE |
| L06 | Hash-verified DOCX | vNEXT scope section controls in/out/deferred | P9644-P9689 | source inspection required | per-row reclassification only | VERIFIED_SOURCE |
| L07 | Product source | queue dispatch requires currentTsaBatchTimeMs() | packages/queue/dispatch.ts at observed HEAD | time initialization | browser submission fails absent TSA | VERIFIED_SOURCE |
| L08 | Product source search | injectTsaBatchTime source definition and tests found, no production caller found in code search | GitHub code search at observed HEAD | exhaustive call graph not yet completed | negative search does not prove nonexistence | CANDIDATE_GAP |
| L09 | Product source | bwrap implementation binds limited standard paths | packages/phase-f/lo3/cage.ts at observed HEAD | runtime executable path | must reproduce runner mismatch | VERIFIED_SOURCE |
| L10 | Codex report + AI-CONTEXT matrix | 2 browser failures, 10 experimental failures, 39/98 reviewed | TASKS/20261008-NEXY-CONTINUOUS-REPAIR-EXECUTION-003.md and TSV | previous exact-head testing | reported, not rerun by this audit | VERIFIED_AS_REPORTED |
| L11 | Prompt audit | 28 distinct review rounds recorded | EVIDENCE/20261008-NEXY-CODEX-NEXT-COMMAND-AUDIT-004.md | review only | prompt execution still pending | VERIFIED_AS_DESIGN |
| L12 | Command | command 004 persisted | COMMANDS/20261008-NEXY-CODEX-NEXT-EXECUTION-COMMAND-004.md GitHub blob 71f40943a180e8c3440b9ea01b4c7230787c2464 | Codex execution | no product change from this task | VERIFIED_READBACK |

RISK: Missing external TSA / CI / DOC-E signoff remains unverified.
ROLLBACK: Revert coordination changes using a forward commit only after HEAD refresh.
FINAL_VERDICT: VERIFIED_WITH_LIMITS, COMMAND_AUTHORED_NOT_EXECUTED.
