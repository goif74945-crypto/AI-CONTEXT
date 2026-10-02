# CASE — Fresh exact-head campaign A93C7809

- CASE_ID: NEXY-EXACT-HEAD-FRESH-CAMPAIGN-A93C7809-8EB145B3
- trace_id: NEXY-A93C7809-8EB145B3-20261002
- cause: previous evidence binding/history could not satisfy current exact-head release proof.
- violation prevented: historical SHA promotion / false release authorization.
- impact: release remains blocked even though exact-head software execution passes.
- status: OPEN_EXTERNAL_BLOCKERS

## Proven state
Railway deployment `8eb145b3-54c1-49f6-b375-3cf94d7e553e` executed source `a93c780972ed7464bfc5f182d54129c54d0393cc` / tree `07b19ad2e0ffb63ffdc958197d8e7d1bfd9654f9` with fresh nonce `a93c780972ed7464bfc5f182d54129c54d0393cc-full-68c1916437d44741a2f57c0d9c082b8a` and completed SUCCESS.

DOC-E E1-E9 = PASS. E10/E11/E12 = BLOCKED_EXTERNAL. Evidence root `a278d2e6b8f2b9f352f43f2973d5fe56fc8cf8ae35f736e9b18f26906ef21d97`; attestation SHA-256 `e23a16b0572439f71bf9bff7e0b3882304d3d36e3887a632f0abaf3866e19f1d`.

## Prevention
Keep source-identity gate fail-closed; never rename or hand-edit historical evidence into current evidence. Require exact SHA/tree/provider execution identity on every release proof.

## Regression
Fresh exact-head software chain passed; GitHub Actions provider reruns had zero executed steps and therefore provide no contradictory code-test result.
