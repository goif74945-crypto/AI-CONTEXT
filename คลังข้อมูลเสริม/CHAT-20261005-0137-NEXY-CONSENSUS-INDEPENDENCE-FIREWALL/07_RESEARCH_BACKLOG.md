# NCIF Research Backlog

**Classification:** AI-PROPOSED FUTURE RESEARCH; NOT CURRENT NEXY REQUIREMENTS

Priority is based on integrity impact for a hypothetical adoption, not commitment.

## P0 — required before serious integration

1. Authenticated provenance envelope with signature/hash/revision binding.
2. Source identity canonicalization for repo/blob/commit, document/hash, URL+snapshot, tool-call receipt, runtime trace and dataset revision.
3. Correlation authority model: who can assert, challenge, revoke or supersede correlation edges.
4. Bounded input quotas for nodes/edges/votes/keys/strings and deterministic oversize FREEZE.
5. Policy version identity embedded in result fingerprint.
6. Cross-stance correlation semantics beyond root overlap, including declared common-cause keys.
7. Independent-vs-diverse distinction: provider diversity is not evidence diversity and vice versa.
8. Safe mapping between NPRG allocation receipts and NCIF result receipts without circular proof.
9. Evidence freshness/expiry semantics and stale-lineage invalidation.
10. Adversarial provenance forgery corpus.

## P1 — robustness and epistemic quality

11. Common-mode failure taxonomy: same dataset, same retrieval index, same API, same benchmark, same human label source, same upstream model-generated summary.
12. Weighted independence model that remains explainable and fail-closed; compare against binary connected components.
13. Hyperedge representation for common causes affecting many roots.
14. Negative/dependent evidence semantics instead of simple SUPPORT/OPPOSE grouping.
15. Contradictory interpretations of identical evidence with adjudication trace.
16. Temporal independence: same source at different revisions may or may not count independently.
17. Experiment independence: replicate vs rerun vs reanalysis vs duplicated logs.
18. Root-removal resilience for multiple simultaneous roots (`k`-root cuts).
19. Minimal cut-set analysis identifying smallest provenance set whose loss destroys quorum.
20. Concentration metrics that do not masquerade as truth probabilities.
21. Provenance graph compression with proof-preserving summaries.
22. Incremental evaluation for streaming evidence without changing deterministic final result.
23. Canonical graph digest independent of input ordering.
24. Tamper-evident NCIF receipt chaining.

## P1 — security/privacy

25. Keyed/tokenized diagnostic IDs to mitigate dictionary attacks on low-entropy provenance labels.
26. Tenant-separated correlation namespaces.
27. Correlation-key poisoning detection and dispute workflow.
28. Sybil-resistant actor identity assumptions outside NCIF core.
29. Sensitive-evidence redaction while retaining equality proofs.
30. Access-controlled “why correlated” detail for auditors without exposing secrets to ordinary operators.
31. Memory/CPU complexity limits with worst-case dense graph analysis.
32. Fuzzing malformed Unicode, oversized integers/strings, duplicate normalization and unusual JSON structures.

## P2 — verification and usability

33. Property-based test suite from independent generator/tooling.
34. Differential implementation in another language to detect same-code blind spots.
35. Model-generated adversarial fixture competition, with deterministic validators judging outcomes.
36. Benchmark corpus of known pseudo-consensus patterns.
37. Human explanation contract: “5 agents, 1 independent root” without implying those agents were dishonest.
38. Visualization contract for provenance groups, root concentration and blocking opposition.
39. Accessibility/localization integration with existing supplemental assurance work.
40. Browser/E2E test if a future control surface exposes NCIF receipts.

## P2 — theoretical work

41. Formalize independence assumptions using causal graphs rather than only provenance overlap.
42. Define conditions under which independence grouping is monotonic under new evidence.
43. Prove invariants for transitive collapse and root-removal metrics.
44. Analyze false-positive/false-negative bounds under incomplete correlation metadata.
45. Explore provenance equivalence classes without relying on secret raw identities.
46. Determine when two independently fetched copies of the same source should count as one evidence root vs two execution witnesses.
47. Separate evidence independence from reasoning independence.
48. Separate reasoning independence from provider/vendor independence.
49. Evaluate consensus under adversarial collusion where provenance is authentic but selection is biased.
50. Define a NEXY-compatible evidence-independence contract only after canonical source authority promotes the need.
