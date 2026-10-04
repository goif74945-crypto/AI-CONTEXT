# NECC Publication Evidence

**Work tag:** `CHAT-20261005-0137-NEXY-EFFECT-CONTRACT-COMPILER`
**Classification:** AI-PROPOSED / RESEARCH PROTOTYPE / NOT NEXY CANON / NOT INTEGRATED INTO NEXY

## Publication method

The GitHub connector available in this session had no bulk sandbox-directory upload operation. The exact verified project tree was therefore packed into a deterministic tar.gz and published on `AI-CONTEXT/main` as base64 text:

`bundle/necc_project_bundle.tar.gz.base64`

This preserves the exact archive bytes after deterministic base64 decode while keeping the repository mutation restricted to AI-CONTEXT.

## Integrity chain

Frozen local tar.gz:
- bytes: 29,574
- SHA-256: `dd514ccf27f9302c286e62a4d5a185210add0a92f8b7b606a859c497e8067a6d`
- Git-blob SHA-1 of decoded tar.gz: `c1504a86d6c8066834ff1150ef8e6619f0bab09f`

Base64 representation:
- text length: 39,432
- SHA-256 computed locally before publication: `128c326a5f1253bcb5a452f79e24db2f974656150917463e57e692eca0ffa060`
- expected Git blob SHA-1: `5a8bd4b4bb11606cff33b3992345218eb273a397`

GitHub readback from `main`:
- observed blob SHA-1: `5a8bd4b4bb11606cff33b3992345218eb273a397`
- observed text length: 39,432
- fetched content compared with the staged exact base64 source: **byte-text equal = true**

Archive publication commit:
`f044b7056bb7dc0eadf086630da550590f305de9`

## Verification from the exact archive

After publication, the frozen local archive was extracted into a clean temporary directory and verified from the archive contents:

- forced `python -m compileall -q -f src tests`: PASS
- `PYTHONPATH=src python -m unittest discover -s tests -v`: 56 / 56 PASS
- elapsed unittest time observed: 1.208 s
- extracted regular file count observed: 53
- archive SHA-256 re-read: `dd514ccf27f9302c286e62a4d5a185210add0a92f8b7b606a859c497e8067a6d`

## Concurrency evidence

Two direct Git-tree publication attempts and four automated fast-forward retries were rejected because other work advanced `main` between precondition read and ref update. GitHub returned 422 `Update is not a fast forward`.

Corrective action:
- no force push was used;
- no history was rewritten;
- no other chat's changes were overwritten;
- publication switched to new-file Contents API operations on `main`.

The rejected commits were never attached to `main` and therefore did not alter branch history.

## Protected scope

No repository whose name contains `NEXY.AI` was mutated in this mission.

## Evidence classification

- archive/readback integrity: E0/E1-style artifact identity evidence;
- unit/adversarial/wire behavior: E2;
- clean wheel install/import is package-level integration evidence, but **not** NEXY integration;
- production/provider/deployment behavior: NOT_VERIFIED.
