# NEXY Railway validation — coverage authority freeze

Target service: `3c290782-e2f0-4e5b-87d9-58bae4d4dba8`
Observed validation deployment: `aedd277b-38b8-4811-875a-bba1468a0d5f`
Branch: `astra/omega-full-spec-convergence`

## Verified gate state
- npm_ci PASS (exit 0)
- prisma_generate PASS (exit 0)
- typecheck PASS (exit 0)
- contract PASS (exit 0)
- integration PASS (exit 0)
- full PASS (exit 0)
- coverage PASS (exit 0)
- coverage_check FAIL/FREEZE (exit 1)
- doc_c PASS (exit 0)
- web_build PASS (exit 0)
- overall FAIL (1)

## Proven remaining blocker
`check:coverage` freezes because API metrics straddle 85% and the authoritative metric is ambiguous: lines=82.00%, statements=80.38%, functions=91.26%, branches=71.98%.
Core/law/judge coverage gates pass under every standard metric.

No production/test/threshold mutation is authorized by evidence because selecting a metric would invent policy. No threshold was weakened.
