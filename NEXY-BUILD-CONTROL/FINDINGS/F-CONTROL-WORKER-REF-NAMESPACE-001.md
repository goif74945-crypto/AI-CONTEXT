# F-CONTROL-WORKER-REF-NAMESPACE-001

STATUS: SUPERSEDED
SEVERITY: P0_SUPPORTING_EVIDENCE
CANONICAL_INCIDENT: INC-BRANCH-NAMESPACE-001
SOURCE_SHA: 608426cb30398b1f3461866f7079d2a435c96b96

SUPPORTING_EVIDENCE:
An independent GitHub create-branch attempt using the mandated prefix `NEXY.AI-Test-AI/work/` returned HTTP 422 while `NEXY.AI-Test-AI` exists. This corroborates the canonical branch-namespace incident.

ACTION:
Use INC-BRANCH-NAMESPACE-001 as the single control-plane blocker. No alternative worker namespace is authorized by this supporting record.

V16_RC1_3_SUPERSESSION:
- PRIOR_STATUS: DUPLICATE_JOINED
- SUPERSEDED_BY: NEXY::EQUAL-PEER-FENCED-ATOMIC-DYNAMIC-SCALE-ENGINEERING-CONSTITUTION-V16-RC1.3
- SUPERSESSION_RECORD: NEXY-BUILD-CONTROL/V16/PREACTIVATION/SUPERSESSIONS/SUPERSESSION-V16RC13-LEGACY-WORKER-NAMESPACE-P0-001.json
- REASON: Legacy V7/V8/V11 required the Git-impossible NEXY.AI-Test-AI/work/<TASK_ID> prefix. V16-RC1.3 preserves isolated worker-branch implementation but removes that literal prefix requirement, so this legacy protocol blocker no longer blocks V16 migration/activation.
- PRESERVED_TECHNICAL_FACT: The literal descendant ref remains impossible while refs/heads/NEXY.AI-Test-AI exists.
- PRODUCT_MUTATION_AUTHORIZED: FALSE
