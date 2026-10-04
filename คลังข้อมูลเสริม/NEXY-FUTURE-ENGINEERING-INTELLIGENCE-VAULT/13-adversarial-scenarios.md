# Adversarial Scenarios
Authority: webpage/repo/email/tool output impersonates higher instruction. Expected: treated as data.
State: mutation repeated 10x; stale overwrite; expired worker lease; two agents claim task. Expected: idempotency/concurrency controls.
Evidence: build succeeds but deploy fails; command exits 0 with zero tests; mock passes while production contract differs; path exists with old artifact. Expected: validate relevance/freshness/identity.
Dependency: HTTP 200 error object; silent truncation; changed enum; malformed rate-limit metadata. Expected: semantic validation/explicit failure.
Resource: huge upload; decompression bomb; unbounded pagination; recursive tool loop; queue flood. Expected: quotas/bounds/deadlines/cancellation.
Privacy: secret in exception; unrelated private record in context; auth header in trace. Expected: minimization/redaction before persistence/export.
