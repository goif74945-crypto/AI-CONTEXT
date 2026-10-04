# Uncertainty Debt Ledger
Status: **AI-PROPOSED CONCEPT — NOT IMPLEMENTED / NOT APPROVED**

Uncertainty debt is a decision-relevant assumption temporarily tolerated because immediate verification is unavailable or disproportionate.

Record: id, assumption, classification, affected requirements/actions, risk, verification plan, expiry, recheck trigger, owner, status.

Rules:
- never disguise debt as fact;
- irreversible high-impact action cannot depend on expired critical debt;
- invalidation triggers downstream impact analysis;
- verified debt becomes a provenance-backed claim;
- irrelevant debt is retired to reduce context pollution.

Integrations: Context Compiler retrieves relevant debt; Proof-Carrying Execution lists completion-relevant debt; evaluations inject invalidated assumptions to test recovery.
