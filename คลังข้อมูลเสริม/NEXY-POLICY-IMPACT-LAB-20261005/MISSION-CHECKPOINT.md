# NEXY Policy Impact Lab — Mission Checkpoint

## Identity
- mission_id: `NEXY-PIL-20261005-0137-ICT`
- chat_id: `UNKNOWN_NOT_EXPOSED_BY_HOST`
- target_repo: `goif74945-crypto/AI-CONTEXT`
- target_branch: `main`
- durable_root: `คลังข้อมูลเสริม/NEXY-POLICY-IMPACT-LAB-20261005/`
- persistence_mode: `DURABLE_RESUMABLE`
- current_phase: `PLAN_LOCKED / TDD_RED_NEXT`
- status: `IN_PROGRESS`

## Objective
Create a standalone, production-oriented, deterministic policy-impact preview engine that can be integrated with NEXY.AI later without modifying the NEXY.AI implementation repository.

The engine evaluates the same bounded scenario corpus against a baseline policy and a candidate policy, then emits a canonical impact report showing decision transitions, triggered-rule changes, freeze blast radius, and provenance hashes.

## Authority
1. Current user directive in the originating chat.
2. AI-CONTEXT root INDEX.md and AI-EXECUTION-KERNEL.md.
3. AI-CONTEXT NEXY.AI overview/status/requirements/current normalized matrix.
4. Read-only observations of `goif74945-crypto/NEXY.AI-` branch `NEXY.ai` for compatibility contracts.
5. This project's design artifacts.
6. Model inference only when explicitly labeled.

## Authorized scope
- Create new files only under `คลังข้อมูลเสริม/NEXY-POLICY-IMPACT-LAB-20261005/` in AI-CONTEXT.
- Read NEXY.AI implementation/context as needed for compatibility analysis.
- Build and test a standalone local copy of this project.
- Persist design, code, tests, evidence, checkpoints, and compatibility notes in the project folder.

## Protected scope
- NO mutation of any repository whose name contains `NEXY.AI`.
- No PR, branch, commit, issue, workflow, settings, file, tag, merge, delete, rename, or other mutation in `goif74945-crypto/NEXY.AI-`.
- No secrets or credentials.
- No claim that preview results are authoritative NEXY runtime decisions.
- No deployment/release claim without matching runtime/deployment evidence.

## Compatibility observations
Read-only NEXY.AI evidence currently shows:
- default branch `NEXY.ai`;
- Node/TypeScript ESM architecture;
- canonical envelope fields include `request_id`, `trace_id`, semver `version`, `status`, `state`, optional `freeze_reason`;
- product-level states include `INIT, READY, RUNNING, VERIFYING, CONSENSUS, STABLE, FREEZE, STOP`;
- freeze semantics and evidence-first behavior are first-class concepts.

These observations are compatibility inputs, not authorization to modify NEXY.AI.

## Product concept
**NEXY Policy Impact Lab (PIL)** is an offline counterfactual safety/preflight engine.

Primary use:
1. Load a baseline policy snapshot.
2. Apply an explicit candidate patch with a required base-policy hash.
3. Evaluate a bounded scenario corpus under baseline and candidate.
4. Produce deterministic per-scenario decision deltas and aggregate blast-radius metrics.
5. Fail closed on malformed policy, ambiguous duplicate IDs, base-hash mismatch, invalid predicates, or missing required scenario identity.
6. Emit canonical hashes so reports can be tied to exact input policy/corpus state.
7. Optionally wrap the preview report in a NEXY-shaped bridge envelope while clearly labeling it as PREVIEW/NON-AUTHORITATIVE.

## Planned core invariants
- Deterministic canonical JSON and SHA-256 hashing.
- Input order does not change semantic evaluation or report hash.
- Policy patch cannot apply when its expected base hash is wrong.
- Rule IDs are unique.
- No executable code, dynamic eval, regex injection, or provider/model calls in policy predicates.
- Rule precedence is explicit and stable.
- No matching rule defaults to FREEZE, not ALLOW.
- Preview never mutates source policies or scenario inputs.
- Every report carries baseline hash, candidate hash, corpus hash, engine version, and scenario count.
- Bridge envelope must preserve request/trace identifiers supplied by the caller.
- Core report excludes wall-clock time so deterministic hashes are reproducible.

## Work DAG
- W1: design/spec + schemas
- W2: failing tests for canonicalization/hash and policy validation
- W3: rule evaluator
- W4: candidate patch application
- W5: impact diff/blast-radius report
- W6: NEXY bridge envelope adapter
- W7: CLI/sample fixtures
- W8: focused + regression + determinism verification
- W9: security/abuse review
- W10: evidence pack + final checkpoint

## Acceptance criteria
- All project tests pass from a clean local project copy.
- Determinism test proves shuffled policy/scenario ordering yields identical canonical report hash.
- Negative tests cover malformed predicate, duplicate rule ID, base hash mismatch, missing scenario ID, unsupported effect, and unsafe prototype-path access.
- Candidate patch is immutable with respect to baseline input.
- Report contains exact transition counts and changed scenario IDs.
- NEXY bridge format validates canonical state/status vocabulary used by the adapter contract.
- README explicitly states integration boundary and non-authoritative preview semantics.
- All durable writes are read back after creation.
- No NEXY.AI implementation mutation occurs.

## Evidence ledger (initial)
- E01: AI-CONTEXT INDEX.md read.
- E02: AI-CONTEXT AI-EXECUTION-KERNEL.md read.
- E03: NEXY.AI overview/status/requirements/current matrix read.
- E04: NEXY.AI implementation repo inspected READ-ONLY.
- E05: NEXY envelope/state/freeze contract files inspected READ-ONLY.
- E06+: reserved for local RED/GREEN test logs and durable write receipts.

## Next legal action
Write failing tests first (TDD RED) in an isolated local project copy, run them, record failure evidence, then implement minimal production modules to make them pass.

## Stop / freeze conditions
- Any required mutation outside the authorized AI-CONTEXT project folder.
- Any mutation request against a repo containing `NEXY.AI`.
- Material compatibility ambiguity that would require pretending a preview result is an authoritative NEXY decision.
- Inability to obtain verification evidence needed for a PASS claim.
