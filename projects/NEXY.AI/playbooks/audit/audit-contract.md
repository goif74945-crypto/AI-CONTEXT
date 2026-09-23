# PLAYBOOK — Audit Contract

## PURPOSE
Verify that a declared API/module/event/storage/schema/error contract is consistent across source, code, consumers and tests.

## PROCEDURE
1. Resolve canonical contract record/version.
2. Resolve authority and requirement IDs.
3. Identify producer/consumer.
4. Inspect input/output runtime schemas.
5. Inspect preconditions/postconditions.
6. Inspect authorization/security boundary.
7. Inspect timeout/retry/idempotency.
8. Inspect error contract.
9. Compare all producers/consumers for drift.
10. Verify runtime validation exists at the boundary when required.
11. Run/inspect contract and negative tests.
12. Check evidence freshness.

## FAILURE PATTERNS
- TypeScript-only validation with no runtime enforcement.
- Route returns non-SystemEnvelope shape.
- Producer and consumer use different schema versions.
- Mutation lacks idempotency/CSRF/auth.
- Error path leaks hidden data.
- timeout/retry semantics differ across layers.
- docs updated without implementation or vice versa.

## VERDICT
PASS only when both sides of the boundary and the required runtime/static evidence agree.
