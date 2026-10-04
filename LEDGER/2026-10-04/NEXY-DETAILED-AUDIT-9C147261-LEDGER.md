LEDGER_ID: NEXY-DETAILED-AUDIT-9C147261
head: 9c1472615d08af96188953fa17b855d8ac45ba31
tree: 4488d57ebca2a50ad338166aa6429c8c4fce3ba3
spec_sha256: b35ee1bf8212579251f24914e11aebe103ff697f549f7a5812f07c53361d26b7

entries:
- L001 VERIFIED: current branch HEAD/tree frozen and unchanged through final prewrite recheck.
- L002 VERIFIED: authoritative DOCX local SHA-256 equals canonical hash.
- L003 VERIFIED: current content-read accounting 878/878 via 871 immutable reuse + 7 fresh delta reads.
- L004 VERIFIED_WITH_LIMITS: normalized source inventory remains 837 unique requirements because canonical source bytes are unchanged.
- L005 VERIFIED: old Core process.hrtime clock finding is stale/resolved at current head.
- L006 CONFLICT: L9 TSA-only/no-monotonic Core clock law vs G19 invariant-TSC/integer-tick clock law has unresolved scope.
- L007 CONTRADICTED_SEMANTICS: LO2/I/O consume currentTick as ms while fallback currentTick advances by call sequence and production TSA injector not found.
- L008 PARTIAL: static determinism checker substantially improved but lacks scanRepository integration regression and does not cover authoritative Phase-F roots.
- L009 VERIFIED: exact-head workflow result is 0/4 success; release/deploy proof absent.
- L010 CORRECTION: WebGPU stub maps to G1-G10 Game Runtime, not G14.
- L011 PARTIAL: G14 static contracts/proof validation exist; real execution evidence remains NOT_VERIFIED.
- L012 NOT_VERIFIED_RISK: localeCompare deterministic-ordering equivalence unresolved in L1o/Lo2/Lo3/Canon Seal/Global Anchor.
- L013 VERIFIED: only NEXY.ai current branch exists; workflow branch patterns and disabled branch protection leave governance enforcement gap.
- L014 AUDIT_INTEGRITY: previous 72/301 control count is not reproducible; conservative reproducible count is 66/301 with PASS=60 PARTIAL=6.
- L015 VERIFIED: 74/74 system rows are represented in generated detailed audit table.
- L016 VERIFIED: whole-project completion remains NOT_PROVEN; NOT_VERIFIED excluded from completion percentage.

final_verdict: PARTIAL / RELEASE_BLOCKED / CLOCK-SCOPE-FROZEN
