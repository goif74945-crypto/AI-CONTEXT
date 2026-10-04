# Option Space & Reversibility Engineering

## Principle
A system should preserve safe future choices, not merely satisfy the present happy path.

Architecture loses option value when it couples unrelated domains, makes irreversible migrations without transition paths, embeds vendor semantics into domain contracts, deletes provenance, conflates identity with presentation, or relies on hidden mutable global state.

## Reversibility classes
R0 local/trivially revertible.
R1 code/config revert; no persistent transformation.
R2 persistent data changed but losslessly reversible.
R3 externally observable/distributed contract changed; coordinated rollback.
R4 destructive or irreversible state/external side effect.

Higher classes require stronger evidence and stricter approval.

## R0-R1 protocol
Validate scope, execute smallest complete change, verify, revert quickly if evidence fails.

## R3-R4 protocol
Capture baseline, prove backup/restore, stage migration, define abort thresholds, canary where applicable, retain old path until exit criteria pass.

## Migration invariants
Define source of truth per phase, read/write paths, reconciliation, version compatibility, rollback boundary and completion evidence.

## Future-proofing test
Ask what information/interface would be needed if the requirement reversed later. Preserve it when cost is reasonable and current requirements permit it.
