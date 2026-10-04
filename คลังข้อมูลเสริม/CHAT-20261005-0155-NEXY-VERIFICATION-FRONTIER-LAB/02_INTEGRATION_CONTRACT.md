# Proposed NEXY Integration Contract

**Status:** PROPOSAL / ADVISORY ONLY  
**Authority:** none over NEXY.AI unless explicitly promoted by project authority.

## Integration law

All five engines are designed as pure or near-pure verification helpers. They should sit outside the authority-bearing core and exchange structured inputs/outputs through adapters.

They MUST NOT:

- grant authorization;
- silently downgrade evidence class;
- mutate NEXY project state by themselves;
- turn model confidence into proof;
- treat advisory output as canonical law;
- bypass a FREEZE decision;
- use hidden network/filesystem/model I/O in the deterministic decision path.

## Proposed placement

```text
Untrusted / external payload
        |
        v
[BPPL strict boundary validation]
        |
        v
NEXY request / policy / verification layers
        |
        +--> [NSCA] audit negative-space evidence coverage (offline/CI)
        |
        +--> [VPO] compute minimum legal verification portfolio (planner)
        |
        +--> [CMAE] challenge verifier adequacy (CI/eval)
        |
        +--> [FWD] minimize observed failure witness (debug/evidence)
```

## Data contracts

### FWD adapter
Input:
- immutable JSON-like request/context snapshot;
- deterministic failure oracle returning an exact signature or `None`.

Output:
- reduced witness;
- preserved signature;
- reduction trace and size delta.

Failure behavior:
- source does not fail → reject;
- unstable oracle → reject;
- convergence bound exceeded → reject.

### VPO adapter
Input:
- claims;
- allowed evidence classes per claim;
- candidate checks with integer cost units and emitted claim/evidence mappings.

Output:
- exact minimum-cost legal check set within configured state-space bound.

Failure behavior:
- no legal portfolio → explicit error;
- excessive claim state space → explicit error;
- duplicate IDs/negative costs → explicit error.

### BPPL adapter
Input:
- raw JSON string or validated JSON object for canonicalization;
- explicit resource limits.

Output:
- parsed value or deterministic canonical JSON.

Failure behavior:
- duplicate keys, Unicode-normalized key collision, non-finite number, depth/node/magnitude limit, malformed JSON → reject before core handling.

### CMAE adapter
Input:
- structured contract;
- deterministic validator/oracle.

Output:
- generated mutants;
- killed/survived sets;
- mutation score.

Failure behavior:
- baseline itself is invalid → reject report rather than invent adequacy.

### NSCA adapter
Input:
- structured requirements with obligation kind;
- structured evidence links with polarity/status/evidence class.

Output:
- negative requirement count;
- covered/missing count;
- exact misleading-positive and failed-negative evidence IDs.

Failure behavior:
- duplicate IDs, invalid polarity, empty evidence-class policy → reject.

## Compatibility strategy

The prototypes intentionally use generic records rather than importing current NEXY implementation types. A future adapter can map NEXY requirement/evidence schemas into these records. This avoids coupling an advisory prototype to a specific branch or transient implementation.

## Promotion gate

Before any production integration:

1. bind interfaces to current NEXY authoritative schemas;
2. add exact-head repository tests;
3. add NEXY-specific integration evidence;
4. run regression and negative-path suites;
5. review performance limits;
6. obtain explicit authority to mutate NEXY.AI.

Until then, status remains `AI-PROPOSED / NOT_INTEGRATED`.
