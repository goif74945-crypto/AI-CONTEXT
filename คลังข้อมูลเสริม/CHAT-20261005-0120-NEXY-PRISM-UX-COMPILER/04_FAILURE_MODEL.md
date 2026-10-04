# NEXY::PRISM Failure Model

## Design rule
When presentation truth and convenience conflict, presentation fails closed.

## Failure classes

### F1 — Backend authorization deny
Requested action disabled. Backend reason code is preserved when provided.

### F2 — Role-surface mismatch
Action disabled even if a malformed caller marks backend authorization true. This is defense-in-depth, not replacement authorization.

### F3 — Release contradiction
Examples: release authorized outside STABLE, without PASS evidence, or while FREEZE/STOP.

Behavior: CONTRACT_CONFLICT trust label, action disabled, conflict codes mandatory, while FREEZE/STOP banner still wins visually.

### F4 — Unverified or rejected evidence
Never VERIFIED_FINAL. Result/export blocked. `OUTPUT_RELEASE:NOT_FINAL` mandatory.

### F5 — FREEZE
FREEZE banner mandatory; only diagnostics and explicitly recoverable OWNER recovery can be enabled; detail floor FORENSIC.

### F6 — STOP
STOP banner mandatory; mutation disabled; only trace/audit diagnostics can remain enabled when backend authorized; detail floor FORENSIC.

### F7 — Irreversible action
Typed confirmation mandatory; detail floor FORENSIC; irreversible disclosure mandatory.

### F8 — Active-state configuration/destruction
Config change and hard delete are disabled outside READY/STABLE in this prototype. This is conservative **AI-proposed future behavior**, not current NEXY law.

## Recovery
PRISM has no recovery state. Recovery remains upstream. PRISM only exposes the affordance when authoritative input says backend-authorized and recoverable.
