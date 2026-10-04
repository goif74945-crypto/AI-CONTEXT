# Risk Register

| Risk | Effect | Current control | Residual status |
|---|---|---|---|
| Wrong traffic model | Certified bound may not cover real queue | contracts are explicit; integration remains NOT_VERIFIED | OPEN |
| Packet/job granularity | fluid bound may omit packetization terms | explicitly out of model | OPEN |
| Hidden cross traffic | service curve may be overstated | no inferred service contract; require authorized contract | OPEN |
| Q64 truncation | bound could be understated | directed ceiling for upper-bound products/divisions | MITIGATED in prototype |
| Raw overflow | corrupted bound | signed-128 range checks, fail closed | MITIGATED in prototype |
| Concurrency drift in AI-CONTEXT | overwrite sibling work | unique namespace; refresh/retry; no force push | MITIGATED |
| Misuse as Canon | Lo4 output gains authority without promotion | proposal-only labels in every major artifact | MITIGATED by documentation, governance still external |
| Fingerprint mistaken for security hash | false integrity assurance | explicitly non-cryptographic; SHA-256 manifest used for artifact evidence | MITIGATED |
| Shaper causes unacceptable throughput reduction | technically feasible but poor product behavior | returns explicit shaped contract; no auto-application | OPEN for future product policy |
