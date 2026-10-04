# Verification Evidence Summary

Exact tested archive SHA-256:
`d6f666df71d104fa3255285858204572dcfb65604f311d66d56dd57b0847ab0f`

Clean authoritative run:
- deterministic source scan: PASS
- TypeScript clean build: PASS
- tests: 35 PASS / 0 FAIL
- AIK modules: exactly 20
- exhaustive deterministic observation/verification corpus: 4,096 states
- Q64 range/overflow/divide-by-zero tests: PASS
- EPC one-KEEP/one-CUT entitlement tests: PASS
- WIP/INSUFFICIENT_EVIDENCE CUT rejection: PASS
- non-destructive CUT semantics: PASS
- Canon authority escalation rejection: PASS

A prior non-authoritative run exposed stale compiled CEK20 tests because tsc does not clean dist. The harness was repaired to run `rm -rf dist` before each compile; only the post-repair 35/35 run is authoritative.

First-generation CEK20 was also discarded despite green tests after semantic collision audit proved substantial overlap with existing Proof Sensitivity, Evidence Independence, Counterfactual Verification, Proof Compiler, Negative-Space, Proof Efficiency, and Evolution Compatibility work.

Claim boundary: this proves standalone source/test behavior for the archive bytes, not NEXY production integration, deployment, universal novelty, security against all attacks, or Canon promotion.
