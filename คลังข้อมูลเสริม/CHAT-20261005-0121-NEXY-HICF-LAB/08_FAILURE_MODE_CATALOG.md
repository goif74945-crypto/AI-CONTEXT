# 08 — FAILURE MODE CATALOG

| ID | Failure | Risk | Required response |
|---|---|---|---|
| HICF-F01 | Re-ask already resolved question | user friction, lost trust | detect repeat, reuse scoped answer or record why stale |
| HICF-F02 | Suppress material question to appear autonomous | incorrect action | ASK; friction budget cannot override |
| HICF-F03 | Proceed through authority conflict | unauthorized mutation | FREEZE |
| HICF-F04 | Treat non-material unknown as global blocker | unnecessary freeze | permit reversible/read-only progress if other gates pass |
| HICF-F05 | Infer durable preference from behavior | hidden policy drift | reject durable record |
| HICF-F06 | Drop immutable constraint during resume | authority break | classify AUTHORITY_BREAK and freeze affected path |
| HICF-F07 | Fingerprint changes due only to collection order | nondeterministic replay | canonical sorting/deduplication |
| HICF-F08 | Prohibited capability represented with friendly UI label | bypass by presentation | gate on canonical capability identity in future implementation |
| HICF-F09 | Stale answer reused after evidence invalidation | incorrect continuity | require staleness/provenance metadata in future version |
| HICF-F10 | HICF treated as safety engine | architectural overreach | keep safety/policy authority external |
| HICF-F11 | Materiality classification produced by untrusted model and accepted blindly | unsafe proceed | future policy must verify/classify materiality using authoritative rules |
| HICF-F12 | Cross-task preference leakage | privacy/scope violation | scope preferences and prevent implicit promotion |

## Known v0 limitations

- capability prohibition matching uses simple text containment in the prototype and is not production-safe;
- materiality is supplied, not derived;
- no temporal expiry/staleness model yet;
- no multi-tenant identity binding;
- no cryptographic signing of decision records;
- no integration with current NEXY code or runtime.
