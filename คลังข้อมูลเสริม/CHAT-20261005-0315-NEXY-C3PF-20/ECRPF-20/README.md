# NEXY Environment Contract & Rollout Proof Fabric (ECRPF-20)

**Classification:** Lo4 AI proposal only. Experimental, non-canonical, non-governing.

ECRPF-20 is an isolated deterministic preflight compiler for configuration changes that cross build-time constants, process environment variables, durable runtime configuration, secret-provider references, deployment-provider bindings, and staged feature rollout. It does **not** mutate NEXY, deploy anything, change Canon, replace `runtime-config.ts`, or grant deployment authority.

The failure boundary is configuration truth fragmentation: individually valid configuration mechanisms can disagree across sources or environments. ECRPF turns a normalized candidate configuration into a 20-mechanism proof capsule and fails closed on unsafe contradictions.

## 20 implemented mechanisms

1. Config Schema Lock
2. Environment Key Canonicalizer
3. Required-Key Closure
4. Forbidden-Key Environment Guard
5. Type & Domain Validator
6. Secret-vs-Plaintext Boundary Detector
7. Default Shadowing Analyzer
8. Override Precedence Proof
9. Conditional Dependency Closure
10. Mutual Exclusion Guard
11. Fail-Mode Safety Classifier
12. Cross-Environment Parity Diff
13. Build-vs-Runtime Immutability Binder
14. Deterministic Rollout Cohort Engine
15. Rollout Monotonicity Gate
16. Rollback Closure Verifier
17. Config Migration Compatibility Proof
18. Q64.64 Blast Radius Estimator
19. Canonical Config Proof Capsule Compiler
20. Non-Authoritative Deployment Handoff Gate

## Determinism

Authoritative scoring and rollout fractions use signed i128-compatible Q64.64 carried by `bigint`; binary floating point is not used for verdict arithmetic. Canonical JSON sorts object keys and explicitly encodes BigInt. Rollout cohorts use SHA-256(flag key, subject) and compare the first 64 hash bits against a Q64.64 fraction, so assignment is reproducible without RNG or wall clock.

## Verification boundary

Local compilation/tests prove only the isolated reference implementation. Integration into NEXY remains a future VERIFY-owned step. No PASS from this lab is production authorization.
