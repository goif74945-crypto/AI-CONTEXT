# LEDGER — NEXY DIALOG exact-head closeout

- trace_id: NEXY-E54ABD31-3F9C4730-20261002
- observed_at: 2026-10-02T15:00:12.355896441Z
- timestamp_source: Railway provider logs
- status: PARTIAL / BLOCKED_EXTERNAL

| Claim | Proof | Dependencies | Risk | Status |
|---|---|---|---|---|
| Canonical source is `e54abd3122427dcfc27f81cc725ec0f43ff00837` / `0ad78e8f8fcdbbeb3141e483fa31e70172e2a08c` | GitHub branch refresh + Railway exact-source build | branch unchanged | HEAD drift | VERIFIED |
| Exact-head software chain executed | Railway `3f9c4730-0681-454f-bba8-0fde2484bdfe`, SUCCESS | provider execution | provider retention | VERIFIED |
| Combined coverage run passes | 152 files / 1040 tests | exact source identity | none observed | VERIFIED |
| DIALOG API tests pass | 10/10 | current head | none observed | VERIFIED |
| DIALOG sandbox tests pass | 6/6 | current head | none observed | VERIFIED |
| DOC-D validation-copy tests pass | 2/2 | current head | none observed | VERIFIED |
| API coverage threshold passes | branches 85.39% >= 85% | direct API tests | regression risk | VERIFIED |
| Core/law/judge coverage pass | 91.23% / 96.83% / 94.01% branches | coverage suite | none observed | VERIFIED |
| DOC-C static + module boundaries pass | build logs | exact head | DOC-C is not release authorization | VERIFIED |
| Web build + BUILD_ID pass | production build logs; routes include /api/dialog and /dialog | exact head | build warning unrelated to DIALOG remains warning | VERIFIED |
| Real application rollback executed | Railway `0f710de0-a24f-4331-b976-f0e2f871c96c`, reason=rollback, SUCCESS | target `8ec411af-170b-412f-8647-4c75e4515cf3` | provider retention | VERIFIED |
| DOC-E E1-E10 and E12 pass | full campaign `3f9c4730-0681-454f-bba8-0fde2484bdfe` | exact SHA/tree + receipts | provider retention | VERIFIED |
| E11 human signoff | E11 validator + campaign summary | genuine authorized human approvals | no authorized signoff receipt | BLOCKED_EXTERNAL |
| Release authorization | attestation `dce37ba1d5a9598d6f394431a4307a71239797f4ebaf8bc79f6d0c36d32509cf` | E11 PASS required | blocker remains | BLOCKED_EXTERNAL |

## DOC-E audit coverage vs completion
- audit coverage: 12/12 gates classified = 100%.
- verified PASS rows: 11.
- blocked external rows: 1.
- completion percentage over verified rows only: 11/11 = 100%.
- E11 is excluded from the completion denominator because it is BLOCKED_EXTERNAL, not silently counted as 0 or 100.
- release authorization remains false despite verified-row completion = 100%.

## Verdict
Software exact-head subset VERIFIED. Full release remains PARTIAL / BLOCKED_EXTERNAL solely at DOC-E E11 within the revalidated DOC-E gate set.
