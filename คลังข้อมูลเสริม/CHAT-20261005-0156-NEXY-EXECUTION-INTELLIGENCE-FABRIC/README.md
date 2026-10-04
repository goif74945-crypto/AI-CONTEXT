# NEXY Execution Intelligence Fabric (EIF)

**Classification:** `AI-PROPOSED / EXPERIMENTAL / NOT CANON`

EIF is a standalone reference package exploring five execution-intelligence mechanisms that can sit beside NEXY-style LAW/JUDGE/RUN/Vault flows through explicit JSON contracts. It does not import NEXY.AI code and does not claim NEXY.AI currently implements any of these systems.

## Why this exists
A control system can be safe yet still annoy users, waste models, ask unnecessary questions, declare tasks complete too early, or discover rollback problems after mutation. EIF targets those gaps with deterministic planning rather than adding another vague “smart agent.”

## Five concepts
1. **Goal-State Compiler (GSC)** — turns desired outcomes, forbidden outcomes, required capabilities and required outputs into a tamper-evident executable acceptance contract.
2. **Unknown Closure Planner (UCP)** — computes the minimum-cost set of questions/probes needed to resolve facts that actually block execution.
3. **Assurance Budget Planner (ABP)** — finds the cheapest deterministic validator set that still satisfies evidence coverage and independence requirements.
4. **Reversibility Envelope (RE)** — refuses mutation plans that lack rollback/compensation or explicit approval for irreversible actions, and computes rollback order before execution.
5. **Counterexample Synthesizer (CES)** — compiles simple field contracts into deterministic negative/boundary test vectors.

## Integrated states
- `READY`: goal verified, unknown closure not needed, assurance plan exists, reversibility plan is legal, counterexample suite valid.
- `ASK`: execution is otherwise legal but specific unresolved facts have a deterministic minimum question set.
- `FREEZE`: goal conflict/failure, unresolvable unknown, insufficient assurance, unsafe irreversible action, invalid base contract, or invalid input.

## Runtime dependencies
Python standard library only. No network access, model calls, subprocess execution inside the library core, database, or NEXY.AI repository dependency.

## Verification entrypoint
```text
python scripts/verify.py
```

## CLI adapter
```text
python cli.py payload.json
cat payload.json | python cli.py
```
Exit codes: `0 READY`, `2 ASK`, `3 FREEZE`, `64 invalid input/contract`.
