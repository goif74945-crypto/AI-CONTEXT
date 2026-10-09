# Repo Code Bridge | Cycle 006 | 2026-10-10 (Asia/Bangkok)

MODE: EXECUTE_NOW / ENGINEERING / EVIDENCE_FIRST / EXACT_HEAD / FAIL_CLOSED
AUTHORIZED_MUTATION: goif74945-crypto/repo-code-bridge-e2e-test/main (isolated tests) and goif74945-crypto/AI-CONTEXT/main (report)
NEXY.AI-: READ-ONLY; no source, branch, settings, CI or secrets mutations.

## Proven bugs / fixes

1. **False positive in search coverage classifier v3**. At exact test HEAD `114a53fa9a54f12f538ad19c59c9f8157a3b18e2`, two independently constructed *inconsistent* search-hit fixtures were both returned as CONSISTENT by `classifySearchCoverage`:
   - claimed path_match=true where path was `src/unrelated.ts` for query `exampleValue`;
   - claimed content match whose line text contained no `exampleValue`.
   These fixtures were executed against the actual GitHub-returned source on Floot Node VM, not just inferred. Actual Gateway searches verified case-insensitive literal substring matches.
2. **Classifier fixed** by verifying path_match against the casefolded path query and each returned content snippet against the casefolded query; whitespace-only query invalid. Eight new adversarial tests plus legacy cases.
   - Verified commit: `069fb6a9e7abaa5257b36c96dbad2adb48a1f783`
   - URL: https://github.com/goif74945-crypto/repo-code-bridge-e2e-test/commit/069fb6a9e7abaa5257b36c96dbad2adb48a1f783
   - Exact readback source blob `42d08aedaf426f5a155955db81b113b9d338ad1a`; test blob `2bdea7d3e682562c1cfe4d7459824dfefdb788c5`.
   - Live 3-query search integration on the same pinned exact head: pathname-only, case-insensitive content, zero-result. **58/58** including 55 synthetic tests, 3 live result tests, zero failures.
3. **Exact Git blob readback verifier added**: `scripts/verify-search-hit-blobs.mjs` and `tests/verify-search-hit-blobs.test.mjs`.
   - Verifies each displayed hit through pinned `repo_read` content, exact repository/revision/path, byte length, Git blob SHA-1 (`blob <length>\\0<bytes>`), exact line number/text, casefolded literal substring and path-only hits.
   - Rejects forged line evidence, stale SHA/revision, mismatched byte size, missing or extra readbacks, unverified filenames.
   - Isolated GitHub commit `ca445ea05293366844ade508245c81377bbdd847`.
   - Link: https://github.com/goif74945-crypto/repo-code-bridge-e2e-test/commit/ca445ea05293366844ade508245c81377bbdd847
   - Readback verifier source SHA `963e4feb88dbe740e923ed033c8d52c3ac8d1424`; initial tests SHA `7dd311b4cfc2f6dcb8d85552095d2117fa9f7fc8`.
   - 22 synthetic tests + 1 live search test on 4 displayed files: **23/23 pass**, exit 0.
4. **Fixed misleading assertion name**: the prior response field `full_text_coverage_verified` could imply entire repository independently verified when only metadata was checked. Replaced with `coverage_metadata_consistent` and `remote_source_authenticity_verified=false`.
   - Isolated GitHub commit `773059b2667dfb7891633c701a66c8d0272e01ec`.
   - Link: https://github.com/goif74945-crypto/repo-code-bridge-e2e-test/commit/773059b2667dfb7891633c701a66c8d0272e01ec
   - Current readback source SHA `cd18227bef6ff0decbc4d14f8edcb199d5629c91`, tests SHA `cffe8197252ac9d93cc8653227f8034a83cdd9a6`.
5. **Cross-connector independent comparison**: GitHub connector `fetch_file` and Bridge `repo_read` returned *exactly matching* bytes and blob SHAs for the four real displayed results (src/example.ts, the smoke workflow, coverage test, blob verifier test). No mismatch. This cross-check is independent of the test suite's synthetic fixtures but does not prove unshown matches are complete.

## Combined suite at exact GitHub HEAD

- Exact source HEAD at full-suite run `773059b2667dfb7891633c701a66c8d0272e01ec`.
- Combined independently executed Floot Node VM: **98/98 pass, 0 fail, exit 0**.
  - 55 Search Coverage synthetic tests.
  - 16 GitHub CI-run evidence synthetic tests.
  - 23 Git Blob Search Hit evidence synthetic tests.
  - 3 live Repo Code Bridge exact-head search response consistency tests.
  - 1 live readback test verifying all four displayed match files.
- Repo Code Bridge `repo_search` returned candidate_files=10, 0 skipped, 0 failed on isolated test repo, with test queries EXAMPLEVALUE (4 hits), CLASSIFY-SEARCH-COVERAGE.MJS (3 hits), __no_rcb_matches_20261010__ (zero matches).
- All outputs remain strictly test-harness validations; no private Site backend code was edited/deployed here.

## GitHub Actions workflow updated and attempted

- Smoke workflow amended through separately authorized GitHub connector to include `node --test tests/verify-search-hit-blobs.test.mjs` alongside the two existing test suites.
- Workflow update commit `67a0e4cdbe44d66614fd5a51218592bb18abbf60`; exact workflow blob `79a0fd72314552201ef7aee3e811379935f0a3de`.
- Actual CI dispatch: run ID `37965613226`, at exact commit `67a0e4cdbe44d66614fd5a51218592bb18abbf60`; GitHub marks completed/failure.
- Job ID `113939084305`, `steps=[]`; attempting job logs returned GitHub BlobNotFound HTTP 404. GitHub Actions never produced executed test-step evidence. Underlying runner/billing/root-cause is **UNKNOWN on this run**, not a tested-source FAIL.
- CI URL: https://github.com/goif74945-crypto/repo-code-bridge-e2e-test/actions/runs/37965613226
- No GitHub Actions PASS claimed, despite successful independent Floot VM testing.

## Live product and Site facts

- `goif74945-crypto/NEXY.AI-` `NEXY.ai` HEAD was observed as `58b1200bd61b867e917057d0019eea78ea9f6b2a`; NOT modified.
- Historical large-project search at prior exact HEADs found candidate enumeration complete but 2 eligible text blob skips; never claim full-text completeness without exact current-head scan and skipped path reasoning.
- Current Site backend `runtime_status`: GitHub connected; gateway version 0.1.0; read/write/CI backends report READY (not action success). Site Library metadata for `Repo Code Bridge`: project id `appgprj_6ac56b9353f88191873e731529a5dc6f`, source_version_number 15, projection_revision 36, status active. These are read-only metadata; no accessible authoritative Site edit/deploy action exposed in current chat.
- Site URL: https://repo-code-bridge.nexy-code-me.chatgpt.site

## Acceptance gates outstanding
- Authoritative Site source edit + deploy + version readback (not performed).
- Live Gateway itself enforcing exact file/line/sha verification and complete coverage or explicit fail-closed reporting (not deployed).
- Identify skipped-file paths/reasons for large repo at CURRENT exact HEAD (unknown).
- Restore GitHub Actions runner and obtain actual job steps / log evidence (BLOCKED).
- Measured benchmark proving any 10x/20x efficiency claim (not performed).

STATUS: ISOLATED_TEST_HARNESS=IMPROVED_AND_VERIFIED; INDEPENDENT_TESTS=98_PASS; WORKFLOW=UPDATED_BUT_CI_FAILED_PRESTEP; PRODUCTION_BACKEND=NOT_VERIFIED; UNIVERSAL_PERFECTION=NOT_CLAIMED.
