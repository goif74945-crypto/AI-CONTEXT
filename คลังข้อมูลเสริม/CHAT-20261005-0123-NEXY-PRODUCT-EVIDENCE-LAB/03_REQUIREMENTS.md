# 03 — Reference Requirements

All requirements below govern this supplemental prototype only.

| ID | Requirement | Verification |
|---|---|---|
| NPEL-R001 | A proposal MUST include stable ID, title, hypothesis, population, primary metric, at least one guardrail, allocation fraction, and duration. | unit |
| NPEL-R002 | Material missing/invalid fields MUST fail compilation; the engine MUST NOT invent defaults for baseline, MDE, standard deviation, population, guardrails, or risk flags. | unit |
| NPEL-R003 | Prohibited risk flags MUST block compilation. | unit |
| NPEL-R004 | Planning sample size MUST be deterministic for identical metric inputs; reference v1 MUST reject non-50/50 allocation because its planning equations assume equal arms. | unit |
| NPEL-R005 | Compiled contracts MUST serialize canonically and expose SHA-256 identity. | unit |
| NPEL-R006 | Evidence MUST bind to the exact contract hash or evaluation MUST FREEZE. | unit |
| NPEL-R007 | Critical data-quality violations MUST FREEZE evaluation. | unit |
| NPEL-R008 | A hard guardrail threshold breach MUST FREEZE before primary success can be released. | unit |
| NPEL-R009 | Underpowered evidence MUST be INCONCLUSIVE, not promoted to support/reject. | unit |
| NPEL-R010 | Supported evidence MUST clear the configured MDE confidence threshold in the desired direction. | unit |
| NPEL-R011 | Rejected evidence MUST have a confidence interval wholly failing the configured MDE threshold. | unit |
| NPEL-R012 | Ambiguous threshold overlap MUST be INCONCLUSIVE. | unit |
| NPEL-R013 | Evaluation output MUST always require a human product decision. | unit |
| NPEL-R014 | Analytics event payloads MUST reject missing required properties and common secret-bearing properties. | unit |
| NPEL-R015 | Core evaluation MUST not use network, current time, or randomness. | static inspection + tests |
| NPEL-R016 | The prototype MUST support both proportion and mean metrics. | unit |
| NPEL-R017 | Contract/evaluation serialization MUST be JSON-safe and deterministic. | unit |
