# Verification Report — NEXY Intent Integrity & Least-Authority Delegation Lab

**Session:** NEXY-IIL-20261005-0121-TH  
**Verification status:** PASS for standalone prototype behavior described below  
**NEXY.AI integration status:** NOT IMPLEMENTED / NOT CLAIMED

## Toolchain

- Node.js: v22.16.0
- npm: 10.9.2
- TypeScript compiler: 5.8.3

## Verification command

`npm run verify`

Result at final local audit:

- TypeScript strict typecheck: PASS
- Automated tests: 45
- Passed: 45
- Failed: 0
- Cancelled: 0
- Skipped: 0

## Behavioral evidence covered

- valid contract admission;
- deterministic SHA-256 contract seal;
- 1000 repeated contract seals identical;
- CRLF/LF normalization equivalence;
- set ordering/duplicate normalization;
- authority-order sensitivity;
- critical UNKNOWN and CONFLICT freeze behavior;
- noncritical UNKNOWN review behavior;
- protected-scope collision;
- seal tampering;
- unknown serialized field rejection;
- missing required section rejection;
- parser section injection and malformed content rejection;
- source and section-entry resource bounds;
- revision parent-seal lineage;
- scope expansion detection;
- weakened acceptance detection;
- mutation matrix across constraints, behaviors, edge cases, failure conditions, validation, stop conditions, inputs, forbidden rules, and immutable rules;
- 250 repeated unsafe-drift evaluations identical;
- CLI compile/verify and exit semantics;
- least-authority delegation admission;
- 500 repeated delegation seals identical;
- delegation input/output/scope privilege escalation rejection;
- protected/out-of-scope delegation collision rejection;
- inherited guardrail removal detection;
- delegation authority tampering detection;
- delegation seal tampering detection;
- delegation request shadow-field rejection;
- CLI delegate/verify-delegation path.

## Contract vectors

- ADMIT contract seal: `sha256:6f7f89c2eed90585dc5e348f0cdc96b5815642487ac419165312214d6b519aa6`
- REVIEW contract seal: `sha256:5173754a86b6aab69e3a4f71b9a8390e15ffb0e2893de50266704589fc180f16`
- FREEZE contract seal: `sha256:42c32af07e785dca570c1b1db9384b9ca98fa8fc7d0c51fae9ea9d14b219fd4c`

The vectors above were generated before the least-authority module was added; the base contract engine source remained semantically unchanged afterward. The final full regression suite was rerun after the delegation addition.

## Evidence-source state observed

Read-only NEXY.AI branch `NEXY.ai` was observed at commit:

`9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

No NEXY.AI mutation was performed by this session.

## Concurrent-work differentiation

During execution, another sibling Intent Integrity project appeared in AI-CONTEXT. This session re-inspected it and added a distinct executable least-authority delegation subsystem rather than pretending the overlap did not exist. See `docs/09_DIFFERENTIATION_AUDIT.md`.

## Limitations of this verification

- Tests are standalone prototype evidence, not production NEXY.AI runtime evidence.
- Parser/path rules are lexical and do not resolve filesystem aliases or symlinks.
- Hash seals provide integrity identity, not signer authentication.
- Node TypeScript stripping is experimental in Node 22 and emits a warning; behavior passed under the recorded toolchain.
