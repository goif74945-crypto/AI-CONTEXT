# NEXY Auditor Playbook

## Universal audit law
1. Pin exact repository/branch/HEAD and observed environment.
2. Resolve source authority and scope before reading code.
3. Separate SOURCE / IMPLEMENTATION / TEST / RUNTIME / DEPLOYMENT / PHYSICAL evidence.
4. Use only: PASS / FAIL / PARTIAL / NOT IMPLEMENTED / NOT VERIFIED / UNKNOWN / BLOCKED / CONFLICT / SCOPE where applicable.
5. File existence, docs, mocks, build success, or comments are never runtime proof.
6. Search failure history and known conflicts before declaring a new root cause.
7. Preserve evidence even when verdict is FAIL.

# Workflow: Audit System

## Sequence
1. Resolve system + descendants from Ontology.
2. Resolve all requirements, dependencies, contracts, FSMs and invariants.
3. Resolve implementation refs; inspect EXACT/GROUP/CANDIDATE targets.
4. Build requirement ledger: requirement → code → test → evidence.
5. Classify each requirement independently.
6. Attack negative/failure paths.
7. Check cross-system effects and forbidden dependency edges.
8. Re-audit after fixes from clean source state.

## Mandatory findings
- missing implementation;
- semantic mismatch;
- stale/absent evidence;
- scope error;
- authority inversion;
- hidden fallback;
- untested critical path.

## DONE
No aggregate PASS without every mandatory requirement having adequate evidence.
