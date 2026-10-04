# Repository Publication Verification

Status: PASS for standalone lab publication and E1/E2 reference-model evidence  
Session code: `NEXY-DIRECTIVE-INTEGRITY-20261005-0121-SOL`  
Verification date: 2026-10-05 (+07:00)

## Published artifact
- Repository: `goif74945-crypto/AI-CONTEXT`
- Folder: `คลังข้อมูลเสริม/CHAT-20261005-0121-NEXY-DIRECTIVE-INTEGRITY-LAB`
- Pull request: `#18`
- Merge commit: `016c3a422546c215f8fa0e8005c4ec8086926967`
- Merge tree: `6dadf4fb55acb922cb99af766e274d36d0e737ca`
- Merge parents: `309c358d2676ee660eaaf043d30a9f4691d64b87`, `7bb8e391348d6c7bb1f489d1c251b55d073466a5`
- Files in the lab at the merge commit: 21

## Concurrent-writer handling
`main` moved repeatedly while the package was being prepared. No force update was used. Several candidate commits were intentionally abandoned when the observed parent was no longer current. The final package was published through an isolated branch and PR merge so concurrent additive work was preserved.

## Exact-byte identity proof
The recursive Git tree for the exact merge commit was fetched from GitHub. Every one of the 21 lab paths was present with a Git blob SHA. The same 21 local files were hashed with `git hash-object`. Every local path/blob pair matched the exact merge-tree path/blob pair.

Critical blob identities:
- `reference/directive_integrity.py` -> `19e0c3b502f82f9c904a5ea567c22a92fcd692e3`
- `reference/test_directive_integrity.py` -> `ac45cb2048e18dd7f8c3c92affcb97a6445acc4f`
- `04_DIRECTIVE_SNAPSHOT.schema.json` -> `7c5037d04c4d8731cf8b854a5ae3865afb4b12fd`
- `MANIFEST.json` -> `16a07f34ef59abe9d9136318db6d1a7d60ce659b`
- `00_EXECUTION_STATE.md` -> `30e4bb9f7e5245f7cfe7ad77f366326a9ac9ede8`

Because the executed local files and exact-commit files have identical Git blob identities, the post-publication executions below apply to the exact bytes stored by the merge commit.

## Post-publication E1/E2 rerun
Executed after publication against the byte-identical local copy:

1. `python -m py_compile reference/directive_integrity.py reference/test_directive_integrity.py` -> PASS / exit 0.
2. JSON Schema Draft 2020-12 self-check plus four fixture validations -> 4/4 PASS.
3. Manifest SHA-256 and byte-length verification -> 20/20 listed files PASS. `MANIFEST.json` intentionally does not list itself.
4. `python -m unittest -v test_directive_integrity.py` -> 22/22 PASS / exit 0.
5. Safe CLI transition -> `PASS`, exit 0.
6. Adversarial broadened transition -> `FREEZE`, exit 2.
7. Adversarial violation codes -> `MUTATION_ESCALATED`, `SCOPE_BROADENED`, `SIDE_EFFECT_ADDED`.

## Evidence boundary
This proves publication, exact-byte identity, syntax/schema correctness, and standalone reference behavior. It does **not** prove NEXY production integration, API/DB integration, browser behavior, operational reliability, deployment, or physical-system behavior. Those remain NOT_VERIFIED because no repository whose name contains `NEXY.AI` was mutated and no production integration was attempted.

## Protected-scope statement
No mutation tool was invoked against `goif74945-crypto/NEXY.AI-` or any other repository whose name contains `NEXY.AI`. NEXY sources were read only as evidence.

## Manifest note
This file is a post-publication evidence record and is intentionally outside the pre-publication `MANIFEST.json`; adding it after verification avoids rewriting the already-verified merge payload merely to describe that verification.
