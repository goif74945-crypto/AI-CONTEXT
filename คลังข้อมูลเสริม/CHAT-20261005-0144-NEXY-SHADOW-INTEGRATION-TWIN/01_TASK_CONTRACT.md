# Task Contract — NEXY Shadow Integration Twin (NSIT)

## OBJECTIVE
Create and verify a standalone deterministic conformance system for proposed NEXY-compatible adapters/modules without modifying NEXY.AI.

## REQUIRED OUTPUT
Design + contracts + TypeScript reference implementation + CLI + fixtures + tests + verification evidence + final audit + resumption state.

## INPUTS
1. Candidate Integration Manifest.
2. Shadow Trace Bundle captured from an isolated candidate runtime.
3. Conformance Profile defining required methods, allowed effects, limits and fail-closed rules.

## AUTHORITY
1. Explicit current user directive.
2. AI-CONTEXT execution/security/verification law.
3. NEXY project context and current build/design hierarchy.
4. This project's AI-proposed design only after it does not conflict with the above.

## IN SCOPE
- deterministic canonical JSON + SHA-256 identity;
- schema/semantic validation;
- manifest/profile/trace validation;
- protocol-state verification;
- replay consistency checks;
- hidden/undeclared effect detection;
- cancellation/terminal-state correctness;
- coverage of required methods/scenarios;
- reason-code taxonomy;
- reproducible compatibility witness;
- CLI and library sharing one engine;
- negative/adversarial tests.

## OUT OF SCOPE
- executing untrusted candidate code;
- production deployment;
- live NEXY integration;
- claiming current NEXY compliance;
- network calls;
- changing NEXY source/spec;
- nondeterministic LLM/embedding similarity.

## IMMUTABLE INVARIANTS
- identical semantic inputs produce byte-stable canonical witness output;
- no floating point in verdict/scoring path;
- missing required evidence cannot PASS;
- protocol violation cannot be downgraded by prose;
- terminal state after cancellation/error is immutable;
- identical replay key with divergent terminal payload must FREEZE;
- undeclared side effect must FREEZE;
- authority/capability widening beyond profile must FREEZE;
- every witness binds profile, manifest and trace bundle hashes;
- reason codes are sorted/deduplicated;
- no NEXY.AI repository mutation.

## REQUIRED EVIDENCE
- E0: published files can be re-read from AI-CONTEXT.
- E1: TypeScript compile succeeds.
- E2: unit/adversarial/metamorphic tests execute and pass.
- E3: CLI integration run on PASS and FREEZE fixtures executes and produces expected machine-readable witness.
- Negative paths: malformed schema, missing coverage, undeclared effect, cancel-then-success, replay divergence, unknown method, excessive limits, critical failure without freeze, trace identity tamper.

## ACCEPTANCE
All required evidence passes, published bytes match tested source, final audit lists exact limitations, protected scope unchanged.

## STOP CONDITIONS
FREEZE if any protected write is required, authority materially conflicts, target path collision appears, or required proof cannot be obtained.
