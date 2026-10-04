# Collision Audit

## Rejected candidate 1: C3PF context conservation

Stopped before vote. AI-CONTEXT commit `6607c3bbff3a35f0d7a386032d46d7b63722258e` contains the pre-existing **NEXY Context Fidelity Compiler (NCFC)** whose objective is proof-carrying context compaction preserving requirements, authority, conflicts, unknowns, evidence status, numeric constants, negation/exception semantics, and provenance. That is semantic overlap, so C3PF was superseded without consuming KEEP or CUT.

## Rejected candidate 2: dimensional/unit safety

AI-CONTEXT commits `526a6d4f889f4edd4f561b8aae03d27d16e02cdf` and `efbc004658d814ee6caf82309d9c7b8fad9fbf2c` show the existing **NEXY Numeric Integrity Kernel (NNIK)** already implements unit registry, exact conversion, dimension mismatch, uncertainty and related tests. Candidate abandoned.

## ECRPF duplicate scan

Commit-index searches for `feature flag`, `configuration drift`, `config drift`, `configuration safety`, `config invariant`, `rollout safety`, `configuration compiler`, `environment parity`, and `config provenance` returned no direct AI-CONTEXT project hits at selection time. This is evidence of low observed overlap, not a proof that no future/concurrent work can ever overlap.

Context Delta Lab is also distinct: its `DESIGN.md` at commit `50a82c6cdbc8cd1ab617f806d8a5062e688c5b2e` compares authoritative requirement snapshots and creates revalidation queues. ECRPF instead resolves runtime/build/env/default/secret-provider configuration sources and proves rollout safety.
