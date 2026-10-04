# NEXY Q64 Constitutional Physics — Lo4 Proposal Lab

**Status:** `Lo4_AI_PROPOSAL_ONLY / ADVISORY / NON_GOVERNING`

This isolated reference lab explores five quantitative control primitives that may be useful to a future NEXY.AI integration review. It does **not** modify NEXY.AI, does not become Canon by existing, and does not prove production integration.

## Why this exists
NEXY's source-derived principles emphasize deterministic execution, explicit authority, verification, freeze-on-ambiguity, and evidence before action. Many control decisions still need quantitative reasoning. Using binary floating point inside authority/safety boundaries can introduce platform-dependent edge behavior, hidden epsilons, and accidental uncertainty collapse. This lab therefore models every quantitative value as checked signed Q64.64 fixed-point.

## Five proposed systems
1. **UMC — Uncertainty Mass Conservation Compiler**: uncertainty may move, be introduced, or be resolved with evidence, but may not silently disappear.
2. **DRC — Decision Robustness Certificate Engine**: certifies whether a bounded perturbation box can flip a linear threshold decision.
3. **VBR — Vector Budget Reactor**: reserves non-fungible plan budgets by dimension without averaging privacy, compute, irreversibility, or other incomparable resources into one scalar.
4. **RHL — Reversibility Half-Life Scheduler**: models deterministic rollback-quality decay and identifies the latest safe execution tick.
5. **EDB — Expectation Divergence Barrier**: blocks execution if the executable consequence model diverges materially from the user-visible preview.

## Numeric law
- raw representation: signed checked 128-bit integer;
- scale: `2^64`;
- multiplication/division rounding: nearest, ties-to-even;
- floats: forbidden at API boundaries;
- overflow/divide-by-zero: fail closed;
- decimal input: explicit decimal strings only;
- UMC conservation tolerance: at most **1 raw ULP** to account for independently quantized decimal identities. This is an exact representation rule, not a floating epsilon.

## Verification
Local isolated reference verification includes compile/static checks, 37 unit/adversarial/integration tests, 1,000 deterministic/property stress checks, an explicit TDD RED record, and a regression RED→GREEN replay for the discovered 1-ULP defect.

See `evidence/EVIDENCE.md` for exact claim boundaries. NEXY runtime integration, deployment, production security, performance under production load, and Canon promotion remain `NOT_VERIFIED`.
