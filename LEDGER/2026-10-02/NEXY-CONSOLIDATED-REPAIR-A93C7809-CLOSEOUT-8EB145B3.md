# LEDGER — NEXY consolidated repair A93C7809 closeout

- trace_id: NEXY-A93C7809-8EB145B3-20261002
- observed_at: 2026-10-02T07:53:35Z
- timestamp_source: Railway provider logs
- status: PARTIAL / BLOCKED_EXTERNAL

| Claim | Proof | Dependencies | Risk | Status |
|---|---|---|---|---|
| Canonical source is `a93c780972ed7464bfc5f182d54129c54d0393cc` / `07b19ad2e0ffb63ffdc958197d8e7d1bfd9654f9` | GitHub branch/tree refresh and Railway source identity | branch unchanged | HEAD drift | VERIFIED |
| Fresh exact-head software chain executed | Railway `8eb145b3-54c1-49f6-b375-3cf94d7e553e`, nonce `a93c780972ed7464bfc5f182d54129c54d0393cc-full-68c1916437d44741a2f57c0d9c082b8a` | provider execution | provider retention | VERIFIED |
| Contract tests pass | 106 files / 572 tests in fresh build logs | exact source identity | none observed | VERIFIED |
| Experimental tests pass | 76 files / 751 tests in fresh build logs | exact source identity | none observed | VERIFIED |
| Integration tests pass | 19 files / 159 tests in fresh build logs | exact source identity | none observed | VERIFIED |
| Coverage gates pass | 149 files / 1020 tests; all configured thresholds pass | exact source identity | none observed | VERIFIED |
| Phase-F, DOC-C, boundaries, web build, BUILD_ID pass | fresh Railway build logs | exact source identity | DOC-C explicitly not release authorization | VERIFIED |
| Six-system code/static gate passes | fresh checker output on exact head | trusted external proof for applicable host/hardware claims | external boundary | VERIFIED_WITH_LIMIT |
| DOC-E E1-E9 pass | full campaign runtime output | exact SHA/tree | provider retention | VERIFIED |
| E10 release runbook provider binding | campaign output | authoritative provider deploy+rollback receipt | absent receipt | BLOCKED_EXTERNAL |
| E11 release signoff | campaign output | authorized human actors | absent authorization | BLOCKED_EXTERNAL |
| E12 rollback proof | campaign output | real rollback + post-checks | rollback action/proof unavailable | BLOCKED_EXTERNAL |
| Full 837/935 row-by-row convergence | AI-CONTEXT provenance summary + source searches | detailed workbooks | source dependency absent | UNKNOWN |
| Release authorization | DOC-E attestation `e23a16b0572439f71bf9bff7e0b3882304d3d36e3887a632f0abaf3866e19f1d` | E10-E12 + critical external proofs | blockers remain | BLOCKED_EXTERNAL |

## Evidence identities
- provider deployment: `8eb145b3-54c1-49f6-b375-3cf94d7e553e`
- OCI image: `sha256:54ba24bda47007c9cbc9eb31f510305004b784914144e3f1c01e6f7188b30fad`
- evidence root: `a278d2e6b8f2b9f352f43f2973d5fe56fc8cf8ae35f736e9b18f26906ef21d97`
- attestation SHA-256: `e23a16b0572439f71bf9bff7e0b3882304d3d36e3887a632f0abaf3866e19f1d`

## Verdict
Exact-head software subset VERIFIED. Full project release gate is NOT RELEASE READY and remains PARTIAL / BLOCKED_EXTERNAL.
