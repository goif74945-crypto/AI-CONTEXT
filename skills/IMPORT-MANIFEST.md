# AI-CONTEXT Skill Import & Navigation Manifest

## Verified source inventory

- **Expected historical count:** 1,306 top-level file entries.
- **Actual source-of-truth count:** **1,352 top-level file entries**.
- **Delta:** **+46**. The expected number is not rewritten to force agreement.
- **All 1,352 top-level entries hashed:** SHA-256 coverage = 1,352 / 1,352.
- **Nested archive members:** 96; separately indexed and **excluded** from the 1,352 top-level count.
- **Top-level archive integrity:** all three supplied ZIP archives passed `testzip()` with no corrupted top-level member reported.
- **Source SKILL.md entries:** 54.

## Source packages

| Package | Top-level file entries | Nested archive members | Integrity |
|---|---:|---:|---|
| `agent-skills-main.zip` | 447 | 96 | PASS (`testzip() == null`) |
| `skills-main.zip` | 783 | 0 | PASS (`testzip() == null`) |
| `skills-main-2.zip` | 122 | 0 | PASS (`testzip() == null`) |
| **TOTAL** | **1,352** | **96** | **PASS** |

## Classification of all top-level entries

- DOCUMENTATION: 696
- UNKNOWN: 172
- CODE: 170
- CONFIG: 136
- ASSET: 73
- SKILL: 54
- LICENSE: 45
- ARCHIVE: 6

**Important:** `UNKNOWN` is an unresolved forensic state, not a success state. Heuristic classification is not proof of semantic role.

## Exact-duplicate evidence

- Exact duplicate SHA-256 groups: **22**
- File occurrences in exact duplicate groups: **95**
- Exact duplicate groups spanning multiple top-level packages: **0**
- Hash equality is treated as exact-content evidence only. All provenance remains authoritative; no automatic merge/delete is authorized by this manifest alone.

## AI navigation contract

Every top-level source entry is represented individually in the generated navigation index with at minimum:

`FILE_NO`, `SOURCE_PACKAGE`, `SOURCE_PATH`, `SOURCE_RELATIVE_PATH`, `DIRECTORY`, `BASENAME`, `EXTENSION`, `SIZE_BYTES`, `SHA256`, `FILE_TYPE`, `CONTENT_KIND`, binary/archive flags, source layer, classification, AI navigation role, skill candidate, target category candidate, duplicate category, exact-duplicate peers, ingestion status, decision status, proposed action, target skill path candidate, provenance key, and readable-content metadata where decoding is possible.

Nested members are separately represented with parent archive path, child path, hash, classification, nested duplicate relationships, and an explicit flag that they are excluded from the top-level count.

## Current state

- **GitHub report update:** this manifest is being corrected to the verified 1,352-entry source-of-truth.
- **Skill construction status:** IN PROGRESS.
- **No COMPLETE claim is made.** Source inventory/hash coverage is verified; Phase 05+ downstream skill audit and global semantic decisioning remain separate work.

## Navigation artifacts

The full local machine-readable index contains all **1,352 individual source records** plus the 96 nested members. The corresponding local files are:

- `AI-NAVIGATION-INDEX.json` — complete 1,352-entry source index with per-file provenance/hash/classification/navigation fields.
- `AI-NAVIGATION-INDEX.md` — human-readable companion.
- `AI-NAVIGATION-NESTED-INDEX.json` — complete 96-member nested index.
- `AI-NAVIGATION-NESTED-INDEX.md` — human-readable nested companion.

## Scope lock

Only `goif74945-crypto/AI-CONTEXT` is a write target. No repository whose name contains `NEXY.AI` is a write target.
