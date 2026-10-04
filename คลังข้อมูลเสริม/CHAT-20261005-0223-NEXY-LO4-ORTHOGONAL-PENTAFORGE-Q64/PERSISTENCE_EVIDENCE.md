# Persistence Evidence

## Status

`PASS` for durable publication/readback of the tested artifact set into the authorized AI-CONTEXT supplemental root.

## Target

`goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/CHAT-20261005-0223-NEXY-LO4-ORTHOGONAL-PENTAFORGE-Q64/**`

No write action in this work targeted `goif74945-crypto/NEXY.AI-`.

## Remote readback

The GitHub contents API read back the published root and the `bundle/`, `src/nexy_lo4_pentaforge/`, and `evidence/` subdirectories from `main`.

Directly readable files include the task/design/evidence/integration/novelty documents, verifier metadata, Q64 kernel, canonical encoder, symmetry explorer, bundle contract, and manifest.

The complete tested local source + tests + raw evidence + original documents are sealed in three ordered Base64 parts.

## Bundle byte-identity proof

The three remote part blobs read back with:

- part00: size 11000, Git blob SHA `c4c2b2bc4d395e0b2f5381f869fea385c514efe7`
- part01: size 11000, Git blob SHA `f2bf0e82d0810c4d75b8cc192a249ba693a8d640`
- part02: size 10256, Git blob SHA `ac53f03bc8a541211f778ec8bfa5be6ff210a098`

Those three SHA/size pairs exactly match Git blob identities independently calculated from the locally tested Base64 parts.

Therefore the remote parts are byte-identical to the local parts used to reconstruct the sealed archive.

Reconstructed archive identity:

- decoded tar.gz bytes: `24190`
- SHA-256: `e7dc7c2378576480ba3ce5471b11e69b6c90f4ceb3ea6bea19dc987bf7a45083`

The reassembly command and expected digest are persisted in `bundle/BUNDLE_SHA256.txt`.

## Direct-file identity examples

Remote Git blob identities also match independently calculated local tested-file blobs for:

- `DESIGN.md`: `53497fe4ea59e16d9da0b4d446c70a26f20c892d`
- `EVIDENCE.md`: `974813f7758fdea4abf71a387a909d1ec51b303b`
- `INTEGRATION_WITH_NEXY.md`: `7e481d288e3c286afe8bd2864fed9b53a4c541c6`
- `NOVELTY_AUDIT.md`: `22d493ffaff3824568b7ec2084c3e3910547ecc2`
- `TASK_CONTRACT.md`: `093247fd9be70a92e4c9c4575a01f26412d70f79`
- `verify.py`: `4ca3be8f405c17fac007df0201ac55088327cdd9`
- `q64.py`: `2636acd6de6940246dc2750ddd0e780bcf7cbe2b`
- `canonical.py`: `7f9a72b9365feb18066f96c5d93a64d987be6969`
- `symmetry.py`: `a9efee1d7c82223c27e75cb35eaed205dcc83f9c`
- `evidence/MANIFEST.sha256`: `394bd5caad8cfd3b233ad91da8d5cf1aa930fa10`

README and session-state are intentionally allowed to evolve after sealing because they contain publication instructions/current checkpoint state; the sealed bundle preserves the exact pre-publication tested versions.

## Scope-confinement audit

Every successful mutation commit created by this work was fetched back and its changed-file list inspected. Each commit changed exactly one file and every changed path was under the authorized Pentaforge root.

The initial README commit, all document/source/bundle/manifest commits, and the README correction commit passed this path check.

Two attempted writes encountered GitHub 409 branch races and were rejected before mutation. One direct source-file creation was blocked by the action safety layer before mutation. No force ref update, rebase, reset, delete, or history rewrite was used.

## Evidence boundary

This proves durable publication/readback and byte identity between the sealed remote artifact and the locally tested artifact. It does not upgrade local E1/E2/E3 evidence into NEXY runtime, deployment, or physical robotics evidence.
