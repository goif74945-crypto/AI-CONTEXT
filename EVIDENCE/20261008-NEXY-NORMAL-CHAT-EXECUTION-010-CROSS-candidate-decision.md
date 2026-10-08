# Candidate decision for EX010
Execution 010 / CROSS / SINGLE_WRITER
PRODUCT_START_HEAD=44bcb8517b5a2ab26f43d52eeeb8e0bc19ca9b08
CONTROL_START_HEAD=f1cfe8706d8ba656c5061e802761b02965f1ba63
SOURCE_DISPATCH_BLOB=002eef253ce836e2cd0e200f5d15cb5042cdeb29
SOURCE_RELEASE_BLOB=e162efc8b2a45014bcefbd60dc67a95d8a1e1003
TEST_HARNESS_BLOB=ffff2888b8fc921415b0f1e6c77d2df9f5aa3036

| Candidate | Patch blob | Patched source blob | EX009 own mock tests | EX010 harness strict TypeScript | EX010 real PG/Redis | Product commit |
|---|---|---|---|---|---|---|
| A FIXED | b7c9444d4348fd84691cea287c9477e6c90dd734 | 36e56aef98a5b8b52f644a0178eb3638d2c4b9af | 9/9 | PASS exit0 after applying A | NOT_RUN | HOLD |
| B fenced | 3296992af5276641046accc5941ed595008b63e3 | 94340b7a591e2961b03591780668352ade165394 | 9/9 | NOT_RUN against EX010 harness | NOT_RUN | HOLD |
| C | 4236bcf95a1541065053d9c77d0558f923523537 | 4610dd2d0da5aee7f1cc525b83b0815eef11fb29 | 10/10 | NOT_RUN against EX010 harness | NOT_RUN | HOLD |
Do not use broken uncorrected patch blob ac06e695aa6e4944acbbaf6d626b5f2a73e91ac8. NO production candidate has proven G3; no winner selected.
