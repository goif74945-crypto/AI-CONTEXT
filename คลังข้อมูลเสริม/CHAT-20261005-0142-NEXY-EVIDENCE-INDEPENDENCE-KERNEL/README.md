# NEXY Evidence Independence Kernel (NEIK)

Status: AI-PROPOSED / STANDALONE / NOT INTEGRATED INTO NEXY.AI
Chat reference: CHAT-20261005-0142-NEXY-EVIDENCE-INDEPENDENCE-KERNEL
Canonical ChatGPT conversation ID: UNKNOWN. It is not exposed to this runtime, so none is invented.
Storage: AI-CONTEXT supplemental knowledge only.
Protected scope: every repository whose name contains NEXY.AI is read-only for this task.

NEIK answers a narrow but dangerous verification question: when several pieces of evidence agree, how many are actually independent?

It prevents correlated-consensus laundering caused by shared source roots, shared producer roots, shared oracle roots, copied proof artifacts, derived evidence counted twice, circular dependency, stale-revision evidence, evidence-class substitution, non-blind verification when blindness is required, and self-verification without a provenance-bearing external oracle.

Core decision states:
- PASS: exact independent quorum exists and no blocking contradiction exists.
- NOT_VERIFIED: evidence exists but configured independence/proof obligations are not met.
- FREEZE: evidence integrity is blocking, for example dependency cycle, sufficient-class PASS/FAIL contradiction, admissible FAIL, or deterministic search-budget exhaustion.

The core uses Python standard library only and emits canonical deterministic JSON plus SHA-256 decision sealing.

Run:
python src/neik.py input.json
PYTHONPATH=src python -m unittest discover -s tests -v

This artifact does not prove the underlying real-world claim. It proves only the configured independence/admissibility property of the supplied evidence graph.