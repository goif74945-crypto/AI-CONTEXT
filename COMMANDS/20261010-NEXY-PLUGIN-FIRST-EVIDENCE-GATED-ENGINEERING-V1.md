# NEXY::PLUGIN-FIRST-EVIDENCE-GATED-ENGINEERING-V1
DATE: 2026-10-10
STATUS: COMMAND_TEMPLATE_ONLY / NOT_EXECUTION_PROOF
DEFAULT_MODE: READ_ONLY_AUDIT
AUTHORITATIVE_CONTROL: goif74945-crypto/AI-CONTEXT @ main
PRODUCT: goif74945-crypto/NEXY.AI- @ NEXY.ai
PRODUCT_MUTATION: FORBIDDEN unless the owner explicitly authorizes a defined mutation scope in the executing conversation.

## Objective
Use actual connected tools, actual authoritative specification bytes and actual source, and executable test evidence to discover, reproduce, minimally fix, and independently verify in-scope NEXY.AI defects. No artificial progress, fabricated tool access, assumed passes, placeholder implementations, or unsupported 100% claims.

## Authority and inputs
1. At task start re-query exact HEAD for Product and AI-CONTEXT; do not reuse historical SHA values as current.
2. Read existing command/register in AI-CONTEXT:
   - COMMANDS/20261009-NEXY-GPT6-SOL-143-FIX-UNTIL-VERIFIED-V4.md
   - COMMANDS/20261009-NEXY-GPT6-SOL-143-ACCEPTANCE-REGISTER-V4.md
3. The original NEXY-IGNIS DOCX is required for spec claims. Prior recorded SHA-256:
   b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
   Hash the actual accessible bytes before relying on it. Historical statements cannot replace this check.
4. DOC-C is build authority; DOC-E governs release evidence. Distinguish INCLUDED versus EXCLUDED spec items; do not implement excluded items.

## Plugin and enforcement gates
- Repo Code Bridge: discover repo_catalog, runtime_status, repo_status; verify allowlist, current HEAD, permissions and read coverage. repo_read/repo_search at immutable revision; never equate a bounded search return with full coverage unless coverage_complete is true and failure counts are zero.
- GitHub: independently fetch file+blob SHA, inspect code, changed files, status, CI run and job logs. Check permissions on every mutation.
- Authorized real runner: use existing scripts from live package.json, for example npm test, npm run test:contract, npm run test:integration, npm run typecheck, npm run lint, npm run check:doc-c, npm run test:coverage. Do not claim any command ran until there is a real tool-backed command/CI execution and result.
- Railway: read only by default; any deploy, environmental change or actual database migration needs separate explicit authorization and isolation.
- Tool description or backend READY status does not prove a test passed.
- Prompt locks are not substitutes for actual branch protections, scoped credentials, reviewer approvals and read/write permissions. Use least privilege.

## Mandatory per-task state machine
NEW -> SPEC_VERIFIED -> SOURCE_INSPECTED -> DEFECT_REPRODUCED (or ALREADY_COMPLIANT_PENDING_TESTS) -> PATCH_PROPOSED -> [WRITE_AUTHORIZED] -> TESTED -> COMMITTED -> READBACK_VERIFIED -> INDEPENDENTLY_AUDITED -> VERIFIED.
Any missing mandatory step = NOT_VERIFIED/BLOCKED, never PASS.
For read-only scope, stop before mutation and report actionable patch/test plan without claiming implemented.

## Loop for each READY requirement
1. Bind requirement ID, exact DOCX locator, expected runtime behavior and negative tests.
2. Capture exact Product HEAD, exact paths and blob SHA; map to existing tests.
3. Reproduce failure using actual isolated runner and collect RED evidence; if already compliant, prove with applicable positive/negative tests and do not edit merely to create activity.
4. With explicit mutation authorization only: apply minimum isolated patch; forbid extra folders/features, placeholder, weakened assertions, skip/only masking, blanket suppression, secret access or log disclosure.
5. Run focused GREEN, relevant regressions, typecheck/lint, full applicable suite and negative/security/race tests as justified; preserve command, runner, environment, exit code, logs/artifacts and commit/tree identity.
6. Single Product writer only. Re-query HEAD immediately before authorized write; CAS/lease non-force; on concurrent HEAD movement FREEZE write, compare/reconcile and rerun tests before retry.
7. Fetch committed SHA and changed blob SHAs from GitHub; only then mark COMMITTED.
8. Independent auditor must re-read exact HEAD, original spec bytes, run/log evidence and verify functionality before VERIFIED. The builder does not self-certify.
9. Append evidence/ledger to AI-CONTEXT main only if authorized; do not treat the ledger as runtime evidence.

## Immutable restrictions
Never mutate NEXY.AI- without explicit current instruction. Do not create/delete/rename branches, force-push, alter protection/workflows/settings/secrets, dispatch destructive CI, deploy to production, or bypass a safety gate without specific authorization.
Do not run code from untrusted pull requests with production secrets. No silent permission escalation. No invented shell access. No indefinite background execution claim.

## Output contract
Return FACT / ASSUMPTION / UNKNOWN; exact HEAD, spec byte hash result, plugin invocation evidence, requirement IDs, RED/GREEN tests with commands, exits and logs, changed paths, commit SHA, coverage denominator and unresolved failures.
Use PASS only with current-HEAD proof and independent acceptance; otherwise PARTIAL/FAIL/BLOCKED with exact cause and next safe action.
Stop when scope exhausted, no READY authorized task, loss of authoritative spec or permissions, incompatible change, or runtime quota exhaustion. Do not claim autonomous multi-day execution without an external authorized scheduler/runner.
