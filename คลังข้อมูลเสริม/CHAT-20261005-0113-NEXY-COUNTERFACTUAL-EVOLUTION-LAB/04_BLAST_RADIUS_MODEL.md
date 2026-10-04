# Change Blast-Radius Model
> AI-PROPOSED CONCEPT.
Nodes: requirement, law, module, API, event, schema, durable state, job, provider, trust boundary, UI contract, evidence, deployment unit, physical boundary.
Edges: CALLS, READS, WRITES, AUTHORIZES, VALIDATES, EMITS, CONSUMES, DERIVES_FROM, DEPLOYS_WITH, ROLLS_BACK_WITH, INVALIDATES_EVIDENCE_OF.
R0 pure local; R1 one component; R2 cross-contract; R3 durable state/schema/async; R4 authority/security/evidence; R5 deployment/physical safety.
UNKNOWN dependency prevents radius reduction. Schema with old readers >=R3. Possible authority bypass=R4. Physical actuation=R5.
Return affected, uncertain, irreversible nodes, owners, evidence, rollback frontier.