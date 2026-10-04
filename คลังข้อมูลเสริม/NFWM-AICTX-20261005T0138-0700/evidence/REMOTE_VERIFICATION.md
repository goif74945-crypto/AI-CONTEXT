# NFWM Remote Verification

## Scope

This record verifies publication identity for the NFWM project only.

- Repository: `goif74945-crypto/AI-CONTEXT`
- Branch: `nfwm-aictx-20261005t0138-0700`
- Project path: `คลังข้อมูลเสริม/NFWM-AICTX-20261005T0138-0700/`
- Branch base observed at creation: `5828007d0287e2270416b0b69a47aefe4f50e0a6`
- Work ID: `AICTX-NFWM-20261005T0138+0700`

## Publication race handling

An initial create-file attempt against the moving `main` branch failed with GitHub HTTP 409 because concurrent work changed HEAD between precondition resolution and mutation.

Observed safety behavior:

- the target NFWM README was checked on `main` after the conflict and was absent;
- no force update was used;
- no unrelated file was overwritten;
- an isolated branch was created from the then-current observed main commit;
- all later NFWM writes were scoped to that branch.

## Byte-identity readback

After publication, 34 published files were individually fetched back from the branch and their Git blob SHA-1 identities were compared with `git hash-object` identities of the locally verified files.

Result:

- expected files: `34`
- read back: `34`
- exact Git blob identity matches: `34`
- mismatches: `0`
- missing files: `0`
- status: `PASS`

This proves that the published source, tests, fixtures, profile, documentation, and pre-final evidence bytes matched the local artifacts used for validation at this gate.

## Verification already bound to those bytes

Local verification recorded before publication:

- E1 `python -m compileall -q src tests` → PASS.
- E2 `PYTHONPATH=src python -m unittest discover -s tests -v` → 17/17 PASS.
- E2 release-after-freeze fixture → 7 events reduced to deterministic 2-event witness.
- E2 witness replay → PASS.
- E2 tampered witness hash → correctly rejected.

## Protected-scope audit

For this NFWM work, connector mutations targeted only:

`goif74945-crypto/AI-CONTEXT`

No mutation tool call from this work targeted a repository whose name contains `NEXY.AI`.

This is a scope/process fact for this execution, not a claim about other chats or actors.

## Evidence boundary

PASS here proves publication identity and the recorded local NFWM behavior.

It does **not** prove:

- live NEXY.AI runtime compatibility;
- NEXY deployment readiness;
- production event-schema compatibility;
- DOC-E completion;
- global minimum witness cardinality.

Those remain explicitly outside this project's verified claim surface.
