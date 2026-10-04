# Architecture — Meta-Assurance Fabric

**Status: PROPOSAL.** This is a standalone research package, not an installed NEXY subsystem.

## System map

```text
Authority-approved contracts / scenarios / constraints
                     |
                     v
        +---------------------------+
        | Meta-Assurance Fabric     |
        |                           |
 input -> MVS  relation evidence    |
 state -> CLL  conservation proof   |
 proof -> MPWE minimal witness       |
 cases -> BFK  behavior fingerprint |
 spec  -> SMS  mutation survivors   |
        +---------------------------+
                     |
                     v
          structured evidence only
                     |
                     v
       NEXY-style Judge / verifier
       (future integration proposal)
```

## Ownership boundary
The fabric owns computation of its five evidence products. It does **not** own:
- user authority;
- policy/spec promotion;
- final NEXY decision;
- runtime action execution;
- canonical evidence retention;
- production deployment.

## Shared invariants
1. Inputs are explicit and validated.
2. Deterministic ordering is defined before hashing/selection/reporting.
3. Invalid definitions fail closed.
4. No core module reaches external state.
5. No module silently promotes a proposal into authority.
6. A local PASS is scoped to that module's proposition only.

## Composition examples

### Compatibility release check
BFK detects behavior drift -> changed scenarios become claims -> MPWE selects the minimum evidence witness supporting approval/rejection.

### Policy gate hardening
SMS finds a surviving illegal mutation -> NEXY-style release process freezes -> fix validator -> rerun SMS -> BFK can fingerprint resulting gate behavior if scenarioized.

### Stateful action assurance
CLL validates state conservation around action candidates -> MVS validates additional relation-based behavior -> evidence proceeds to an external judge.

## Non-goals
- replacing integration/E2E/runtime evidence;
- deciding authority;
- hiding uncertainty behind a score;
- probabilistic confidence as proof;
- writing into NEXY.AI automatically.

## Versioning law
Any future incompatible change to serialized evidence structures should version the interface explicitly. Behavioral compatibility should be tested with BFK rather than inferred from package version strings.
