# NEXY Numeric Integrity Kernel — Execution State

STATUS: IN_PROGRESS

## Identity
- Durable session code: `CHAT-20261005-0134-NEXY-NUMERIC-INTEGRITY-KERNEL`
- Deterministic conversation identifier: `PROJECT-CONVERSATION-2026-10-05T01:34+07:00`
- Platform-native ChatGPT conversation ID: UNKNOWN_NOT_EXPOSED_BY_AVAILABLE_TOOLS
- Repository: `goif74945-crypto/AI-CONTEXT`
- Branch: `main`
- Authorized write root: `คลังข้อมูลเสริม/CHAT-20261005-0134-NEXY-NUMERIC-INTEGRITY-KERNEL/`
- Observed pre-mutation HEAD: `3116d70b104c31353e7bcf3d27805360399b78e8`

## Objective
Design, implement, execute, test, audit, and persist an additive standalone numeric-integrity reference system useful to future NEXY.AI development while never mutating any repository whose name contains `NEXY.AI`.

## Selected AI-proposed concept
**NEXY Numeric Integrity Kernel (NNIK)**

NNIK is a deterministic, exact-rational numeric contract evaluator intended to prevent silent errors caused by unit mismatches, binary floating-point behavior, ambiguous thresholds, affine unit conversions, rounding ambiguity, and measurement uncertainty.

This is an AI-proposed supplemental R&D artifact. It is NOT a current NEXY requirement and must not be treated as canonical law merely because it exists.

## Authority
1. Current explicit user directive.
2. `AI-EXECUTION-KERNEL.md`.
3. `rules/GLOBAL.md`, `rules/SECURITY.md`, `rules/VERIFICATION.md`.
4. NEXY project authority boundary and current 837-row normalization rule.
5. Current repository/runtime evidence.
6. AI proposal/inference.

## Source-grounded facts used
- NEXY is described as deterministic, evidence-first, zero-guess, freeze-on-ambiguity control.
- Design, implementation, runtime, and deployment are separate truth domains.
- PASS/COMPLETE claims require matching evidence.
- Current source normalization denominator is 837 requirement rows; the legacy 215 registry is deprecated for current counts.

## Non-duplication scan
Repository searches returned zero indexed matches for dedicated implementations/documents matching:
- dimensional analysis
- unit conversion
- floating point
- rounding policy
- Decimal precision
- measurement uncertainty
- numeric tolerance
- quantity units
- NEXY Numeric Integrity Kernel

Existing sibling work covers verification, proof invalidation, combinatorial scenarios, formal state assurance, privacy, UX, counterfactual reasoning, resource governance, localization, and related topics. This mission therefore targets numeric semantics rather than another general verifier.

## Scope lock
### IN SCOPE
- New files only under this mission folder.
- Architecture, contracts, Python 3.11+ standard-library reference implementation, CLI, fixtures, tests, verification evidence, adoption proposal, and final audit.
- Exact rational parsing and arithmetic for finite decimal/rational inputs.
- Closed unit registry with explicit dimensions and exact affine conversions.
- Deterministic bound evaluation with inclusive/exclusive semantics.
- Explicit uncertainty intervals.
- Structured ACCEPT / REJECT / FREEZE verdicts.
- Deterministic canonical JSON and SHA-256 identities.
- Negative-path, determinism, conversion, and boundary tests.
- Local isolated test execution and post-persistence read-back verification.

### OUT OF SCOPE / PROTECTED
- Any mutation to any repository whose name contains `NEXY.AI`.
- Editing sibling supplemental projects.
- Promoting this proposal into canonical NEXY scope.
- Claiming integration, deployment, or runtime behavior in NEXY.AI.
- Live currency conversion or any conversion requiring external rates.
- Secrets, credentials, private tokens, or unrelated personal data.
- Force push, destructive history rewrite, or unrelated refactoring.

## Immutable design rules
1. No binary float is accepted as an authoritative numeric value by the library API.
2. Decimal strings and integer values are converted to exact rational values.
3. Unit conversions are closed, explicit, dimension-checked, and exact.
4. Unknown units or cross-dimension conversions FREEZE rather than guess.
5. Contract boundaries explicitly define inclusive/exclusive semantics.
6. If an uncertainty interval straddles an acceptance boundary, verdict is FREEZE.
7. ACCEPT is allowed only when the full uncertainty interval satisfies the contract.
8. REJECT is allowed only when the full uncertainty interval lies outside the accepted set.
9. Equivalent normalized inputs must produce byte-stable canonical output and identical digests.
10. No eval/exec, network access, model calls, random sampling, hidden fallback, or guessed aliases.
11. Unit names are case-sensitive and explicit.
12. Built-in currency conversion is forbidden because exchange rates are time-dependent external facts.

## Evidence target
- E0: intended artifacts exist in AI-CONTEXT and can be re-read.
- E1: Python compile/static checks and JSON parsing pass.
- E2: unit tests execute successfully against exact authored source.
- E3-local: CLI + package interaction is executed locally with representative fixtures.
- No E4/E5/E6 claim about NEXY.AI itself.

## Work DAG
- W01 boot/context/authority — PASS
- W02 sibling collision scan — PASS
- W03 durable temporary memory — PASS after this commit
- W04 architecture + contracts — IN_PROGRESS
- W05 reference implementation — PENDING
- W06 fixtures + tests — PENDING
- W07 execute tests and repair — PENDING
- W08 persist verified artifact set — PENDING
- W09 re-read committed files and verify commit — PENDING
- W10 final audit + resumption capsule — PENDING

## Resume rule
Re-read this file, root execution kernel, and current folder state. Continue from the first non-PASS work item. Never infer that a local or planned artifact exists until read-back evidence confirms it.
