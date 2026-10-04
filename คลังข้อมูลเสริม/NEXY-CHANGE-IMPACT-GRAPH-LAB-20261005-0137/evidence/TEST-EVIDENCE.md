# Test Evidence

Evidence date: 2026-10-05 (+07)
Environment: local isolated container provided to this ChatGPT session
Node runtime observed: v22.16.0

## Evidence class
- E1 static/syntax: Node syntax checks.
- E2 unit: Node built-in test runner.
- E2 deterministic replay: semantically reordered graph produces identical digest/output.
- Demo is illustrative behavior evidence for the reference implementation only, not NEXY integration evidence.

## Commands executed
```bash
node --version
npm test
npm run demo
node --check src/impact_graph.mjs
node --check src/cli.mjs
```

## Initial unit run
- tests: 10
- pass: 10
- fail: 0

## Regression expansion
Additional tests added for:
- duplicate/multi-change collapse;
- noncritical isolated change;
- invalid limit configuration;
- change-set digest order/duplicate invariance.

Final results are recorded after rerun below.

## Integration boundary
No write, test, build, or runtime action was performed against any repository whose name contains `NEXY.AI`.
Therefore:
- reference engine behavior: testable here;
- NEXY.AI integration: NOT_VERIFIED;
- NEXY.AI production compatibility: NOT_VERIFIED;
- deployment readiness: NOT_VERIFIED.

## Failure/recovery record
Regression expansion initially produced 13 PASS / 1 FAIL. The failing assertion incorrectly expected `CONTRACT-A` to disappear when both `REQ-A` and `MODULE-A` were changed. The graph semantics still require `CONTRACT-A` to be impacted by the changed requirement. The test expectation was corrected; core code was not changed for this failure. Full suite was then rerun.

## Final regression result
- tests: 14
- pass: 14
- fail: 0
- Node syntax checks: PASS for `src/impact_graph.mjs` and `src/cli.mjs`
- demo: PASS
- demo summary: 7 nodes, 6 edges, 1 changed node, 6 impacted nodes, 3 required revalidations
- demo graph digest: `8ccd3fd2e2bcf06ad1a15c37e6a57342058410e51f94d7d5b6ebeac79606619f`

## Stress observation
A synthetic acyclic chain of 10,000 module nodes and 9,999 `depends_on` edges was passed through `validateGraph` under Node v22.16.0 and returned PASS without throwing. This is E2/local-runtime evidence only for this runtime and graph shape; it is not a universal performance or stack-safety guarantee.

## Artifact SHA-256 (local pre-write snapshot)
- `src/impact_graph.mjs`: `84d8a05c89a124bc7b1edd8d4e5090020e3cf143542bf17fa4c2a16fe22da8e4`
- `src/cli.mjs`: `f7405e78d43099aa313a890ae4ff04e0c2cc57094d67d0d86d8224814b72c53f`
- `tests/impact_graph.test.mjs`: `aaf88859f97e158b68378845c3476d51782189c4ce7b7326f1944316cd09b884`
- `fixtures/nexy.sample.json`: `9f89f7961bcd17c7f10f1f76f0c0ad5d68db418586be21e92b6abebf4edaabaa`
