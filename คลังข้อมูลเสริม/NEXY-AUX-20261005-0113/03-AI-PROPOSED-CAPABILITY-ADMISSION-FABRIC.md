# AI-PROPOSED CONCEPT — Capability Admission, Quarantine & Revocation Fabric
Status: PROPOSAL / FUTURE ARCHITECTURE

## Problem
Capability availability is not capability trust. Models, tools, plugins and runtimes can change behavior, permissions or supply-chain identity.

## CapabilityManifest
capability_id; provider; version; immutable digest where possible; declared actions; permissions; data-egress behavior; network/filesystem/process access; deterministic classification; side-effect class; reversibility; secret requirements; I/O schemas; limits; known failures; provenance; verification profile.

## Trust states
UNSEEN→DISCOVERED→QUARANTINED→EVALUATING→ADMITTED_LIMITED→ADMITTED→SUSPENDED→REVOKED.
No direct UNSEEN→ADMITTED.

## Admission gates
identity/provenance; schema; least privilege; I/O validation; side-effect classification; failure semantics; security abuse tests; explicit determinism expectations; matching evidence; LAW/JUDGE authorization.

## Permission axes proposed
READ_PUBLIC, READ_PROJECT, READ_SENSITIVE, WRITE_EPHEMERAL, WRITE_PROJECT, EXECUTE_SANDBOX, EXECUTE_NETWORK, EXECUTE_HOST, DEPLOY, SECRET_USE, HUMAN_COMMUNICATION, FINANCIAL_OR_IRREVERSIBLE_ACTION.

Permissions should be scoped, bounded and independently revocable.

## Quarantine
isolated filesystem; no ambient credentials; deny-by-default network; synthetic fixtures; bounded CPU/memory/time; output capture; no durable project mutation; deterministic replay where possible.

## Re-admission triggers
artifact/version change; permission expansion; provider ownership change; material schema change; dependency change; security-policy change; behavioral drift; critical incident.

## Behavioral fingerprint
HYPOTHESIS, non-authoritative:
schema conformance; replay consistency; timeout/error distributions; unexpected egress; policy denials; hallucinated-success rate.
Never substitute this fingerprint for explicit proof of critical actions.

## Revocation
block new invocations; classify in-flight work; freeze affected protected mutations; invalidate disallowed evidence when policy requires; preserve forensics; enumerate dependent workflows; require re-admission.

## Adversarial scenarios
read-only tool performs write; model fabricates evidence refs; update expands permissions; compromised provider reuses version string; success returned before commit; duplicate callback duplicates mutation; output carries prompt injection; tool leaks secrets; agent asks for privilege escalation in natural language.

Expected: quarantine/freeze/deny, not trust by optimism.

## Integration sketch
LAW=admission policy; JUDGE=admission/revocation decision; VAULT=manifest/evidence/history; RUN=enforcement; SWARM=constrained workers; VIEW=state/reason; PULSE=drift/revocation health.

## Verification if promoted
schema/property tests; permission-denial tests; sandbox escape tests; replay/idempotency; revocation races; dependency invalidation; malicious output/prompt injection; crash consistency.

## Non-goals
popularity-based trust; permanent trust after one test; brand-as-proof; worker self-granted permissions.
