# DESIGN — 20 Lo4 Systems

Authority: advisory only.
Spec SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
NEXY source commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`

## S01 — Action Reversibility Preflight
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Block destructive actions without a proven rollback path.
- **PROBLEM:** Block destructive actions without a proven rollback path. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** destructive:boolean; reversible:boolean; rollback_proof:sha256
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** destructive implies reversible plus valid rollback proof.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S02 — Queue Wait Fairness Monitor
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Detect queue starvation using exact Q64.64 wait fairness.
- **PROBLEM:** Detect queue starvation using exact Q64.64 wait fairness. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** wait_ticks map; min_fairness_q64 raw
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** fairness=min(wait)/max(wait), all-zero=1; threshold exact.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S03 — Non-Goal Creep Sentinel
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Reject requests that intersect authoritative excluded scope.
- **PROBLEM:** Reject requests that intersect authoritative excluded scope. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** requested_features[]; excluded_features[]
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** intersection must be empty.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S04 — Retry Harm Guard
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Block retries that can duplicate ambiguous side effects.
- **PROBLEM:** Block retries that can duplicate ambiguous side effects. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** attempt; retry_budget; prior-effect; side_effect_free; idempotency_proven
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** attempt within budget and unknown effect requires safety proof.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S05 — Precondition Disclosure Gate
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Require execution preconditions to be satisfied and disclosed.
- **PROBLEM:** Require execution preconditions to be satisfied and disclosed. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** preconditions[{id,satisfied,disclosed}]
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** every precondition satisfied and disclosed.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S06 — Session Expiry Transparency Gate
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Require deterministic expiry warning and block expired sessions.
- **PROBLEM:** Require deterministic expiry warning and block expired sessions. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** current_tick; warning_tick; expiry_tick; user_warned
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** warning<=expiry; warning disclosed; expired freezes.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S07 — Session Revocation Completeness Proof
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Detect residual active session handles after revocation.
- **PROBLEM:** Detect residual active session handles after revocation. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** revocation_requested; active_handles[]; revoked_handles[]
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** active handles subset of revoked handles when requested.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S08 — Structured Error Actionability Gate
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Require errors to expose actionable structured recovery data.
- **PROBLEM:** Require errors to expose actionable structured recovery data. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** code; blocking_layer; recoverable; remediation
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** all four fields required; actionability score must be Q64 one.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S09 — Partial Success Prohibition Gate
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Prevent aggregate PASS/OK over mixed component outcomes.
- **PROBLEM:** Prevent aggregate PASS/OK over mixed component outcomes. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** component_statuses[]; reported_status
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** success report only when every required component PASS.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S10 — State Disclosure Consistency Gate
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Verify visible state matches authoritative internal state.
- **PROBLEM:** Verify visible state matches authoritative internal state. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** internal_state; visible_state
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** states must match exactly.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S11 — Secret Placeholder Integrity Gate
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Reject literal secret material from configuration artifacts.
- **PROBLEM:** Reject literal secret material from configuration artifacts. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** server_only; config map
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** server-only and sensitive values must be runtime placeholders.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S12 — Ownership Export Completeness Verifier
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Verify every owned ID is exported or explicitly excluded.
- **PROBLEM:** Verify every owned ID is exported or explicitly excluded. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** owned_ids[]; exported_ids[]; excluded map
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** owned = exported union justified exclusions, no foreign IDs.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S13 — Capability Claim Calibration Gate
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Block capability claims lacking verified capability IDs.
- **PROBLEM:** Block capability claims lacking verified capability IDs. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** declared[]; verified[]
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** declared subset of verified; Q64 coverage=1.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S14 — Idempotency Feedback Gate
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Require exact replay identity and visible REPLAYED feedback.
- **PROBLEM:** Require exact replay identity and visible REPLAYED feedback. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** duplicate; intent/result hashes; user_feedback
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** duplicate replay requires equal intent/result hashes and REPLAYED disclosure.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S15 — Rate-Limit Recovery Contract Auditor
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Require consistent retry timing and user disclosure.
- **PROBLEM:** Require consistent retry timing and user disclosure. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** limited; current_tick; retry_after_ticks; unlock_tick; disclosure
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** unlock=current+retry_after and recovery disclosed.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S16 — Audit Correlation Completeness Compiler
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Verify correlated audit event chains remain reconstructable.
- **PROBLEM:** Verify correlated audit event chains remain reconstructable. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** events[{sequence,request_id,trace_id,correlation_id}]
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** sequence contiguous and correlation IDs stable.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S17 — Cancellation Propagation Witness
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Verify cancellation reached all participants with no later effect.
- **PROBLEM:** Verify cancellation reached all participants with no later effect. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** cancel_requested; components; post-cancel effects
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** all participants CANCELLED/STOPPED and no later effect.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S18 — Stale-Job User Impact Gate
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Prevent hidden or effectful stale jobs.
- **PROBLEM:** Prevent hidden or effectful stale jobs. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** stale; expired; user_status; side_effect_after_expiry
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** stale implies expired+disclosed and no post-expiry effect.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S19 — Evidence Explanation Loss Auditor
**NOVELTY:** UNKNOWN; absolute uniqueness is not claimed.
- **PURPOSE:** Detect missing or invented evidence refs in explanations.
- **PROBLEM:** Detect missing or invented evidence refs in explanations. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** required_evidence[]; explained_evidence[]
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** sets must match exactly; Q64 coverage=1.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.

## S20 — Canonical Reason Precedence Resolver
**NOVELTY:** PARTIAL; absolute uniqueness is not claimed.
- **PURPOSE:** Make multi-failure presentation order-independent.
- **PROBLEM:** Make multi-failure presentation order-independent. is not guaranteed by a generic success/failure surface alone.
- **THREAT MODEL:** malformed, stale, reordered, incomplete, misleading or authority-bypassing inputs; omission attacks remain possible if an upstream inventory is incomplete.
- **INPUT:** reasons[]
- **OUTPUT:** deterministic PASS or FREEZE decision, reason, metrics when applicable, and SHA-256 evidence root.
- **STATE:** stateless evaluation of an explicit snapshot.
- **INVARIANTS:** select only by governed total precedence; unknown reason freezes.
- **AUTHORITY BOUNDARY:** verifier only; cannot execute, release, promote, mutate Canon/Core/LAW/JUDGE, or widen permissions.
- **FAILURE MODES:** malformed input, missing evidence, invariant violation, stale/incomplete adapter data, numeric fault when quantitative.
- **FREEZE CONDITIONS:** malformed/unsupported input or any violation of the stated invariant.
- **DEPENDENCIES:** future adapter plus authoritative source/inventory appropriate to this system.
- **SECURITY MODEL:** minimal identifiers/hashes/statuses; no secret echo; no side effects.
- **DETERMINISM MODEL:** canonical UTF-8 data, Unicode-scalar key ordering, no time/random/network/hidden I/O; quantitative paths use checked signed Q64.64 only.
- **INTEGRATION CONTRACT:** adapter must bind exact NEXY/spec version, preserve evidence identity, and treat PASS as advisory predicate only.
- **TEST PLAN:** positive, negative, malformed, replay/order, authority-bypass and boundary tests as applicable.
- **ACCEPTANCE CRITERIA:** all tested invariant violations FREEZE; valid reference case PASS; repeated semantic input produces identical result/root.
- **EVIDENCE REQUIREMENTS:** local E1/E2 tests now; future exact-head integration/runtime evidence before promotion.
- **TRADE-OFFS:** standalone verifier strength depends on completeness and truth of upstream evidence.
- **FUTURE EXTENSIONS:** versioned governed adapter/schema plus integration-specific proof obligations.
