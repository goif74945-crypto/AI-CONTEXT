# Non-Duplication / Adjacent Work Note

> **AI-PROPOSED / EXPERIMENTAL / NOT CANON**

This note was added after refreshing `AI-CONTEXT/main` and observing concurrently-created supplemental workstreams.

## Adjacent artifacts observed

- `NEXY-META-VERIFICATION-LAB-20261005.md` — broad epistemic-integrity research: truth lattice, evidence decay, uncertainty, adversarial verification, coverage-graph theory.
- `formal-assurance-lab/` — formalizable authority/proof semantics and counterexample-driven assurance research.
- `CHAT-20261005-0121-NEXY-EVIDENCE-CAPSULE-LAB/` — privacy-preserving/selective-disclosure evidence capsules and tamper-evident commitments.
- `CHAT-20261005-0122-NEXY-VERIFIED-REUSE-KERNEL/` — safe reuse/caching decisions for previously verified outputs.

## ProofGraph Lab's distinct boundary

ProofGraph Lab is a **concrete, dependency-free executable linter/graph/hash tool for the AI-CONTEXT filesystem itself**. Its implemented scope is deliberately narrower and operational:

1. local Markdown reference validation;
2. reverse-reference impact closure;
3. SHA-256 truth-lock generation and stale-lock verification;
4. deterministic checks for NEXY denominator semantics: historical/deprecated `215`, current normalized `837`, and current-build `773`;
5. explicit experimental-proposal labeling checks;
6. conservative credential-signature detection with redacted fingerprints;
7. stable CLI + machine-readable JSON schemas + executed tests.

It does not attempt to replace the sibling labs' theory, evidence privacy, formal proof calculus, or reuse policy. Their future concepts could consume ProofGraph output, but no integration is claimed or required here.

## Dedup conclusion

**REPO_FACT:** adjacent assurance/evidence projects exist.  
**INFERENCE:** scope adjacency exists around evidence freshness and graphs.  
**DISTINCTION:** no observed sibling artifact implements this exact filesystem lint + local-link impact + truth-lock CLI contract.  
**STATUS:** distinct enough to proceed as an isolated additive tool, while avoiding claims that the broader research concepts are unique.
