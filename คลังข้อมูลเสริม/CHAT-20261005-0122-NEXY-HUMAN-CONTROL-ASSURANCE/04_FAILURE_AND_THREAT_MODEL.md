# Failure and Threat Model

Status: **AI-PROPOSED ANALYSIS**

## Threats HCAS can detect statically
- UI role visibility treated as if it were authorization metadata;
- high-impact action without declared explicit confirmation;
- mutating action without audit event;
- hidden/maskable/non-sticky freeze surface contract;
- pending state misclassified as success/evidence;
- missing visible failure/freeze path;
- inconsistent read-only/mutation declaration;
- reversible action with no rollback path;
- irreversible mutation with no warning contract;
- duplicate action IDs.

## Threats HCAS cannot prove
- backend actually enforces role/permission;
- browser actually renders sticky FREEZE;
- confirmation cannot be bypassed;
- audit event is durably stored;
- rollback works;
- accessibility behavior works with assistive technology;
- network/service failure behaves as declared;
- live NEXY implementation matches the manifest.

Those require E3/E4/E5 evidence. Treating HCAS PASS as runtime proof would itself be an evidence-class violation.
