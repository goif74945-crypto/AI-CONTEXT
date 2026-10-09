# AI.AI Source and Multi-Chat Version Catalog | 2026-10-09

## Governance
[CONSTITUTION.md](CONSTITUTION.md) and [REGISTRY.md](REGISTRY.md) are authoritative. One GitHub writing branch: `AI-CONTEXT/main`. All contributions must include a uniquely evidenced criticism, nonduplicate system idea, complete integration code, negative and positive tests, pinned source version and test output. A name change alone is not novelty.

## Full sources stored and audited
| Version | Source files | Readable individual source tree | Independent full archive |
|---|---:|---|---|
| v0.1.0 | 20 | [source tree](versions/v0.1.0/source/tree/) | [base64 ZIP](versions/v0.1.0/source/FULL-SOURCE-ARCHIVE.md) |
| v0.2.0 | 28 | [source tree](versions/v0.2.0/source/tree/) | [base64 ZIP](versions/v0.2.0/source/FULL-SOURCE-ARCHIVE.md) |
| v0.3.0 | 31 | [source tree](versions/v0.3.0/source/tree/) | [base64 ZIP](versions/v0.3.0/source/FULL-SOURCE-ARCHIVE.md) |
| v0.4.0 | 34 | [source tree](versions/v0.4.0/source/tree/) | [base64 ZIP](versions/v0.4.0/source/FULL-SOURCE-ARCHIVE.md) |

**Verified:** 113/113 source files in exact GitHub tree at `AI-CONTEXT/main` commit `95483bca196c1443a372ae51b9ebf5b1e975d96f`. Tree SHA `64ee9306ba00287698b85a12bc87f24283bc79c2`; tree result `truncated=false`; 526 total entries, missing source files = 0, SHA/size mismatches = 0. Independent expectation: [SOURCE-BLOB-MANIFEST.json](versions/SOURCE-BLOB-MANIFEST.json) includes SHA-1 Git blob identities, SHA-256 file contents and lengths.

Source-only Base64 ZIPs also read back exactly from GitHub and locally decoded with SHA/CRC; to restore without overwriting run [tools/decode_snapshots.py](tools/decode_snapshots.py) with `--snapshot` and a NEW `--destination` directory.

## Version rules
- Never infer `v0.5.0` exists unless new product source and release evidence prove it. Do not create speculative version directories.
- A version folder already present receives new distinct contribution files, not duplicate folders or overwrites.
- Code snapshots are immutable once verified. Do not mutate files in any directory named `โค้ดโปรเจคปัจจุบัน` anywhere; keep all snapshot work under this versioned safe namespace.
- A snapshot is the **original product code of that version**, not an applied proposal; code from PROPOSALS is not automatically merged.

## Registered contributions
- [AAI-20261009-001](PROPOSALS/AAI-20261009-001-file-read-integrity/): v0.2.0 file.read truncated-result integrity repair, tested on pinned source. Do not assume v0.4 compatibility.
- [AAI-20261009-002](PROPOSALS/AAI-20261009-002-adaptive-ocr-click/): v0.4.0 stale OCR click coordinate critique and adaptive third-frame gate; isolated patch `git apply --check` and `git apply` succeeded; 224/224 Python tests PASS, physical device E2E NOT_RUN.

## Branch/path scope audit
Compared `AI-CONTEXT` HEAD `edd6301851ab4f712f24bcd8f59cb32df716ab4f` to `95483bca196c1443a372ae51b9ebf5b1e975d96f`: GitHub reported `ahead_by=30`, `files_returned=145`, all changed paths in `AI.AI/` and no changed segment named `โค้ดโปรเจคปัจจุบัน`. Further commits to update version READMEs and this catalog also target `AI.AI/` only.

## Explicit limitations
GitHub remote repository `goif74945-crypto/AI.AI` was not created/verified. The full code is stored in `goif74945-crypto/AI-CONTEXT/AI.AI/versions/`, not deployed to a live AI.AI product repo. Existing tests do not establish universal computer or phone control, and proposals do not imply product merge.
