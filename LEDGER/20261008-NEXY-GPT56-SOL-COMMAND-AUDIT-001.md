# Ledger — NEXY GPT-5.6 Sol Command Audit

| ID | Source | Claim | Proof | Deps | Risk | Status |
|---|---|---|---|---|---|---|
| L1 | AI-CONTEXT matrix | latest controlled row matrix has 98 rows | blob bf3ebde2..., parsed counts 71/15/5/7 | GitHub read | future newer matrix | VERIFIED |
| L2 | AI-CONTEXT matrix | duplicate requirement IDs = 0 | parsed row IDs | matrix freshness | malformed TSV | VERIFIED |
| L3 | AI-CONTEXT search | no newer 20261008 full-spec matrix found | scoped repository search | search index completeness | unindexed file | VERIFIED_WITH_LIMITS |
| L4 | GitHub branch list final gate | only NEXY.ai exists | branches endpoint | concurrent drift | may change later | VERIFIED |
| L5 | GitHub branch list final gate | NEXY.ai HEAD = 9e615b04... | branches endpoint | concurrent drift | may change later | VERIFIED |
| L6 | GitHub repo metadata | current connector reports push=true | repository permissions | token state | may change later | VERIFIED |
| L7 | audit memory | prompt underwent 28 unique review rounds | R01-R28 + structural validator | local file integrity | local file not canonical repo | VERIFIED |
| L8 | command file | V4 contains local-blocker, concurrency, anti-fake-pass and exact-head gates | COMMANDS/20261008-NEXY-GPT56-SOL-CONTINUOUS-REPAIR-V4.md | command execution | not yet executed | VERIFIED_AS_DESIGN |
| L9 | historical evidence | baseline Actions billing failure is infra, not code failure | EVIDENCE/20261007-NEXY-DIRECT-RUN-BILLING-BLOCK-006.md | historical record | stale for current execution | HISTORICAL |
| L10 | historical Railway evidence | SKIPPED run is neither PASS nor code FAIL | EVIDENCE/20261007-NEXY-DIRECT-RUN-BILLING-BLOCK-006.md | historical record | stale | HISTORICAL |

FINAL_STATUS: VERIFIED_WITH_LIMITS
TRACE_ID: 20261008-NEXY-GPT56-SOL-COMMAND-AUDIT-001