# LEDGER
Execution 010 / CROSS / SINGLE_WRITER
PRODUCT_START_HEAD=44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL_START_HEAD=f1cfe8706d8ba656c5061e802761b02965f1ba63
SOURCE_DISPATCH_BLOB=002eef253ce836e2cd0e200f5d15cb5042cdeb29
SOURCE_RELEASE_BLOB=e162efc8b2a45014bcefbd60dc67a95d8a1e1003
TEST_HARNESS_BLOB=ffff2888b8fc921415b0f1e6c77d2df9f5aa3036

| Stage | Observed evidence | Verdict |
|---|---|---|
| Product source | HEAD 44bcb851..., dispatch blob 002eef25... | FENCED |
| Local strict TS on harness | EXIT 0 | COMPILATION_PASS |
| A FIXED patch test-scope | Git blob b7c9444d..., source blob 36e56aef..., strict TS EXIT 0; reverse restored original | CODE_CANDIDATE_ONLY |
| Startup without isolated DB | EX010_BLOCKED, EXIT 1 | EXPECTED_FAIL_CLOSED |
| Real PostgreSQL + Redis | no authorized disposable running services found | NOT_RUN |
| Full production worker | no live real services | NOT_RUN |
| Signed TSA | no authentic witness | NOT_VERIFIED |
| LAW vs cancellation lock | source-based interleaving risk, no real DB test | RISK_UNPROVEN |
| Cage Linux sandbox | bwrap false direct spawn and no proven seccomp | SECURITY_UNVERIFIED |
| CI attempt2 | exact-head fail, job steps empty | ROOT_CAUSE_UNKNOWN |
| DOC-E | approvals/rollback/current-head CI not passed | NOT_AUTHORIZED |
