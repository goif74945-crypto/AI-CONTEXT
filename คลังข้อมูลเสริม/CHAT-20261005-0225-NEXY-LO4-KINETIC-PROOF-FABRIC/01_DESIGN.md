# 01 — Kinetic Proof Fabric Design Contract

Status: Lo4_AI_PROPOSAL_ONLY / EXPERIMENTAL / NON-CANON
Work code: CHAT-20261005-0225-NEXY-LO4-KINETIC-PROOF-FABRIC

## Objective
Create a deterministic cyber-physical pre-actuation verification fabric compatible with the future NEXY Robotics/RCL direction while remaining strictly below Canon and below the independent physical Safety Kernel.

## Authority boundary
The current NEXY context says Robotics/RCL is SOURCE-DESIGN / future direction and not verified runtime. The current normalized source matrix contains 837 requirement rows but does not prove implementation. This lab therefore does not claim current NEXY integration, deployment, HIL, certification, or physical safety.

## Exact five Lo4 proposals
1. PSTL — Physical State Trust Lattice
2. WMDS — World-Model Divergence Sentinel
3. AEPE — Actuation Envelope Proof Engine
4. CHI — Cumulative Hazard Integrator
5. RHPV — Reflex/Safe-Path Handoff Verifier

Proposed composition:
Sensors -> PSTL -> WMDS -> AEPE -> CHI -> RHPV -> proposed actuation capsule -> independent Safety Kernel

## Global invariants
KPF-I1: All real-valued decision arithmetic uses checked signed Q64.64.
KPF-I2: Python float and bool numeric input are forbidden in the deterministic decision path.
KPF-I3: Signed raw range is [-2^127, 2^127-1]; overflow fails closed.
KPF-I4: Same canonical software inputs produce the same structural result.
KPF-I5: Upstream uncertainty may not silently become downstream certainty.
KPF-I6: Unsafe cumulative-hazard proposals never commit.
KPF-I7: A latched reflex stop cannot be overridden by Safe Path in the same epoch.
KPF-I8: Braking proof uses max(abs(current_velocity), abs(target_velocity)); deceleration intent cannot erase existing kinetic risk.
KPF-I9: Independent Safety Kernel remains superior authority.
KPF-I10: No artifact in this folder can self-promote into NEXY Canon.

## Q64.64 contract
real = raw / 2^64, where raw is a checked signed 128-bit integer.
Addition/subtraction are exact raw operations with overflow checks.
Multiplication uses truncation-toward-zero of (a.raw*b.raw)/2^64.
Division uses truncation-toward-zero of (a.raw*2^64)/b.raw.
Decimal text is parsed by integer arithmetic, never binary floating point.

## PSTL
Inputs: source id, value, uncertainty radius, trust, age, max age.
Algorithm:
- validate source uniqueness and numeric bounds;
- exclude stale and below-policy-trust samples;
- convert each eligible sample to a closed interval;
- run weighted endpoint sweep O(n log n);
- choose deterministic lowest coordinate among equal maximum-support points;
- recover supporting intervals;
- require minimum source count and trust quorum;
- output the bounded intersection midpoint + uncertainty, otherwise FREEZE.

## WMDS
For each required axis:
normalized_residual = abs(observed-predicted)/tolerance.
hard threshold is inclusive and FREEZEs.
soft threshold is inclusive and yields CAUTION.
Missing axes, invalid tolerance, negative weights, or zero weight mass fail closed.

## AEPE
Checks speed, force, acceleration transition, projected boundary, and stopping clearance.

v_brake = max(abs(current_v), abs(target_v))
d_stop = v_brake^2/(2*max_deceleration) + v_brake*reaction_time
Required clearance = d_stop + margin.

Development defect lineage:
The first implementation used target velocity alone in d_stop. A regression case with current velocity 9 and target velocity 1 exposed a false PASS. The implementation was repaired and the regression retained.

## CHI
State dimensions in this reference model: thermal, energy, wear.
proposed = current*decay + impulse
If every proposed dimension <= cap, commit.
If any dimension exceeds cap, FREEZE and retain the prior committed state.

## RHPV
Commands bind source, kind, epoch, sequence, issued time, lease expiry and canonical state SHA-256.
- future/expired/invalid lease -> FREEZE;
- replay/non-monotonic sequence -> FREEZE;
- SAFE requires exact epoch + state hash;
- REFLEX may only STOP and latches;
- SAFE is blocked while latched;
- reset is externally authorized and advances epoch exactly one.

## Cross-module transaction law
Externally visible state is not treated as committed until all five stages pass. If a later handoff stage fails, the hazard ledger returned to the caller remains the pre-command committed state.

## Non-goals
No ROS2 transport, hardware driver, SLAM, PID/MPC, real-time guarantee, WCET proof, HIL proof, safety certification, physical emergency-stop proof, deployment claim, self-modifying policy, or Canon promotion.

## Promotion gate
Any future adoption requires explicit authorized promotion, current compatibility review against NEXY requirements, exact-revision integration tests, target-runtime evidence and physical/HIL evidence appropriate to the claimed safety property.
