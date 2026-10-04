# Evidence and Final Audit

Work ID: `CHAT-20261005-0137-NEXY-AUTHORITY-COLLISION-COMPILER`
Artifact version: `0.2.0`
Evidence date: 2026-10-05 (+07:00)

## Source authority used
- AI-CONTEXT Execution Kernel / global verification law.
- `projects/NEXY.AI/overview.md` for source-grounded NEXY identity and freeze/authority direction.
- `CURRENT-SYSTEM-FEATURE-BUILD-MATRIX.md` for current 837-row source-normalization policy and authority separation.
- This artifact remains an AI proposal, not canonical NEXY law.

## Failure -> repair -> re-test lineage
The initial implementation intentionally went through executed verification rather than prose-only review:
1. FAIL `TS2688`: missing ambient Node type definitions. Fixed by isolating source compilation and adding a minimal `node:crypto` declaration instead of silently installing dependencies.
2. FAIL `TS2322`: no-decision status widened to `string`. Fixed with explicit resolution status typing.
3. FAIL `TS7053`: readonly JSON object narrowing. Fixed after array handling plus plain-object prototype validation.
4. PASS initial hardened prototype: 20/20 tests.
5. Persistable v0.2 bundle was rebuilt to ensure committed code is the same code tested.

## Final v0.2 verification
Command: `npm test`
Environment observed: Node v22.16.0, npm 10.9.2, TypeScript 5.8.3.
Result: **PASS**.

Executed test result:
- 17 tests
- 17 pass
- 0 fail
- 0 cancelled
- 0 skipped
- 500 seeded directive-order permutations preserved deep-equal output and both input/decision fingerprints.
- Protected NEXY.AI fixture resolved `mutation.allowed=false`; hypothetical lower-authority model suggestion was `SHADOWED`.

Evidence classes:
- E1 strict TypeScript compilation: PASS.
- E2 isolated behavior/determinism tests: PASS.
- E0 GitHub persistence: pending until post-write re-read.
- E3+ NEXY integration/runtime/deployment: NOT_VERIFIED and OUT OF SCOPE.

## Scope audit
Authorized mutation repository: `goif74945-crypto/AI-CONTEXT` only.
Authorized path: `คลังข้อมูลเสริม/NEXY-AUTHORITY-COLLISION-COMPILER-20261005-0137/`.
No repository whose name contains `NEXY.AI` is an authorized mutation target for this work.

## Known limitations
- ACC expects normalized directives; natural-language policy interpretation is out of scope.
- Authority ranks are caller-supplied and must be derived by a future authorized NEXY adapter from canonical law.
- Conditions support exact equality only.
- Runtime uses Node built-ins only; building TypeScript requires a compatible `tsc`.

## Final artifact gate before persistence
Design: PASS.
Code: PASS E1/E2.
Tests: PASS E2.
Evidence lineage: PASS.
NEXY integration claim: NOT_VERIFIED / OUT OF SCOPE.
