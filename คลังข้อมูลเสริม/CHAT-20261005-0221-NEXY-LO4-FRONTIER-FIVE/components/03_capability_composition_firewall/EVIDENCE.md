# CCF Evidence

- E1: AST/compileall PASS.
- E2: secret-read + network-egress composition freezes; scope lock prevents unapproved composition; initial forbidden state freezes; witness/fingerprint stable under input order.
- Stress: CCF fingerprint stable across seeded capability permutations in combined 40,000-check stress run.
- E3: integrated promotion gate freezes when composition risk exists.

Limits: a production policy must define privilege tokens and forbidden conjunctions correctly. This prototype cannot infer all real-world side effects of arbitrary tools.
