# Future Research Backlog
> Every item here is an AI-PROPOSED IDEA, not an approved NEXY.AI requirement.

## R1 Temporal type system
Explore types such as Fact<AsOf=T>, Policy<Version=V>, Capability<Environment=E>, and Decision<DependsOn={...}> so freshness becomes machine-checkable.

## R2 Semantic diff for evidence
Detect whether a source changed meaningfully rather than treating every byte change as invalidation.

## R3 Counterfactual stale-use simulator
Replay decisions under old versus refreshed evidence and measure consequence delta.

## R4 Verification economics
Optimize which claims to refresh under finite compute, latency, API quotas, and human-review capacity.

## R5 Provenance-preserving summarization
Require summaries to retain claim-to-source mappings instead of flattening provenance.

## R6 Knowledge garbage collection
Archive unreachable low-value knowledge without deleting audit history.

## R7 Trust-domain transitions
Model when evidence crosses from external web, user input, model inference, tool output, or project authority and require explicit promotion rules.

## R8 Freshness-aware retrieval
Rank not merely by semantic similarity but by authority, validity window, contradiction state, and consumer context.

## R9 Invalidation chaos testing
Randomly expire or contradict upstream nodes and verify the system never silently reuses invalid critical descendants.

## R10 Knowledge SLOs
Define measurable objectives such as maximum age of critical claims, maximum unresolved contradiction duration, and provenance coverage.
