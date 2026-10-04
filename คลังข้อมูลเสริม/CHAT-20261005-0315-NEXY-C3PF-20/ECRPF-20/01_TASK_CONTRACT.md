# ECRPF-20 Task Contract

## OBJECTIVE
Deliver an isolated, executable, deterministic Lo4 reference implementation of exactly 20 configuration and rollout assurance mechanisms that can be adapted to current NEXY configuration surfaces without mutating NEXY.

## REQUIRED OUTPUT
- exact source, tests, design, integration contract, collision audit, evidence, manifest, final audit;
- signed-i128-compatible Q64.64 BigInt arithmetic for decision metrics;
- deterministic SHA-256 proof capsules and rollout cohorts;
- fail-closed validation of unsafe configuration states;
- EPC evidence sufficient for at most one KEEP or one CUT decision for this chat.

## IN SCOPE
Only additive artifacts in the ECRPF candidate path and one append-only vote record if a vote is justified.

## OUT OF SCOPE
NEXY source mutation, live configuration writes, secret retrieval, environment mutation, deployment execution, automatic promotion, Canon change, Core/JUDGE/SWARM authority change.

## IMMUTABLE RULES
- Canon/LAW/JUDGE/CORE outrank ECRPF.
- ECRPF PASS is advisory evidence only.
- Secret plaintext may never be normalized into a valid sensitive configuration value.
- Production fail-open modes marked dev-only must fail.
- Build-immutable values may not change through runtime rollout.
- Q64.64 is the only authoritative fractional arithmetic in this lab.
- No RNG, wall clock, locale, network, or object insertion order may affect a verdict.
- Existing EPC vote records are immutable; no vote reset on candidate pivot.

## ACCEPTANCE CRITERIA
- 20/20 mechanisms present.
- strict TypeScript compile PASS.
- final tests PASS twice from exact source bytes.
- Q64 overflow/divide-by-zero/adverse boundaries PASS.
- deterministic proof under repeated evaluation, entry reorder, and rule reorder.
- production fail-open mutation set fully rejected.
- plaintext-secret mutation set fully rejected.
- source nondeterminism and float audit PASS.
- exact published bytes match local SHA-256 manifest.
- no NEXY repository writes.
- overlap scan does not reveal a stronger semantically equivalent existing system.

## STOP CONDITIONS
Freeze KEEP if publication readback differs, NEXY head materially changes assumptions, a stronger duplicate appears, any final test fails, or current evidence cannot support compatibility claims.
