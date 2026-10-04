# 03 — Architecture

## Components

### 1. Directive Authority Adapter
Outside this reference core. Converts already-authorized structured operator decisions into `DirectiveEvent` objects. It owns identity/authentication and must not ask this core to infer intent.

### 2. Directive Epoch Firewall Core
Deterministic pure protocol logic. Owns:
- current directive epoch;
- current directive identity/hash;
- authority lineage hash;
- allowed action-kind set;
- freeze/revocation state;
- commit-time authority checks.

### 3. Prepared Action Envelope
Carries the exact action digest and the authority snapshot under which it was created.

### 4. Commit Gate
The final guard immediately before an external side effect. It recomputes payload identity and compares all authority bindings against current state.

### 5. Protocol Journal
Hash-chained record of accepted/failed directive attempts, commit attempts and recovery attempts. The journal is sufficient for deterministic replay of this reference state machine.

### 6. Side-Effect Executor
Out of scope. It may execute only after `ALLOW`. A real integration must make gate decision + durable execution boundary transactional enough to avoid a second race after the check.

## Data flow

```text
Authenticated Operator / NEXY authority
        |
        v
structured DirectiveEvent
        |
        v
+-------------------------+
| Directive Epoch Firewall|
| current epoch + lineage |
+------------+------------+
             |
             +--> prepare_action --> PreparedAction
             |                         |
new directive|                         | later
may arrive   v                         v
        update epoch              commit_gate
                                     |
                      +--------------+--------------+
                      |                             |
                    ALLOW                       REJECT/FREEZE
                      |                             |
              Side-effect executor             no mutation
```

## Key hashes

### Directive hash
Digest of the normalized directive event. It identifies the exact accepted structured directive.

### Authority lineage hash
Chained digest derived from previous lineage + directive event digest + resulting epoch. It detects substitution of the authority history even if an epoch number is reused elsewhere.

### Action digest
Domain-separated digest over action ID, action kind and exact payload.

### Journal record hash
Digest over record index, kind, payload, outcome, resulting state hash and previous record hash.

## Complexity
- Commit-gate check: O(1) over protocol metadata plus O(payload size) hashing.
- Directive apply: O(1) over state metadata plus O(event payload size) hashing.
- Full replay: O(number of journal records + total serialized payload size).
- Memory in the reference implementation: O(journal size + event-id registry).

## Concurrency law for a production integration
The reference class is intentionally single-process/single-authority. A distributed implementation must enforce atomic compare-and-set semantics around current epoch and commit authorization. Reading epoch N and writing after epoch N+1 without an atomic guard would recreate the exact bug DEF exists to stop.
