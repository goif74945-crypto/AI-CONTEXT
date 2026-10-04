# Architecture

Classification: `AI-PROPOSED / EXPERIMENTAL / NOT CANON`

## System boundary

```text
User-authorized objective / acceptance policy
                |
                v
        [ OCC compiler ]
                |
      canonical contract + hash
                |
      +---------+----------+
      |                    |
      v                    v
[ ODV verifier ]      [ OSF frontier ]
      |                    |
      +---------+----------+
                |
                v
      [ BRG regression guard ]
                |
       PASS / PARTIAL / FAIL / FREEZE
                |
          if not PASS
                v
       [ ORP recovery planner ]
                |
     proposed repair plan only
                |
                v
      future NEXY authority/JUDGE
```

## Ownership

- **OCC owns contract normalization**, not user authority.
- **ODV owns deterministic comparison**, not observation collection.
- **OSF owns nondominated-option computation**, not final choice authority.
- **BRG owns protected-benefit regression detection**, not metric definition.
- **ORP owns bounded repair-set search**, not repair execution.
- Any future NEXY adapter remains responsible for authorization, provenance, observation trust, execution, evidence class, and release decisions.

## Shared data contracts

### Outcome contract
- stable `objective_id` and human-readable objective;
- criteria with operator `min | max | eq | range | in`;
- hard vs soft status;
- soft weight for reporting only;
- per-criterion `regression_guard` and `max_regression`;
- forbidden effects;
- deterministic `contract_version` and SHA-256 identity.

### Observation
OAF accepts an already-collected JSON object. OAF intentionally does not access the network/runtime/filesystem to collect the state itself. Observation provenance must be attached/validated by a future integration layer.

### Recovery action
A candidate action contains stable ID, cost, risk, reversibility, and a deterministic map of proposed end-state effects. The reference engine simulates only `set value at path`; it does not invoke the action.

## Invariants

1. Unknown contract fields are rejected, not ignored.
2. Hard criterion violation or forbidden observed effect cannot be hidden by soft score.
3. Missing or invalid material observations produce `FREEZE`, not optimistic failure/pass.
4. Pareto frontier excludes `FAIL` and `FREEZE` candidates.
5. BRG can fail even when the candidate's weighted score improves.
6. ORP returns only plans whose simulated outcome reaches `PASS`.
7. ORP rejects conflicting action effects and can require every action to be reversible.
8. Equal normalized input yields equal contract/report structure and hashes.
9. The core performs no external I/O or hidden state access.
10. No OAF output is itself execution authorization.

## Complexity

- OCC: `O(C + F)` criteria + forbidden effects.
- ODV: `O(C + F)`.
- BRG: `O(C + F)` through verification plus `O(C)` guards.
- OSF: `O(N^2 * S)` dominance checks for `N` admissible candidates and `S` soft criteria.
- ORP: exact bounded search `O(2^A * (C + F))`; reference v1 rejects `A > 16` rather than pretending an unbounded exact search is cheap.

The exponential recovery cap is deliberate evidence honesty. A future implementation may use SAT/SMT/ILP/search heuristics, but only with separately verified equivalence/optimality claims.
