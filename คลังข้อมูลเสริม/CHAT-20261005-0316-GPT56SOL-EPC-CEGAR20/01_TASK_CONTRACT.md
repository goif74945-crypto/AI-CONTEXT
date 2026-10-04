# TASK CONTRACT — EPC CEGAR20

## OBJECTIVE
Create a standalone, deterministic, evidence-producing Lo4 reference crate implementing exactly 20 Abstract Interpretation + CEGAR mechanisms for future NEXY EPC use, using checked signed Q64.64 and preserving NEXY authority boundaries.

## REQUIRED OUTPUT
- exactly 20 documented and executable mechanisms
- checked signed Q64.64 arithmetic
- canonical deterministic effect IR and hashes
- tests: positive, adverse, arithmetic boundary, lattice, loop/fixpoint, counterexample, spurious-refinement, integrated CEGAR, determinism
- Design + Code + Tests + Evidence + exact hash manifest
- compatibility notes against exact read-only NEXY commit
- durable resume memory
- no NEXY.AI mutation

## AUTHORITY SOURCES
1. Explicit current user directive including EPC vote law.
2. Direct raw canonical NEXY-IGNIS source, SHA-256 b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7.
3. Current read-only NEXY implementation at 9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43.
4. AI-CONTEXT execution/security/verification/memory laws.
5. Lo4 output from this task is experimental only.

## IN SCOPE
Only new additive files under:
- คลังข้อมูลเสริม/CHAT-20261005-0316-GPT56SOL-EPC-CEGAR20/**
Potential future append-only vote record under:
- คลังข้อมูลเสริม/VOTES/**

## OUT OF SCOPE
- any mutation to NEXY.AI repositories
- Canon/DOC-B/DOC-C modification or promotion
- production integration/deployment
- claiming this standalone proof engine proves NEXY runtime behavior
- generic model checking, deontic jurisprudence, benchmarking, phase-boundary analysis, compatibility migration already owned by adjacent labs

## IMMUTABLE REQUIREMENTS
- AGENT/Lo4 proposes only; no state mutation authority.
- CORE/JUDGE remain decision authority.
- Missing proof or material contradiction fails closed / DEFER or FREEZE-compatible result.
- Authoritative numeric operations use signed Q64.64 only.
- Overflow/div-zero/malformed interval invalidates the analysis path.
- Abstract analysis must be conservative: never claim SAFE when the over-approximation intersects unsafe states.
- CEGAR may refine precision but never convert an unvalidated abstract witness into a concrete violation.
- Bounded iteration exhaustion yields INCONCLUSIVE, never optimistic PASS.
- One CHAT_ID gets one KEEP and one CUT lifetime round.
- UNKNOWN/WIP/INSUFFICIENT_EVIDENCE cannot justify CUT.
- CUT means archive/reject/supersede, not physical deletion.
- No score/vote auto-promotes or overrides Canon/Law/JUDGE.

## ACCEPTANCE CRITERIA
AC01 exactly 20 mechanism IDs map to implementation and tests.
AC02 cargo fmt --check PASS.
AC03 cargo clippy --all-targets --all-features -- -D warnings PASS if toolchain component exists; otherwise explicit BLOCKED for clippy only.
AC04 cargo test PASS after final source bytes.
AC05 arithmetic boundary tests include min/max, overflow, divide-by-zero.
AC06 lattice join/meet monotonicity and interval validity tests PASS.
AC07 abstract transfer never under-approximates tested concrete samples.
AC08 unsafe intersection is never reported SAFE.
AC09 spurious abstract witness triggers refinement rather than false FAIL.
AC10 real concrete witness remains a violation after replay.
AC11 loop analysis converges or returns bounded INCONCLUSIVE.
AC12 repeated identical inputs produce byte-identical capsule/hash.
AC13 no f32/f64 authoritative decision path.
AC14 no network/wall-clock/randomness used in proof decisions.
AC15 published source/test/evidence bytes are read back from GitHub.
AC16 final protected NEXY head unchanged by this task.
AC17 KEEP/CUT only after direct spec + exact NEXY + current AI-CONTEXT evidence.
AC18 evidence distinguishes standalone E1/E2/E3 from unverified NEXY integration.

## STOP CONDITIONS
Stop promotion/vote and preserve DEFER/NOT_VERIFIED if:
- protected scope mutation would be required
- current NEXY head drift invalidates pinned compatibility evidence
- source authority conflicts materially
- final tested bytes differ from published bytes
- any soundness regression remains unresolved
