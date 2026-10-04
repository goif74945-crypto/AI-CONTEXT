# Architecture

## System position

These mechanisms are designed as **pre-release assurance gates** around candidate work produced by generators/agents. They do not replace NEXY::LAW, NEXY::CORE or NEXY::JUDGE. A future integration would treat their outputs as typed evidence or blockers consumed by an authorized adjudication layer.

```text
User Law / Canon / Task Contract
              |
              v
       Candidate execution
              |
      +-------+-------+----------------+------------------+
      |               |                |                  |
   AURORA          MARGIN             UPA            TRACEWEIGHT
      |               |                |                  |
      +---------------+-------+--------+------------------+
                              |
                       CONTRACT-DRIFT
                              |
                              v
                 Lo4 release-candidate gate
                              |
                   RELEASE_CANDIDATE / FREEZE
```

`RELEASE_CANDIDATE` is deliberately weaker than Canon approval or production release.

## Shared invariants

1. Deterministic given equal normalized input and policy.
2. No external model call is required to adjudicate a result.
3. Invalid structural input fails explicitly rather than receiving a guessed default.
4. Each mechanism exposes a small report with machine-readable status and reasons.
5. A freeze reason is preserved rather than silently repaired.
6. No mechanism can promote itself to Canon.

## Module ownership

- `lo4lab/aurora.py` / `typescript/src/aurora.ts`: abstention reliability.
- `lo4lab/margin.py` / `typescript/src/margin.ts`: constraint slack and legality margin.
- `lo4lab/upa.py` / `typescript/src/upa.ts`: four-valued evidence logic.
- `lo4lab/traceweight.py` / `typescript/src/traceweight.ts`: causal source influence propagation.
- `lo4lab/contract_drift.py` / `typescript/src/contractDrift.ts`: structured Task Contract mutation audit.
- `lo4lab/integration.py`: reference five-gate composition.
- `interop/`: representative cross-runtime parity proof.

## Security and trust boundary

Inputs are untrusted structured data. Validation rejects malformed weights, duplicate identifiers, missing parents, invalid numeric values, cycles and structurally invalid cases. This is not a complete security sandbox and does not prove resistance to arbitrary hostile runtime code.

## Evolution law

Version changes that alter report status semantics, threshold interpretation, truth tables, influence normalization or drift-event cost must be treated as semantic changes and require parity/regression revalidation. Backward-compatible new report metadata may be added only if existing decisions remain unchanged for existing inputs.
