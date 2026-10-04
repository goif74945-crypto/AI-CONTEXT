# Knowledge Debt Ledger
> Classification: AI-PROPOSED CONCEPT. Not an authoritative NEXY.AI requirement.

Knowledge debt is future verification/correction burden caused by reusable information lacking provenance, freshness rules, dependency links, uncertainty labels, or ownership.

## Dimensions
P provenance; F freshness; D dependency; C contradiction; S semantic ambiguity; V verification; O orphan debt.

## Prioritization heuristic
KD = impact_weight * (P + F + D + C + S + V + O)
This is a planning heuristic, not a scientific metric.

## Ledger record
item_id; dimensions; affected_consumers; impact; evidence_gap; cheapest_safe_remediation; estimated_cost; trigger_or_deadline; status.

## Rules
- High-impact executable knowledge with UNKNOWN provenance is P0 debt.
- One unsafe executable assumption may outrank thousands of stale low-risk notes.
- Prefer repairing shared upstream nodes when one correction resolves many downstream debts.

## Metrics
Provenance coverage; freshness-policy coverage; stale critical claims; invalidated claims still referenced; revalidation backlog age; stale-node fan-out.
