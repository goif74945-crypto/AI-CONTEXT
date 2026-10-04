# Future Ideas

All items are AI proposals, not current NEXY requirements.

1. Authenticated lineage attestations: sign producer/oracle/source roots so evidence cannot merely claim independence.
2. Prompt-family fingerprints: detect different agents produced through effectively identical prompting/compiler paths.
3. Retrieval-set MinHash: estimate shared source-corpus overlap without storing raw private context.
4. Common-cause discovery: infer hidden shared roots from build graphs, artifact SBOMs and model-routing traces.
5. Risk-tiered deterministic quorum: higher independence requirements for irreversible or high-impact operations.
6. Counterfactual independence mutation testing: collapse one root deliberately and require PASS to downgrade.
7. Evidence diversity receipts: explain why N agreeing artifacts count as only M independent confirmations.
8. Cross-model independence law: formalize when different model families are independent enough to count separately.
9. Oracle-monoculture warnings: detect many tests that depend on the same evaluator, parser, golden generator, or checker.
10. Proof-supply-chain SBOM: source -> producer -> tool -> oracle -> evidence -> decision graph with reproducible identities.
11. Signed blind-test envelopes: prove expected outcome was hidden from the producer before execution.
12. Correlation budget visualization: report which roots dominate the evidence surface without collapsing the result into a vague confidence percentage.