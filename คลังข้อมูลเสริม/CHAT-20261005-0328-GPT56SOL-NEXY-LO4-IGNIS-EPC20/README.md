# NEXY Lo4 IGNIS EPC20 Research Portfolio

CHAT_ID: `CHAT-20261005-0328-GPT56SOL-NEXY-LO4-IGNIS-EPC20`
PLATFORM_NATIVE_CHAT_ID: `UNKNOWN_NOT_EXPOSED`
STATUS: `Lo4 / ADVISORY / NOT CANON / NOT PROMOTED`

Authoritative NEXY-IGNIS source SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`
Inspected NEXY commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
Protected target: `goif74945-crypto/NEXY.AI-` branch `NEXY.ai`, READ ONLY.

This namespace contains 20 standalone deterministic Lo4 verifiers for future adapter-based integration research. A PASS is never release authorization and cannot override Canon, CORE, LAW, or JUDGE.

## Systems
- **S01 Action Reversibility Preflight**: Block destructive actions without a proven rollback path. NOVELTY=PARTIAL
- **S02 Queue Wait Fairness Monitor**: Detect queue starvation using exact Q64.64 wait fairness. NOVELTY=PARTIAL
- **S03 Non-Goal Creep Sentinel**: Reject requests that intersect authoritative excluded scope. NOVELTY=PARTIAL
- **S04 Retry Harm Guard**: Block retries that can duplicate ambiguous side effects. NOVELTY=PARTIAL
- **S05 Precondition Disclosure Gate**: Require execution preconditions to be satisfied and disclosed. NOVELTY=PARTIAL
- **S06 Session Expiry Transparency Gate**: Require deterministic expiry warning and block expired sessions. NOVELTY=PARTIAL
- **S07 Session Revocation Completeness Proof**: Detect residual active session handles after revocation. NOVELTY=PARTIAL
- **S08 Structured Error Actionability Gate**: Require errors to expose actionable structured recovery data. NOVELTY=PARTIAL
- **S09 Partial Success Prohibition Gate**: Prevent aggregate PASS/OK over mixed component outcomes. NOVELTY=PARTIAL
- **S10 State Disclosure Consistency Gate**: Verify visible state matches authoritative internal state. NOVELTY=PARTIAL
- **S11 Secret Placeholder Integrity Gate**: Reject literal secret material from configuration artifacts. NOVELTY=PARTIAL
- **S12 Ownership Export Completeness Verifier**: Verify every owned ID is exported or explicitly excluded. NOVELTY=PARTIAL
- **S13 Capability Claim Calibration Gate**: Block capability claims lacking verified capability IDs. NOVELTY=PARTIAL
- **S14 Idempotency Feedback Gate**: Require exact replay identity and visible REPLAYED feedback. NOVELTY=PARTIAL
- **S15 Rate-Limit Recovery Contract Auditor**: Require consistent retry timing and user disclosure. NOVELTY=PARTIAL
- **S16 Audit Correlation Completeness Compiler**: Verify correlated audit event chains remain reconstructable. NOVELTY=PARTIAL
- **S17 Cancellation Propagation Witness**: Verify cancellation reached all participants with no later effect. NOVELTY=PARTIAL
- **S18 Stale-Job User Impact Gate**: Prevent hidden or effectful stale jobs. NOVELTY=PARTIAL
- **S19 Evidence Explanation Loss Auditor**: Detect missing or invented evidence refs in explanations. NOVELTY=UNKNOWN
- **S20 Canonical Reason Precedence Resolver**: Make multi-failure presentation order-independent. NOVELTY=PARTIAL

## Verified local evidence
- TDD RED observed before implementation.
- First implementation: 36/37 tests PASS, S09 parser defect found.
- Minimal repair performed; regression 37/37 PASS.
- compileall PASS.
- Cross-process deterministic replay: identical bytes for PYTHONHASHSEED 0,1,2,42,999,random.
- Portfolio deterministic digest: `15a4bd7b4f5dc784713bfeeb3cbb38550b230d2f4216e507dbfc6ba9ced81630`.

See DESIGN, ARCHITECTURE, TEST_EVIDENCE, COLLISION_MAP, COMPARISON_MATRIX and FINAL_AUDIT.
