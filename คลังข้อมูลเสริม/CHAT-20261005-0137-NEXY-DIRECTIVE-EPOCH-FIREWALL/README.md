# NEXY Directive Epoch Firewall (DEF)

**Status:** AI-PROPOSED REFERENCE SYSTEM / NOT NEXY.AI CURRENT IMPLEMENTATION

DEF is a deterministic last-mile execution guard for long-running or concurrent AI work. It prevents an action prepared under an older human directive from committing after that directive has been replaced, narrowed, revoked, or otherwise superseded.

## Why this exists

A worker may prepare a valid action at time T. At T+1 the operator can change the directive. Without a commit-time authority recheck, the old worker can still perform a now-unauthorized side effect. This is an instruction-level time-of-check/time-of-use (TOCTOU) failure.

DEF binds every prepared action to:
- logical directive epoch;
- active directive digest;
- authority-lineage digest;
- exact action digest;
- optional exact irreversible-action approval binding.

Immediately before mutation, the commit gate revalidates those bindings against current state. Any stale/tampered authority binding causes deterministic FREEZE rather than silent rebasing or guessed continuation.

## Scope boundary

This project lives only in `goif74945-crypto/AI-CONTEXT/คลังข้อมูลเสริม/...`.

It does **not** modify, patch, branch, configure, commit to, or otherwise mutate any repository whose name contains `NEXY.AI`.

## Relationship to nearby supplemental systems

- **HICF / intent continuity** asks whether the human objective or constraints drifted during interaction.
- **Intent Integrity Guard** checks whether a proposed plan respects a task contract, scope, evidence and protected repositories.
- **DEF** sits later, immediately before a side effect, and asks whether this exact prepared action still has current authority to commit.

These layers are complementary rather than replacements.

## Reference implementation

Python >=3.11, standard library only.

Key properties:
- monotonic logical directive epochs;
- compare-and-set style `expected_epoch` transition preconditions;
- NEW / REPLACE / NARROW / REVOKE operations;
- narrowing is monotonic in allowed action kinds;
- event ID idempotency with duplicate-content verification;
- stale action rejection/freeze at commit;
- tampered action digest detection;
- exact irreversible-action approval binding;
- hash-chained journal of directive, commit and recovery attempts;
- deterministic journal replay with tamper/outcome/state verification;
- freeze-first recovery through a new replacement epoch.

## Run

```bash
PYTHONPATH=src python scripts/run_validation.py
PYTHONPATH=src python scripts/adversarial_validation.py
PYTHONPATH=src python benchmarks/benchmark.py
```

## Evidence boundary

Current evidence proves this isolated reference implementation only. It does not prove NEXY production integration, distributed consensus, durable database semantics, cryptographic operator authentication, deployment security, or target-environment SLOs.
