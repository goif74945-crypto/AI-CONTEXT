# State-Space and Edge-Case Matrix
Production behavior spans state, permissions, data quality, timing, dependency health, retries, concurrency, and intent.

Dimensions: data valid/missing/stale/malformed/conflicting/partial; identity anonymous/authenticated/expired/unauthorized/privileged; dependency healthy/slow/timeout/4xx/5xx/inconsistent; mutation first/retry/duplicate/concurrent/reordered; network online/degraded/interrupted/recovered; lifecycle create/read/update/delete/rollback/migration; time before-valid/valid-now/expired/future-dated/clock-skew; capacity empty/nominal/boundary/overloaded.

Use pairwise coverage first, then force high-risk triples and known incident combinations. Mandatory adversarial cases include success status with incomplete payload, retry after commit plus client timeout, stale cache masking deletion, duplicate delivery, permission revoked between read/write, semantically impossible dependency data, equal-authority conflict, partial rollback, and resumed work after specification change.

A branch in code is not coverage. Observable evidence is coverage.