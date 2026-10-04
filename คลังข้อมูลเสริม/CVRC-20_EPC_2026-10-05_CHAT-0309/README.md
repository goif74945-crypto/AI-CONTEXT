# NEXY Cross-Version Refinement Calculus (CVRC-20)

**Layer:** Lo4 AI-proposed reference lab  
**Authority:** NONE until formal NEXY governance/promotion  
**Storage:** AI-CONTEXT only  
**NEXY mutation:** forbidden

## Locked target
- repo: `goif74945-crypto/NEXY.AI-`
- branch: `NEXY.ai`
- commit: `9e615b04ecd1e9b8b5afcd5f812ea17bd78d4a43`
- source Canon SHA-256: `b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7`

CVRC-20 is a deterministic, scope-aware compatibility court for proposed NEXY evolution. Systems 01–19 prove distinct preservation obligations; system 20 aggregates them into a proposal-only verdict: `KEEP_CANDIDATE | REJECT | DEFER`.

## Hard invariants
1. Missing/malformed evidence cannot produce KEEP.
2. Proven regression produces REJECT, but REJECT itself has no Canon authority.
3. Q64.64 verdict telemetry uses signed-i128 bounded bigint, not IEEE-754.
4. Numeric law is scope-aware: current NEXY Core L9 overflow FREEZEs, while Game G15 saturates.
5. Target commit mismatch yields DEFER.
6. CVRC exports no Core/Law/Vault mutation or Canon-promotion API.
7. Deterministic summaries use canonical ordering and SHA-256.

## Verification performed
- syntax: PASS
- unit suite: PASS, 83 assertions
- malformed corpus: PASS, 26 cases
- deterministic mutation stress: PASS, 5,000/5,000 regressions rejected and 5,000/5,000 replay hashes identical
- benchmark observation: about 5.7k evaluations/sec in the local execution environment; non-authoritative and excluded from verdicts

## Important repair history
The first unit run failed because the test incorrectly expected `1.5 * (2/3)` to equal exact 1.0 in Q64.64. Since 2/3 is not exactly representable, the exact result is `ONE - 1 raw unit`. Only the test oracle was corrected. Later code-to-target inspection found two baseline-model defects before publication: `AgentAdapter.supported_modes` had initially been named `modes`, and the Evidence contract initially omitted required provenance fields. Both were corrected and the full suite rerun.

See `20_DESIGNS.md`, `EVIDENCE.md`, and the source/test files in this folder.
