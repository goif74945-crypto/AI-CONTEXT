# Concept, Distinctness, and Non-Goals

## Observed source context
The AI-CONTEXT inventory inspected before design already contains workstreams for delegation leases, resource governance, verified reuse, evidence capsules, human authority, privacy, localization, counterfactual assurance, formal methods, and other reliability topics.

Three nearby concepts were explicitly inspected:

- `CHAT-20261005-0122-NEXY-DELEGATION-LEASE-LAB`: authority lease + intent drift; it answers **what delegated authority exists and whether a plan still fits it**.
- `CHAT-20261005-0122-NEXY-RESOURCE-GOVERNOR`: resource allocation under cost/latency/proof constraints; it answers **which workers/resources are feasible**.
- `CHAT-20261005-0120-NEXY-OXC-LAB`: deterministic authoritative-state-to-UI compilation; it answers **how trusted state is rendered without inventing authority**.

WOCF answers a different pre-execution question:

**Does a newly proposed workstream collide with or substantially duplicate another workstream before either writes shared state?**

## Proposed mechanism
A workstream submits a manifest containing repository, namespace, objective, concept tags, write paths, read paths, and exclusive resources. WOCF validates the manifest and compares it against a catalog.

Hard blockers:
- protected repository target;
- duplicate workstream identifier;
- overlapping namespace;
- overlapping write-set;
- exclusive resource conflict;
- identical concept fingerprint;
- lexical-concept score above configured freeze threshold;
- malformed/unsafe path or catalog entry.

Warnings:
- lexical-concept score above warning threshold but below freeze threshold.

## Why deterministic lexical overlap instead of embeddings
Embeddings would introduce provider/model/version dependency and can silently change. This lab deliberately uses a weaker but reproducible signal. The output is a guardrail, not a semantic oracle.

## Non-goals
WOCF does not:
- decide user authority;
- grant or revoke permissions;
- allocate agents or token budgets;
- verify whether code is correct;
- merge branches;
- serialize all work globally;
- infer hidden intent;
- claim that low lexical overlap proves conceptual novelty;
- become part of NEXY merely because this proposal exists.
