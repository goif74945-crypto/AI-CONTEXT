# LEDGER 20261009-NEXY-EX013-BUILDER-INSTRUCTION-AUDIT
| ID | Source | Claim | Evidence/locator | Status |
|---|---|---|---|---|
| L01 | live GitHub Product NEXY.ai | 90fac4835788e867559858fc92d093ded3dcb1eb | branch API, latest 6 commits | VERIFIED_AT_OBSERVATION |
| L02 | live GitHub control main | ccd0fb088039b3136611d50e906a1d75a314d1c8 at start | branch API, latest 7 commits | VERIFIED_AT_OBSERVATION |
| L03 | Product prerelease.ts | quorum guard committed, source blob 696acae9428a347e91eb32a26b692f6d913f1bf0 | source Git blob read at Product HEAD | VERIFIED_SOURCE |
| L04 | Product LAW regression | test blob 417f3932f3eaf649eb11e56963838727f3537f67 | GitHub file read | VERIFIED_FILE |
| L05 | tests/contract/core-kernel-no-authoritative-rng.test.ts | invokes cargo check --locked -p nexy-daemon | Git blob 15c7aa81abefff26652ad6561981195764812b8a | VERIFIED_SOURCE; prior cargo ENOENT |
| L06 | tests/contract/core-kernel-rust.test.ts | invokes cargo test --locked -p core-kernel --lib | blob db615351a8d128b65d3184d0e2acc16ae0f2ae5b | VERIFIED_SOURCE; prior cargo ENOENT |
| L07 | tests/contract/core-kernel-tier-depth-compile.test.ts | two tests invoke rustc; actual runtime error cause unknown | blob f7e38f02d835ed851e8947601348ede68c36c25e | VERIFIED_SOURCE; NOT_RETESTED |
| L08 | tests/contract/current-head-attestation.test.ts | 2 expected success cases got child exit1 in EX012 | blob ca14e01e1b6ce7d4c3e8f45aa3767fd238d00360 | SOURCE_AND_PRIOR_TEST; ROOT_CAUSE_UNKNOWN |
| L09 | scripts/current-head-attestation.ts | explicit --output, no historical overwrite, Git HEAD and porcelain identity | blob 821db8e891eed377bb77ab6f3e99aba8fae907d1 | VERIFIED_SOURCE |
| L10 | EX012 evidence | broad 905/911 pass, 6 fail, LAW related 58/58, typecheck exit0 | AI-CONTEXT EVIDENCE/20261008-NEXY-EX012-LAW-PRODUCT-REPAIR.md | HISTORICAL_EXECUTION |
| L11 | NEW command | 22 review checks all passed; explicit independent auditor and no guessed tool success | COMMANDS/20261009-NEXY-NORMAL-CHAT-EXECUTION-013-BUILDER.md, GitHub read-back | VERIFIED_COMMAND_ONLY |
UNKNOWN: precise Rust tier spawn cause, attestation exit1 cause, broad current new HEAD CI issues, DOC-C completeness, PG/Redis G3.
RELEASE: NOT_AUTHORIZED.
