# Change Impact Radius Protocol

## Purpose
Prevent local edits from causing remote regressions.

## Radius
L0 edited artifact.
L1 direct callers/importers/consumers.
L2 transitive service/domain dependencies.
L3 persistence, events, cache, auth and external contracts.
L4 deploy, monitoring, rollback and support surfaces.
L5 user/business invariants.

## Inventory
For meaningful changes record changed contract, affected producers/consumers, state compatibility, temporal compatibility, failure-mode changes, observability changes and test evidence by layer.

## Temporal coupling
Check old producer -> new consumer; new producer -> old consumer; rolling-deployment overlap; delayed queue messages; stale caches; pre-deployment retries; long-running jobs spanning versions.

## Radius stopping rule
Stop expanding only when every frontier node is either proven unaffected by contract analysis or covered by relevant verification evidence. “Probably unrelated” is not a stopping rule.

## Practical result
This protocol converts blast-radius reasoning from intuition into a bounded graph traversal with an explicit evidence-based stopping condition.
