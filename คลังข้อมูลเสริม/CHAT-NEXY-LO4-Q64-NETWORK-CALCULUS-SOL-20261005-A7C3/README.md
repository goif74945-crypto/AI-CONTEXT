# NEXY Lo4 Q64 Network Calculus Foundry

**Status:** `Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON_CANONICAL`  
**Work code:** `CHAT-NEXY-LO4-Q64-NETWORK-CALCULUS-SOL-20261005-A7C3`  
**Target:** future-compatible advisory tooling for NEXY.AI.  
**Protected boundary:** this lab does not modify any repository whose name contains `NEXY.AI`.

This project explores deterministic network-calculus primitives for NEXY-style bounded queues and multi-stage pipelines. It converts explicit token-bucket arrival contracts and rate-latency service contracts into conservative Q64.64 certificates for admission, backlog, latency, chain composition, and shaping.

## Five systems

1. **FLOWGUARD-64** — admits a flow only when the declared service rate is sufficient and all requested bounds are met.
2. **QUEUEBOUND-64** — computes a conservative worst-case backlog bound `B = b + rT` and checks an explicit buffer cap.
3. **DEADLINE-64** — computes a conservative worst-case delay bound `D = T + b/R` with upward Q64.64 rounding.
4. **CHAIN-64** — composes a fluid rate-latency service chain with effective `R = min(R_i)` and `T = sum(T_i)` before certifying end-to-end bounds.
5. **SHAPER-64** — synthesizes a reduced burst/rate envelope that satisfies declared backlog/deadline limits when possible.

## Why this is different

The inspected supplemental work already contains many proof, authority, replay, uncertainty, robotics, preference, and generic resource-governance systems. This lab targets a narrower mathematical surface: deterministic queue/pipeline envelope bounds using a shared exact Q64.64 substrate. A repository keyword collision scan found no direct match for the network-calculus mechanisms used here at the inspected baseline.

## Numeric and failure law

- Decision quantities are signed-128-compatible raw Q64.64 `bigint` values.
- Binary floating point is not accepted or used by quantitative decision modules.
- Overflow never wraps or saturates.
- Upper safety bounds use directed ceiling operations where truncation could understate risk.
- Invalid contracts become `FREEZE`; unstable flows are rejected/frozen according to the owning certifier; no silent fallback upgrades them to PASS.
- The deterministic result fingerprint is an identity aid, not a cryptographic integrity primitive. Repository SHA-256 manifests provide artifact integrity evidence.

## Verification

`bash scripts/verify.sh` performs typecheck, build, unit/integration tests, a bounded 5,670-case stress corpus, no-float/no-dynamic-network static audit, and a 200-vector independent Python integer-oracle cross-check.

Passing these checks proves only the isolated reference implementation at the tested bytes. NEXY runtime integration, production load behavior, deployment readiness, and Canon promotion remain `NOT_VERIFIED`.
