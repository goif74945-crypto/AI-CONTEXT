# Contract Semantics — AI-Proposed NPRG

Machine-readable shape: `contracts/resource-governor.schema.json`.

## Task contract fields

- `task_id`: stable identity for one task revision, not a user-facing title.
- `required_capabilities`: hard worker capability set.
- `data_class`: `public | internal | confidential | restricted`.
- `risk_tier`: `low | medium | high | critical`.
- `required_evidence_class`: E0-E7 encoded as integer 0-7. This is a downstream proof requirement, not model confidence.
- `worker_*_tokens`, `verifier_*_tokens`: deterministic planning estimates supplied by an upstream estimator/policy.
- `require_independent_verifier`: explicit hard request. High/critical risk also forces independence under the reference policy.
- `min_quality_bps`: optimization-admission floor from 0-10000. It is not evidence and must not be presented as probability of correctness.
- `max_total_tokens`, `max_cost_microunits`, `max_latency_ms`: nullable hard ceilings.

## Agent contract fields

- `agent_id`: unique stable identity inside the inventory revision.
- `provider_domain`: coarse independence/failure domain used by the reference policy.
- `roles`: `worker` and/or `verifier`.
- `capabilities`: declared worker capabilities.
- `clearance`: maximum data classification the agent is allowed to receive.
- `max_context_tokens`: context capacity used as an admission gate.
- cost fields: integer microunits per 1000 tokens.
- `estimated_latency_ms`: deterministic input estimate, not measured truth unless provenance says so.
- `quality_bps`: policy-controlled optimization signal only.
- `max_evidence_class`: maximum evidence class the verifier executor is permitted/capable to service. Selection still does not constitute evidence.
- `active`: inventory availability gate.
- `quarantined`: explicit deny gate with priority over attractive optimization metrics.

## Decision contract

### `PLAN_READY`
Means only that at least one legal allocation exists under the supplied snapshot and one deterministic best plan was selected.

It does **not** mean:
- execution succeeded;
- a model produced a correct answer;
- required tests ran;
- evidence passed;
- NEXY may release a final output.

Every plan therefore carries `verification_status = NOT_VERIFIED`.

### `FREEZE`
No legal plan exists under the supplied contract/policy/inventory snapshot. The caller must change an authorized input or wait for state to change. The governor does not auto-relax constraints.

## Versioning requirement before production
A production contract should bind task revision, policy revision, inventory revision, metadata provenance revision and cost snapshot into the plan identity. This reference lab deliberately does not invent canonical NEXY versioning fields.
