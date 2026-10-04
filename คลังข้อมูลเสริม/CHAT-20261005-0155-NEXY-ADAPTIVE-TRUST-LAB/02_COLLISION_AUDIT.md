# Collision Audit

Status: AI_PROPOSAL / NON_GOVERNING

The current `คลังข้อมูลเสริม` tree was inspected before selecting these concepts. Existing work already includes, among other things:
- model conformance/substitution harnesses;
- delegation leases and authority controls;
- privacy/context egress firewalls;
- evidence invalidation/proof sensitivity;
- side-effect transactions and shadow execution;
- capability negotiation;
- generic agent handoff protocols;
- interaction-friction and clarification optimization.

## Selected separation boundaries

### MCAE
Not a model-conformance harness. It arbitrates conflicting *claims from multiple modalities/sources at runtime* and explicitly returns CONFLICT/FREEZE when authority-equivalent evidence disagrees.

### CPAC
Not a delegation lease. It compiles *explicit user consent + declared purpose* into a narrow action decision/receipt. It does not grant agent authority, renew privileges, or replace RBAC/LAW.

### EMCR
Not static model conformance. It performs *empirical, capability-specific calibration from observed outcomes* and routes only within explicit quality/latency/cost constraints.

### IVS
Not an invalidation calculus. Existing work determines when evidence becomes stale. IVS consumes an impact/dependency relation and produces a deterministic, cost-aware *rerun schedule* for the affected verification surface.

### CDHC
Not the generic handoff protocol. It packages a minimal approved handoff state into an authenticated, expiring, target-bound capsule with secret-field minimization. Key distribution/device attestation remain out of scope.

## Remaining collision risk
Semantic overlap is possible because all five operate inside the same NEXY reliability/control ecosystem. Their ownership boundaries are therefore intentionally narrow and should be rechecked before any future promotion.
