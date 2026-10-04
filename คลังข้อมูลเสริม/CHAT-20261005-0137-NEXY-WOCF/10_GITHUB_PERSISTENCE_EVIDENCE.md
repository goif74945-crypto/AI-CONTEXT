# GitHub Persistence Evidence

Status: PASS

## Merge
- Pull request: #41
- PR URL: https://github.com/goif74945-crypto/AI-CONTEXT/pull/41
- Verified PR head SHA: `ac0bbb6130f48d660f8fd763eb3f1944c122164a`
- Merge commit SHA: `103bb87d01dc3329acb9d4394c1e35a60cfd0215`
- GitHub merge result: merged=true

## Post-merge main re-read
A later observed `main` HEAD was `81a1a91b40034aa263ce2bc482ca35325c67ed8d`. The WOCF subtree still contained all 22 merged blobs at that observation.

The nine verification-critical files were re-compared on `main` against the Git blob SHA of the locally executed files. Mismatch count: **0**.

Key exact-byte bindings:
- `src/wocf.py` → `9a2f0438a7585309a482102974e2ab7a43abe575`
- `tests/test_wocf.py` → `b816ef2148619fa83f9c671861fbba6c3e1a1106`
- `scripts/run_verification.py` → `2cec576a94fa0d838ff87a003d670c844a4159d6`
- four fixtures and two schemas also matched their locally tested blob SHAs.

## Scope proof
PR #41 changed exactly 22 filenames before merge. Every filename started with:
`คลังข้อมูลเสริม/CHAT-20261005-0137-NEXY-WOCF/`

No file outside that namespace was part of the PR diff.

## Protected repository proof boundary
All mutations performed by this workstream targeted only `goif74945-crypto/AI-CONTEXT`. No repository whose name contains `NEXY.AI` was used as a mutation target.

## Evidence boundary
This proves repository persistence and exact-byte identity for the tested standalone lab artifacts. It does not prove production NEXY integration or E3+ runtime/deployment behavior.
