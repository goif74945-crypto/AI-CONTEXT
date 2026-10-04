# Design — Lo4 Q64.64 Human-Control Coordination Fabric 20

Classification: `AI_PROPOSED / EXPERIMENTAL / NON-CANON / ADVISORY`

## Shared architecture

```text
Normalized adapter inputs
  -> strict Q64.64 boundary (float rejected)
  -> one or more of 20 pure deterministic scorers
  -> stable rank(score desc, UTF-8 key asc)
  -> advisory coordination artifact
  -> existing NEXY authority / LAW / JUDGE remains superior
```

The reference implementation is pure and side-effect free. It does not read secrets, mutate repositories, call networks, or claim authority. Python integers are used as the backing arithmetic carrier, but every Q64 value is range-checked to signed 128-bit raw space `[-2^127, 2^127-1]`. Multiplication/division compute exact integer intermediates then truncate toward zero once into Q64.64. Floats are rejected.

## 20 systems

### 01 DAB — Deterministic Attention Budgeter
Objective: allocate scarce attention using urgency, impact, uncertainty and interruption cost. Output: `[0,1]`. Failure: any non-unit input raises explicit error. Future adapter: UI notification/agent scheduling hints only.

### 02 CEG — Context Entropy Governor
Objective: detect whether working context is concentrated or dispersed using a Gini-Simpson-style `1-sum(p²)` proxy without logarithms. Requires concentrations to sum to exact Q64 ONE. Output `[0,1]`. Useful for deciding when context should be compressed or partitioned, not what content is authoritative.

### 03 SDI — Semantic Drift Integrator
Objective: normalized L1 drift between same-length Q64 vectors. Mismatched/empty vectors fail. Can expose change magnitude across requirement snapshots or agent state without pretending similarity equals truth.

### 04 ICP — Intent Compression Planner
Objective: prioritize compression only where redundancy and retrieval cost are high and information importance is low. It never deletes content by itself.

### 05 UFF — User Friction Field
Objective: quantify steps, reversals, ambiguity and latency into a deterministic friction score. This gives NEXY UX adapters a measurable optimization target rather than aesthetic guesswork.

### 06 DVS — Deferred Value Scheduler
Objective: value work after delay with rational Q64 decay plus explicit dependency gain. It is advisory and does not dispatch jobs.

### 07 IGR — Information Gain Router
Objective: prioritize information-seeking action as `unknown_mass * resolvable_mass / cost`. Zero cost is rejected to prevent infinite/undefined priority.

### 08 TICS — Tool Invocation Cost Surface
Objective: combine success, evidence gain, latency cost and mutation risk. It can rank tools/calls after permissions are already resolved; it cannot grant permissions.

### 09 EDC — Explanation Density Controller
Objective: estimate useful verified-claim density per token, penalized by unresolved ratio. It can help keep outputs dense without hiding uncertainty.

### 10 RPO — Recovery Priority Orchestrator
Objective: order recovery candidates by blast radius, user impact, irreversibility and weak evidence. It only ranks; actual recovery remains governed elsewhere.

### 11 MHUI — Multi-Horizon Utility Integrator
Objective: combine immediate/near/long utility then discount irreversible penalty. It prevents one-horizon optimization from dominating planning by default.

### 12 CSM — Capability Saturation Monitor
Objective: combine demand/capacity utilization with queue pressure. Zero capacity is explicit error. It can trigger scale/defer proposals but not capability admission.

### 13 IRR — Interaction Rhythm Regulator
Objective: quantify pacing pressure from message rate, correction rate and inverse idle ratio. Intended for adaptive conversational pacing, not psychological inference.

### 14 DRM — Decision Reversibility Meter
Objective: measure rollback coverage, state capture and lack of external side effects. Useful when choosing between equally legal actions; it does not authorize irreversible work.

### 15 SFDE — State Freshness Decay Engine
Objective: deterministic rational decay `initial/(1 + pressure*age)` without floating exponentials. Produces a freshness signal, not an evidence-validity verdict.

### 16 BESA — Budget-aware Evidence Sampling Allocator
Objective: rank missing evidence by materiality, uncertainty, uncovered mass and sample cost. It optimizes which proof to seek next without declaring proof sufficient.

### 17 CCM — Cross-model Calibration Mixer
Objective: weighted mean of normalized model estimates using explicit Q64 confidences. Zero total weight fails. It is not consensus authority and never outranks JUDGE.

### 18 SCIW — Spec Change Impact Wavefront
Objective: score likely impact from direct impact, fanout, coupling and test gap. It helps select audit depth after a spec change without mutating code.

### 19 DHCE — Deterministic Handoff Continuity Engine
Objective: score resumption quality from state coverage, decision provenance, blocker clarity and evidence links. Designed to reinforce AI-CONTEXT long-context survival.

### 20 UVFE — User Value Frontier Estimator
Objective: rank candidate experiences using correctness-dominant weighting plus usefulness, low latency, low cognitive load and low lock-in. Correctness gets the largest share and existing NEXY law still dominates this advisory score.

## Shared invariants
1. `float` never enters the Q64 decision boundary.
2. Signed Q64.64 raw range is checked on construction and every arithmetic output.
3. Division by zero fails explicitly.
4. Unit-domain inputs are validated where semantically required.
5. Stable ranking uses score descending then UTF-8 key bytes ascending.
6. No function has side effects.
7. No scorer output is authority; adapters must treat it as advisory.
8. Mutation, security permission, release, Canon promotion and physical safety remain outside this fabric.
