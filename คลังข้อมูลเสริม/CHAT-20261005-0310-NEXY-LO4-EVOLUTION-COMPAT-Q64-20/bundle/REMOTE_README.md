# ECPC-20 sealed archive remote transport

Remote archive chunks are named `archive-part-00.b64` through `archive-part-07.b64`.

Reconstruct:
```sh
cat archive-part-*.b64 | base64 -d > ecpc20-sealed-source.tar.gz
sha256sum ecpc20-sealed-source.tar.gz
```

Expected SHA-256:
`ef83a3ca988a4177b15f8a61910305bef7a5465a31d04f64aa5245ab1e9905be`

The archive contains the full TypeScript source, tests, docs, evidence captured before sealing, and each concept's DESIGN/CODE/TEST/EVIDENCE quartet.

Fresh-extraction evidence before publication:
- typecheck PASS
- strict hardening PASS
- build PASS
- 62/62 tests PASS
- source scan PASS

The archive is reference/evidence material only. It has no Canon authority and cannot auto-promote into NEXY.AI.
