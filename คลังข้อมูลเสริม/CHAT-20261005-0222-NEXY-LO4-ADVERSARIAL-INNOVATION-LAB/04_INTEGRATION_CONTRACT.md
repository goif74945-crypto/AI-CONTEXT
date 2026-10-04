# Future NEXY Integration Contract

Status: `PROPOSAL_ONLY / NOT_INTEGRATED`

## Preferred path

Because current NEXY build direction is Next.js + TypeScript, the TypeScript implementation is the preferred future integration surface. The Python implementation is a reference oracle and testable independent implementation.

## Placement proposal

A future NEXY integration could place these gates between candidate synthesis and final adjudication:

```text
NEXY::SWARM / generators
        |
        v
candidate package + provenance + Task Contract
        |
        v
Lo4 assurance adapters
        |
        +-- AURORA report
        +-- MARGIN report
        +-- UPA evidence-state report
        +-- TRACEWEIGHT report
        +-- CONTRACT-DRIFT report
        |
        v
NEXY::JUDGE / authorized release logic
```

## Stable conceptual report shape

Each report exposes:
- `status` or release status;
- deterministic reason codes;
- numeric diagnostics where applicable;
- no hidden auto-fix;
- enough provenance/identity to bind the report to its input package.

## Required integration work before promotion

1. Map NEXY canonical Task Contract and evidence types to these adapter inputs.
2. Decide authoritative threshold ownership under User Law / system law.
3. Add exact-version input digests to reports.
4. Add schema validation in the NEXY runtime language/environment.
5. Execute integration tests against the exact NEXY commit.
6. Execute regression and abuse cases.
7. Evaluate latency/cost under realistic payload sizes.
8. Obtain explicit promotion authority.

Until those steps occur, this folder proves only the isolated prototypes and local parity checks.
