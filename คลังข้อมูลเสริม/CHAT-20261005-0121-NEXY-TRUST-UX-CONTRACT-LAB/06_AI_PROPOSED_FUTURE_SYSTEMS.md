# AI-PROPOSED Future Systems

Everything below is **PROPOSAL**, not current NEXY requirement or implementation truth.

## 1. Trust Surface Conformance Gate
A CI/static test that feeds canonical backend envelopes into the real frontend renderer and proves:
- FREEZE never renders result CTA;
- pending never renders success language;
- STOP never exposes ordinary recover;
- unknown states fail closed;
- role-visible actions match backend permission intent.

Potential value: catches UI truth regressions before release.

## 2. Semantic Copy Linter
A deterministic linter for system-state copy that rejects wording known to blur truth boundaries, such as success language during pending states or retry language on blocked legal states.

Trade-off: copy linting can become overly rigid. It should validate semantic classes, not brand voice.

## 3. Evidence-to-UX Compression Layer
A governed transformer that turns a large evidence bundle into a compact user-facing proof summary while keeping exact evidence references available for audit.

Failure risk: compression can omit decisive caveats. Any summary must be mechanically linked to full evidence and carry completeness limits.

## 4. Operator Consequence Preview
Before a dangerous request, show a deterministic impact preview generated from authoritative metadata: affected object, reversibility, required role, rollback availability, and expected audit record.

Failure risk: stale impact metadata can create false confidence. Preview must carry source revision and freshness.

## 5. Accessibility Truth Equivalence Tests
Prove that visual, screen-reader, keyboard-only, reduced-motion, and mobile presentations preserve the same authoritative state. A sticky red banner is useless if screen-reader order still announces a stale success result first. Humanity has managed stranger UI bugs.

## Adoption rule
No proposal may enter current build scope merely because it is attractive. Promotion requires explicit authority, requirement mapping, implementation design, and matching evidence.
